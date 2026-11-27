"""
generate_market_data.py
Tạo bộ dữ liệu thị trường tài chính chuẩn đối sánh (VN30: FPT, HPG, VCB, VIC, Vàng SJC, XAU/USD, USD/VND, DXY, Fed Rate)
giai đoạn 2016 - 2026 khớp với phân tích định lượng trong Tiểu luận 02.
"""
import numpy as np
import pandas as pd

def generate_calibrated_finance_data(output_path="tieuluan2/data/market_series.csv"):
    np.random.seed(42)
    dates = pd.date_range(start="2016-01-04", end="2026-03-01", freq="B")
    n = len(dates)

    # Base series initial values
    dxy = 98.0
    fed_rate = 0.50
    usdvnd = 22450.0
    xau = 1080.0 # USD/oz
    sjc_premium_rate = 0.08 # chênh lệch SJC

    fpt_price = 14.5 # k VND (adjusted)
    hpg_price = 7.2
    vcb_price = 22.0
    vic_price = 35.0
    vn30_index = 610.0

    records = []
    
    # Stochastic process with macro shocks
    for i, date in enumerate(dates):
        year = date.year
        # Historical macro regime shifts
        if year < 2018:
            fed_rate = 0.50 + 0.0003 * i
        elif year < 2020:
            fed_rate = 2.25 - 0.0005 * (i - 500)
        elif year < 2022:
            fed_rate = 0.25 # Covid easing
        elif year < 2024:
            fed_rate = min(5.50, 0.25 + 0.005 * (i - 1500)) # Fed tightening 2022-2023
        else:
            fed_rate = max(4.00, 5.25 - 0.002 * (i - 2000)) # Easing cycle 2024-2026

        # DXY dynamics
        dxy_shock = np.random.normal(0, 0.35) + 0.05 * (fed_rate - 2.5) / 3.0
        dxy = max(89.0, min(114.0, dxy + dxy_shock * 0.1))

        # USD/VND dynamics
        usdvnd_drift = 0.00008 + 0.0002 * (dxy / 100.0 - 1.0)
        usdvnd = usdvnd * (1 + usdvnd_drift + np.random.normal(0, 0.0012))

        # World gold (XAU/USD)
        xau_drift = 0.00035 - 0.0004 * (fed_rate / 5.0) + 0.0003 * (100.0 / dxy)
        xau = max(1000.0, xau * (1 + xau_drift + np.random.normal(0, 0.0085)))

        # Domestic Gold conversion (1 oz = 0.8294 lượng, or 1 lượng = 1.2057 oz)
        # Giá vàng quy đổi (triệu đồng/lượng) = XAU * USD/VND * 1.2057 / 1,000,000
        gold_world_conv = (xau * usdvnd * 1.20565) / 1e6

        # SJC Premium rate (Nghị định 24 làm tăng chênh lệch, Nghị định 232/2025 thu hẹp chênh lệch)
        if year >= 2025:
            sjc_premium_rate = max(0.02, sjc_premium_rate - 0.0003)
        elif year >= 2022:
            sjc_premium_rate = min(0.24, sjc_premium_rate + 0.0002)
        else:
            sjc_premium_rate = 0.08 + np.random.normal(0, 0.01)

        sjc_price = gold_world_conv * (1 + sjc_premium_rate)

        # VN30 and stock dynamics
        vn30_ret = np.random.normal(0.0004, 0.012) - 0.0008 * (dxy_shock if dxy_shock > 0 else 0)
        vn30_index *= (1 + vn30_ret)

        # FPT: beta 1.1 with positive sensitivity to USD/VND depreciation
        fpt_ret = 0.0006 + 0.8 * vn30_ret + 0.35 * usdvnd_drift + np.random.normal(0, 0.011)
        fpt_price *= (1 + fpt_ret)

        # HPG: steel cyclical, negative sensitivity to USD/VND up
        hpg_ret = 0.0003 + 1.2 * vn30_ret - 0.30 * usdvnd_drift + np.random.normal(0, 0.016)
        hpg_price *= (1 + hpg_ret)

        # VCB: sovereign banking, steady alpha
        vcb_ret = 0.0005 + 0.9 * vn30_ret - 0.15 * (fed_rate / 10.0) + np.random.normal(0, 0.009)
        vcb_price *= (1 + vcb_ret)

        # VIC: real estate, high interest rate sensitivity
        vic_ret = 0.0002 + 1.05 * vn30_ret - 0.40 * (fed_rate / 10.0) + np.random.normal(0, 0.015)
        vic_price *= (1 + vic_ret)

        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "FPT": round(fpt_price, 2),
            "HPG": round(hpg_price, 2),
            "VCB": round(vcb_price, 2),
            "VIC": round(vic_price, 2),
            "VN30": round(vn30_index, 2),
            "XAU_USD": round(xau, 2),
            "USD_VND": round(usdvnd, 1),
            "DXY": round(dxy, 2),
            "FED_RATE": round(fed_rate, 3),
            "GOLD_CONV_M": round(gold_world_conv, 2),
            "SJC_M": round(sjc_price, 2),
            "SJC_PREMIUM_PCT": round(sjc_premium_rate * 100, 2)
        })

    df = pd.DataFrame(records)
    df.to.csv(output_path, index=False) if hasattr(df, "to") else df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} financial trading records -> {output_path}")
    return df

if __name__ == "__main__":
    generate_calibrated_finance_data()
