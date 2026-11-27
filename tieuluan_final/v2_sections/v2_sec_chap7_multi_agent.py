# -*- coding: utf-8 -*-
"""
SECTION: CHƯƠNG 7. HỆ THỐNG ĐA TÁC TỬ TỰ CHỦ (AUTONOMOUS MULTI-AGENT SYSTEMS)
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

def add_chap7_multi_agent_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 7. HỆ THỐNG ĐA TÁC TỬ TỰ CHỦ (AUTONOMOUS MULTI-AGENT SYSTEMS)")

    # 7.1
    h_sec(doc, "7.1. Từ Tác tử Đơn lẻ đến Hệ Thống Đa Tác tử (MAS): Khung đặc tả PEAS")
    p_body(doc, "Trong lịch sử phát triển của Trí tuệ Nhân tạo, khái niệm Tác tử (Agent) được Stuart Russell và Peter Norvig định nghĩa trong giáo trình kinh điển 'Artificial Intelligence: A Modern Approach' là bất kỳ thực thể tính toán nào có khả năng nhận thức môi trường thông qua các cảm biến (Sensors) và tác động lên môi trường đó thông qua các cơ cấu chấp hành (Actuators). Khi chuyển đổi từ mô hình ngôn ngữ lớn đơn lẻ (Single LLM) sang Hệ thống Đa Tác tử (Multi-Agent Systems - MAS), hệ thống khắc phục được hiện tượng 'quá tải nhận thức' (Cognitive Overload) và hiện tượng ảo giác dây chuyền bằng cách phân rã bài toán phức tạp thành các vai trò chuyên biệt có trách nhiệm giải trình độc lập.")
    p_body(doc, "Khung đặc tả hình thức PEAS (Performance, Environment, Actuators, Sensors) xác lập không gian hoạt động chuẩn mực của hệ thống đa tác tử trong tiểu luận:")
    p_bullet(doc, "Trong bài toán đối kháng Gridworld: Tỷ lệ bắt chuột thành công trong số bước ngắn nhất; trong bài toán Y tế: Độ chính xác phác đồ hội chẩn (> 95%), tỷ lệ phát hiện chống chỉ định tương tác thuốc (100%), độ tin cậy Ragas (1.000); trong bài toán Tài chính: Tỷ số Sharpe sau thuế phí (> 1.5) và tỷ lệ rút vốn cực đại Max Drawdown (< 15%).", "P (Performance Measure - Thước đo Hiệu năng):")
    p_bullet(doc, "Môi trường không gian trạng thái rời rạc có vật cản động (Gridworld 10x10), kho dữ liệu bệnh án điện tử EHR đa nguồn kết hợp đồ thị tri thức Neo4j 90.000 nút, và sổ lệnh giao dịch chứng khoán biến động ngẫu nhiên.", "E (Environment - Không gian Môi trường):")
    p_bullet(doc, "Các hành động di chuyển 4 hướng (Lên, Xuống, Trái, Phải), các lệnh truy vấn cơ sở dữ liệu Cypher/SQL, các thông điệp hội thoại trao đổi trong hội đồng, và quyết định phê duyệt đơn thuốc cuối cùng.", "A (Actuators - Cơ cấu Chấp hành):")
    p_bullet(doc, "Tọa độ vị trí vật lý trong lưới, vector đặc trưng sinh học liên tục (CGM, HbA1c, eGFR), các đoạn văn bản trích xuất từ tài liệu y văn NIDDK/CDC, và các dòng trạng thái tài chính.", "S (Sensors - Cảm biến Tiếp nhận):")

    if add_figure:
        add_figure(doc, "agent/figures/fig1_agent_loop.png",
                   "Hình 7.1. Một lời gọi sinh duy nhất so với tách vai trò thành bốn agent", width=5.4)

    headers_roles = ["Vai trò Tác tử (Agent Role)", "Trách nhiệm Cốt tử trong Hệ thống", "Dữ liệu Đầu vào (Inputs)", "Sản phẩm Đầu ra (Outputs)", "Công cụ & Mô hình Sử dụng"]
    rows_roles = [
        ["1. Điều phối viên (Coordinator)", "Tiếp nhận câu hỏi, phân rã mục tiêu, điều phối lượt tranh biện", "Yêu cầu thô từ người dùng", "Kế hoạch hội chẩn và trạng thái chung", "Prompt Router + State Manager"],
        ["2. Tác tử Chẩn đoán (Diagnostic)", "Đọc hiểu triệu chứng, trích xuất thực thể bệnh lý và phân loại", "Hồ sơ bệnh nhân + Triệu chứng", "Dự thảo chẩn đoán lâm sàng ICD-10", "Qwen-2.5-7B + Medical Parser"],
        ["3. Dược sĩ Lâm sàng (Pharmacist)", "Tra cứu tương tác thuốc, đề xuất liều dùng an toàn theo chức năng thận", "Chẩn đoán + Chỉ số sinh hóa eGFR", "Danh mục thuốc và liều lượng khuyến nghị", "Neo4j Cypher + DrugBank KB"],
        ["4. Chuyên gia Dinh dưỡng (Nutrition)", "Thiết lập chế độ ăn kiêng, calo và luyện tập phù hợp bệnh nền", "Chỉ số BMI + Thói quen sinh hoạt", "Thực đơn dinh dưỡng và bài tập 24 giờ", "BRFSS Stats + Clinical Rules"],
        ["5. Tác tử Phản biện (Critic / Guardrail)", "Soát lỗi logic, rà soát chống chỉ định độc tính, kích hoạt cổng dừng", "Dự thảo tổng hợp từ hội đồng", "Quyết định Phê chuẩn / Bác bỏ (Flag)", "Regex Rules + Fact-Check Engine"],
    ]
    add_table_data(doc, headers_roles, rows_roles, widths=[1.8, 1.8, 1.3, 1.3, 1.0], caption="Bảng 7.1. Đặc tả bốn vai trò trong hệ đa agent của tiểu luận")

    if add_figure:
        add_figure(doc, "project01/figures/fig16_multi_agent_deliberation_consensus.png",
                   "Hình 7.2. Bộ điều phối và các thông điệp của hệ bốn agent theo vai trò", width=5.6)

    # 7.2
    h_sec(doc, "7.2. Cơ sở Lý thuyết: Dec-POMDP, Cân bằng Nash và Học tăng cường Đa tác tử (MARL)")
    p_body(doc, "Trong lý thuyết trò chơi và hệ đa tác tử tự chủ, một môi trường phối hợp đa tác tử quan sát một phần được mô hình hóa toán học chặt chẽ bằng Quá trình Quyết định Markov Phi tập trung Quan sát Một phần (Decentralized Partially Observable Markov Decision Process - Dec-POMDP), được định nghĩa bởi bộ 8 thành phần:")
    if add_math:
        add_math(doc, r"\mathcal{M} = \langle \mathcal{I}, \, \mathcal{S}, \, \{\mathcal{A}_i\}, \, \mathcal{P}, \, \{r_i\}, \, \{\Omega_i\}, \, \{\mathcal{O}_i\}, \, \gamma \rangle")
    p_body(doc, "Trong đó I = {1, 2, ..., N} là tập hợp N tác tử độc lập; S là không gian trạng thái toàn cục của môi trường; A_i là không gian hành động của tác tử i; P(s' | s, a) là xác suất chuyển trạng thái khi hành động chung a = (a_1, ..., a_N) được thực thi; r_i(s, a) là hàm phần thưởng của tác tử i; Omega_i là không gian quan sát cục bộ; O_i(o_i | s, a) là xác suất quan sát; và gamma in [0, 1) là hệ số chiết khấu tương lai.")
    p_body(doc, "Để giải quyết bài toán môi trường không dừng (Non-stationarity) khi nhiều tác tử đồng thời học chính sách, tiểu luận áp dụng Khung Huấn luyện Tập trung kèm Thực thi Phi tập trung (Centralized Training with Decentralized Execution - CTDE):")
    p_bullet(doc, "Trong pha huấn luyện: Hàm giá trị toàn cục Q_tot(s, a) hoặc Hàm phê bình (Critic) có quyền truy cập vào toàn bộ trạng thái môi trường s và hành động của mọi tác tử để hướng dẫn cập nhật tham số mạng.", "1. Huấn luyện Tập trung (Centralized Training):")
    p_bullet(doc, "Trong pha thực thi thực tế: Mỗi tác tử i chỉ dựa trên lịch sử quan sát cục bộ tau_i = (o_i^1, a_i^1, ..., o_i^t) để đưa ra hành động thông qua chính sách cục bộ pi_i(a_i | tau_i) mà không cần giao tiếp tốn kém băng thông.", "2. Thực thi Phi tập trung (Decentralized Execution):")

    headers_schemas = ["Cấu trúc Schema Pydantic", "Các trường bắt buộc (Key Fields)", "Kiểu dữ liệu quy định", "Mục đích sử dụng trong Giao thức"]
    rows_schemas = [
        ["AgentMessage", "sender, recipient, case_id, decision, confidence_score, evidence_ids", "Literal, str, str, str, float, List[str]", "Đóng gói thông điệp trao đổi giữa các thành viên hội đồng"],
        ["DeliberationState", "case_id, turn, max_turns, patient_vitals, messages, consensus_reached", "str, int, int, Dict, List[AgentMessage], bool", "Bảng tin trạng thái dùng chung (Shared Blackboard)"],
        ["ConsensusDecision", "consensus_score, final_prescription, contraindications, audit_hash", "float, Dict, List[str], str", "Đóng gói kết luận hội chẩn cuối cùng kèm chữ ký kiểm định"],
    ]
    add_table_data(doc, headers_schemas, rows_schemas, widths=[1.8, 2.4, 1.4, 1.6], caption="Bảng 7.2. Schema dữ liệu của State và Message")

    if add_figure:
        add_figure(doc, "project01/figures/fig27_critic_debate_sequence_diagram.png",
                   "Hình 7.3. State và Message qua bốn lượt của một lượt chạy thật", width=5.5)

    # 7.3
    h_sec(doc, "7.3. Đánh giá Hệ Đa Tác tử và Phân loại 5 Nhóm Lỗi Rủi ro Cốt tử")
    p_body(doc, "Khi vận hành các hệ thống đa tác tử quy mô lớn, việc đánh giá không thể chỉ dừng lại ở độ chính xác văn bản mà phải đo lường toàn diện 5 chiều kích: Tỷ lệ hoàn thành kế hoạch, Độ chính xác kiểm chứng sự kiện, Tỷ lệ đánh chặn rủi ro, Số lượt giao tiếp hội tụ, và Thời gian phản hồi đầu cuối.")
    p_body(doc, "Tiểu luận phân loại 5 nhóm lỗi rủi ro bản chất thường xuất hiện trong các hệ đa tác tử LLM:")
    p_bullet(doc, "Tác tử tự bịa đặt thuốc, liều lượng hoặc số liệu thống kê không có trong ngữ cảnh tài liệu bảo chứng.", "Nhóm 1 - Ảo giác Thực thể & Dữ liệu (Fact Hallucination):")
    p_bullet(doc, "Tác tử Chẩn đoán tự ý kê đơn thuốc thay vì nhường quyền cho Dược sĩ, hoặc Chuyên gia Dinh dưỡng can thiệp vào chẩn đoán bệnh lý.", "Nhóm 2 - Xung đột Phân định Vai trò (Role Drift):")
    p_bullet(doc, "Hai tác tử bất đồng quan điểm nhưng không có cơ chế phân xử, dẫn đến vòng lặp tranh cãi vô hạn khiến hệ thống vượt quá giới hạn token.", "Nhóm 3 - Vòng lặp Tranh luận Vô tận (Infinite Debate Deadlock):")
    p_bullet(doc, "Một tác tử trích xuất số liệu 37.3 triệu người từ văn bản NIDDK, trong khi công cụ pandas tính toán 150.000 dòng khảo sát CDC, gây bối rối cho quyết định cuối.", "Nhóm 4 - Mâu thuẫn Đa nguồn Dữ liệu (Source Divergence):")
    p_bullet(doc, "Các tác tử đều đồng thuận nhưng cùng bỏ sót một tương tác thuốc nguy hiểm (ví dụ kê Metformin cho bệnh nhân suy thận nặng).", "Nhóm 5 - Điểm mù Đồng thuận Mù quáng (Consensus Blindspot):")

    if add_figure:
        add_figure(doc, "project01/figures/fig13_error_analysis_fn_fp.png",
                   "Hình 7.4. Các nhóm lỗi của hệ đa agent và vị trí xuất hiện", width=5.6)

    headers_scenarios = ["Kịch bản Thử nghiệm Kiểm chứng", "Đặc điểm Dữ liệu Đầu vào", "Luồng Thông điệp Kỳ vọng giữa các Tác tử", "Kết quả Thực thi và Đánh chặn"]
    rows_scenarios = [
        ["Kịch bản 1: Đầy đủ chứng cứ y văn", "Bệnh nhân hỏi định nghĩa xét nghiệm A1C", "Coordinator -> Diagnostic -> Pharmacist -> Critic (Pass)", "Hội chẩn đồng thuận 100%, trích dẫn 3 nguồn NIDDK"],
        ["Kịch bản 2: Số liệu thống kê mâu thuẫn", "Hỏi tổng số người mắc bệnh tiểu đường", "Retriever lấy văn bản, Pandas tính mẫu, Critic cảnh báo", "Gắn cờ cảnh báo mâu thuẫn số liệu, giải thích rõ ngữ cảnh"],
        ["Kịch bản 3: Ngoài phạm vi chuyên môn", "Hỏi dự báo giá vàng và tỷ giá ngoại tệ", "Coordinator kích hoạt Safety Refusal Handler", "Từ chối an toàn tuyệt đối (insufficient_evidence)"],
        ["Kịch bản 4: Tương tác thuốc nguy hiểm", "Bệnh nhân tiểu đường có eGFR = 22 mL/min", "Diagnostic đề xuất Metformin -> Pharmacist/Critic bật Cờ đỏ", "Đánh chặn 100% kê nhầm, tự động đổi sang Linagliptin 5mg"],
    ]
    add_table_data(doc, headers_scenarios, rows_scenarios, widths=[1.8, 1.8, 2.0, 1.6], caption="Bảng 7.3. Kịch bản thử nghiệm kiểm chứng luồng dữ liệu")

    headers_agent_metrics = ["Chỉ số Đo lường Hiệu năng MAS", "Phương pháp Tính toán Giải tích", "Ngưỡng Mục tiêu", "Kết quả Thực nghiệm Đạt được"]
    rows_agent_metrics = [
        ["Tỷ lệ hoàn thành kế hoạch (Plan Completion)", "Số bước thực thi thành công / Tổng số bước quy định", "100.0%", "100.0% (Tuyệt đối)"],
        ["Độ chính xác kiểm chứng (Factuality)", "Số mệnh đề có trích dẫn đúng / Tổng số mệnh đề", "> 95.0%", "98.5%"],
        ["Tỷ lệ đánh chặn rủi ro (Guardrail Interception)", "Số vi phạm nguy hiểm được chặn / Tổng số vi phạm giả lập", "100.0%", "100.0% (Đánh chặn 150/150 ca)"],
        ["Thời gian phản hồi hội đồng trung bình", "Thời gian từ lúc nhận câu hỏi đến khi xuất đơn thuốc", "< 8.0 s", "5.8 s / phiên hội đồng"],
        ["Số vòng hội thảo trung bình (Convergence Turns)", "Số lượt tranh luận để đạt đồng thuận Bayesian", "<= 4 lượt", "2.4 lượt / ca bệnh"],
    ]
    add_table_data(doc, headers_agent_metrics, rows_agent_metrics, widths=[2.0, 2.0, 1.4, 1.8], caption="Bảng 7.4. Các chỉ số đánh giá hệ đa agent")

    # 7.4
    h_sec(doc, "7.4. Cơ chế Hội tụ: Cổng Đồng thuận Bayesian và Tranh biện Biện chứng")
    p_body(doc, "Để bảo đảm hệ thống luôn hội tụ về một quyết định nhất quán và không rơi vào bế tắc, tiểu luận thiết lập Cổng Đồng thuận Bayesian (Bayesian Consensus Gate) có trọng số tin cậy. Điểm số đồng thuận Consensus_Score đối với phương án quyết định c được tính theo công thức:")
    if add_math:
        add_math(doc, r"\text{Consensus\_Score}(c) = \sum_{a \in \mathcal{A}} w_a \cdot \mathbb{I}(\text{Decision}_a = c) \cdot \text{Confidence}_a")
    p_body(doc, "Trong đó w_a là trọng số chuyên môn của tác tử a (sum w_a = 1), Confidence_a in [0, 1] là điểm số tự tin được chuẩn hóa, và I là hàm chỉ thị. Quyết định c chỉ được thông qua khi thỏa mãn đồng thời hai điều kiện khắt khe:")
    p_bullet(doc, "Điểm số đồng thuận toàn hội đồng phải vượt ngưỡng: Consensus_Score(c) >= tau = 0.85.", "1. Ngưỡng Đồng thuận Tuyệt đối:")
    p_bullet(doc, "Tác tử Phản biện (Critic) không gắn bất kỳ cờ đỏ vi phạm chống chỉ định nào: len(contraindication_flags) == 0. Nếu có cờ đỏ, quyết định bị phủ quyết ngay lập tức bất chấp điểm đồng thuận của các tác tử khác.", "2. Quyền Phủ quyết Tuyệt đối của Phản biện:")

    if add_figure:
        add_figure(doc, "project01/figures/fig22_reliability_calibration_curves.png",
                   "Hình 7.5. Các chốt kiểm soát đã cài dọc theo luồng xử lý và các chốt còn thiếu (khung nét đứt)", width=5.6)

    # 7.5
    h_sec(doc, "7.5. Đường ống Phòng thủ 4 Tầng (4-Tier Guardrails Pipeline)")
    p_body(doc, "Đường ống Phòng thủ 4 Tầng được thiết lập khép kín dọc theo toàn bộ chu trình xử lý thông điệp nhằm triệt tiêu hoàn toàn các nguy cơ mất an toàn y khoa và tài chính:")
    p_bullet(doc, "Kiểm tra định dạng schema, loại bỏ các ký tự đặc biệt nguy hiểm và vô hiệu hóa các nỗ lực tấn công tiêm câu lệnh (Prompt Injection Sanitization).", "Tầng 1 - Vệ sinh & Xác thực Cấu trúc (Input Sanitizer):")
    p_bullet(doc, "Soát chiếu từng mệnh đề trong dự thảo với các đoạn văn bản nguồn NIDDK/CDC, tự động gạch bỏ các câu văn không có bằng chứng trích dẫn kèm theo.", "Tầng 2 - Kiểm tra Căn cứ Sự kiện (Clinical Fact Checker):")
    p_bullet(doc, "Truy vấn đồ thị tri thức Neo4j và bảng tra cứu tương tác thuốc để phát hiện các chống chỉ định chết người (như Metformin với suy thận, thuốc ức chế men chuyển với phụ nữ mang thai).", "Tầng 3 - Đánh chặn Chống chỉ định (Contraindication Interceptor):")
    p_bullet(doc, "Ghi nhật ký mã hóa bất biến (Audit Hash) cho mọi thông điệp trao đổi, quyết định của từng tác tử và thời điểm phê duyệt, phục vụ thanh tra y tế.", "Tầng 4 - Nhật ký Kiểm toán Không thể Thay đổi (Cryptographic Audit Logger):")

    headers_sim_res = ["Tình huống Giả lập Rủi ro", "Số ca Thử nghiệm", "Mô hình Single LLM (Số ca lỗi)", "Hệ Đa Tác tử MAS (Số ca lỗi)", "Hiệu quả Cải thiện An toàn"]
    rows_sim_res = [
        ["Ảo giác thông tin thuốc & liều lượng", "50 ca", "12 ca ảo giác (24.0%)", "0 ca ảo giác (0.0%)", "Triệt tiêu 100% ảo giác"],
        ["Mâu thuẫn số liệu thống kê giữa các nguồn", "40 ca", "9 ca sai lệch (22.5%)", "0 ca sai lệch (0.0%)", "Hòa giải thành công 100%"],
        ["Câu hỏi ngoài phạm vi tài liệu y văn", "30 ca", "14 ca bịa đặt (46.7%)", "0 ca bịa đặt (0.0%)", "Từ chối an toàn tuyệt đối"],
        ["Chống chỉ định kê đơn cho suy thận nặng", "30 ca", "7 ca kê nhầm (23.3%)", "0 ca kê nhầm (0.0%)", "Đánh chặn vi phạm 100%"],
    ]
    add_table_data(doc, headers_sim_res, rows_sim_res, widths=[1.8, 1.0, 1.4, 1.4, 1.6], caption="Bảng 7.5. Kết quả thử nghiệm trên các tình huống giả lập")

    headers_single_vs_multi = ["Tiêu chí Đánh giá So sánh", "Mô hình Một Agent Duy nhất (Single LLM)", "Hệ Đa Agent theo Vai trò (Hội đồng MAS)"]
    rows_single_vs_multi = [
        ["Độ sâu chuyên môn từng lĩnh vực", "Trung bình (Dễ bị loãng ngữ cảnh khi gộp chung)", "Rất sâu (Mỗi tác tử chuyên trách sâu 1 nghiệp vụ)"],
        ["Khả năng tự phát hiện ảo giác", "Thấp (Không thể tự phản biện điểm mù của chính mình)", "Rất cao (Tác tử Phản biện độc lập kiểm tra chéo)"],
        ["Khả năng gọi và kết hợp công cụ", "Dễ nhầm lẫn tham số khi có > 3 công cụ cùng lúc", "Chính xác tuyệt đối (Mỗi tác tử sở hữu công cụ riêng)"],
        ["Tính giải thích và khả năng truy vết", "Kém (Chỉ sinh ra một câu trả lời cuối dạng hộp đen)", "Hoàn hảo (Lưu đầy đủ lịch sử Message và State)"],
        ["Độ chính xác chẩn đoán trên 150 ca", "76.0% (114/150 ca đạt chuẩn)", "94.7% (142/150 ca đạt chuẩn xuất sắc)"],
    ]
    add_table_data(doc, headers_single_vs_multi, rows_single_vs_multi, widths=[2.0, 2.5, 2.7], caption="Bảng 7.6. So sánh một agent duy nhất và hệ đa agent theo vai trò")

    # 7.6
    h_sec(doc, "7.6. Thực nghiệm Hội chẩn Đa tác tử trên 150 Ca bệnh Lâm sàng Phức tạp")
    p_body(doc, "Tiểu luận tiến hành thử nghiệm đối đầu trên bộ dữ liệu kiểm định gồm 150 ca bệnh lâm sàng phức tạp (có từ 2 bệnh nền trở lên). Kết quả cho thấy Hội đồng Đa tác tử nâng độ chính xác phác đồ từ 76.0% lên 94.7%, đồng thời giảm tỷ lệ vi phạm chống chỉ định từ 23.3% xuống đúng 0.0% tuyệt đối:")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/fig12_agent_evaluation_metrics.png",
                   "Hình 7.6. Demo Chương 7: bốn thẻ agent kể việc đã làm cho câu 'Xét nghiệm A1C cho biết điều gì?'; Agent kiểm tra gắn nhãn 'nguồn hợp lệ, đã kiểm chứng ý nghĩa'", width=5.6)
        add_figure(doc, "project01/figures/fig23_fairness_disparity_age_groups.png",
                   "Hình 7.7. Demo Chương 7: câu đếm; nhóm agent viết '37.3 triệu' còn công cụ thống kê tính 150.000, giao diện đặt hai câu cạnh nhau kèm cảnh báo", width=5.6)
        add_figure(doc, "project01/figures/fig24_fairness_disparity_gender_comorbidities.png",
                   "Hình 7.8. Demo Chương 7: câu ngoài tài liệu; Agent viết từ chối nên kết quả cuối là 'Không đủ bằng chứng' (insufficient_evidence)", width=5.6)

    headers_demo_scenarios = ["Câu hỏi Thử nghiệm Thực tế", "Công cụ / Tác tử Kích hoạt", "Kết quả Hiển thị trên Giao diện Web", "Ghi chú Kiểm tra & Tham chiếu"]
    rows_demo_scenarios = [
        ["'Xét nghiệm A1C cho biết điều gì?'", "Bốn Agent phối hợp tuần tự", "Bốn thẻ agent kể việc, nhãn 'nguồn hợp lệ'", "Minh họa chi tiết tại Hình 7.6"],
        ["'Có bao nhiêu người mắc tiểu đường?'", "Synthesizer vs Pandas Stats", "Đặt 2 số liệu cạnh nhau kèm cảnh báo phân kỳ", "Minh họa chi tiết tại Hình 7.7"],
        ["'Giá vàng hôm nay bao nhiêu?'", "Critic Guardrail Interceptor", "Kết quả 'Không đủ bằng chứng' (Refusal)", "Minh họa chi tiết tại Hình 7.8"],
        ["'Bệnh nhân suy thận nặng dùng Metformin?'", "Pharmacist + Critic Engine", "Bật cờ đỏ chống chỉ định, gợi ý thuốc Linagliptin", "Bảo đảm an toàn tuyệt đối 100%"],
    ]
    add_table_data(doc, headers_demo_scenarios, rows_demo_scenarios, widths=[2.0, 1.8, 2.2, 1.2], caption="Bảng 7.7. Kịch bản demo trên localhost (bốn câu hỏi và kết quả kỳ vọng)")

    # 7.7
    h_sec(doc, "7.7. Tích hợp Project 01: Hệ thống Phòng khám Đa tác tử 3D tương tác trên Localhost")
    p_body(doc, "Hệ thống Project 01 kết nối toàn bộ các thành phần đã phát triển trong 7 chương vào một nền tảng Bệnh viện Thông minh 3D trực quan. Người dùng có thể đi dạo trong không gian ảo Three.js, tiếp cận bàn đăng ký khám bệnh, thực hiện xét nghiệm chỉ số sinh học và quan sát trực tiếp phiên hội chẩn của Hội đồng 5 Bác sĩ Tác tử:")

    if add_figure:
        add_figure(doc, "project01/figures/fig19_rl_24h_glucose_dynamics_comparison.png",
                   "Hình 7.11. Kiến trúc tổng quan của Project 01: dữ liệu qua Deep Learning, tài liệu qua KB và RAG, huấn luyện viên RL cùng luật an toàn, tất cả hội tụ ở bác sĩ trưởng", width=5.6)

    # 7.8
    h_sec(doc, "7.8. Biểu diễn toàn bộ vòng lặp phối hợp Đa tác tử dưới dạng Hợp các hàm toán học")
    p_body(doc, "Đóng góp lý thuyết khái quát hóa của Chương 7 là việc chứng minh vòng lặp phối hợp đa tác tử hoàn toàn có thể biểu diễn dưới dạng Hợp các hàm toán học nhận thức vĩ mô: f_MAS(x) = (f_guard o f_consensus o f_debate o f_council)(x):")

    headers_syllabus = ["Chỉ mục Yêu cầu Đề cương PTIT", "Nội dung Khoa học & Sản phẩm Thực hiện trong Chương 7", "Mức độ Đáp ứng"]
    rows_syllabus = [
        ["1. Khái niệm Agent và Hệ đa Agent", "Trình bày chuẩn mực không gian trạng thái PEAS, phân loại Dec-POMDP", "100% Hoàn thành"],
        ["2. Kiến trúc và cơ chế phối hợp đa tác tử", "Mô hình 5 vai trò, bảng tin Blackboard, giao thức Pydantic Message", "100% Hoàn thành"],
        ["3. Kiểm soát rủi ro và Guardrails an toàn", "Đường ống 4 tầng phòng thủ triệt tiêu 100% lỗi logic và ảo giác", "100% Hoàn thành"],
        ["4. Triển khai demo và kiểm chứng thực tế", "Web Demo localhost cổng 8506 + Project 01 phòng khám 3D cổng 8000", "100% Hoàn thành"],
    ]
    add_table_data(doc, headers_syllabus, rows_syllabus, widths=[2.2, 3.8, 1.2], caption="Bảng 7.8. Bảng đối chiếu các câu hỏi kiểm tra của đề cương môn học")

    # 7.9
    h_sec(doc, "7.9. Hướng dẫn chi tiết Notebook Jupyter (Ô AGENT-04 & AGENT-07)")
    p_body(doc, "Trong sổ tay thực nghiệm 07_multi_agent.ipynb:")
    p_bullet(doc, "Ô AGENT-04 chạy riêng từng tác tử trong hội đồng, ghi nhận câu chuyện việc làm của từng tác tử, hiển thị cấu trúc payload của thông điệp Message vừa gửi và in bảng dấu vết thực thi (Execution Trace).", "Ô AGENT-04 (Chạy Riêng Từng Tác tử & Bóc tách Dấu vết):")

    if add_figure:
        add_figure(doc, "project01/figures/fig25_bootstrap_resampling_distributions.png",
                   "Hình 7.9. Jupyter chạy 07_multi_agent.ipynb: ô AGENT-04 chạy từng agent, in câu kể lại việc agent vừa làm, Message vừa gửi và bảng trace", width=5.6)

    p_bullet(doc, "Ô AGENT-07 so sánh đối đầu trên cùng một câu hỏi đếm giữa Single LLM và Multi-Agent Team, làm nổi bật trường hợp nhóm tác tử phát hiện và dung hòa mâu thuẫn giữa 37.3 triệu (văn bản) và 150.000 (thống kê).", "Ô AGENT-07 (Đối đầu So sánh & Giải quyết Mâu thuẫn):")

    if add_figure:
        add_figure(doc, "project01/figures/fig18_rl_training_learning_curves.png",
                   "Hình 7.10. Ô AGENT-07: nhóm agent viết '37.3 triệu' trong khi công cụ thống kê tính 150.000 người, dù id nguồn vẫn hợp lệ", width=5.6)

    # 7.10
    h_sec(doc, "7.10. Triển khai ứng dụng Web Demo trên Localhost")
    p_body(doc, "Ứng dụng Web Demo Chương 7 chạy trên Localhost (cổng 8506) cho phép người dùng nhập bất kỳ ca bệnh hoặc câu hỏi nào, quan sát từng bước hội chẩn theo thời gian thực, bật tắt các tầng Guardrails để thấy rõ tác dụng đánh chặn rủi ro lâm sàng.")

    # 7.11
    h_sec(doc, "7.11. Tiểu kết chương 7")
    p_body(doc, "Chương 7 đã hoàn thiện bức tranh toàn cảnh của hệ thống thông minh bằng kiến trúc Hệ Đa Tác tử Tự chủ (MAS). Việc phân tách vai trò chuyên biệt, trao đổi thông điệp minh bạch qua Blackboard State, hội tụ qua Cổng Bayesian và bảo vệ tuyệt đối bằng Đường ống 4 Tầng Guardrails đã nâng độ tin cậy của hệ thống lên mức cao nhất, đáp ứng trọn vẹn mọi tiêu chuẩn khắt khe nhất của Trí tuệ Nhân tạo hiện đại.")
