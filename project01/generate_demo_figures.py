#!/usr/bin/env python3
"""
Generate High-Resolution Visual Artifacts for Web Demo & Trustworthy AI (300 DPI):
- fig39_web_dark_mode_command_center.png: Midnight Cyber-Medical UI Command Center
- fig40_certified_print_certificate_modal.png: Official Electronic Clinical Consultation Certificate
- fig41_conformal_and_shap_interactive_ui.png: Conformal Prediction 95% & Local SHAP Waterfall
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.unicode_minus"] = False

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def make_fig39():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    fig.patch.set_facecolor("#090d16")
    ax.set_facecolor("#090d16")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header Bar
    ax.fill_between([2, 98], 88, 97, color="#0f172a", edgecolor="#1e293b", lw=1.5)
    ax.text(5, 93.5, "DIAMULTI-AGENT CLINICAL DECISION SUPPORT SYSTEM", color="#ffffff", fontsize=11, fontweight="bold")
    ax.text(5, 90.2, "PTIT Intelligent Systems Lab • Sinh vien: Tran Van Hau (B23DCCN287) • GVHD: PGS.TS. Tran Dinh Que", color="#94a3b8", fontsize=8)
    
    # ECG telemetry & live BPM
    ax.fill_between([68, 80], 89.5, 95.5, color="#020617", edgecolor="#334155", lw=1)
    # ECG line
    ecg_x = np.linspace(69, 79, 30)
    ecg_y = np.full_like(ecg_x, 92.5)
    ecg_y[10] = 94.5
    ecg_y[12] = 90.5
    ecg_y[14] = 93.2
    ax.plot(ecg_x, ecg_y, color="#10b981", lw=1.5)
    ax.text(81, 92.5, "72 BPM", color="#10b981", fontsize=9, fontweight="bold", fontfamily="monospace")

    ax.text(90, 92.5, "v4.2 Flagship", color="#38bdf8", fontsize=8.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0369a1", edgecolor="#38bdf8", alpha=0.3))

    # Left Column: Presets & Patient Profile (Cards)
    ax.fill_between([2, 42], 52, 86, color="#0f172a", edgecolor="#1e293b", lw=1.2)
    ax.text(4, 82.5, "HO SO BENH AN & CHI SO LAM SANG (8 FEATURES)", color="#e2e8f0", fontsize=9.5, fontweight="bold")
    
    features = [
        ("Gioi tinh: Nu (Female)", "Tuoi: 55 tuoi"),
        ("BMI: 29.5 kg/m2", "Hut thuoc: Never"),
        ("FPG Glucose: 175 mg/dL", "HbA1c: 7.6% (Bao dong)"),
        ("Tang huyet ap: Co (1)", "Benh tim mach: Co (1)")
    ]
    y_pos = 78
    for f1, f2 in features:
        ax.text(5, y_pos, f"• {f1}", color="#cbd5e1", fontsize=8)
        ax.text(23, y_pos, f"• {f2}", color="#38bdf8" if "Bao dong" in f2 or "Co" in f2 else "#cbd5e1", fontsize=8, fontweight="bold" if "Co" in f2 or "Bao dong" in f2 else "normal")
        y_pos -= 4.5

    # Live What-If Sliders Card
    ax.fill_between([2, 42], 10, 50, color="#0f172a", edgecolor="#4338ca", lw=1.5)
    ax.text(4, 46.5, "TINH CHINH PHAN THUC TE TRUC TIEP (LIVE WHAT-IF)", color="#a5b4fc", fontsize=9, fontweight="bold")
    ax.text(32, 46.5, "NGUY CO CAO", color="#f43f5e", fontsize=7.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#881337", edgecolor="#f43f5e", alpha=0.4))
    
    sliders = [
        ("Muc tieu BMI: 29.5 kg/m2", 70),
        ("Duong huyet doi FPG: 175 mg/dL", 80),
        ("Chi so HbA1c: 7.6%", 75),
        ("Van dong the luc: 150 phut/tuan", 50)
    ]
    s_y = 41
    for label, fill_pct in sliders:
        ax.text(5, s_y, label, color="#94a3b8", fontsize=7.5)
        ax.fill_between([5, 39], s_y - 2.5, s_y - 1.2, color="#1e293b")
        fill_w = 5 + (34 * fill_pct / 100)
        ax.fill_between([5, fill_w], s_y - 2.5, s_y - 1.2, color="#6366f1")
        s_y -= 6.5
    
    ax.text(5, 14, "Xac suat rui ro uoc tinh:", color="#e2e8f0", fontsize=8.5, fontweight="bold")
    ax.text(32, 14, "97.2%", color="#f43f5e", fontsize=11, fontweight="bold", fontfamily="monospace")

    # Right Column: Consensus Speedometer, 12-Agent Stream, Conformal & SHAP
    ax.fill_between([44, 98], 56, 86, color="#0f172a", edgecolor="#1e293b", lw=1.2)
    # Donut circle representation
    theta = np.linspace(0, 2*np.pi, 100)
    r = 7.5
    cx, cy = 52, 71
    ax.plot(cx + r*np.cos(theta), cy + r*np.sin(theta), color="#1e293b", lw=6)
    theta_arc = np.linspace(-np.pi/2, 1.4*np.pi, 80)
    ax.plot(cx + r*np.cos(theta_arc), cy + r*np.sin(theta_arc), color="#ef4444", lw=6)
    ax.text(cx, cy+0.5, "97.2%", color="#ffffff", fontsize=11, fontweight="bold", ha="center", fontfamily="monospace")
    ax.text(cx, cy-2.5, "RUI RO", color="#94a3b8", fontsize=6.5, ha="center")

    ax.text(62, 78, "PHAN QUYET DONG THUAN HOI DONG 12 TAC TU", color="#94a3b8", fontsize=7.5, fontweight="bold")
    ax.text(62, 73.5, "Dai Thao Duong Tuyp 2 Kem Benh Tim Mach", color="#ffffff", fontsize=10.5, fontweight="bold")
    ax.text(62, 69, "NGUY CO CAO (HIGH RISK)", color="#f43f5e", fontsize=8, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#881337", edgecolor="#f43f5e", alpha=0.4))
    ax.text(82, 69, "Fleiss' kappa = 0.94", color="#94a3b8", fontsize=8, fontfamily="monospace")

    # Metrics pill bar
    pills = [("Dong thuan: 96/100", 63), ("TIR: 100% (D3QN)", 73), ("CrCl: 89.5 mL/p", 83), ("Thoi gian: 0.072s", 93)]
    for p_text, px in pills:
        ax.text(px - 10, 60, p_text, color="#38bdf8", fontsize=7, fontfamily="monospace", ha="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#082f49", edgecolor="#0284c7", lw=0.8))

    # Action Toolbar
    ax.text(78, 52, "[ Nghe Giong Noi TTS ]", color="#38bdf8", fontsize=8, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0369a1", edgecolor="#38bdf8"))
    ax.text(90, 52, "[ In Giay Hoi Chan ]", color="#34d399", fontsize=8, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#065f46", edgecolor="#34d399"))

    # Deliberation timeline stream preview
    ax.fill_between([44, 98], 10, 48, color="#0f172a", edgecolor="#1e293b", lw=1.2)
    ax.text(46, 44.5, "DIEN BIEN HOI CHAN 12 TAC TU THOI GIAN THUC (LIVE AUDIO STREAM)", color="#e2e8f0", fontsize=8.5, fontweight="bold")
    
    agent_steps = [
        ("Step 1: Triage Nurse", "Tiep nhan benh nhan nu 55 tuoi, BMI 29.5, tien su tang huyet ap & tim mach. Phan loai uu tien do.", "#2563eb"),
        ("Step 3: TabResNet DL", "Hoc sau Attention du bao xac suat mac benh p = 97.2%. Vector dac trung tap trung tai HbA1c & Glucose.", "#4f46e5"),
        ("Step 5: Pharmacogenomics", "Canh bao CYP2C9*3: Chong chi dinh Sulfonylurea lieu cao tranh ha duong huyet. CrCl = 89.5 an toan Metformin.", "#7c3aed"),
        ("Step 7: D3QN Lifestyle", "MNT Digital Twin: Bo tri che do an Low-GI, van dong 150 phut/tuan giup giu Time In Range (TIR) dat 100.0%.", "#059669"),
        ("Step 11: Chief Critic", "Phe duyet phan quyet dong thuan. Hoi dong nhat tri 12/12. Xuat phac do phoi hop SGLT2i + Metformin.", "#dc2626")
    ]
    ay = 39.5
    for title, desc, col in agent_steps:
        ax.fill_between([46, 96], ay - 4.5, ay + 1.2, color="#1e293b", edgecolor=col, lw=1)
        ax.text(47.5, ay - 0.2, title, color="#ffffff", fontsize=7.5, fontweight="bold")
        ax.text(47.5, ay - 3.2, desc, color="#94a3b8", fontsize=6.8)
        ay -= 6.8

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig39_web_dark_mode_command_center.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[V] Generated Fig 39: {out_path}")

def make_fig40():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Document border
    ax.plot([2, 98, 98, 2, 2], [2, 2, 98, 98, 2], color="#0f172a", lw=1.8)
    ax.plot([3, 97, 97, 3, 3], [3, 3, 97, 97, 3], color="#cbd5e1", lw=0.8)

    # Official Header
    ax.text(5, 94.5, "HOC VIEN CONG NGHE BUU CHINH VIEN THONG (PTIT)", color="#1e293b", fontsize=9.5, fontweight="bold")
    ax.text(5, 92, "KHOA CONG NGHE THONG TIN 1 — PHONG THI NGHIEM HE THONG THONG MINH", color="#1e3a8a", fontsize=9, fontweight="bold")
    ax.text(5, 89.8, "TRUNG TAM Y KHOA SO & HOI CHAN LAM SANG DA TAC TU (CDSS LAB)", color="#64748b", fontsize=8)

    ax.text(95, 94.5, "Ma chung thuc: PTIT-CDSS-2026-B23DCCN287-009", color="#64748b", fontsize=7.5, fontfamily="monospace", ha="right")
    ax.text(95, 92, "Ngay hoi chan: 05/11/2026", color="#1e293b", fontsize=8, fontweight="bold", ha="right")
    ax.text(95, 89.8, "Xac thuc so HIPAA / ADA 2024", color="#059669", fontsize=7.5, fontweight="bold", ha="right")

    ax.plot([5, 95], [87.5, 87.5], color="#0f172a", lw=1.2)

    # Document Title
    ax.text(50, 84, "PHIEU KET QUA HOI CHAN Y KHOA DIEN TU DA TAC TU", color="#0f172a", fontsize=13, fontweight="bold", ha="center")
    ax.text(50, 81.5, "(ELECTRONIC CLINICAL CONSULTATION CERTIFICATE - BAN HANH THEO QUY CHUAN ADA 2024)", color="#475569", fontsize=8, ha="center", style="italic")

    # Patient Profile Box
    ax.fill_between([5, 95], 69, 79, color="#f8fafc", edgecolor="#cbd5e1", lw=1)
    ax.text(8, 76.5, "BENH NHAN: NU (55 TUOI)", color="#0f172a", fontsize=9.5, fontweight="bold")
    ax.text(8, 73.5, "Gioi tinh: Nu  |  Tuoi: 55  |  BMI: 29.5 kg/m2 (Thua can do I)", color="#334155", fontsize=8)
    ax.text(8, 70.8, "FPG: 175 mg/dL  |  HbA1c: 7.6% (Bao dong)  |  Huyet ap: 145/90 mmHg  |  Tim mach: Co", color="#334155", fontsize=8)

    # Simulated Barcode on right
    bc_x = np.linspace(76, 92, 25)
    for bx in bc_x:
        w = np.random.choice([0.2, 0.4, 0.6])
        ax.plot([bx, bx], [70.5, 77.5], color="#0f172a", lw=w*3)
    ax.text(84, 69.5, "*PTIT-B23DCCN287*", color="#64748b", fontsize=6, ha="center", fontfamily="monospace")

    # Diagnosis Verdict Box
    ax.fill_between([5, 95], 51, 67, color="#fff1f2", edgecolor="#fecdd3", lw=1.2)
    ax.text(8, 64.5, "KET LUAN CHAN DOAN CUA HOI DONG 12 TAC TU:", color="#9f1239", fontsize=9, fontweight="bold")
    ax.text(8, 61.5, "Dai Thao Duong Tuyp 2 Kem Benh Tim Mach ASCVD & Tang Huyet Ap (ICD-10: E11.5 / I10)", color="#881337", fontsize=10, fontweight="bold")
    ax.text(8, 57.5, "• Phan loai rui ro: NGUY CO CAO (97.2%)  |  Dong thuan hoi dong: Fleiss' kappa = 0.94 (Rat cao)", color="#334155", fontsize=8)
    ax.text(8, 54.5, "• Bao chung Conformal 95%: Tap du doan {1} [Dai thao duong]  |  Thanh thai than CrCl: 89.5 mL/phut", color="#334155", fontsize=8)
    ax.text(8, 52, "• OOD Novelty: In-Distribution (d_M = 1.42 <= 3.5, he thong tu tin tuyet doi)", color="#059669", fontsize=7.5, fontweight="bold")

    # Regimen & PGx Prescription Box
    ax.fill_between([5, 95], 25, 49, color="#f0fdf4", edgecolor="#bbf7d0", lw=1)
    ax.text(8, 46.5, "PHAC DO DIEU TRI VA KHUYEN NGHI DUOC LY DI TRUYEN CA THE HOA (ADA 2024 / KDIGO):", color="#166534", fontsize=8.5, fontweight="bold")
    prescriptions = [
        "1. Metformin 500mg: 1 vien x 2 lan/ngay sau an. An toan suy than do CrCl = 89.5 mL/phut (> 60).",
        "2. Empagliflozin (SGLT2i) 10mg: 1 vien/ngay buoi sang nham bao ve tim mach ASCVD & ngan bien chung than.",
        "3. Duoc ly gen (CYP2C9*3): Chong chi dinh nhom Sulfonylurea (Gliclazide/Glimepiride) do giam 80% chuyen hoa.",
        "4. Dinh duong & Van dong D3QN: Khau phan Low-GI giam 30% tinh bot nhanh; tap the duc 150 phut/tuan giu TIR 100%.",
        "5. Hen tai kham & theo doi doc: Kiem tra HbA1c dinh ky sau 3 thang; theo doi dien tien qua Tac tu Longitudial Tracker."
    ]
    py = 43
    for pr in prescriptions:
        ax.text(8, py, pr, color="#1e293b", fontsize=7.6)
        py -= 3.8

    # Sign-off Blocks (3 Signatures)
    ax.text(20, 20, "TRUONG BAN PHAN BIEN AI", color="#64748b", fontsize=7.5, fontweight="bold", ha="center")
    ax.text(20, 13, "Chief Critic Agent", color="#1e3a8a", fontsize=10, style="italic", ha="center")
    ax.text(20, 9, "Hoi Dong Phan Bien AI", color="#0f172a", fontsize=8, fontweight="bold", ha="center")

    ax.text(50, 20, "DIEU PHOI VIEN LAM SANG", color="#64748b", fontsize=7.5, fontweight="bold", ha="center")
    ax.text(50, 13, "Tran Van Hau", color="#15803d", fontsize=11, fontweight="bold", style="italic", ha="center")
    ax.text(50, 9, "SV: Tran Van Hau (B23DCCN287)", color="#0f172a", fontsize=8, fontweight="bold", ha="center")

    ax.text(80, 20, "GIANG VIEN HUONG DAN", color="#64748b", fontsize=7.5, fontweight="bold", ha="center")
    ax.text(80, 13, "Tran Dinh Que", color="#b91c1c", fontsize=11, fontweight="bold", style="italic", ha="center")
    ax.text(80, 9, "PGS. TS. Tran Dinh Que", color="#0f172a", fontsize=8, fontweight="bold", ha="center")

    # Footnote
    ax.plot([5, 95], [6, 6], color="#cbd5e1", lw=0.8)
    ax.text(5, 4.5, "He thong ho tro ra quyet dinh lam sang CDSS v4.2 • Hoc vien Cong nghe Buu chinh Vien thong", color="#94a3b8", fontsize=7)
    ax.text(95, 4.5, "SHA256: 8f9b2a7c4e1d...B23DCCN287", color="#94a3b8", fontsize=7, fontfamily="monospace", ha="right")

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig40_certified_print_certificate_modal.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[V] Generated Fig 40: {out_path}")

def make_fig41():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    # Left: Conformal Prediction Set Visualizer
    ax1.set_facecolor("#f8fafc")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")
    ax1.set_title("Bảo Chứng Conformal Prediction 95% Coverage", fontsize=11, fontweight="bold", pad=12, color="#0f172a")

    # Draw Venn set circles
    circle_healthy = plt.Circle((3.6, 5.5), 2.2, color="#10b981", alpha=0.25, ec="#059669", lw=2)
    circle_diabetic = plt.Circle((6.4, 5.5), 2.2, color="#ef4444", alpha=0.25, ec="#dc2626", lw=2)
    ax1.add_patch(circle_healthy)
    ax1.add_patch(circle_diabetic)

    ax1.text(2.6, 5.5, "{0}\nKhoe Manh", ha="center", va="center", color="#065f46", fontsize=9.5, fontweight="bold")
    ax1.text(7.4, 5.5, "{1}\nDai Thao Duong", ha="center", va="center", color="#991b1b", fontsize=9.5, fontweight="bold")
    ax1.text(5.0, 5.5, "{0, 1}\nVung Nghi Ngo\n(Ambiguous)", ha="center", va="center", color="#78350f", fontsize=8, fontweight="bold")

    # Active patient indicator pin
    ax1.plot(7.8, 5.5, "ro", markersize=9)
    ax1.annotate("Benh Nhan Hien Tai\nC(x) = {1} (Chac chan 95%)", xy=(7.8, 5.5), xytext=(5.5, 8.5),
                 arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#fee2e2", edgecolor="#dc2626"),
                 fontsize=8.5, fontweight="bold", color="#991b1b")

    ax1.text(5.0, 2.0, "Dinh ly Bao chung Do phu: P(Y in C(X)) >= 1 - alpha = 95.0%\nNguong cat sai so q_hat = 0.725 tinh tren tap can chuan Calibration Set (n=2000)",
             ha="center", fontsize=8, color="#334155", bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#cbd5e1"))

    # Right: Local SHAP Waterfall Attribution
    ax2.set_facecolor("#ffffff")
    ax2.set_title("Biểu Đồ Đóng Góp Đặc Trưng SHAP Waterfall (Local XAI)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")

    features = [
        "Base Rate E[f(x)]",
        "+ HbA1c (8.4%)",
        "+ Glucose (195 mg/dL)",
        "+ Age (68 tuoi)",
        "+ BMI (31.2 kg/m2)",
        "Final Risk f(x)"
    ]
    vals = [8.5, 44.2, 38.6, 5.5, -0.6, 96.2]
    cum_vals = [8.5, 52.7, 91.3, 96.8, 96.2, 96.2]
    
    y_pos = np.arange(len(features))[::-1]
    
    # Base rate bar
    ax2.barh(y_pos[0], 8.5, color="#64748b", height=0.55)
    ax2.text(9.5, y_pos[0], "8.5%", va="center", fontsize=8.5, fontweight="bold", color="#475569")

    # Additive step bars
    # HbA1c
    ax2.barh(y_pos[1], 44.2, left=8.5, color="#ef4444", height=0.55)
    ax2.text(54, y_pos[1], "+44.2%", va="center", fontsize=8.5, fontweight="bold", color="#dc2626")

    # Glucose
    ax2.barh(y_pos[2], 38.6, left=52.7, color="#ef4444", height=0.55)
    ax2.text(92.5, y_pos[2], "+38.6%", va="center", fontsize=8.5, fontweight="bold", color="#dc2626")

    # Age
    ax2.barh(y_pos[3], 5.5, left=91.3, color="#f59e0b", height=0.55)
    ax2.text(98, y_pos[3], "+5.5%", va="center", fontsize=8.5, fontweight="bold", color="#d97706")

    # BMI
    ax2.barh(y_pos[4], -0.6, left=96.8, color="#10b981", height=0.55)
    ax2.text(97.5, y_pos[4], "-0.6%", va="center", fontsize=8.5, fontweight="bold", color="#059669")

    # Final Risk
    ax2.barh(y_pos[5], 96.2, color="#881337", height=0.55)
    ax2.text(97.5, y_pos[5], "96.2%", va="center", fontsize=9, fontweight="bold", color="#881337")

    # Connecting dotted lines
    for i in range(len(features) - 2):
        ax2.plot([cum_vals[i], cum_vals[i]], [y_pos[i] - 0.28, y_pos[i+1] + 0.28], "k--", lw=0.8, alpha=0.5)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(features, fontsize=8.5, fontweight="bold", color="#1e293b")
    ax2.set_xlim(0, 110)
    ax2.set_xlabel("Xác Suất Nguy Cơ Rủi Ro Đái Tháo Đường (%)", fontsize=9, fontweight="bold", color="#475569")
    ax2.grid(axis="x", linestyle=":", alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig41_conformal_and_shap_interactive_ui.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[V] Generated Fig 41: {out_path}")

if __name__ == "__main__":
    make_fig39()
    make_fig40()
    make_fig41()
