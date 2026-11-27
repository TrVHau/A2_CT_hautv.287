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
from gasf_gadf import series_to_log_returns_dataset
from models_pytorch import SimpleRNNNet, LSTMNet, GRUNet, BiLSTMNet, TemporalAttentionLSTM
from backtest_engine import run_backtest, block_bootstrap_ci

def load_market_data(ticker_file):
    path = os.path.join(config.DATA_DIR, ticker_file)
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def train_eval_rnn():
    markets = [
        ('S&P 500', 'sp500_daily.csv', 'SP500', 252),
        ('VN-Index', 'vnindex_daily.csv', 'VNINDEX', 252),
        ('Bitcoin', 'btc_daily.csv', 'BTC', 365),
        ('Ethereum [UPGRADE]', 'eth_daily.csv', 'ETH', 365)
    ]
    
    results = []
    backtest_results = []
    
    for mname, mfile, fee_key, ann_factor in markets:
        df = load_market_data(mfile)
        prices = df['Close'].values
        # Note: log returns has length len(prices) - 1
        dates = df['Date'].values[1 + config.WINDOW_SIZE:]
        test_prices = prices[1 + config.WINDOW_SIZE:]
        
        X, y = series_to_log_returns_dataset(prices, window_size=config.WINDOW_SIZE)
        
        train_mask = dates < np.datetime64(config.VAL_START_DATE)
        val_mask = (dates >= np.datetime64(config.VAL_START_DATE)) & (dates < np.datetime64(config.TEST_START_DATE))
        test_mask = dates >= np.datetime64(config.TEST_START_DATE)
        
        X_train, y_train = X[train_mask], y[train_mask]
        X_val, y_val = X[val_mask], y[val_mask]
        X_test, y_test = X[test_mask], y[test_mask]
        prices_test = test_prices[test_mask]
        
        # Standardize using ONLY Train mean and std to prevent data leakage
        mean_tr = np.mean(X_train)
        std_tr = np.std(X_train) + 1e-8
        X_train = (X_train - mean_tr) / std_tr
        X_val = (X_val - mean_tr) / std_tr
        X_test = (X_test - mean_tr) / std_tr
        
        X_tr_t = torch.from_numpy(X_train)
        y_tr_t = torch.from_numpy(y_train)
        X_va_t = torch.from_numpy(X_val)
        y_va_t = torch.from_numpy(y_val)
        X_te_t = torch.from_numpy(X_test)
        y_te_t = torch.from_numpy(y_test)
        
        fee_rate = config.FEES[fee_key]
        
        # 1. Buy & Hold Backtest
        bh_metrics = run_backtest(prices_test, np.ones(len(y_test)), threshold=0.5, fee_rate=fee_rate, annual_factor=ann_factor)
        backtest_results.append({
            'market': mname, 'strategy': 'Buy & Hold', 'seed': 0,
            'cagr_pre': bh_metrics['cagr_bh'], 'cagr_post': bh_metrics['cagr_bh'],
            'sharpe': bh_metrics['sharpe_bh'], 'sortino': bh_metrics['cagr_bh'] / max(bh_metrics['vol_bh'] * 0.7, 1e-6),
            'vol': bh_metrics['vol_bh'], 'max_dd': bh_metrics['max_drawdown_bh'],
            'calmar': bh_metrics['cagr_bh'] / max(bh_metrics['max_drawdown_bh'], 1e-6),
            'holding_pct': 1.0, 'trades': 1, 'win_rate': bh_metrics['win_rate'], 'profit_factor': bh_metrics['profit_factor']
        })
        
        # 2. Momentum Baseline Backtest
        prev_dir = (prices[config.WINDOW_SIZE : -1] > prices[config.WINDOW_SIZE - 1 : -2]).astype(float)
        prev_dir_test = prev_dir[test_mask]
        mom_metrics = run_backtest(prices_test, prev_dir_test, threshold=0.5, fee_rate=fee_rate, annual_factor=ann_factor)
        backtest_results.append({
            'market': mname, 'strategy': 'Repeat Last Day (Momentum)', 'seed': 0,
            'cagr_pre': mom_metrics['cagr_pre'], 'cagr_post': mom_metrics['cagr_post'],
            'sharpe': mom_metrics['sharpe_post'], 'sortino': mom_metrics['sortino_post'],
            'vol': mom_metrics['vol_post'], 'max_dd': mom_metrics['max_drawdown_post'],
            'calmar': mom_metrics['calmar_post'],
            'holding_pct': mom_metrics['holding_pct'], 'trades': mom_metrics['trades_count'],
            'win_rate': mom_metrics['win_rate'], 'profit_factor': mom_metrics['profit_factor']
        })
        
        # Models
        model_factories = [
            ('SimpleRNN', SimpleRNNNet),
            ('LSTM', LSTMNet),
            ('GRU', GRUNet),
            ('Bi-LSTM [UPGRADE]', BiLSTMNet),
            ('Attention-LSTM [UPGRADE]', TemporalAttentionLSTM)
        ]
        
        for mod_name, mod_cls in model_factories:
            seed_probs = []
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
                seed_probs.append(probs)
                
                auc = roc_auc_score(y_test, probs)
                ci_low, ci_high = block_bootstrap_ci(y_test.flatten(), probs, roc_auc_score)
                ap = average_precision_score(y_test, probs)
                bal_acc = balanced_accuracy_score(y_test, (probs >= 0.5).astype(int))
                
                results.append({
                    'market': mname, 'model': mod_name, 'seed': seed, 'params': num_params,
                    'roc_auc': auc, 'ci_lower': ci_low, 'ci_upper': ci_high,
                    'ap': ap, 'bal_acc': bal_acc, 'time_sec': t_train
                })
            
            # Backtest on ensemble average probability of 3 seeds
            avg_prob = np.mean(seed_probs, axis=0)
            bt_m = run_backtest(prices_test, avg_prob, threshold=0.5, fee_rate=fee_rate, annual_factor=ann_factor)
            backtest_results.append({
                'market': mname, 'strategy': mod_name, 'seed': 'Ensemble (3 seeds)',
                'cagr_pre': bt_m['cagr_pre'], 'cagr_post': bt_m['cagr_post'],
                'sharpe': bt_m['sharpe_post'], 'sortino': bt_m['sortino_post'],
                'vol': bt_m['vol_post'], 'max_dd': bt_m['max_drawdown_post'],
                'calmar': bt_m['calmar_post'],
                'holding_pct': bt_m['holding_pct'], 'trades': bt_m['trades_count'],
                'win_rate': bt_m['win_rate'], 'profit_factor': bt_m['profit_factor']
            })

    res_df = pd.DataFrame(results)
    bt_df = pd.DataFrame(backtest_results)
    return res_df, bt_df

if __name__ == '__main__':
    print("Running Chapter 4 RNN Experiments across 4 Markets...")
    res_df, bt_df = train_eval_rnn()
    print("\nSummary RNN Accuracy Metrics (Mean across 3 seeds):")
    summary = res_df.groupby(['market', 'model']).agg({
        'roc_auc': ['mean', 'std'],
        'ci_lower': 'mean',
        'ci_upper': 'mean',
        'params': 'first'
    }).round(4)
    print(summary)
    
    print("\nSummary Backtest Trading Performance (Test Period 2023-2026):")
    print(bt_df[['market', 'strategy', 'cagr_pre', 'cagr_post', 'sharpe', 'sortino', 'max_dd', 'calmar', 'trades']].round(3))
    
    res_df.to_csv(os.path.join(config.DATA_DIR, 'ch4_rnn_results.csv'), index=False)
    bt_df.to_csv(os.path.join(config.DATA_DIR, 'ch4_backtest_results.csv'), index=False)
    print("Saved results to tieuluan1/data/ch4_rnn_results.csv and ch4_backtest_results.csv")
