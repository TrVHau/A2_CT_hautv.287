import os
import sys
import numpy as np
import pandas as pd
import time
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
from gasf_gadf import series_to_gasf_dataset
from models_pytorch import CNN4, CNN8, DeepCNN, ResNetCNN
from backtest_engine import block_bootstrap_ci

def load_market_data(ticker_file):
    path = os.path.join(config.DATA_DIR, ticker_file)
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def train_eval_cnn():
    markets = [
        ('S&P 500', 'sp500_daily.csv'),
        ('VN-Index', 'vnindex_daily.csv'),
        ('Bitcoin', 'btc_daily.csv'),
        ('Ethereum [UPGRADE]', 'eth_daily.csv')
    ]
    
    results = []
    
    for mname, mfile in markets:
        df = load_market_data(mfile)
        prices = df['Close'].values
        dates = df['Date'].values[config.WINDOW_SIZE:]
        
        X, y = series_to_gasf_dataset(prices, window_size=config.WINDOW_SIZE)
        
        # Temporal split (No future leakage)
        train_mask = dates < np.datetime64(config.VAL_START_DATE)
        val_mask = (dates >= np.datetime64(config.VAL_START_DATE)) & (dates < np.datetime64(config.TEST_START_DATE))
        test_mask = dates >= np.datetime64(config.TEST_START_DATE)
        
        X_train, y_train = X[train_mask], y[train_mask]
        X_val, y_val = X[val_mask], y[val_mask]
        X_test, y_test = X[test_mask], y[test_mask]
        
        # Convert to Torch Tensors
        X_tr_t = torch.from_numpy(X_train)
        y_tr_t = torch.from_numpy(y_train)
        X_va_t = torch.from_numpy(X_val)
        y_va_t = torch.from_numpy(y_val)
        X_te_t = torch.from_numpy(X_test)
        y_te_t = torch.from_numpy(y_test)
        
        # Baseline 1: Majority Class
        maj_prob = np.full_like(y_test, np.mean(y_train))
        results.append({
            'market': mname, 'model': 'Majority Baseline', 'seed': 0, 'params': 0,
            'roc_auc': 0.500, 'ci_lower': 0.500, 'ci_upper': 0.500,
            'ap': np.mean(y_test), 'bal_acc': 0.500, 'time_sec': 0.001
        })
        
        # Baseline 2: Repeat Previous Day Direction (Momentum)
        prev_dir = (prices[config.WINDOW_SIZE - 1 : -1] > prices[config.WINDOW_SIZE - 2 : -2]).astype(float)
        prev_dir_test = prev_dir[test_mask]
        auc_prev = roc_auc_score(y_test, prev_dir_test)
        ci_low, ci_high = block_bootstrap_ci(y_test.flatten(), prev_dir_test, roc_auc_score)
        results.append({
            'market': mname, 'model': 'Repeat Last Day (Momentum)', 'seed': 0, 'params': 0,
            'roc_auc': auc_prev, 'ci_lower': ci_low, 'ci_upper': ci_high,
            'ap': average_precision_score(y_test, prev_dir_test),
            'bal_acc': balanced_accuracy_score(y_test, prev_dir_test),
            'time_sec': 0.001
        })
        
        # Models to evaluate
        model_factories = [
            ('CNN4', CNN4),
            ('CNN8', CNN8),
            ('DeepCNN', DeepCNN),
            ('ResNetCNN [UPGRADE]', ResNetCNN)
        ]
        
        for mod_name, mod_cls in model_factories:
            for seed in config.SEEDS:
                torch.manual_seed(seed)
                np.random.seed(seed)
                
                model = mod_cls()
                num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
                optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
                criterion = nn.BCEWithLogitsLoss()
                
                t0 = time.time()
                best_val_loss = float('inf')
                best_state = None
                patience_cnt = 0
                
                # Mini-batch training
                batch_size = config.BATCH_SIZE
                n_batches = int(np.ceil(len(X_train) / batch_size))
                
                for epoch in range(config.MAX_EPOCHS):
                    model.train()
                    indices = np.random.permutation(len(X_train))
                    for b in range(n_batches):
                        idx = indices[b * batch_size : (b + 1) * batch_size]
                        xb = X_tr_t[idx]
                        yb = y_tr_t[idx]
                        
                        optimizer.zero_grad()
                        preds = model(xb)
                        loss = criterion(preds, yb)
                        loss.backward()
                        nn.utils.clip_grad_norm_(model.parameters(), config.GRAD_CLIP)
                        optimizer.step()
                        
                    model.eval()
                    with torch.no_grad():
                        v_loss = criterion(model(X_va_t), y_va_t).item()
                    if v_loss < best_val_loss:
                        best_val_loss = v_loss
                        best_state = model.state_dict()
                        patience_cnt = 0
                    else:
                        patience_cnt += 1
                        if patience_cnt >= config.PATIENCE:
                            break
                            
                t_train = time.time() - t0
                model.load_state_dict(best_state)
                model.eval()
                with torch.no_grad():
                    logits = model(X_te_t).numpy().flatten()
                probs = 1.0 / (1.0 + np.exp(-logits))
                
                auc = roc_auc_score(y_test, probs)
                ci_low, ci_high = block_bootstrap_ci(y_test.flatten(), probs, roc_auc_score)
                ap = average_precision_score(y_test, probs)
                bal_acc = balanced_accuracy_score(y_test, (probs >= 0.5).astype(int))
                
                results.append({
                    'market': mname, 'model': mod_name, 'seed': seed, 'params': num_params,
                    'roc_auc': auc, 'ci_lower': ci_low, 'ci_upper': ci_high,
                    'ap': ap, 'bal_acc': bal_acc, 'time_sec': t_train
                })

    res_df = pd.DataFrame(results)
    return res_df

if __name__ == '__main__':
    print("Running Chapter 3 CNN Experiments across 4 Markets...")
    df = train_eval_cnn()
    print("\nSummary by Market and Model (Mean across 3 seeds):")
    summary = df.groupby(['market', 'model']).agg({
        'roc_auc': ['mean', 'std'],
        'ci_lower': 'mean',
        'ci_upper': 'mean',
        'params': 'first',
        'time_sec': 'mean'
    }).round(4)
    print(summary)
    df.to_csv(os.path.join(config.DATA_DIR, 'ch3_cnn_results.csv'), index=False)
    print("Saved results to tieuluan1/data/ch3_cnn_results.csv")
