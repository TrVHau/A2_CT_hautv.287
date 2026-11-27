import numpy as np
import pandas as pd

def run_backtest(prices, probs, threshold=0.5, fee_rate=0.0005, annual_factor=252):
    """
    Simulate quantitative long/cash strategy on test set.
    
    Parameters:
    - prices: 1D array of daily closing prices
    - probs: 1D array of predicted probabilities of next-day upward move
    - threshold: decision cutoff (selected on validation)
    - fee_rate: one-way trading fee (e.g., 0.0005 for SP500, 0.0020 for VNIndex)
    - annual_factor: trading days per year (252 for stocks, 365 for crypto)
    """
    # Next-day percentage return: R_t = (P_{t+1} - P_t) / P_t
    raw_returns = (prices[1:] - prices[:-1]) / prices[:-1]
    n = min(len(probs), len(raw_returns))
    raw_returns = raw_returns[:n]
    
    # Position: 1 if prob >= threshold else 0
    positions = (probs[:n] >= threshold).astype(float)
    
    # Detect trades: transition from 0 to 1 (buy) or 1 to 0 (sell)
    position_changes = np.diff(np.insert(positions, 0, 0.0))
    trades_count = np.sum(np.abs(position_changes) > 0)
    
    # Strategy daily returns before fee
    strat_returns_pre_fee = positions * raw_returns
    
    # Transaction cost impact: deduction on trade day
    fee_impact = np.abs(position_changes) * fee_rate
    strat_returns_post_fee = strat_returns_pre_fee - fee_impact
    
    # Cumulative NAV curves (starting at 1.0)
    cum_nav_pre = np.cumprod(1.0 + strat_returns_pre_fee)
    cum_nav_post = np.cumprod(1.0 + strat_returns_post_fee)
    cum_nav_buy_hold = np.cumprod(1.0 + raw_returns)
    
    # Metrics computation
    total_days = n
    years = total_days / annual_factor
    
    cagr_pre = (cum_nav_pre[-1] ** (1.0 / max(years, 0.1))) - 1.0
    cagr_post = (cum_nav_post[-1] ** (1.0 / max(years, 0.1))) - 1.0
    cagr_bh = (cum_nav_buy_hold[-1] ** (1.0 / max(years, 0.1))) - 1.0
    
    vol_pre = np.std(strat_returns_pre_fee) * np.sqrt(annual_factor)
    vol_post = np.std(strat_returns_post_fee) * np.sqrt(annual_factor)
    vol_bh = np.std(raw_returns) * np.sqrt(annual_factor)
    
    sharpe_post = cagr_post / (vol_post + 1e-8)
    sharpe_bh = cagr_bh / (vol_bh + 1e-8)
    
    # Sortino ratio: downside deviation only
    downside_rets = strat_returns_post_fee[strat_returns_post_fee < 0]
    downside_vol = np.std(downside_rets) * np.sqrt(annual_factor) if len(downside_rets) > 0 else 1e-8
    sortino_post = cagr_post / (downside_vol + 1e-8)
    
    # Maximum Drawdown
    running_max = np.maximum.accumulate(cum_nav_post)
    drawdowns = (cum_nav_post - running_max) / running_max
    max_drawdown_post = np.abs(np.min(drawdowns))
    
    running_max_bh = np.maximum.accumulate(cum_nav_buy_hold)
    drawdowns_bh = (cum_nav_buy_hold - running_max_bh) / running_max_bh
    max_drawdown_bh = np.abs(np.min(drawdowns_bh))
    
    # Calmar ratio
    calmar_post = cagr_post / (max_drawdown_post + 1e-8)
    
    # Holding period percentage
    holding_pct = np.mean(positions)
    
    # Win rate and Profit factor
    trade_returns = strat_returns_post_fee[positions == 1.0]
    win_rate = np.mean(trade_returns > 0) if len(trade_returns) > 0 else 0.0
    gross_profits = np.sum(trade_returns[trade_returns > 0]) if np.any(trade_returns > 0) else 1e-8
    gross_losses = np.abs(np.sum(trade_returns[trade_returns < 0])) if np.any(trade_returns < 0) else 1e-8
    profit_factor = gross_profits / gross_losses

    return {
        'cagr_pre': cagr_pre,
        'cagr_post': cagr_post,
        'cagr_bh': cagr_bh,
        'vol_post': vol_post,
        'vol_bh': vol_bh,
        'sharpe_post': sharpe_post,
        'sharpe_bh': sharpe_bh,
        'sortino_post': sortino_post,
        'calmar_post': calmar_post,
        'max_drawdown_post': max_drawdown_post,
        'max_drawdown_bh': max_drawdown_bh,
        'holding_pct': holding_pct,
        'trades_count': int(trades_count),
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'cum_nav_post': cum_nav_post,
        'cum_nav_buy_hold': cum_nav_buy_hold
    }

def block_bootstrap_ci(y_true, y_pred, metric_fn, block_size=20, n_bootstraps=1000, ci=0.95):
    """
    Circular Block Bootstrap for time-series dependent confidence interval estimation.
    Resamples contiguous blocks of size 20 to preserve autocorrelation structure.
    """
    n = len(y_true)
    num_blocks = int(np.ceil(n / block_size))
    scores = []
    
    np.random.seed(42)
    for _ in range(n_bootstraps):
        start_indices = np.random.randint(0, n, size=num_blocks)
        sample_indices = []
        for s in start_indices:
            # circular wrap around
            block = [(s + k) % n for k in range(block_size)]
            sample_indices.extend(block)
        sample_indices = np.array(sample_indices[:n])
        
        try:
            score = metric_fn(y_true[sample_indices], y_pred[sample_indices])
            scores.append(score)
        except Exception:
            continue
            
    scores = np.array(scores)
    lower = np.percentile(scores, (1.0 - ci) / 2.0 * 100)
    upper = np.percentile(scores, (1.0 + ci) / 2.0 * 100)
    return lower, upper
