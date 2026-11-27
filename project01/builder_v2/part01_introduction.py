#!/usr/bin/env python3
"""
Part 01: Chapter 1 - Introduction, Motivation, Clinical Epidemiology, and Ethical Declarations.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, populate_table

def build_chapter1(doc):
    print("  [+] Building Chapter 1: Introduction & Clinical Motivation...")
    
    add_custom_heading(doc, "1. GIỚI THIỆU, ĐỘNG LỰC NGHIÊN CỨU & BỐI CẢNH LÂM SÀNG", level=1)
    
    add_custom_heading(doc, "1.1. Bối Cảnh Dịch Tễ Học & Gánh Nặng Y Tế Toàn Cầu Của Bệnh Đái Tháo Đường", level=2)
    add_body_p(
        doc,
        "Đái tháo đường (Diabetes Mellitus) là một trong những đại dịch bệnh lý không lây nhiễm đe dọa nghiêm trọng nhất sức khỏe cộng đồng "
        "và sự bền vững của các hệ thống an sinh xã hội toàn cầu trong thế kỷ 21. Theo Báo cáo Dịch tễ học thường niên của Liên đoàn Đái tháo đường "
        "Quốc tế (IDF Diabetes Atlas, 10th Edition) và Tổ chức Y tế Thế giới (WHO 2024), hiện có hơn 537 triệu người trưởng thành (độ tuổi 20–79) "
        "đang phải sống chung với bệnh đái tháo đường trên toàn cầu. Dự báo đến năm 2045, con số này sẽ chạm mốc 783 triệu người, tương ứng mức tăng "
        "trưởng 46%. Đáng chú ý, hơn 90% các ca mắc thuộc về Đái tháo đường Tuýp 2 (Type 2 Diabetes Mellitus - T2D) — một bệnh lý rối loạn chuyển hóa "
        "đặc trưng bởi tình trạng đề kháng insulin ngoại biên kết hợp với sự suy giảm tương đối chức năng tiết insulin của tế bào beta đảo tụy."
    )
    add_body_p(
        doc,
        "Tại Việt Nam, theo số liệu điều tra dịch tễ của Bộ Y tế và Viện Nội tiết Trung ương, tỷ lệ mắc đái tháo đường trong dân số trưởng thành đã "
        "vượt ngưỡng 7.3%, và tỷ lệ tiền đái tháo đường (Prediabetes) lên tới gần 14%. Gần 50% người mắc bệnh trong cộng đồng chưa từng được chẩn đoán "
        "hoặc phát hiện muộn khi đã xuất hiện các biến chứng mạn tính đe dọa tính mạng như: bệnh thận đái tháo đường (Diabetic Kidney Disease - DKD), "
        "bệnh tim mạch xơ vữa (Atherosclerotic Cardiovascular Disease - ASCVD), suy tim (Heart Failure - HF), tổn thương võng mạc gây mù lòa "
        "(Diabetic Retinopathy) và hoại tử chi dưới do bệnh động mạch ngoại biên (PAD). Tổng chi phí y tế trực tiếp và gián tiếp cho điều trị biến chứng "
        "đái tháo đường tại Việt Nam ước tính chiếm tới gần 10% tổng ngân sách chi cho y tế quốc gia."
    )

    add_custom_heading(doc, "1.2. Khoảng Trống Nghiên Cứu & Thách Thức Cốt Tử Của Trí Tuệ Nhân Tạo Trong Y Sinh", level=2)
    add_body_p(
        doc,
        "Mặc dù các ứng dụng Trí tuệ Nhân tạo (AI) và Học máy (Machine Learning) trong y tế số đã đạt được những bước tiến đáng kể trong thập kỷ qua, "
        "việc đưa các mô hình dự đoán vào triển khai thực tế tại các bệnh viện và cơ sở khám chữa bệnh lâm sàng vẫn gặp phải những rào cản mang tính sống còn:"
    )
    add_body_p(
        doc,
        "• Rào cản Hộp Đen (Black-box Dilemma): Các mô hình học sâu (Deep Neural Networks) hoặc các thuật toán tổ hợp cây quyết định phân tầng cao "
        "(XGBoost, CatBoost) có độ chính xác cao nhưng không thể cung cấp lời giải thích cơ chế sinh lý bệnh học rõ ràng. Một bác sĩ nội tiết không thể "
        "chấp nhận kê một đơn thuốc điều trị suốt đời chỉ dựa vào một con số xác suất xác suất vô căn cứ mà không hiểu rõ nguyên nhân.",
        bold_prefix="1. Thiếu khả năng giải thích sinh học minh bạch: "
    )
    add_body_p(
        doc,
        "• Nguy cơ Ảo giác của Mô hình Ngôn ngữ Lớn (LLM Hallucinations): Sự xuất hiện của các mô hình LLM tạo sinh (Generative AI) mở ra khả năng "
        "tương tác tự nhiên, nhưng chúng thường xuyên 'bịa đặt' các phác đồ điều trị nguy hiểm, dẫn chứng các tài liệu y văn không có thật hoặc nhầm lẫn "
        "liều lượng thuốc giữa các nhóm bệnh nhân suy giảm chức năng gan thận.",
        bold_prefix="2. Ảo giác phác đồ điều trị đe dọa sinh mạng: "
    )
    add_body_p(
        doc,
        "• Vi phạm Quy chuẩn An toàn Lâm sàng (Safety Guardrail Omission): Các hệ thống AI đơn lẻ không có cơ chế kiểm tra chéo các chống chỉ định y khoa. "
        "Ví dụ: kê đơn Metformin cho bệnh nhân có độ lọc cầu thận eGFR < 30 mL/phút có thể gây toan acid lactic cấp tính với tỷ lệ tử vong lên tới 50%; "
        "hoặc kê đơn Sulfonylurea liều cao cho bệnh nhân cao tuổi có mang alen đột biến chuyển hóa gan chậm CYP2C9*3 gây hạ đường huyết nguy kịch.",
        bold_prefix="3. Thiếu vắng cơ chế kiểm duyệt luật an toàn cứng: "
    )
    add_body_p(
        doc,
        "• Sai lệch Dữ liệu Khảo sát Tự khai (Survey Data Blind Spot): Các nghiên cứu AI tiền nhiệm (điển hình như bài báo cơ sở dựa trên dữ liệu BRFSS 2015 CDC "
        "với 253.680 hồ sơ) phụ thuộc hoàn toàn vào bảng hỏi tự khai của người dân. Tập dữ liệu này thiếu vắng hai chỉ số sinh hóa vàng là HbA1c và Glucose máu lúc đói, "
        "dẫn đến việc mô hình có diện tích dưới đường cong ROC chỉ đạt quanh 0.782 và bỏ sót hơn 80% trường hợp tiền đái tháo đường trong cộng đồng.",
        bold_prefix="4. Lỗ hổng chết người của dữ liệu sàng lọc khảo sát: "
    )

    add_custom_heading(doc, "1.3. Mục Tiêu Nghiên Cứu, Phạm Vi & Tuyên Bố Đạo Đức Y Sinh Học", level=2)
    add_body_p(
        doc,
        "Để khắc phục triệt để các khoảng trống nghiên cứu trên, công trình này đặt ra 4 mục tiêu nghiên cứu cốt lõi:\n"
        "1. Kiến tạo Hội đồng Lâm sàng Đa Tác tử (DiaMulti-Agent CDSS v2) gồm 12 tác tử chuyên trách, mô phỏng hoàn hảo quy trình hội chẩn liên chuyên khoa "
        "theo chuẩn Hiệp hội Đái tháo đường Hoa Kỳ (ADA Standards of Care 2024) và Hướng dẫn chẩn đoán và điều trị đái tháo đường của Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT).\n"
        "2. Phát triển Mạng Nơ-ron PyTorch TabResNet Attention và Bộ Học Siêu Cấp Super Stacking Ensemble trên Chiến lược Đa Cohort Kép (100.000 hồ sơ EHR trực tiếp), "
        "đồng thời chứng minh tính toàn vẹn toán học qua Kiểm định Đồng đẳng Tri-Framework Parity Check.\n"
        "3. Xây dựng Đồ thị Tri thức Đái tháo đường đa nguồn trên Neo4j (56 nút, 60 cạnh) và Động cơ Graph-RAG Hybrid truy xuất chứng cứ đa chặng, bảo đảm "
        "100% các khuyến nghị đưa ra đều có trích dẫn tài liệu y văn chính thức.\n"
        "4. Tích hợp Học tăng cường D3QN điều hòa lối sống thích ứng nhịp sinh học 24 giờ, tối ưu hóa can thiệp phản thực tế (Counterfactual XAI), dược lý di truyền (PGx), "
        "bảo chứng toán học Conformal Prediction 95% và triển khai hệ thống Web CDSS Enterprise trực quan, bảo mật."
    )

    add_callout(
        doc,
        "TUYÊN BỐ VỀ ĐẠO ĐỨC Y SINH & PHẠM VI ỨNG DỤNG HỌC THUẬT:\n"
        "• Bản báo cáo nghiên cứu và phần mềm đi kèm là công trình học thuật phục vụ mục đích nghiên cứu, đào tạo chuyên sâu và trình diễn kỹ thuật trong khuôn khổ "
        "môn học Phát triển Các Hệ thống Thông minh tại Học viện Công nghệ Bưu chính Viễn thông.\n"
        "• Hệ thống đóng vai trò Hệ Thống Hỗ Trợ Ra Quyết Định Lâm Sàng (Clinical Decision Support System - CDSS), KHÔNG THAY THẾ quyết định chuyên môn và chứng chỉ "
        "hành nghề của bác sĩ chuyên khoa nội tiết. Mọi can thiệp điều trị trên người bệnh thực tế bắt buộc phải được bác sĩ khám trực tiếp phê duyệt.\n"
        "• Toàn bộ dữ liệu bệnh án điện tử EHR và khảo sát BRFSS sử dụng trong nghiên cứu đều là dữ liệu mở, đã được khử định danh hoàn toàn (de-identified) "
        "tuân thủ nghiêm ngặt Đạo luật về Trách nhiệm giải trình và Cung cấp Bảo hiểm Y tế Hoa Kỳ (HIPAA Privacy Rule) và Tuyên ngôn Helsinki về Nghiên cứu Y sinh học.",
        title="TUYÊN BỐ ĐẠO ĐỨC VÀ KHUYẾN CÁO AN TOÀN Y SINH HỌC",
        border_color="DC2626",
        fill_hex="FEF2F2"
    )

    add_custom_heading(doc, "1.4. Đóng Góp Khoa Học & Cấu Trúc Tổng Thể Của Báo Cáo", level=2)
    add_body_p(
        doc,
        "Báo cáo chuyên sâu này được tổ chức thành 10 chương chuyên môn, 1 phần kết luận và các phụ lục mã nguồn chi tiết:\n"
        "• Chương 1: Giới thiệu, bối cảnh dịch tễ học và động lực bài toán.\n"
        "• Chương 2: Cơ sở lý thuyết nền tảng về Hệ đa tác tử (Multi-Agent Systems Theory) và mô hình Blackboard.\n"
        "• Chương 3: Thiết kế kiến trúc tổng thể Hội đồng 12 Tác tử Lâm sàng và Giao thức Tranh luận Phản biện 3 vòng.\n"
        "• Chương 4: Kỹ thuật dữ liệu đa nguồn (Dual Cohorts 100k EHR + 253k BRFSS) và phân tích khám phá dữ liệu (EDA).\n"
        "• Chương 5: Dẫn xuất toán học giải tích Scratch, Tri-Framework Parity, PyTorch TabResNet Attention và Super Stacking Ensemble.\n"
        "• Chương 6: Cơ sở dữ liệu đồ thị Neo4j, ngôn ngữ Cypher và động cơ Graph-RAG Hybrid truy xuất chứng cứ lâm sàng.\n"
        "• Chương 7: Học tăng cường sâu D3QN huấn luyện viên lối sống 24 giờ thích ứng nhịp sinh học bình minh.\n"
        "• Chương 8: Khả năng giải thích SHAP, tối ưu can thiệp phản thực tế, Conformal Prediction, Dược lý di truyền và Kiểm toán công bằng.\n"
        "• Chương 9: Kiến trúc mã nguồn hệ thống, giao diện Web CDSS Enterprise 8 Tabs và kịch bản thực nghiệm mẫu.\n"
        "• Chương 10: Thảo luận đối sánh học thuật quốc tế, phân tích hạn chế và định hướng phát triển tương lai.\n"
        "• Kết luận, Danh mục 45 Tài liệu tham khảo uy tín và Phụ lục mã nguồn triển khai thực tế."
    )
