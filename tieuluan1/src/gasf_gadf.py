import numpy as np

def min_max_scale_window(window, eps=1e-8):
    """
    Min-Max scale a 1D window to [0, 1] strictly using only window's min and max.
    This prevents look-ahead bias (data leakage).
    """
    w_min = np.min(window)
    w_max = np.max(window)
    if w_max - w_min < eps:
        return np.zeros_like(window)
    return (window - w_min) / (w_max - w_min)

def compute_gasf(window):
    """
    Compute Gramian Angular Summation Field (GASF) for a 1D sequence.
    Formula:
        tilde_x in [0, 1]
        phi = arccos(tilde_x)
        G[i, j] = cos(phi_i + phi_j) = tilde_x_i * tilde_x_j - sqrt(1 - tilde_x_i^2) * sqrt(1 - tilde_x_j^2)
    Output shape: (N, N) where N = len(window)
    """
    scaled = min_max_scale_window(window)
    # Clip to avoid float precision issues in arccos
    scaled = np.clip(scaled, 0.0, 1.0)
    phi = np.arccos(scaled)
    # Vectorized computation of cos(phi_i + phi_j)
    gasf = np.cos(phi[:, None] + phi[None, :])
    return gasf

def compute_gadf(window):
    """
    Compute Gramian Angular Difference Field (GADF) [UPGRADE].
    Formula:
        D[i, j] = sin(phi_i - phi_j) = tilde_x_j * sqrt(1 - tilde_x_i^2) - tilde_x_i * sqrt(1 - tilde_x_j^2)
    Output shape: (N, N)
    """
    scaled = min_max_scale_window(window)
    scaled = np.clip(scaled, 0.0, 1.0)
    phi = np.arccos(scaled)
    gadf = np.sin(phi[:, None] - phi[None, :])
    return gadf

def compute_mtf(window, n_bins=4):
    """
    Compute Markov Transition Field (MTF) [UPGRADE].
    Discretizes window into n_bins quantile states, computes transition matrix W,
    then assigns MTF[i, j] = W[state_i, state_j].
    """
    scaled = min_max_scale_window(window)
    # Quantile binning
    bins = np.linspace(0, 1, n_bins + 1)
    states = np.digitize(scaled, bins) - 1
    states = np.clip(states, 0, n_bins - 1)
    
    # Compute Markov transition matrix
    W = np.zeros((n_bins, n_bins))
    for t in range(len(states) - 1):
        W[states[t], states[t+1]] += 1
    # Normalize row sums
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    W = W / row_sums
    
    # Map back to sequence length N x N
    mtf = np.zeros((len(window), len(window)))
    for i in range(len(window)):
        for j in range(len(window)):
            mtf[i, j] = W[states[i], states[j]]
    return mtf

def series_to_gasf_dataset(prices, window_size=20):
    """
    Convert price series to GASF images and binary target:
    X: (M, 1, window_size, window_size)
    y: (M, 1) where y=1 if next close > current close, else 0
    """
    n = len(prices)
    X = []
    y = []
    for i in range(window_size, n):
        win = prices[i - window_size : i]
        img = compute_gasf(win)
        label = 1.0 if prices[i] > prices[i - 1] else 0.0
        X.append(img)
        y.append(label)
    
    X = np.array(X, dtype=np.float32)[:, None, :, :]  # Shape: (M, 1, 20, 20)
    y = np.array(y, dtype=np.float32)[:, None]        # Shape: (M, 1)
    return X, y

def series_to_log_returns_dataset(prices, window_size=20):
    """
    Convert price series to sequence of 20 log-returns and binary target:
    X: (M, window_size, 1)
    y: (M, 1) where y=1 if next return > 0, else 0
    """
    log_rets = np.diff(np.log(prices))
    n = len(log_rets)
    X = []
    y = []
    for i in range(window_size, n):
        win = log_rets[i - window_size : i]
        label = 1.0 if log_rets[i] > 0 else 0.0
        X.append(win)
        y.append(label)
    
    X = np.array(X, dtype=np.float32)[:, :, None]     # Shape: (M, 20, 1)
    y = np.array(y, dtype=np.float32)[:, None]        # Shape: (M, 1)
    return X, y
