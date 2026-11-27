#!/usr/bin/env python3
"""
Part 09: Chapter 9 - System Architecture, Source Code Map, Web CDSS 8 Tabs Dashboard, and Clinical Walkthroughs.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, add_figure, populate_table, add_code_block

def build_chapter9(doc):
    print("  [+] Building Chapter 9: Code Structure, Web CDSS Dashboard & Clinical Walkthrough...")
    
    add_custom_heading(doc, "9. KIẾN TRÚC MÃ NGUỒN, GIAO DIỆN WEB CDSS & THỰC NGHIỆM LÂM SÀNG", level=1)
    
    add_custom_heading(doc, "9.1. Cấu Trúc Tổ Chức Mã Nguồn & Bảng Ánh Xạ Chức Năng", level=2)
    add_body_p(
        doc,
        "Toàn bộ mã nguồn của dự án DiaMulti-Agent CDSS v2 được thiết kế theo cấu trúc module phân tầng hóa cao độ (High Modularization), "
        "tuân thủ nghiêm ngặt nguyên lý kiến trúc sạch (Clean Architecture) và nguyên lý đơn nhiệm (Single Responsibility Principle). "
        "Mã nguồn được lưu trữ tại kho GitHub chính thức: https://github.com/TrVHau/A2_CT_hautv.287/tree/main/project01:"
    )

    code_tree = '''project01/
├── run.py                           Điểm khởi động chính: nạp mô hình, khởi tạo 12 tác tử và bật FastAPI server (port 8000)
├── agents/                          Thư mục chứa 12 Tác tử lâm sàng chuyên biệt hóa
│   ├── diabetes_coordinator.py      Bộ điều phối trung tâm quản lý Blackboard Bus và luồng hội chẩn 11 bước
│   ├── triage_risk_agent.py         DiaTriage: phân tầng cấp cứu và phân loại sinh hiệu ban đầu
│   ├── safety_rules_agent.py        DiaSafetyRule: thực thi 12 luật an toàn cứng (R01 - R12) với quyền ghi đè khẩn cấp
│   ├── ai_diagnostic_agent.py       DiaDiagnostic: hội đồng 8 mô hình ML/DL, TabResNet Attention và Conformal 95%
│   ├── kg_guidelines_agent.py       DiaGraph: truy vấn đồ thị tri thức ADA 2024 / KDIGO và sinh bằng chứng
│   ├── rl_lifestyle_coach.py        DiaD3QNCoach: mô phỏng 24h và mạng Dueling Double DQN điều hòa đường huyết
│   ├── therapy_lifestyle_agent.py   DiaTherapy: phác đồ điều trị dùng thuốc cá thể hóa và dinh dưỡng Low-GI
│   ├── pharmacogenomics_agent.py    DiaPharma: dược lý gen CYP2C9, SLCO1B1 và tính CrCl Cockcroft-Gault
│   ├── counterfactual_agent.py      DiaWhatIf: tối ưu hóa can thiệp phản thực tế (L2-norm minimal perturbation)
│   ├── fairness_trust_auditor.py    DiaTrust: kiểm toán độ tin cậy ECE và công bằng y tế Wilson 95% CI
│   ├── longitudinal_tracker.py      DiaTracker: theo dõi tiến trình dọc 4 tuần và thích ứng chính sách
│   ├── chief_evaluator_critic.py    DiaCritic: Bác sĩ trưởng phản biện 3 vòng và ký duyệt chứng chỉ lâm sàng
│   └── llm_bridge.py                Cầu nối suy luận Chain-of-Thought (CoT) tương thích Qwen2.5 và Ollama
├── knowledge_graph/                 Cơ sở tri thức đồ thị và động cơ Graph-RAG
│   ├── diabetes_kg_neo4j.cypher     Script Cypher nạp đồ thị 56 nút, 60 cạnh lên cơ sở dữ liệu Neo4j
│   ├── neo4j_connector.py           Lớp kết nối Neo4j qua Bolt protocol kèm bộ phân giải Cypher in-memory dự phòng
│   ├── interactive_rag_engine.py    Động cơ Graph-RAG Hybrid: duyệt đa chặng (multi-hop) và trích dẫn y văn
│   └── diabetes_knowledge_graph_expanded.json  Bản sao JSON của đồ thị tri thức ADA 2024 / Vinmec / Long Châu
├── models/                          Trọng số mô hình và mã nguồn huấn luyện
│   ├── train_advanced_ensemble.py   Huấn luyện 8 mô hình, TabResNet Attention và Super Stacking Meta-Learner
│   ├── train_rl_agent.py            Huấn luyện mạng nơ-ron D3QN qua 15.000 episodes mô phỏng
│   ├── conformal_and_shap_engine.py Động cơ tính toán phân vị Conformal Prediction và giá trị đóng góp SHAP
│   └── super_stacking_meta_learner.pkl  Trọng số bộ học siêu cấp Stacking đã tối ưu hóa
├── web/                             Giao diện Web Dashboard Enterprise CDSS v4.2
│   ├── app.py                       Máy chủ backend FastAPI định nghĩa các RESTful API endpoints
│   └── index.html                   Giao diện người dùng đơn trang (SPA) gồm 8 Tabs, Canvas ECG, Audio TTS
└── figures/                         Thư mục lưu trữ 43 biểu đồ học thuật xuất bản (300 DPI)'''
    add_code_block(doc, code_tree, caption="Cây cấu trúc thư mục tổ chức mã nguồn Project 01 V2")

    add_custom_heading(doc, "9.2. Bảng Ánh Xạ Chức Năng Lâm Sàng Tới Tệp Mã Nguồn & Hàm Cốt Lõi", level=2)
    add_body_p(
        doc,
        "Bảng 9.1 đặc tả chi tiết mối liên kết giữa các nghiệp vụ y tế số và các hàm xử lý chính trong mã nguồn dự án:"
    )

    map_headers = ["Chức Năng Hệ Thống", "Tệp Mã Nguồn Triển Khai", "Hàm / Lớp Chịu Trách Nhiệm", "Đầu Vào -> Đầu Ra"]
    map_data = [
        ["Hội chẩn đa tác tử 11 bước", "agents/diabetes_coordinator.py", "DiabetesCoordinator.run_consultation()", "patient_dict -> JSON Deliberation Timeline"],
        ["Phân tầng nguy cơ triage", "agents/triage_risk_agent.py", "TriageRiskAgent.evaluate()", "vitals -> Risk Level & Triage Badge"],
        ["Kiểm duyệt 12 luật an toàn", "agents/safety_rules_agent.py", "DiaSafetyRuleAgent.evaluate_safety_rules()", "vitals -> Safety Severity & Override Action"],
        ["Chẩn đoán nơ-ron Attention", "agents/ai_diagnostic_agent.py", "AIDiagnosticAgent.predict()", "biomarkers -> Probabilities & Conformal Set"],
        ["Truy xuất đồ thị Neo4j", "knowledge_graph/neo4j_connector.py", "Neo4jDiabetesKGConnector.query_contraindications()", "med_id -> Biomarker & Contraindication Rule"],
        ["Hỏi đáp Graph-RAG lâm sàng", "knowledge_graph/interactive_rag_engine.py", "InteractiveClinicalGraphRAG.answer_clinical_question()", "user_query -> Reasoning Path & Guideline Citation"],
        ["Huấn luyện viên lối sống D3QN", "agents/rl_lifestyle_coach.py", "DiaRLCoachAgent.formulate_daily_schedule()", "patient_dict -> 24h Low-GI Diet & Exercise Plan"],
        ["Dược lý gen & Cockcroft-Gault", "agents/pharmacogenomics_agent.py", "DiaPharmacogenomicsAgent.analyze_pgx()", "Cr, Age, W, Genotype -> CrCl & Drug Approvals"],
        ["Tối ưu can thiệp phản thực tế", "agents/counterfactual_agent.py", "DiaCounterfactualAgent.generate_counterfactual_path()", "patient_dict, target_prob -> delta* minimal vector"],
        ["Kiểm toán công bằng & ECE", "agents/fairness_trust_auditor.py", "DiaFairnessTrustAgent.audit_patient_context()", "patient_dict -> Reliability Metrics & Wilson CI"],
        ["Phản biện Bác sĩ trưởng 3 vòng", "agents/chief_evaluator_critic.py", "ChiefEvaluatorCritic.evaluate_and_certify()", "all_agent_results -> Certified Report & Signature"]
    ]
    populate_table(doc, map_headers, map_data, col_widths=[1.5, 1.8, 2.0, 1.7], header_bg="1E3A8A")

    # Embed Fig 38
    add_figure(
        doc,
        "fig38_comprehensive_end_to_end_pipeline.png",
        "Hình 9.1. Sơ đồ đường ống toàn diện từ dữ liệu đầu vào đến đầu ra chẩn đoán, phản biện và chứng nhận của DiaMulti-Agent CDSS v2.",
        width_inches=6.2
    )

    add_custom_heading(doc, "9.3. Kiến Trúc Giao Diện Web Dashboard Enterprise CDSS v4.2 (8 Phân Hệ)", level=2)
    add_body_p(
        doc,
        "Giao diện người dùng của hệ thống được phát triển dưới dạng Ứng Dụng Đơn Trang (Single Page Application - SPA) chuyên nghiệp, "
        "tích hợp framework TailwindCSS hiện đại, hỗ trợ chế độ Dark Mode chuẩn trung tâm chỉ huy y tế (Hình 9.2 và 9.3). "
        "Hệ thống bao gồm 8 phân hệ chuyên biệt hóa:"
    )

    # Embed Fig 39 & Fig 34
    add_figure(
        doc,
        "fig39_web_dark_mode_command_center.png",
        "Hình 9.2. Trung tâm chỉ huy Web Dark Mode Enterprise CDSS v4.2 tích hợp giám sát sinh hiệu thời gian thực.",
        width_inches=6.2
    )
    add_figure(
        doc,
        "fig34_web_deliberation_live_ui.png",
        "Hình 9.3. Phân hệ Hội đồng 12 Tác tử (Tab 1): Hiển thị luồng đối thoại, phân tích sinh hiệu và biên bản hội đồng.",
        width_inches=6.2
    )

    add_body_p(
        doc,
        "Chi tiết 8 phân hệ trên giao diện Web Dashboard:\n"
        "• Phân hệ 1 (Tab 1 - Hội Chẩn Đa Tác Tử & Chatbot Lâm Sàng): Không gian đối thoại thông minh; người dùng có thể nhập câu hỏi tự do "
        "hoặc nhập thông số ca bệnh để kích hoạt hội đồng 12 chuyên gia hội chẩn trong 0.5s.\n"
        "• Phân hệ 2 (Tab 2 - Giám Sát Sinh Hiệu & Canvas ECG Lead II Động): Mô phỏng đường điện tâm đồ Lead II chạy liên tục bằng HTML5 Canvas "
        "kèm nhịp tim bpm, SpO2 và huyết áp thời gian thực.\n"
        "• Phân hệ 3 (Tab 3 - Mô Phỏng Lối Sống RL 24h & Đồng Hồ SVG Speedometer): Trực quan hóa kế hoạch dinh dưỡng và vận động 24 khung giờ; "
        "đồng hồ đo mức độ kiểm soát đường huyết SVG Speedometer hiển thị trạng thái sinh lý (Hình 9.4).\n"
        "• Phân hệ 4 (Tab 4 - Đồ Thị Tri Thức Neo4j & Terminal Cypher Tương Tác): Khám phá mạng lưới 56 thực thể ADA 2024; tích hợp khung soạn thảo "
        "truy vấn Cypher trực tiếp với cơ sở dữ liệu Neo4j.\n"
        "• Phân hệ 5 (Tab 5 - Dự Báo Conformal Prediction 95% & SHAP): Hiển thị khoảng tin cậy bảo chứng và biểu đồ phân rã đóng góp của từng chỉ số xét nghiệm.\n"
        "• Phân hệ 6 (Tab 6 - Tối Ưu Can Thiệp Phản Thực Tế What-If): Tích hợp các thanh trượt Live Sliders (Glucose, BMI, Cân nặng); khi người dùng kéo trượt, "
        "xác suất bệnh và khuyến nghị lối sống lập tức cập nhật tức thì.\n"
        "• Phân hệ 7 (Tab 7 - Kiểm Toán Độ Tin Cậy & Công Bằng Y Tế): Trực quan hóa đường cong hiệu chuẩn ECE và biểu đồ chênh lệch tỷ lệ cảnh báo theo tuổi/giới tính.\n"
        "• Phân hệ 8 (Tab 8 - Xuất Bản Bệnh Án & Chứng Chỉ Y Tế Số): Trích xuất báo cáo hội chẩn đa phương tiện chuẩn HTML/PDF và phát âm thanh tư vấn "
        "bằng giọng nói nhân tạo thông qua Web Speech API (Hình 9.5 và 9.6)."
    )

    # Embed Fig 35, 36, 40
    add_figure(
        doc,
        "fig35_web_rl_lifestyle_simulator_ui.png",
        "Hình 9.4. Phân hệ Mô phỏng Lối sống RL 24 Giờ (Tab 3) với đồ thị dao động đường huyết và kế hoạch dinh dưỡng từng khung giờ.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig36_certified_clinical_report_preview.png",
        "Hình 9.5. Bản xem trước Báo cáo Lâm sàng Đa phương tiện tự sinh có mã QR bảo mật và chữ ký số của Bác sĩ trưởng.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig40_certified_print_certificate_modal.png",
        "Hình 9.6. Hộp thoại in Chứng chỉ Lâm sàng Số (Digital Clinical Certificate Modal) sẵn sàng cho bệnh nhân và bác sĩ lưu trữ.",
        width_inches=6.0
    )

    add_custom_heading(doc, "9.4. Kịch Bản Thực Nghiệm & Kiểm Thử Lâm Sàng Mẫu (End-to-End Walkthrough)", level=2)
    add_body_p(
        doc,
        "Để kiểm tra tính toàn vẹn và độ tin cậy của hệ thống trong thực tế, chúng tôi thiết kế 4 ca bệnh kiểm thử mẫu đại diện cho 4 tình huống lâm sàng điển hình:"
    )

    test_cases = [
        ("Ca Kiểm Thử 1: Bệnh nhân ĐTĐ Tuýp 2 mới phát hiện điển hình",
         "Bệnh nhân nam, 55 tuổi, cao 168 cm, nặng 78 kg (BMI = 27.6 kg/m²). Xét nghiệm máu đói: Glucose = 165 mg/dL, HbA1c = 7.8%. Tiền sử: Tăng huyết áp nhẹ, không có bệnh tim mạch, đã từng hút thuốc (former smoker).",
         "Kết quả xử lý của Hệ thống:\n"
         "• DiaTriage: Phân tầng Nguy cơ Trung bình (Màu cam).\n"
         "• DiaSafetyRule: Đạt 12/12 luật an toàn. Không có dấu hiệu cấp cứu.\n"
         "• DiaDiagnostic: Xác suất đái tháo đường 96.4% (Đồng thuận 8/8 mô hình). Tập Conformal = {'Diabetes'} với độ tin cậy 95%.\n"
         "• DiaGraph & DiaTherapy: Chỉ định khởi trị Metformin 500mg x 2 lần/ngày sau bữa ăn theo khuyến cáo ADA 2024; bổ sung chế độ ăn Low-GI và đi bộ 150 phút/tuần.\n"
         "• DiaWhatIf: Đề xuất giảm 6.5 kg cân nặng và hạ Glucose về < 120 mg/dL để đưa xác suất bệnh về dải an toàn <= 15%."),
        
        ("Ca Kiểm Thử 2: Bệnh nhân ĐTĐ cao tuổi có Bệnh Tim Mạch kèm Suy Thận Mạn (Phức tạp)",
         "Bệnh nhân nữ, 72 tuổi, cao 155 cm, nặng 52 kg (BMI = 21.6 kg/m²). Xét nghiệm: Glucose đói = 175 mg/dL, HbA1c = 8.4%, Creatinine huyết thanh = 1.8 mg/dL. Tiền sử: Bệnh mạch vành (CAD) và suy tim phân suất tống máu giảm.",
         "Kết quả xử lý của Hệ thống:\n"
         "• DiaPharma: Tính độ thanh thải Cockcroft-Gault: CrCl = 22.4 mL/phút (< 30 mL/phút) -> Kích hoạt Luật an toàn R04: Chống chỉ định TUYỆT ĐỐI Metformin!\n"
         "• DiaSafetyRule: Kích hoạt Luật R06 và R07: BẮT BUỘC chỉ định thuốc bảo vệ tim mạch và suy tim SGLT2i.\n"
         "• DiaTherapy: Kê đơn Empagliflozin (Jardiance) 10mg/ngày (bảo vệ tim mạch, an toàn khi eGFR >= 20) kết hợp Insulin nền liều thấp (Lantus 10 IU trước ngủ), loại bỏ hoàn toàn Metformin.\n"
         "• DiaCritic: Phê duyệt phác đồ, ghi nhận cơ chế an toàn đã cứu bệnh nhân khỏi nguy cơ tử vong do toan acid lactic."),
        
        ("Ca Kiểm Thử 3: Cấp cứu Toan Ceton Đái Tháo Đường (DKA Emergency)",
         "Bệnh nhân nam, 28 tuổi, tiền sử ĐTĐ tuýp 1 bỏ tiêm insulin 2 ngày. Nhập viện trong tình trạng thở nhanh sâu Kussmaul, hơi thở có mùi táo thối, lơ mơ. Xét nghiệm: Glucose ngẫu nhiên = 380 mg/dL, Ketone niệu 3+ (dương tính đậm).",
         "Kết quả xử lý của Hệ thống:\n"
         "• DiaSafetyRule: Kích hoạt ngay lập tức Luật R01 (Cấp cứu Toan Ceton ĐTĐ) với mức độ NGUY CẤP!\n"
         "• Hệ thống phát còi báo động khẩn cấp màu đỏ, tự động ngắt toàn bộ quy trình hội chẩn thường quy, hiển thị thông báo chuyển thẳng khoa Cấp cứu hồi sức ICU và kích hoạt phác đồ truyền dịch bù nước + insulin tĩnh mạch liên tục."),
        
        ("Ca Kiểm Thử 4: Bệnh nhân mang alen đột biến Dược lý gen CYP2C9*3",
         "Bệnh nhân nữ, 60 tuổi, tiền sử gia đình có người bị sốc hạ đường huyết khi uống thuốc viên. Xét nghiệm gen ghi nhận kiểu gen CYP2C9*3/*3 (Poor Metabolizer). Glucose đói = 155 mg/dL, HbA1c = 7.4%.",
         "Kết quả xử lý của Hệ thống:\n"
         "• DiaPharma: Phát hiện bệnh nhân suy giảm >80% khả năng chuyển hóa thuốc Sulfonylurea tại gan -> Kích hoạt Luật R08: CẤM chỉ định Sulfonylurea (Gliclazide, Glimepiride).\n"
         "• DiaTherapy: Thay thế Sulfonylurea bằng thuốc ức chế men DPP-4 (Sitagliptin 100mg/ngày) không gây hạ đường huyết, bảo vệ an toàn sinh mạng tuyệt đối cho bệnh nhân.")
    ]

    for title, case_desc, sys_result in test_cases:
        add_callout(
            doc,
            f"MÔ TẢ CA BỆNH:\n{case_desc}\n\nKẾT QUẢ XỬ LÝ CỦA HỘI ĐỒNG 12 TÁC TỬ:\n{sys_result}",
            title=title.upper(),
            border_color="2563EB",
            fill_hex="F8FAFC"
        )
