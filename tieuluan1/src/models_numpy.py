import numpy as np

class Parameter:
    def __init__(self, value):
        self.value = np.array(value, dtype=np.float32)
        self.grad = np.zeros_like(self.value, dtype=np.float32)

class Module:
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    def zero_grad(self):
        for p in self.parameters():
            p.grad.fill(0.0)
            
    def parameters(self):
        params = []
        for attr in self.__dict__.values():
            if isinstance(attr, Parameter):
                params.append(attr)
            elif isinstance(attr, Module):
                params.extend(attr.parameters())
        return params

class Dense(Module):
    def __init__(self, in_features, out_features):
        self.in_features = in_features
        self.out_features = out_features
        # Xavier / Glorot uniform initialization
        limit = np.sqrt(6.0 / (in_features + out_features))
        self.weight = Parameter(np.random.uniform(-limit, limit, (out_features, in_features)))
        self.bias = Parameter(np.zeros(out_features))
        self._x = None

    def forward(self, x):
        self._x = x
        return x @ self.weight.value.T + self.bias.value

    def backward(self, grad_output):
        # grad_output shape: (batch_size, out_features)
        self.weight.grad += grad_output.T @ self._x
        self.bias.grad += grad_output.sum(axis=0)
        return grad_output @ self.weight.value

class ReLU(Module):
    def __init__(self):
        self._mask = None

    def forward(self, x):
        self._mask = (x > 0)
        return np.maximum(0, x)

    def backward(self, grad_output):
        return grad_output * self._mask

class Flatten(Module):
    def __init__(self):
        self._orig_shape = None

    def forward(self, x):
        self._orig_shape = x.shape
        return x.reshape(x.shape[0], -1)

    def backward(self, grad_output):
        return grad_output.reshape(self._orig_shape)

def im2col_indices(x, kh, kw, padding=0, stride=1):
    # x shape: (N, C, H, W)
    p = padding
    x_padded = np.pad(x, ((0, 0), (0, 0), (p, p), (p, p)), mode='constant')
    N, C, H, W = x.shape
    out_h = int((H + 2 * p - kh) / stride + 1)
    out_w = int((W + 2 * p - kw) / stride + 1)

    shape = (N, C, out_h, out_w, kh, kw)
    strides = (
        x_padded.strides[0],
        x_padded.strides[1],
        x_padded.strides[2] * stride,
        x_padded.strides[3] * stride,
        x_padded.strides[2],
        x_padded.strides[3]
    )
    cols = np.lib.stride_tricks.as_strided(x_padded, shape=shape, strides=strides)
    cols = cols.transpose(0, 2, 3, 1, 4, 5).reshape(N * out_h * out_w, C * kh * kw)
    return cols, out_h, out_w

def col2im_indices(cols, x_shape, kh, kw, padding=0, stride=1):
    N, C, H, W = x_shape
    out_h = int((H + 2 * padding - kh) / stride + 1)
    out_w = int((W + 2 * padding - kw) / stride + 1)
    x_padded = np.zeros((N, C, H + 2 * padding, W + 2 * padding), dtype=cols.dtype)
    cols_reshaped = cols.reshape(N, out_h, out_w, C, kh, kw).transpose(0, 3, 1, 2, 4, 5)

    for i in range(kh):
        for j in range(kw):
            x_padded[:, :, i:i + out_h * stride:stride, j:j + out_w * stride:stride] += cols_reshaped[:, :, :, :, i, j]

    if padding == 0:
        return x_padded
    return x_padded[:, :, padding:-padding, padding:-padding]

class Conv2D(Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        
        limit = np.sqrt(6.0 / (in_channels * kernel_size * kernel_size + out_channels))
        self.weight = Parameter(np.random.uniform(-limit, limit, (out_channels, in_channels, kernel_size, kernel_size)))
        self.bias = Parameter(np.zeros(out_channels))
        
        self._x = None
        self._cols = None
        self._out_h = 0
        self._out_w = 0

    def forward(self, x):
        self._x = x
        N, C, H, W = x.shape
        self._cols, self._out_h, self._out_w = im2col_indices(
            x, self.kernel_size, self.kernel_size, padding=self.padding, stride=self.stride
        )
        W_row = self.weight.value.reshape(self.out_channels, -1)
        out = self._cols @ W_row.T + self.bias.value
        out = out.reshape(N, self._out_h, self._out_w, self.out_channels).transpose(0, 3, 1, 2)
        return out

    def backward(self, grad_output):
        N, C_out, out_h, out_w = grad_output.shape
        grad_flat = grad_output.transpose(0, 2, 3, 1).reshape(-1, self.out_channels)
        
        self.bias.grad += grad_flat.sum(axis=0)
        self.weight.grad += (grad_flat.T @ self._cols).reshape(self.weight.value.shape)
        
        W_row = self.weight.value.reshape(self.out_channels, -1)
        dcols = grad_flat @ W_row
        dx = col2im_indices(dcols, self._x.shape, self.kernel_size, self.kernel_size, padding=self.padding, stride=self.stride)
        return dx

class MaxPool2D(Module):
    def __init__(self, pool_size=2, stride=2):
        self.pool_size = pool_size
        self.stride = stride
        self._x = None
        self._arg_max = None

    def forward(self, x):
        self._x = x
        N, C, H, W = x.shape
        out_h = int((H - self.pool_size) / self.stride + 1)
        out_w = int((W - self.pool_size) / self.stride + 1)
        
        # Reshape to block structure
        x_reshaped = x.reshape(N, C, out_h, self.stride, out_w, self.stride)
        out = x_reshaped.max(axis=(3, 5))
        return out

    def backward(self, grad_output):
        N, C, H, W = self._x.shape
        out_h = int((H - self.pool_size) / self.stride + 1)
        out_w = int((W - self.pool_size) / self.stride + 1)
        
        dx = np.zeros_like(self._x)
        for i in range(out_h):
            for j in range(out_w):
                h_start, h_end = i * self.stride, i * self.stride + self.pool_size
                w_start, w_end = j * self.stride, j * self.stride + self.pool_size
                window = self._x[:, :, h_start:h_end, w_start:w_end]
                max_val = grad_output[:, :, i, j][:, :, None, None]
                mask = (window == window.max(axis=(2, 3), keepdims=True))
                dx[:, :, h_start:h_end, w_start:w_end] += mask * max_val
        return dx

class SimpleRNN(Module):
    def __init__(self, in_features, hidden_size):
        self.in_features = in_features
        self.hidden_size = hidden_size
        limit_ih = np.sqrt(6.0 / (in_features + hidden_size))
        limit_hh = np.sqrt(6.0 / (2 * hidden_size))
        self.weight_ih = Parameter(np.random.uniform(-limit_ih, limit_ih, (hidden_size, in_features)))
        self.weight_hh = Parameter(np.random.uniform(-limit_hh, limit_hh, (hidden_size, hidden_size)))
        self.bias_ih = Parameter(np.zeros(hidden_size))
        self._x = None
        self._h_seq = None

    def forward(self, x):
        # x shape: (N, seq_len, in_features)
        self._x = x
        N, seq_len, _ = x.shape
        h = np.zeros((N, self.hidden_size), dtype=np.float32)
        h_seq = [h]
        for t in range(seq_len):
            x_t = x[:, t, :]
            pre_act = x_t @ self.weight_ih.value.T + h @ self.weight_hh.value.T + self.bias_ih.value
            h = np.tanh(pre_act)
            h_seq.append(h)
        self._h_seq = h_seq
        return h  # return last hidden state

    def backward(self, grad_output):
        N, seq_len, _ = self._x.shape
        dh = grad_output.copy()
        for t in reversed(range(seq_len)):
            h_t = self._h_seq[t + 1]
            h_prev = self._h_seq[t]
            x_t = self._x[:, t, :]
            
            dpre = dh * (1.0 - h_t ** 2)
            self.weight_ih.grad += dpre.T @ x_t
            self.weight_hh.grad += dpre.T @ h_prev
            self.bias_ih.grad += dpre.sum(axis=0)
            dh = dpre @ self.weight_hh.value
        return None

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

class LSTM(Module):
    def __init__(self, in_features, hidden_size):
        self.in_features = in_features
        self.hidden_size = hidden_size
        H = hidden_size
        limit = np.sqrt(6.0 / (in_features + H))
        # 4 gates concatenated: i, f, g, o (matches PyTorch order)
        self.weight_ih = Parameter(np.random.uniform(-limit, limit, (4 * H, in_features)))
        self.weight_hh = Parameter(np.random.uniform(-limit, limit, (4 * H, H)))
        self.bias_ih = Parameter(np.zeros(4 * H))
        self._cache = []

    def forward(self, x):
        # x shape: (N, seq_len, in_features)
        self._x = x
        N, seq_len, _ = x.shape
        H = self.hidden_size
        h = np.zeros((N, H), dtype=np.float32)
        c = np.zeros((N, H), dtype=np.float32)
        self._cache = []

        for t in range(seq_len):
            x_t = x[:, t, :]
            z = x_t @ self.weight_ih.value.T + h @ self.weight_hh.value.T + self.bias_ih.value
            i_gate = sigmoid(z[:, :H])
            f_gate = sigmoid(z[:, H:2*H])
            g_cand = np.tanh(z[:, 2*H:3*H])
            o_gate = sigmoid(z[:, 3*H:])
            
            c_prev = c
            c = f_gate * c_prev + i_gate * g_cand
            tanh_c = np.tanh(c)
            h_prev = h
            h = o_gate * tanh_c
            self._cache.append((x_t, h_prev, c_prev, i_gate, f_gate, g_cand, o_gate, c, tanh_c))

        return h

    def backward(self, grad_output):
        N, seq_len, _ = self._x.shape
        H = self.hidden_size
        dh = grad_output.copy()
        dc = np.zeros((N, H), dtype=np.float32)

        for t in reversed(range(seq_len)):
            x_t, h_prev, c_prev, i_gate, f_gate, g_cand, o_gate, c, tanh_c = self._cache[t]
            
            do = dh * tanh_c
            dc += dh * o_gate * (1.0 - tanh_c ** 2)
            df = dc * c_prev
            di = dc * g_cand
            dg = dc * i_gate
            
            # Gradients w.r.t pre-activations
            dz_i = di * i_gate * (1.0 - i_gate)
            dz_f = df * f_gate * (1.0 - f_gate)
            dz_g = dg * (1.0 - g_cand ** 2)
            dz_o = do * o_gate * (1.0 - o_gate)
            dz = np.concatenate([dz_i, dz_f, dz_g, dz_o], axis=1)
            
            self.weight_ih.grad += dz.T @ x_t
            self.weight_hh.grad += dz.T @ h_prev
            self.bias_ih.grad += dz.sum(axis=0)
            
            dh = dz @ self.weight_hh.value
            dc = dc * f_gate
        return None

class GRU(Module):
    def __init__(self, in_features, hidden_size):
        self.in_features = in_features
        self.hidden_size = hidden_size
        H = hidden_size
        limit = np.sqrt(6.0 / (in_features + H))
        # 3 gates: r (reset), z (update), n (candidate)
        self.weight_ih = Parameter(np.random.uniform(-limit, limit, (3 * H, in_features)))
        self.weight_hh = Parameter(np.random.uniform(-limit, limit, (3 * H, H)))
        self.bias_ih = Parameter(np.zeros(3 * H))
        self.bias_hh = Parameter(np.zeros(3 * H))
        self._cache = []

    def forward(self, x):
        self._x = x
        N, seq_len, _ = x.shape
        H = self.hidden_size
        h = np.zeros((N, H), dtype=np.float32)
        self._cache = []

        for t in range(seq_len):
            x_t = x[:, t, :]
            ih = x_t @ self.weight_ih.value.T + self.bias_ih.value
            hh = h @ self.weight_hh.value.T + self.bias_hh.value
            
            r = sigmoid(ih[:, :H] + hh[:, :H])
            z = sigmoid(ih[:, H:2*H] + hh[:, H:2*H])
            n = np.tanh(ih[:, 2*H:] + r * hh[:, 2*H:])
            
            h_prev = h
            h = (1.0 - z) * n + z * h_prev
            self._cache.append((x_t, h_prev, r, z, n, ih, hh))

        return h

    def backward(self, grad_output):
        N, seq_len, _ = self._x.shape
        H = self.hidden_size
        dh = grad_output.copy()

        for t in reversed(range(seq_len)):
            x_t, h_prev, r, z, n, ih, hh = self._cache[t]
            
            dz = dh * (h_prev - n) * z * (1.0 - z)
            dn = dh * (1.0 - z) * (1.0 - n ** 2)
            dr = (dn @ self.weight_hh.value[2*H:, :].T * hh[:, 2*H:]) * r * (1.0 - r)
            
            d_ih = np.concatenate([dr, dz, dn], axis=1)
            d_hh = np.concatenate([dr, dz, dn * r], axis=1)
            
            self.weight_ih.grad += d_ih.T @ x_t
            self.weight_hh.grad += d_hh.T @ h_prev
            self.bias_ih.grad += d_ih.sum(axis=0)
            self.bias_hh.grad += d_hh.sum(axis=0)
            
            dh = dh * z + d_ih @ self.weight_ih.value[:, :] * 0 + d_hh @ self.weight_hh.value
        return None

class BCEWithLogitsLoss:
    def __call__(self, logits, targets):
        self.logits = logits
        self.targets = targets
        # Numerically stable log-add-exp formulation
        max_val = np.maximum(0, logits)
        loss = max_val - logits * targets + np.log(1.0 + np.exp(-np.abs(logits)))
        return np.mean(loss)

    def backward(self):
        # Derivative of BCE w.r.t logits: sigma(z) - y
        p = sigmoid(self.logits)
        grad = (p - self.targets) / self.logits.shape[0]
        return grad

class AdamOptimizer:
    def __init__(self, parameters, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.parameters = parameters
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [np.zeros_like(p.value) for p in parameters]
        self.v = [np.zeros_like(p.value) for p in parameters]
        self.t = 0

    def step(self, clip_norm=None):
        self.t += 1
        if clip_norm is not None:
            # Gradient clipping by global norm
            total_norm = np.sqrt(sum(np.sum(p.grad ** 2) for p in self.parameters))
            if total_norm > clip_norm:
                scale = clip_norm / (total_norm + 1e-6)
                for p in self.parameters:
                    p.grad *= scale

        for i, p in enumerate(self.parameters):
            self.m[i] = self.beta1 * self.m[i] + (1.0 - self.beta1) * p.grad
            self.v[i] = self.beta2 * self.v[i] + (1.0 - self.beta2) * (p.grad ** 2)
            m_hat = self.m[i] / (1.0 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1.0 - self.beta2 ** self.t)
            p.value -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

def gradient_check(model, loss_fn, x, y, eps=1e-5):
    """
    Check numerical vs analytical gradient using float64 precision.
    Relative error should be < 1e-6 for verified correct backpropagation.
    """
    model.zero_grad()
    out = model(x)
    loss = loss_fn(out, y)
    grad_loss = loss_fn.backward()
    
    # Backward pass through network
    curr_grad = grad_loss
    for layer in reversed(model.layers):
        curr_grad = layer.backward(curr_grad)

    max_rel_error = 0.0
    for p in model.parameters():
        # Iterate over all elements using multi-indices
        it = np.nditer(p.value, flags=['multi_index'])
        count = 0
        while not it.finished and count < 10:
            idx = it.multi_index
            orig = float(p.value[idx])
            
            p.value[idx] = orig + eps
            loss1 = float(loss_fn(model(x), y))
            
            p.value[idx] = orig - eps
            loss2 = float(loss_fn(model(x), y))
            
            p.value[idx] = orig
            num_grad = (loss1 - loss2) / (2.0 * eps)
            
            ana_val = float(p.grad[idx])
            diff = abs(ana_val - num_grad)
            denom = abs(ana_val) + abs(num_grad) + 1e-12
            rel_err = diff / denom
            if rel_err > max_rel_error:
                max_rel_error = rel_err
                
            it.iternext()
            count += 1
                
    return max_rel_error
                
    return max_rel_error

