#!/usr/bin/env python3
"""
Part 02: Chapter 2 - Multi-Agent Systems Theory, Russell & Norvig framework, BDI, Blackboard Architecture.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, add_figure, populate_table, add_code_block

def build_chapter2(doc):
    print("  [+] Building Chapter 2: Multi-Agent Systems Theory & Blackboard Architecture...")
    
    add_custom_heading(doc, "2. CƠ SỞ LÝ THUYẾT VỀ HỆ ĐA TÁC TỬ (MULTI-AGENT SYSTEMS THEORY)", level=1)
    
    add_custom_heading(doc, "2.1. Nền Tảng Lý Thuyết Tác Tử Theo Khung Chuẩn Russell & Norvig", level=2)
    add_body_p(
        doc,
        "Theo định nghĩa kinh điển của Stuart Russell và Peter Norvig trong tác phẩm tiêu chuẩn 'Artificial Intelligence: A Modern Approach' "
        "(4th Edition, 2020), một tác tử (Agent) là bất kỳ thực thể nào có khả năng nhận thức môi trường xung quanh thông qua các cảm biến (Sensors), "
        "tiến hành phân tích, lập luận dựa trên tri thức nội tại, và tác động trở lại môi trường thông qua các cơ cấu tác động (Actuators). "
        "Mô hình toán học của một tác tử thông minh được đặc tả bởi hàm tác tử f: P* -> A, ánh xạ chuỗi lịch sử các cảm nhận (Percept history P*) "
        "thành hành động cụ thể (Action A)."
    )
    add_body_p(
        doc,
        "Trong bối cảnh y tế số và hỗ trợ quyết định lâm sàng, vòng lặp hoạt động của một tác tử y tế thông minh trải qua bốn pha liên tục:\n"
        "1. Cảm nhận (Sense / Perceive): Thu nhận dữ liệu hồ sơ lâm sàng, các chỉ số xét nghiệm sinh hóa, tiền sử bệnh tật và các triệu chứng cơ năng.\n"
        "2. Lập luận (Reason / Plan): Đối chiếu thông tin thu nhận với mô hình học máy, mạng nơ-ron sâu hoặc cơ sở tri thức đồ thị để xác định trạng thái bệnh lý.\n"
        "3. Hành động (Act): Phát sinh các khuyến nghị điều trị, đề xuất phác đồ dùng thuốc, điều chỉnh kế hoạch dinh dưỡng hoặc kích hoạt còi báo động khẩn cấp.\n"
        "4. Phản tư & Học hỏi (Reflect / Learn): Tiếp nhận phản hồi từ kết quả theo dõi bệnh nhân hoặc sự can thiệp của bác sĩ để cập nhật hàm chính sách và trọng số tri thức."
    )

    add_callout(
        doc,
        "ĐẶC TẢ KHUNG PEAS CHO HỆ ĐA TÁC TỬ LÂM SÀNG ĐÁI THÁO ĐƯỜNG (DIAMULTI-AGENT CDSS):\n"
        "• Tiêu chuẩn đo lường hiệu năng (Performance Measure - P): Độ chuẩn xác chẩn đoán (AUC > 0.97, F1 > 80%), tỷ lệ thời gian đường huyết an toàn "
        "(Time-in-Range TIR > 95%), tỷ lệ phát hiện vi phạm an toàn y khoa (100%), độ phủ bảo chứng Conformal (95%) và không thiên vị chủng tộc/giới tính.\n"
        "• Môi trường lâm sàng (Environment - E): Hồ sơ bệnh án điện tử (EHR), phòng khám đa khoa, dữ liệu khảo sát cộng đồng, bệnh nhân ngoại trú theo dõi 24 giờ.\n"
        "• Cơ cấu hành động (Actuators - A): Báo cáo hội chẩn đa tác tử có chữ ký số, khuyến nghị điều chỉnh đơn thuốc, kế hoạch can thiệp lối sống từng giờ, thông báo khẩn cấp.\n"
        "• Cơ cấu cảm nhận (Sensors - S): Dữ liệu nhập từ bác sĩ/bệnh nhân qua giao diện Web REST API, kết quả xét nghiệm máu (HbA1c, FPG, Creatinine), cảm biến đo đường huyết liên tục CGM.",
        title="KHUNG ĐẶC TẢ PEAS CHUẨN MỰC CHO CDSS",
        border_color="2563EB",
        fill_hex="EFF6FF"
    )

    add_custom_heading(doc, "2.2. Mô Hình BDI (Belief - Desire - Intention) & Cơ Chế Tự Chủ Của Tác Tử", level=2)
    add_body_p(
        doc,
        "Để đảm bảo tính tự chủ và khả năng lập luận minh bạch, các tác tử trong hệ thống DiaMulti-Agent CDSS v2 được thiết kế dựa trên kiến trúc nhận thức "
        "BDI (Beliefs - Desires - Intentions) do Michael Bratman đề xướng:\n"
        "• Niềm tin (Beliefs): Đại diện cho lượng tri thức mà tác tử nắm giữ về trạng thái hiện tại của bệnh nhân và môi trường y tế. Niềm tin này được cập nhật "
        "liên tục từ các xét nghiệm phòng lab, kết quả suy luận của các mô hình học máy và các nút được kích hoạt trên Đồ thị Tri thức Neo4j.\n"
        "• Mong muốn (Desires): Mục tiêu lâm sàng tối thượng mà tác tử hướng tới. Ví dụ: Tác tử Triage mong muốn phân tầng rủi ro chính xác nhất; Tác tử RL Coach "
        "mong muốn tối đa hóa tỷ lệ thời gian đường huyết nằm trong ngưỡng sinh lý an toàn 70–140 mg/dL; Tác tử Safety Rule mong muốn ngăn chặn 100% các biến cố ngộ độc thuốc.\n"
        "• Ý định (Intentions): Các kế hoạch hành động cụ thể mà tác tử cam kết thực thi sau khi đã cân nhắc các ràng buộc lâm sàng. Ví dụ: khi bệnh nhân có eGFR < 30 mL/phút, "
        "ý định của Safety Rule Agent là ghi đè khẩn cấp để tước bỏ chỉ định Metformin, bất chấp mô hình chẩn đoán AI có xác suất bệnh cao."
    )

    add_custom_heading(doc, "2.3. Tại Sao Phải Là Hệ Đa Tác Tử (MAS)? So Sánh Định Lượng Với Các Hệ Thống Đơn Lẻ", level=2)
    add_body_p(
        doc,
        "Một trong những câu hỏi căn bản của ngành khoa học máy tính ứng dụng y tế là: Tại sao không dùng một mô hình Deep Learning hoặc một mô hình LLM duy nhất "
        "để thực hiện mọi công việc từ chẩn đoán, tra cứu phác đồ cho tới lập kế hoạch vận động? Câu trả lời nằm ở bản chất đa chiều và rủi ro cực cao của y khoa:"
    )

    # Comparison Table MAS vs Single
    mas_cmp_headers = ["Tiêu Chí So Sánh Kỹ Thuật", "Hệ Thống Đơn Lẻ (Single-Agent / Monolithic AI)", "Hệ Thống Dựa Trên Luật Cứng (Rule-based Expert System)", "Hệ Đa Tác Tử Lâm Sàng (DiaMulti-Agent CDSS — PTIT v2)"]
    mas_cmp_data = [
        ["Độ phức tạp tính toán từng phần", "Rất cao: nhồi nhét quá nhiều nhiệm vụ vào 1 mô hình dẫn đến hiện tượng 'quên thảm họa' (Catastrophic Forgetting).", "Thấp: mã nguồn phân nhánh if-else chằng chịt, dễ xung đột logic khi số lượng luật vượt quá 100.", "Tối ưu: Chia nhỏ bài toán theo nguyên lý đơn nhiệm (Single Responsibility Principle); mỗi agent tối ưu cho một kỹ thuật riêng."],
        ["Khả năng kiểm thử & Cô lập lỗi", "Cực kỳ khó khăn: khi xảy ra lỗi kê đơn sai, không thể xác định do trọng số nơ-ron nào trong hàng triệu tham số.", "Dễ kiểm tra từng nhánh nhưng khó kiểm soát hiệu ứng lề (Side-effects) giữa các luật giao thoa.", "Tuyệt vời: Mỗi agent có bộ kiểm thử tự động độc lập (Unit Test); có thể cô lập lỗi tại đúng agent chịu trách nhiệm chuyên môn."],
        ["Độ tin cậy & Kiểm soát An toàn", "Kém: Mô hình học máy chỉ tối ưu hóa hàm mất mát toán học, hoàn toàn có thể sinh ra kết quả vi phạm an toàn y khoa.", "Tốt về mặt tuân thủ luật nhưng hoàn toàn bất lực trước các ca bệnh phức tạp chưa được lập trình sẵn.", "Đạt mức tối đa: Tác tử an toàn (Safety Agent) và Bác sĩ phản biện (Chief Critic) có quyền phủ quyết tuyệt đối các đề xuất nguy hiểm."],
        ["Khả năng mở rộng & Bảo trì", "Kém: Cập nhật một phác đồ y khoa mới của ADA 2024 đòi hỏi phải thu thập dữ liệu và huấn luyện lại toàn bộ mô hình từ đầu.", "Trung bình: Phải sửa mã nguồn thủ công, nguy cơ gây lỗi hồi quy (Regression bugs) rất cao.", "Vượt trội: Thêm hoặc nâng cấp một tác tử mới (ví dụ thêm tác tử Dược lý gen PGx) hoàn toàn không làm gián đoạn các tác tử khác."],
        ["Tính minh bạch giải thích (XAI)", "Hộp đen (Black-box): chỉ xuất ra một con số xác suất hoặc đoạn văn tạo sinh không thể truy vết ngược nguồn gốc.", "Minh bạch nhưng khô cứng, không lượng hóa được mức độ đóng góp xác suất của từng dấu ấn sinh học.", "Đa tầng: Kết hợp SHAP, tối ưu hóa can thiệp phản thực tế (What-If), đường đi suy luận đồ thị Neo4j và biên bản tranh luận 3 vòng."]
    ]
    populate_table(doc, mas_cmp_headers, mas_cmp_data, col_widths=[1.5, 1.8, 1.5, 2.2], header_bg="1E3A8A")

    add_custom_heading(doc, "2.4. Kiến Trúc Bảng Đen (Blackboard Architecture) & Bus Sự Kiện (Event-Driven Message Bus)", level=2)
    add_body_p(
        doc,
        "Để các tác tử độc lập có thể cộng tác mượt mà và chia sẻ dữ liệu hội chẩn mà không bị phụ thuộc chặt chẽ vào nhau (Loose Coupling), hệ thống áp dụng "
        "Kiến trúc Bảng đen (Blackboard Architectural Pattern) — một mẫu kiến trúc kinh điển được phát triển đầu tiên trong hệ thống Hearsay-II tại Đại học Carnegie Mellon. "
        "Kiến trúc Bảng đen bao gồm ba thành phần chủ chốt:\n"
        "1. Bảng đen (Blackboard Data Store): Kho dữ liệu trung tâm lưu trữ toàn bộ trạng thái của ca bệnh hiện tại, các giả thuyết chẩn đoán trung gian, "
        "kết quả tính toán của từng tác tử và biên bản tranh luận lâm sàng.\n"
        "2. Các nguồn tri thức (Knowledge Sources - 12 Agents): Mỗi tác tử đóng vai trò một chuyên gia độc lập, liên tục giám sát Bảng đen và chỉ kích hoạt "
        "khi trên Bảng đen xuất hiện dữ liệu thuộc phạm vi chuyên môn của mình.\n"
        "3. Cơ chế điều khiển & Bus sự kiện (Control Component & Event-Driven Bus): Bộ điều phối trung tâm (Diabetes Coordinator Agent) chịu trách nhiệm "
        "quản lý quyền truy cập, phát các sự kiện thay đổi trạng thái và bảo đảm quy trình hội chẩn diễn ra đúng trình tự quy định."
    )

    # Embed Fig 00
    add_figure(
        doc,
        "fig00_blackboard_architecture_spec.jpg",
        "Hình 2.1. Đặc tả kiến trúc Bảng đen (Blackboard Architecture) và Bus sự kiện giữa 12 Tác tử lâm sàng trong DiaMulti-Agent CDSS v2.",
        width_inches=6.0
    )

    add_body_p(
        doc,
        "Hợp đồng dữ liệu trao đổi giữa các tác tử được chuẩn hóa dưới dạng JSON Message Payload có cấu trúc chặt chẽ, bảo đảm tính toàn vẹn thông tin:"
    )

    code_contract = '''{
  "session_id": "PTIT_CLINICAL_SESSION_2026_09",
  "timestamp": "2026-11-13T07:15:00.000Z",
  "patient_vitals": {
    "age": 58, "gender": "Male", "bmi": 28.4,
    "blood_glucose_level": 175.0, "HbA1c_level": 8.2,
    "hypertension": 1, "heart_disease": 0, "smoking_history": "former"
  },
  "deliberation_state": {
    "current_stage": "STAGE_4_KNOWLEDGE_GRAPH_RETRIEVAL",
    "safety_status": "NORMAL_GUARDRAILS_PASSED",
    "ai_consensus_prob": 0.945,
    "conformal_prediction_set": ["Diabetes"],
    "conformal_confidence": 0.95,
    "active_agent": "DiaGraph-Agent",
    "blackboard_hypotheses": [
      {"source": "DiaDiagnostic", "claim": "Xác suất đái tháo đường 94.5% (Ensemble 8 Models)"},
      {"source": "DiaSafetyRule", "claim": "Đạt 12/12 luật an toàn; không có dấu hiệu DKA khẩn cấp"}
    ]
  }
}'''
    add_code_block(doc, code_contract, caption="Cấu trúc Hợp đồng Dữ liệu Sự kiện (JSON Event Contract) trên Blackboard Bus")
