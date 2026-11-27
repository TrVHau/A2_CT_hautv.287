import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CHARTS_DIR = os.path.join(BASE_DIR, 'charts')
REPORTS_DIR = BASE_DIR
WEB_DIR = os.path.join(BASE_DIR, 'web')

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

# Random Seeds for Deterministic Multi-Run Benchmarking
SEEDS = [11, 22, 33]

# Time series configuration
WINDOW_SIZE = 20  # 20 trading sessions window
TEST_START_DATE = '2023-01-01'
VAL_START_DATE = '2020-01-01'

# Transaction costs (one-way fees + tax)
FEES = {
    'SP500': 0.0005,    # 0.05% ETF standard fee
    'VNINDEX': 0.0020,  # 0.20% brokerage + selling tax
    'BTC': 0.0010,      # 0.10% crypto spot exchange fee
    'ETH': 0.0010       # 0.10% crypto spot exchange fee
}

# Training Hyperparameters
BATCH_SIZE = 64
LEARNING_RATE = 0.001
MAX_EPOCHS = 60
PATIENCE = 8
GRAD_CLIP = 1.0
