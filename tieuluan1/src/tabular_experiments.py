import os
import sys
import numpy as np
import pandas as pd
import time
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
from models_numpy import Dense as NPDense, ReLU as NPReLU, BCEWithLogitsLoss as NPBCE, AdamOptimizer as NPAdam
from models_pytorch import MLP as PTMLP
from models_keras import build_keras_mlp
from weights_sync import sync_mlp_weights

def load_and_preprocess_tabular(dataset_name='bankruptcy'):
    if dataset_name == 'bankruptcy':
        path = os.path.join(config.DATA_DIR, 'taiwan_bankruptcy.csv')
        df = pd.read_csv(path)
        y = df.iloc[:, 0].values.astype(np.float32)
        X = df.iloc[:, 1:].values.astype(np.float32)
    else:
        path = os.path.join(config.DATA_DIR, 'taiwan_credit_default.csv')
        df = pd.read_csv(path)
        # Drop ID if present
        if 'ID' in df.columns:
            df = df.drop(columns=['ID'])
        y = df.iloc[:, -1].values.astype(np.float32)
        X = df.iloc[:, :-1].values.astype(np.float32)
        
    return X, y

def train_eval_tabular():
    results = []
    datasets = ['bankruptcy', 'credit_default']
    
    for dname in datasets:
        X, y = load_and_preprocess_tabular(dname)
        
        for seed in config.SEEDS:
            np.random.seed(seed)
            torch.manual_seed(seed)
            
            # Stratified split: 70% Train, 15% Val, 15% Test
            X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=seed)
            X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.17647, stratify=y_temp, random_state=seed)
            
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            X_test = scaler.transform(X_test)
            
            in_dim = X_train.shape[1]
            
            # 1. Baseline: Majority Class
            maj_prob = np.full_like(y_test, np.mean(y_train))
            results.append({
                'dataset': dname, 'model': 'Majority Baseline', 'seed': seed,
                'roc_auc': 0.500, 'ap': np.mean(y_test), 'bal_acc': 0.500, 'time_sec': 0.001
            })
            
            # 2. Logistic Regression
            t0 = time.time()
            lr = LogisticRegression(max_iter=1000, random_state=seed)
            lr.fit(X_train, y_train)
            lr_prob = lr.predict_proba(X_test)[:, 1]
            t_lr = time.time() - t0
            results.append({
                'dataset': dname, 'model': 'Logistic Regression', 'seed': seed,
                'roc_auc': roc_auc_score(y_test, lr_prob),
                'ap': average_precision_score(y_test, lr_prob),
                'bal_acc': balanced_accuracy_score(y_test, (lr_prob >= 0.5).astype(int)),
                'time_sec': t_lr
            })
            
            # 3. Random Forest
            t0 = time.time()
            rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=seed, n_jobs=-1)
            rf.fit(X_train, y_train)
            rf_prob = rf.predict_proba(X_test)[:, 1]
            t_rf = time.time() - t0
            results.append({
                'dataset': dname, 'model': 'Random Forest', 'seed': seed,
                'roc_auc': roc_auc_score(y_test, rf_prob),
                'ap': average_precision_score(y_test, rf_prob),
                'bal_acc': balanced_accuracy_score(y_test, (rf_prob >= 0.5).astype(int)),
                'time_sec': t_rf
            })
            
            # 4. LightGBM [UPGRADE]
            t0 = time.time()
            lgb_model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.05, random_state=seed, verbose=-1)
            lgb_model.fit(X_train, y_train)
            lgb_prob = lgb_model.predict_proba(X_test)[:, 1]
            t_lgb = time.time() - t0
            results.append({
                'dataset': dname, 'model': 'LightGBM [UPGRADE]', 'seed': seed,
                'roc_auc': roc_auc_score(y_test, lgb_prob),
                'ap': average_precision_score(y_test, lgb_prob),
                'bal_acc': balanced_accuracy_score(y_test, (lgb_prob >= 0.5).astype(int)),
                'time_sec': t_lgb
            })
            
            # 5. MLP PyTorch
            t0 = time.time()
            pt_mlp = PTMLP(in_dim)
            optimizer = optim.Adam(pt_mlp.parameters(), lr=0.001)
            criterion = nn.BCEWithLogitsLoss()
            
            X_tr_t = torch.from_numpy(X_train.astype(np.float32))
            y_tr_t = torch.from_numpy(y_train[:, None].astype(np.float32))
            X_val_t = torch.from_numpy(X_val.astype(np.float32))
            y_val_t = torch.from_numpy(y_val[:, None].astype(np.float32))
            X_te_t = torch.from_numpy(X_test.astype(np.float32))
            
            best_val_loss = float('inf')
            patience_cnt = 0
            best_state = None
            
            for epoch in range(60):
                pt_mlp.train()
                optimizer.zero_grad()
                out = pt_mlp(X_tr_t)
                loss = criterion(out, y_tr_t)
                loss.backward()
                nn.utils.clip_grad_norm_(pt_mlp.parameters(), 1.0)
                optimizer.step()
                
                pt_mlp.eval()
                with torch.no_grad():
                    v_loss = criterion(pt_mlp(X_val_t), y_val_t).item()
                if v_loss < best_val_loss:
                    best_val_loss = v_loss
                    best_state = pt_mlp.state_dict()
                    patience_cnt = 0
                else:
                    patience_cnt += 1
                    if patience_cnt >= 8:
                        break
                        
            pt_mlp.load_state_dict(best_state)
            pt_mlp.eval()
            with torch.no_grad():
                mlp_logits = pt_mlp(X_te_t).numpy().flatten()
            mlp_prob = 1.0 / (1.0 + np.exp(-mlp_logits))
            t_mlp = time.time() - t0
            
            results.append({
                'dataset': dname, 'model': 'MLP (PyTorch)', 'seed': seed,
                'roc_auc': roc_auc_score(y_test, mlp_prob),
                'ap': average_precision_score(y_test, mlp_prob),
                'bal_acc': balanced_accuracy_score(y_test, (mlp_prob >= 0.5).astype(int)),
                'time_sec': t_mlp
            })

    res_df = pd.DataFrame(results)
    return res_df

if __name__ == '__main__':
    print("Running Chapter 2 Tabular Experiments...")
    df = train_eval_tabular()
    print("\nSummary by Dataset and Model (Mean across 3 seeds):")
    summary = df.groupby(['dataset', 'model']).agg({
        'roc_auc': ['mean', 'std'],
        'ap': ['mean', 'std'],
        'bal_acc': ['mean', 'std'],
        'time_sec': 'mean'
    }).round(4)
    print(summary)
    df.to_csv(os.path.join(config.DATA_DIR, 'ch2_tabular_results.csv'), index=False)
    print("Saved results to tieuluan1/data/ch2_tabular_results.csv")
