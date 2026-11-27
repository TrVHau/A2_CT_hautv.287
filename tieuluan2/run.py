"""
run.py
Điểm khởi chạy trung tâm (Master CLI Entrypoint) cho Tiểu luận 2:
Hỗ trợ kiểm thử, huấn luyện mô hình, sinh biểu đồ, chạy demo CLI và khởi động Web Dashboard.
"""
import sys
import os
import argparse

# Ensure utf-8 encoding for console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_demo():
    print("\n" + "="*70)
    print("DEMO HỆ THỐNG TÁC TỬ THÔNG MINH (KG + RAG + MULTI-AGENT) - TIỂU LUẬN 2")
    print("="*70)

    from tieuluan2.agents.react_orchestrator import ReActAgent
    agent = ReActAgent()

    test_queries = [
        (
            "TÌNH HUỐNG LÂM SÀNG 1 (Y TẾ):",
            "Tôi nam 52 tuổi, HbA1c 7.3, glucose lúc đói 138, BMI 26.5. Đang uống Metformin 500mg, tối nay đi tiệc có uống rượu bia được không?"
        ),
        (
            "TÌNH HUỐNG DINH DƯỠNG 2 (Y TẾ):",
            "Bị đái tháo đường típ 2 có ăn được thịt gà và cơm trắng không? Hướng dẫn cách ăn đúng."
        ),
        (
            "TÌNH HUỐNG VĨ MÔ 3 (TÀI CHÍNH):",
            "Tỷ giá USD/VND tăng mạnh thì cổ phiếu FPT và HPG bị ảnh hưởng như thế nào?"
        ),
        (
            "TÌNH HUỐNG THỊ TRƯỜNG VÀNG 4 (TÀI CHÍNH):",
            "Nghị định 232/2025/NĐ-CP thay đổi gì đối với vàng miếng SJC và giá thế giới quy đổi hôm nay bao nhiêu?"
        )
    ]

    for title, q in test_queries:
        print(f"\n>>> {title}")
        print(f"Câu hỏi: {q}")
        res = agent.run(q)
        print(f"Miền: {res['domain'].upper()} | Thời gian: {res['total_ms']} ms")
        print("\n--- CÁC BƯỚC SUY LUẬN (REACT TRACE) ---")
        for step in res["trace"]:
            if step["type"] == "THOUGHT":
                print(f"  💭 [THOUGHT]: {step['text']}")
            elif step["type"] == "ACTION":
                print(f"  ⚙️ [ACTION]: Tool '{step['tool']}' ({step['kind']}) [{step['ms']} ms]")
            else:
                print(f"  👁️ [OBSERVATION]: {step['text'][:140]}...")
        print("\n--- CÂU TRẢ LỜI ĐÃ KIỂM CHỨNG ---")
        print(res["answer"])
        print(f"Trạng thái kiểm định: {res['verification']}")
        print("-" * 70)

def main():
    parser = argparse.ArgumentParser(description="CLI Runner cho Tiểu Luận 2")
    parser.add_argument("--test", action="store_true", help="Chạy bộ kiểm thử tự động unittest")
    parser.add_argument("--train", action="store_true", help="Huấn luyện mô hình ResMLP và BiLSTM")
    parser.add_argument("--figures", action="store_true", help="Sinh 14 biểu đồ khoa học 300 DPI")
    parser.add_argument("--serve", action="store_true", help="Khởi chạy máy chủ Web FastAPI trên cổng 8092")
    parser.add_argument("--demo", action="store_true", help="Chạy demo CLI tương tác")

    args = parser.parse_args()

    if args.test:
        import unittest
        from tieuluan2.test_all import TestIntelligentSystem
        suite = unittest.TestLoader().loadTestsFromTestCase(TestIntelligentSystem)
        unittest.TextTestRunner(verbosity=2).run(suite)
    elif args.train:
        from tieuluan2.models.train_healthcare import train_healthcare_model
        from tieuluan2.models.train_finance import train_finance_model
        train_healthcare_model()
        train_finance_model()
    elif args.figures:
        from tieuluan2.generate_tieuluan2_figures import main as gen_figs
        gen_figs()
    elif args.serve:
        import uvicorn
        print("Đang khởi chạy máy chủ FastAPI tại http://127.0.0.1:8092 ...")
        uvicorn.run("tieuluan2.web.app:app", host="127.0.0.1", port=8092, reload=False)
    else:
        # Default run demo
        run_demo()

if __name__ == "__main__":
    main()
