#!/usr/bin/env python3
"""
Part 03: Chapter 3 - 12 Agents Council Architecture, Deliberation Protocols, Chief Critic Debate.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, add_figure, populate_table

def build_chapter3(doc):
    print("  [+] Building Chapter 3: 12-Agent Council Architecture & Deliberation Protocols...")
    
    add_custom_heading(doc, "3. KIẾN TRÚC TỔNG QUAN HỘI ĐỒNG 12 TÁC TỬ LÂM SÀNG (DIAMULTI-AGENT CDSS v2)", level=1)
    
    add_custom_heading(doc, "3.1. Danh Mục & Bảng Phân Công Nhiệm Vụ Chi Tiết Của 12 Tác Tử", level=2)
    add_body_p(
        doc,
        "Khác biệt với các hệ thống AI đơn nhiệm hoặc hệ thống 6–7 tác tử cơ sở, DiaMulti-Agent CDSS v2 thiết lập một Hội đồng Lâm sàng ảo "
        "gồm đúng 12 tác tử chuyên biệt hóa, mô phỏng hoàn chỉnh quy trình hội chẩn liên chuyên khoa (Multidisciplinary Team - MDT) tại một "
        "bệnh viện đa khoa quốc tế tiêu chuẩn JCI. Mỗi tác tử có một vai trò học thuật riêng, sở hữu công nghệ cốt lõi và tiêu chí đánh giá KPI độc lập:"
    )

    agent_headers = ["STT / Tên Tác Tử", "Vai Trò Lâm Sàng", "Dữ Liệu Đầu Vào", "Công Nghệ / Thuật Toán Cốt Lõi", "Sản Phẩm Đầu Ra", "Chỉ Số KPI"]
    agent_data = [
        ["1. DiaTriage\n(TriageRiskAgent)", "Tiếp đón, sàng lọc sơ bộ & phân tầng cấp cứu khẩn cấp.", "Triệu chứng 4P (khát, tiểu, đói, sụt cân), SpO2, mạch, huyết áp, tri giác.", "Phân loại phân tầng nguy cơ 4 mức (Khẩn cấp, Cao, Trung bình, Thấp) theo chuẩn Bộ Y tế.", "Thẻ phân loại triage, huy hiệu cảnh báo cấp cứu.", "Thời gian xử lý < 5ms; độ nhạy ca cấp cứu = 100%."],
        ["2. DiaSafetyRule\n(DiaSafetyRuleAgent)", "Giám sát an toàn y khoa, thực thi 12 luật bảo vệ sinh mạng.", "Glucose ngẫu nhiên, tiền sử toan ceton, ketone niệu, huyết áp tâm thu.", "Hệ chuyên gia 12 luật an toàn cứng (Hard Clinical Guardrails R01-R12) với quyền ghi đè khẩn cấp.", "Thông điệp cảnh báo an toàn, cờ ghi đè khẩn cấp (Emergency Override).", "Tỷ lệ phát hiện vi phạm quy tắc = 100%; không bỏ sót toan ceton."],
        ["3. DiaDiagnostic\n(AIDiagnosticAgent)", "Chẩn đoán xác suất, phát hiện tương tác sinh học phi tuyến.", "Bộ dấu ấn sinh hóa (HbA1c, Glucose lúc đói, BMI, tuổi, giới, bệnh tim, THA).", "8 mô hình ML/DL + PyTorch TabResNet Multi-Head Attention + Super Stacking Ensemble.", "Xác suất bệnh lý tổng hợp, khoảng tin cậy Conformal Prediction 95%.", "ROC-AUC = 0.9793; Macro-F1 = 80.75%; Brier Score = 0.0240."],
        ["4. DiaGraph\n(KGGuidelinesAgent)", "Thủ thư Đồ thị tri thức, truy xuất phác đồ chuẩn ADA 2024.", "Thực thể bệnh học, biến chứng mục tiêu, loại thuốc được đề xuất.", "Đồ thị tri thức Neo4j (56 nút, 60 cạnh) + Động cơ Graph-RAG Hybrid truy xuất đa chặng.", "Đường đi suy luận đồ thị, danh mục thuốc khuyến nghị, trích dẫn y văn.", "Hit@3 = 100%; MRR = 0.948; 100% có trích dẫn ADA/KDIGO."],
        ["5. DiaD3QNCoach\n(DiaRLCoachAgent)", "Huấn luyện viên tối ưu hóa lối sống & nhịp sinh học 24 giờ.", "Độ nhạy insulin cá thể, lịch trình sinh hoạt 24h, thói quen ăn uống/vận động.", "Học tăng cường Dueling Double Deep Q-Network (D3QN) PyTorch + Prioritized Replay.", "Kế hoạch can thiệp 24 khung giờ: dinh dưỡng Low-GI, tập luyện aerobic/kháng lực.", "TIR (70-140 mg/dL) đạt 99.8% - 100.0%; dập tắt đỉnh đường huyết."],
        ["6. DiaTherapy\n(TherapyLifestyleAgent)", "Bác sĩ chuyên khoa điều trị: xây dựng phác đồ thuốc cá thể hóa.", "Kết quả chẩn đoán từ DiaDiagnostic, khuyến nghị từ DiaGraph và hồ sơ bệnh.", "Cây quyết định phân tầng điều trị ADA 2024 (Đơn trị Metformin, phối hợp đôi SGLT2i/GLP-1 RA).", "Đơn thuốc chi tiết: tên hoạt chất, liều lượng chuẩn, thời điểm uống trong ngày.", "Tuân thủ 100% hướng dẫn ADA 2024 và Quyết định 5481/QĐ-BYT."],
        ["7. DiaPharma\n(PharmacogenomicsAgent)", "Chuyên gia Dược lý di truyền & chức năng thanh thải gan thận.", "Kiểu gen CYP2C9, SLCO1B1, nồng độ Creatinine huyết thanh, tuổi, cân nặng, giới tính.", "Công thức Cockcroft-Gault tính CrCl; bảng tra cứu tương tác thuốc và chuyển hóa gen CPIC.", "Cảnh báo chống chỉ định Metformin, điều chỉnh liều Sulfonylurea, lựa chọn Statin an toàn.", "Ngăn ngừa 100% nguy cơ toan acid lactic và sốc hạ đường huyết do gen."],
        ["8. DiaWhatIf\n(DiaCounterfactualAgent)", "Chuyên gia giải thích can thiệp phản thực tế (Counterfactual XAI).", "Vector đặc trưng bệnh nhân hiện tại và xác suất bệnh lý mục tiêu (<= 15%).", "Thuật toán tối ưu hóa lồi có ràng buộc tìm vector can thiệp nhỏ nhất delta* theo chuẩn L2-norm.", "Lộ trình hành động khả thi: cần giảm bao nhiêu kg cân nặng, hạ bao nhiêu mg/dL glucose.", "Khoảng cách can thiệp trung bình L2 = 0.42; 100% can thiệp khả thi thực tế."],
        ["9. DiaTrust\n(DiaFairnessTrustAgent)", "Kiểm toán viên độc lập về độ tin cậy và công bằng y tế số.", "Dự đoán của mô hình trên 4 nhóm nhân khẩu (tuổi, giới tính, tiền sử tim mạch).", "Hiệu chuẩn sai số dự báo (ECE), kiểm định tỷ lệ cảnh báo với khoảng tin cậy Wilson 95%.", "Báo cáo kiểm toán công bằng, biểu đồ hiệu chuẩn độ tin cậy (Calibration curve).", "Sai số hiệu chuẩn ECE = 0.29%; không có thiên vị bất bình đẳng giới/tuổi."],
        ["10. DiaTracker\n(DiaFollowupTrackerAgent)", "Bác sĩ theo dõi tiến trình dọc & thích ứng kế hoạch 4 tuần.", "Lịch sử tuân thủ điều trị, diễn biến đường huyết và cân nặng qua 4 tuần.", "Mô hình chuỗi thời gian tự hồi quy kết hợp chính sách thích ứng D3QN qua các tuần.", "Đồ thị quỹ đạo đường huyết 4 tuần, kế hoạch chuyển đổi lối sống thích nghi.", "Tỷ lệ thuyên giảm bệnh đạt 85% sau 4 tuần mô phỏng tuân thủ."],
        ["11. DiaCritic\n(ChiefEvaluatorCritic)", "Bác sĩ trưởng chủ trì hội chẩn, phản biện & chứng nhận lâm sàng.", "Toàn bộ ý kiến, khuyến nghị, cảnh báo và đơn thuốc của 11 tác tử thành viên.", "Giao thức Phản tư Tranh luận 3 Vòng (Chief Critic Deliberation) giải quyết mâu thuẫn.", "Biên bản hội chẩn thống nhất, chứng chỉ bảo đảm an toàn có chữ ký số.", "Hệ số đồng thuận liên tác tử Cohen's Kappa = 0.94; giải quyết 100% xung đột."],
        ["12. DiaReporter\n(DiaReportGeneratorAgent)", "Thư ký y khoa tổng hợp hồ sơ & xuất bản báo cáo đa phương tiện.", "Biên bản hội chẩn của Bác sĩ trưởng, đồ thị ECG, chỉ số sinh hiệu, đơn thuốc.", "Động cơ tạo tài liệu HTML/PDF tự động, Web Speech API tổng hợp giọng nói đọc bệnh án.", "Báo cáo lâm sàng đa phương tiện (HTML, PDF tải về), âm thanh thuyết minh tư vấn.", "Thời gian tạo báo cáo < 0.5s; định dạng chuẩn y khoa quốc tế."]
    ]
    populate_table(doc, agent_headers, agent_data, col_widths=[1.2, 1.2, 1.1, 1.2, 1.1, 0.7], header_bg="1E3A8A")

    add_custom_heading(doc, "3.2. Sơ Đồ Tuần Tự Tương Tác 12 Tác Tử Trong Một Ca Hội Chẩn Lâm Sàng", level=2)
    add_body_p(
        doc,
        "Một quy trình hội chẩn lâm sàng hoàn chỉnh trong DiaMulti-Agent CDSS v2 không diễn ra ngẫu nhiên mà tuân theo một quy trình điều phối chặt chẽ "
        "gồm 11 bước kế tiếp, được giám sát bởi Diabetes Coordinator Agent:"
    )

    # Embed Fig 26
    add_figure(
        doc,
        "fig26_multi_agent_architecture_flowchart.png",
        "Hình 3.1. Sơ đồ kiến trúc tổng thể và luồng điều phối thông tin giữa 12 Tác tử lâm sàng trong DiaMulti-Agent CDSS v2.",
        width_inches=6.2
    )

    add_body_p(
        doc,
        "Luồng tuần tự 11 bước diễn ra như sau:\n"
        "1. Bước 1 (Triage Screening): Bệnh nhân nhập thông tin sinh hiệu; DiaTriage phân tầng nguy cơ cấp cứu trong 5ms.\n"
        "2. Bước 2 (Safety Guardrail Check): DiaSafetyRule kiểm tra ngay lập tức 12 luật an toàn cứng; nếu phát hiện nguy kịch (ví dụ toan ceton DKA), "
        "hệ thống phát còi báo động khẩn cấp và ngắt quy trình khám thường quy.\n"
        "3. Bước 3 (Multi-Model AI Diagnosis): DiaDiagnostic nạp dữ liệu vào 8 mô hình ML/DL, tính toán Attention weights và Super Stacking Meta-Learner, "
        "đồng thời sinh khoảng bảo chứng Conformal Prediction 95%.\n"
        "4. Bước 4 (Knowledge Graph Retrieval): DiaGraph đối chiếu chẩn đoán với Đồ thị Tri thức Neo4j ADA 2024, truy xuất các liên kết bệnh lý và danh mục thuốc đầu tay.\n"
        "5. Bước 5 (RL Lifestyle Schedule Formulation): DiaD3QNCoach chạy mạng D3QN mô phỏng 24 giờ, lập lịch can thiệp dinh dưỡng Low-GI và tập thể dục thích ứng nhịp sinh học.\n"
        "6. Bước 6 (Therapy & Drug Prescription): DiaTherapy tổng hợp chỉ định dược lý, lựa chọn hoạt chất và liều lượng tối ưu cá thể hóa.\n"
        "7. Bước 7 (Pharmacogenomics & Renal Clearance): DiaPharma kiểm tra đột biến gen CYP2C9 và tính độ thanh thải thận Cockcroft-Gault để phê duyệt hoặc cấm thuốc.\n"
        "8. Bước 8 (Counterfactual What-If Optimization): DiaWhatIf giải bài toán tối ưu hóa lồi tìm kiếm các mục tiêu thay đổi lối sống khả thi nhất cho người bệnh.\n"
        "9. Bước 9 (Fairness & Calibration Audit): DiaTrust kiểm toán sai số dự báo và kiểm tra bất bình đẳng giữa các nhóm tuổi và giới tính.\n"
        "10. Bước 10 (Longitudinal 4-Week Tracking): DiaTracker mô phỏng quỹ đạo cải thiện đường huyết trong 4 tuần tới khi bệnh nhân tuân thủ phác đồ.\n"
        "11. Bước 11 (Chief Critic Deliberation & Certification): Bác sĩ trưởng DiaCritic chủ trì tranh luận, kiểm định chéo và ký số chứng chỉ xuất bản qua DiaReporter."
    )

    add_custom_heading(doc, "3.3. Cơ Chế Phản Tư & Tranh Luận 3 Vòng Của Bác Sĩ Trưởng (Chief Critic Deliberation)", level=2)
    add_body_p(
        doc,
        "Điểm đột phá độc nhất vô nhị của DiaMulti-Agent CDSS v2 so với các nghiên cứu tiền nhiệm là Cơ chế Tranh luận Đa Tác tử (Multi-Agent Deliberation Protocol). "
        "Trong y khoa thực tế, các bác sĩ chẩn đoán hình ảnh, bác sĩ xét nghiệm và bác sĩ điều trị thường xuyên có quan điểm bất đồng. Hệ thống mô hình hóa mâu thuẫn này "
        "thông qua một quy trình phản tư 3 vòng do Bác sĩ trưởng (DiaCritic) điều hành:"
    )

    # Embed Fig 27
    add_figure(
        doc,
        "fig27_critic_debate_sequence_diagram.png",
        "Hình 3.2. Sơ đồ tuần tự Tranh luận Phản tư 3 Vòng (Chief Critic Deliberation Protocol) giữa Bác sĩ trưởng và các Tác tử thành viên.",
        width_inches=6.0
    )

    add_body_p(
        doc,
        "Chi tiết 3 vòng tranh luận giải quyết mâu thuẫn:\n"
        "• Vòng 1 (Nêu Bằng Chứng & Phản Biện Chéo - Cross-Examination): Bác sĩ trưởng đối chiếu kết luận của mô hình AI với dữ liệu đo trực tiếp. "
        "Ví dụ: Trường hợp ca bệnh 'Cô Hoa' (58 tuổi, BMI = 22.0, không hút thuốc, lối sống lành mạnh) nhưng có xét nghiệm đường huyết đói Glucose = 185 mg/dL và HbA1c = 8.1%. "
        "Mô hình AI chỉ dựa trên khảo sát lối sống (như BRFSS) sẽ báo nguy cơ thấp (Low Risk = 18%). Bác sĩ trưởng lập tức phản biện: 'Có sự mâu thuẫn nghiêm trọng giữa hồ sơ lối sống "
        "và kết quả sinh hóa trực tiếp!'\n"
        "• Vòng 2 (Bảo Vệ & Viện Dẫn Luật - Defense & Guideline Argumentation): Tác tử DiaDiagnostic bảo vệ kết quả mô hình nơ-ron; tuy nhiên Tác tử DiaSafetyRule viện dẫn "
        "Luật R01 (HbA1c >= 6.5% hoặc Glucose >= 126 mg/dL là tiêu chuẩn vàng chẩn đoán ĐTĐ theo ADA 2024). Đồng thời, Thủ thư DiaGraph trích xuất nguyên văn chương 2 "
        "tài liệu ADA Standards of Care khẳng định giá trị chẩn đoán xác định của HbA1c.\n"
        "• Vòng 3 (Phán Quyết & Chứng Nhận Lâm Sàng - Final Ruling & Certification): Bác sĩ trưởng áp dụng Nguyên Tắc Ưu Tiên Số Đo Trực Tiếp (Direct Measurement Primacy Rule): "
        "ghi đè mức nguy cơ từ Thấp lên NGUY CƠ CAO (High Risk), xác lập chẩn đoán Đái tháo đường Tuýp 2, đồng thời yêu cầu chuyển sang phác đồ điều trị dùng thuốc ngay lập tức."
    )

    # Embed Fig 16
    add_figure(
        doc,
        "fig16_multi_agent_deliberation_consensus.png",
        "Hình 3.3. Phân phối mức độ đồng thuận giữa 12 tác tử qua 3 vòng tranh luận, đạt hệ số tin cậy liên tác tử Cohen's Kappa = 0.94.",
        width_inches=5.8
    )

    add_callout(
        doc,
        "NGUYÊN TẮC GIẢI QUYẾT XUNG ĐỘT TRONG HỘI CHẨN ĐA TÁC TỬ (PTIT CDSS v2):\n"
        "1. Nguyên tắc An toàn Tuyệt đối (Absolute Safety Primacy): Ý kiến của DiaSafetyRule luôn có quyền phủ quyết cao nhất nếu phát hiện nguy cơ tử vong hoặc toan acid lactic.\n"
        "2. Nguyên tắc Số đo Khách quan (Objective Evidence Primacy): Các xét nghiệm sinh hóa đo trực tiếp trong máu (HbA1c, FPG, Creatinine) luôn có trọng số cao hơn các câu trả lời khảo sát tự khai.\n"
        "3. Nguyên tắc Đồng thuận Khoa học (Peer-Review Consensus): Phác đồ cuối cùng chỉ được thông qua khi đạt hệ số đồng thuận liên tác tử Cohen's Kappa >= 0.85.",
        title="NGUYÊN TẮC PHÁN QUYẾT LÂM SÀNG CỦA BÁC SĨ TRƯỞNG",
        border_color="059669",
        fill_hex="ECFDF5"
    )
