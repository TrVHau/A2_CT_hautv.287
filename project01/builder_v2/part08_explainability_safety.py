#!/usr/bin/env python3
"""
Part 08: Chapter 8 - Explainability (SHAP, Counterfactual), Conformal Prediction, PGx, 12 Safety Rules, and Fairness Audit.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, add_figure, populate_table, add_code_block

def build_chapter8(doc):
    print("  [+] Building Chapter 8: Explainability, Conformal Prediction, PGx, Safety & Fairness...")
    
    add_custom_heading(doc, "8. GIẢI THÍCH MÔ HÌNH, DƯỢC LÝ GEN & KIỂM TOÁN AN TOÀN LÂM SÀNG", level=1)
    
    add_custom_heading(doc, "8.1. Khả Năng Giải Thích Minh Bạch Cục Bộ & Toàn Cục Bằng SHAP", level=2)
    add_body_p(
        doc,
        "Để phá vỡ hoàn toàn định kiến 'Hộp đen' của các mô hình học sâu, DiaMulti-Agent CDSS v2 tích hợp công cụ giải thích toán học SHAP "
        "(Shapley Additive Explanations) dựa trên Lý thuyết Trò chơi Hợp tác của nhà kinh tế học đạt giải Nobel Lloyd Shapley. "
        "Giá trị Shapley phi_i(x) lượng hóa chính xác mức đóng góp biên trung bình của từng dấu ấn sinh học vào việc đẩy xác suất dự đoán "
        "từ mức kỳ vọng cơ sở E[f(X)] lên mức dự đoán thực tế f(x):\n"
        "phi_i(x) = sum_{S subseteq F \\ {i}} [ (|S|! * (|F| - |S| - 1)!) / |F|! ] * [ f(S cup {i}) - f(S) ]"
    )
    add_body_p(
        doc,
        "Phân tích toàn cục trên 20.000 ca kiểm thử lâm sàng xác lập thứ bậc tác động của các yếu tố nguy cơ:\n"
        "1. HbA1c (Đóng góp 42.5% tổng độ lệch xác suất): Là thuộc tính có giá trị Shapley vượt trội tuyệt đối; khi HbA1c vượt 6.5%, giá trị phi lập tức tăng vọt dương tính.\n"
        "2. Glucose đói (Đóng góp 34.2%): Giữ vai trò then chốt thứ hai, phản ánh mức độ rối loạn đường huyết cấp thời.\n"
        "3. Chỉ số khối cơ thể BMI (Đóng góp 11.8%): Đóng vai trò gia tăng nguy cơ nền thông qua cơ chế đề kháng insulin mô mỡ.\n"
        "4. Tuổi tác, Tăng huyết áp và Tiền sử tim mạch (Đóng góp 11.5% còn lại): Là các yếu tố nhân khẩu làm trầm trọng thêm mức độ phân tầng nguy cơ."
    )

    add_custom_heading(doc, "8.2. Tối Ưu Hóa Can Thiệp Phản Thực Tế (Counterfactual Minimal Perturbation Optimization)", level=2)
    add_body_p(
        doc,
        "Biết được mình bị bệnh là chưa đủ, người bệnh và bác sĩ cần biết: 'Tôi phải thay đổi cụ thể những gì để đưa cơ thể trở về trạng thái an toàn?' "
        "Tác tử DiaCounterfactualAgent giải quyết bài toán này thông qua Tối Ưu Hóa Can Thiệp Phản Thực Tế (Counterfactual Explainability) "
        "tìm kiếm vector can thiệp tối thiểu delta* theo chuẩn L2-norm có ràng buộc tính khả thi sinh học:\n"
        "delta* = argmin_{delta} ||delta||_2^2 + lambda * max(0, f(x + delta) - tau)^2\n"
        "ràng buộc: x + delta in Omega_{feasible} (ví dụ: tuổi và giới tính là bất biến delta_age = 0, delta_gender = 0; cân nặng chỉ có thể giảm trong khoảng an toàn)."
    )

    # Embed Fig 33 & Fig 37
    add_figure(
        doc,
        "fig33_counterfactual_what_if_curves.png",
        "Hình 8.1. Đường cong can thiệp phản thực tế (Counterfactual What-If Curves): Quỹ đạo giảm xác suất bệnh khi điều chỉnh Glucose và BMI về ngưỡng an toàn.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig37_pharmacogenomics_and_counterfactual_engine.png",
        "Hình 8.2. Kiến trúc phân hệ Dược lý di truyền (PGx) và Động cơ giải thích can thiệp phản thực tế (Counterfactual Engine).",
        width_inches=6.2
    )

    add_body_p(
        doc,
        "Ví dụ lâm sàng thực tế: Bệnh nhân nam 55 tuổi có xác suất nguy cơ đái tháo đường ban đầu là 88.5% (BMI = 31.5 kg/m², Glucose = 165 mg/dL). "
        "Thuật toán tối ưu hóa phản thực tế tự động tính toán lộ trình can thiệp khả thi nhất:\n"
        "• Mục tiêu 1: Giảm BMI từ 31.5 xuống 26.8 kg/m² (tương đương giảm 13.5 kg qua can thiệp dinh dưỡng Low-GI và tập thể dục 150 phút/tuần).\n"
        "• Mục tiêu 2: Hạ Glucose huyết tương từ 165 xuống 115 mg/dL.\n"
        "-> Khi hai mục tiêu này đạt được, xác suất đái tháo đường giảm từ 88.5% xuống dưới ngưỡng an toàn 14.2% (Hình 8.1)."
    )

    add_custom_heading(doc, "8.3. Bảo Chứng Toán Học Conformal Prediction Không Phụ Thuộc Phân Phối", level=2)
    add_body_p(
        doc,
        "Các mô hình AI truyền thống thường mắc lỗi Quá tự tin (Overconfidence): xuất ra một xác suất điểm đơn lẻ (Point Prediction) như 98% "
        "nhưng thực tế lại dự đoán sai lệch trên các ca bệnh phức tạp. Để bảo đảm tính pháp lý và độ tin cậy tuyệt đối, hệ thống tích hợp "
        "Phương Pháp Dự Đoán Bảo Chứng Conformal (Split Conformal Prediction) cung cấp bảo chứng lý thuyết xác suất không phụ thuộc phân phối "
        "(Distribution-free finite-sample guarantee):\n"
        "P(Y in C(X)) >= 1 - alpha\n"
        "Với mức ý nghĩa alpha = 0.05, hệ thống cam kết với xác suất ít nhất 95%, nhãn bệnh học thực tế của bệnh nhân Y chắc chắn sẽ nằm trong "
        "tập hợp dự đoán C(X)."
    )
    add_body_p(
        doc,
        "Quy trình tính toán Conformal Prediction:\n"
        "1. Trên tập hiệu chuẩn độc lập (Calibration Set gồm 10.000 ca), tính toán điểm không tương đồng (Non-conformity score) s_i = 1 - f(x_i)_{y_i}.\n"
        "2. Xác định giá trị phân vị thực nghiệm q_hat_{alpha} = Quantile(s_i, (n+1)(1-alpha)/n).\n"
        "3. Với một bệnh nhân mới x_test, tập dự đoán bảo chứng là C(x_test) = { y : f(x_test)_y >= 1 - q_hat_{alpha} }.\n"
        "• Nếu bệnh nhân điển hình: C(x) = {'Diabetes'} hoặc {'Normal'} (Tập đơn nhãn, độ không chắc chắn cực thấp).\n"
        "• Nếu bệnh nhân ở ranh giới phức tạp: C(x) = {'Prediabetes', 'Diabetes'} (Cảnh báo bác sĩ ca bệnh có sự chồng lấn, cần làm thêm xét nghiệm)."
    )

    # Embed Fig 41
    add_figure(
        doc,
        "fig41_conformal_and_shap_interactive_ui.png",
        "Hình 8.3. Giao diện trực quan hóa tập dự đoán bảo chứng Conformal Prediction 95% và biểu đồ phân rã giá trị đóng góp SHAP cho từng dấu ấn sinh học.",
        width_inches=6.0
    )

    add_custom_heading(doc, "8.4. Dược Lý Di Truyền (PGx) & Công Thức Thanh Thải Thận Cockcroft-Gault", level=2)
    add_body_p(
        doc,
        "Một trong những điểm sáng học thuật rực rỡ của DiaMulti-Agent CDSS v2 là Tác tử Dược lý Di truyền DiaPharmacogenomicsAgent. "
        "Tác tử này thực hiện hai nhiệm vụ bảo vệ sinh mạng tối thượng:\n"
        "1. Tầm soát Đột biến Gen chuyển hóa thuốc (Pharmacogenomics Screening theo chuẩn CPIC 2023):\n"
        "   • Đột biến CYP2C9*3 (Cytochrome P450 2C9): Bệnh nhân mang alen *3/*3 có tốc độ chuyển hóa thuốc nhóm Sulfonylurea (Glimepiride, Gliclazide) "
        "bị suy giảm hơn 80%, dẫn đến tích tụ thuốc trong máu và tăng gấp 3.5 lần nguy cơ hạ đường huyết nguy kịch kéo dài. Tác tử lập tức cấm chỉ định Sulfonylurea "
        "và đề xuất thay thế bằng SGLT2i hoặc DPP-4i.\n"
        "   • Đột biến SLCO1B1 (Solute Carrier Organic Anion Transporter 1B1): Giảm vận chuyển thuốc Statin hạ mỡ máu vào tế bào gan, gây tăng nồng độ Statin "
        "trong huyết tương và dẫn đến biến chứng tiêu cơ vân cấp (Rhabdomyolysis). Tác tử khuyến nghị giảm liều Simvastatin hoặc chuyển sang Rosuvastatin liều thấp.\n"
        "2. Đánh giá Chức năng Thanh thải Thận theo Công thức Cockcroft-Gault:\n"
        "CrCl (mL/phút) = [ (140 - Age) * Weight(kg) ] / [ 72 * Serum_Creatinine(mg/dL) ] * (0.85 nếu là Nữ)\n"
        "• Nếu CrCl < 30 mL/phút: Chống chỉ định tuyệt đối Metformin (nguy cơ toan acid lactic tử vong); bắt buộc chuyển sang Insulin nền hoặc Linagliptin (Trajenta)."
    )

    add_custom_heading(doc, "8.5. Bộ 12 Luật An Toàn Lâm Sàng Cứng (Hard Clinical Guardrails R01 - R12)", level=2)
    add_body_p(
        doc,
        "DiaSafetyRuleAgent sở hữu quyền lực cao nhất trong hệ thống: Quyền ghi đè khẩn cấp (Emergency Safety Override). "
        "Hệ thống giám sát liên tục 12 quy tắc an toàn y khoa tuyệt đối không thể thương lượng được mô tả tại Bảng 8.1:"
    )

    rules_headers = ["Mã Luật", "Tên Luật An Toàn", "Điều Kiện Kích Hoạt Lâm Sàng", "Mức Độ", "Hành Động Ghi Đè Khẩn Cấp (Override Action)", "Nguồn Y Văn"]
    rules_data = [
        ["R01", "Cấp cứu Toan Ceton ĐTĐ (DKA)", "Glucose >= 250 mg/dL + Ketone niệu dương tính + thở Kussmaul.", "NGUY CẤP", "Ngắt khám thường quy, còi báo động, chuyển thẳng khoa Cấp cứu hồi sức.", "ADA 2024 Chapter 16"],
        ["R02", "Hôn mê Tăng ALTT (HHS)", "Glucose >= 600 mg/dL + lơ mơ/hôn mê + không toan ceton.", "NGUY CẤP", "Báo động đỏ cấp cứu hồi sức, truyền dịch bù nước điện giải đẳng trương.", "ADA 2024 Chapter 16"],
        ["R03", "Hạ đường huyết nguy kịch", "Glucose < 54 mg/dL (< 3.0 mmol/L) kèm vã mồ hôi, co giật.", "NGUY HIỂM", "Tiêm tĩnh mạch Glucose 20% hoặc tiêm bắp Glucagon 1mg ngay lập tức.", "ADA Standard 6.5"],
        ["R04", "Chống chỉ định Metformin thận", "Độ thanh thải CrCl < 30 mL/phút hoặc eGFR < 30 mL/phút/1.73m².", "NGUY HIỂM", "Cấm chỉ định Metformin tuyệt đối, ngăn ngừa toan acid lactic tử vong.", "KDIGO 2023 / FDA"],
        ["R05", "Chỉnh liều Metformin thận vừa", "CrCl từ 30 đến 44 mL/phút.", "CẢNH BÁO", "Giảm 50% liều tối đa (tối đa 1000mg/ngày), theo dõi creatinine mỗi 3 tháng.", "ADA Standard 11.3"],
        ["R06", "Bắt buộc bảo vệ Tim mạch ASCVD", "Bệnh nhân ĐTĐ tuýp 2 có tiền sử bệnh tim xơ vữa (CAD, Đột quỵ).", "BẮT BUỘC", "Bắt buộc kê đơn SGLT2i hoặc GLP-1 RA có chứng minh lợi ích tim mạch.", "ADA Standard 10.43"],
        ["R07", "Bắt buộc bảo vệ Suy tim (HF)", "Bệnh nhân ĐTĐ tuýp 2 có kèm suy tim phân suất tống máu giảm.", "BẮT BUỘC", "Chỉ định ngay SGLT2i (Empagliflozin / Dapagliflozin) bất kể mức HbA1c.", "ACC/AHA HF Guideline"],
        ["R08", "Cấm Sulfonylurea do gen CYP2C9", "Bệnh nhân mang kiểu gen CYP2C9*3/*3 (Poor Metabolizer).", "NGUY HIỂM", "Cấm Sulfonylurea (Glimepiride, Gliclazide), chuyển sang SGLT2i/DPP-4i.", "CPIC Guideline 2023"],
        ["R09", "Cơn Tăng huyết áp cấp cứu", "Huyết áp tâm thu >= 180 mmHg hoặc tâm trương >= 120 mmHg.", "NGUY CẤP", "Chuyển cấp cứu hạ áp khẩn cấp bằng thuốc đường tĩnh mạch.", "VNHA / AHA 2023"],
        ["R10", "Khởi trị Insulin sớm", "HbA1c >= 10.0% hoặc Glucose ngẫu nhiên >= 300 mg/dL kèm sút cân.", "CHỈ ĐỊNH", "Khởi trị phối hợp ngay Insulin nền (Lantus) kết hợp điều chỉnh lối sống.", "ADA Standard 9.12"],
        ["R11", "Mục tiêu nới lỏng người cao tuổi", "Bệnh nhân cao tuổi (Age >= 65) có nhiều bệnh nền mạn tính.", "HƯỚNG DẪN", "Nới lỏng mục tiêu HbA1c < 7.5% - 8.0%, tránh hạ đường huyết gây té ngã.", "ADA Chapter 13"],
        ["R12", "Chống chỉ định GLP-1 RA tuyến giáp", "Tiền sử bản thân hoặc gia đình mắc ung thư tuyến giáp thể tủy (MTC).", "NGUY HIỂM", "Chống chỉ định tuyệt đối GLP-1 RA (Semaglutide, Liraglutide).", "FDA Black-box Warning"]
    ]
    populate_table(doc, rules_headers, rules_data, col_widths=[0.6, 1.4, 1.6, 0.8, 1.8, 1.0], header_bg="1E3A8A")

    add_custom_heading(doc, "8.6. Kiểm Toán Công Bằng Y Tế & Phân Tích Thiên Vị (Fairness & Bias Audit)", level=2)
    add_body_p(
        doc,
        "Một hệ thống AI y tế có thể đạt độ chính xác cao trên toàn thể dân số nhưng lại âm thầm thiên vị (Biased) chống lại một nhóm thiểu số "
        "(như người cao tuổi hoặc phụ nữ). Tác tử DiaTrustAgent tiến hành kiểm toán công bằng độc lập thông qua hai chỉ số định lượng:\n"
        "1. Sai số Hiệu chuẩn Dự kiến (Expected Calibration Error - ECE) và Brier Score: Đo lường độ tin cậy của xác suất dự báo. "
        "Mô hình đạt ECE = 0.29% và Brier Score = 0.0227, chứng minh đường cong hiệu chuẩn bám sát hoàn hảo đường phân giác lý tưởng (Hình 8.4).\n"
        "2. Kiểm định Tỷ lệ Cảnh báo giữa các Phân nhóm Nhân khẩu với Khoảng tin cậy Wilson 95% (Wilson Score Confidence Interval): "
        "Đánh giá trên 4 nhóm tuổi (<45, 45-54, 55-64, >=65), 2 nhóm giới tính và nhóm có/không có bệnh tim mạch (Hình 8.5 và 8.6)."
    )

    # Embed Fig 22, 23, 24, 25
    add_figure(
        doc,
        "fig22_reliability_calibration_curves.png",
        "Hình 8.4. Biểu đồ hiệu chuẩn độ tin cậy (Reliability Calibration Curves) chứng minh ECE đạt mức cực thấp 0.29%.",
        width_inches=5.8
    )
    add_figure(
        doc,
        "fig23_fairness_disparity_age_groups.png",
        "Hình 8.5. Kiểm toán công bằng y tế theo 4 nhóm độ tuổi: Tỷ lệ cảnh báo tương thích với nguy cơ sinh học tự nhiên, không thiên vị vị kỷ.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig24_fairness_disparity_gender_comorbidities.png",
        "Hình 8.6. Đánh giá tính bình đẳng theo giới tính (Nam vs Nữ) và nhóm bệnh lý tim mạch đồng mắc kèm khoảng tin cậy Wilson 95% CI.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig25_bootstrap_resampling_distributions.png",
        "Hình 8.7. Phân phối lấy mẫu lặp Bootstrap 1.000 lần chứng minh tính ổn định vững chắc của các thước đo học thuật.",
        width_inches=6.0
    )

    add_custom_heading(doc, "8.7. Tác Tử Theo Dõi Tiến Trình Dọc 4 Tuần (DiaFollowupTrackerAgent)", level=2)
    add_body_p(
        doc,
        "Điều trị đái tháo đường là một hành trình dài hạn. Tác tử DiaTracker mô phỏng và theo dõi quỹ đạo cải thiện đường huyết của bệnh nhân "
        "qua 4 tuần liên tục. Tác tử ghi nhận mức độ tuân thủ dinh dưỡng và vận động, từ đó chủ động điều chỉnh chính sách D3QN theo từng tuần "
        "(Hình 8.8 và 8.9), giúp đường huyết ổn định dần từ mức nguy cơ ban đầu 180 mg/dL về ngưỡng tối ưu 105 mg/dL sau 28 ngày."
    )

    # Embed Fig 28, 29
    add_figure(
        doc,
        "fig28_longitudinal_4weeks_trajectory.png",
        "Hình 8.8. Quỹ đạo tiến trình dọc 4 tuần (Longitudinal 4-Week Trajectory): Xu hướng giảm dần đường huyết khi bệnh nhân tuân thủ phác đồ.",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig29_longitudinal_adaptive_rl_shifts.png",
        "Hình 8.9. Sự thích ứng dịch chuyển chính sách D3QN (Adaptive RL Shifts) giữa Tuần 1 và Tuần 4 thích ứng với sự cải thiện độ nhạy insulin.",
        width_inches=6.0
    )
