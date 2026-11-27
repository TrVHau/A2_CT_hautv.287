import sys, os
import numpy as np

# Ensure src in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from models_numpy import Dense, ReLU, BCEWithLogitsLoss

class DummyMLP:
    def __init__(self, in_features):
        self.layers = [
            Dense(in_features, 8),
            ReLU(),
            Dense(8, 1)
        ]
        # Use float64 for analytical vs numerical verification
        for p in self.parameters():
            p.value = p.value.astype(np.float64)
            p.grad = p.grad.astype(np.float64)

    def __call__(self, x):
        out = x
        for l in self.layers:
            out = l.forward(out)
        return out
        
    def zero_grad(self):
        for l in self.layers:
            l.zero_grad()
            
    def parameters(self):
        p = []
        for l in self.layers:
            p.extend(l.parameters())
        return p

def test_mlp_gradient_checking():
    np.random.seed(42)
    x = np.random.randn(10, 5).astype(np.float64)
    y = np.random.randint(0, 2, (10, 1)).astype(np.float64)
    
    model = DummyMLP(5)
    loss_fn = BCEWithLogitsLoss()
    
    model.zero_grad()
    out = model(x)
    loss = loss_fn(out, y)
    grad = loss_fn.backward()
    for l in reversed(model.layers):
        grad = l.backward(grad)

    eps = 1e-6
    max_rel_error = 0.0
    for p_idx, p in enumerate(model.parameters()):
        it = np.nditer(p.value, flags=['multi_index'])
        while not it.finished:
            idx = it.multi_index
            orig = float(p.value[idx])
            p.value[idx] = orig + eps
            l1 = float(loss_fn(model(x), y))
            p.value[idx] = orig - eps
            l2 = float(loss_fn(model(x), y))
            p.value[idx] = orig
            
            num_grad = (l1 - l2) / (2.0 * eps)
            ana_val = float(p.grad[idx])
            diff = abs(ana_val - num_grad)
            denom = abs(ana_val) + abs(num_grad) + 1e-12
            rel_err = diff / denom
            if rel_err > max_rel_error:
                max_rel_error = rel_err
            it.iternext()

    print(f"MLP Numerical Gradient Check Max Relative Error: {max_rel_error:.2e}")
    assert max_rel_error < 1e-7, f"Gradient check failed with error {max_rel_error}"

if __name__ == '__main__':
    test_mlp_gradient_checking()
    print("Gradient check test PASSED successfully (Verified < 1e-7)!")
