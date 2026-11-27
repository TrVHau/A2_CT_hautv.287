# -*- coding: utf-8 -*-
"""Section: MỞ ĐẦU (Introduction)"""

def add_mo_dau(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data):
    h_chap(doc, "MỞ ĐẦU")
    
    h_sec(doc, "1. Lý do chọn đề tài")
    p_body(doc, "Kỷ nguyên công nghệ số năm 2026 đang chứng kiến sự hội tụ bùng nổ chưa từng có giữa các nhánh nghiên cứu của Trí tuệ Nhân tạo (Artificial Intelligence - AI). Nếu như trong giai đoạn 2012–2021, tâm điểm của cuộc cách mạng AI tập trung vào Học sâu (Deep Learning) với khả năng trích xuất đặc trưng tự động trên các dạng dữ liệu cảm quan phi cấu trúc như hình ảnh (thông qua Convolutional Neural Networks - CNN) hay chuỗi thời gian tuần tự (thông qua Recurrent Neural Networks - RNN, LSTM, GRU); thì từ năm 2022 đến nay, làn sóng Mô hình Nền tảng (Foundation Models), Đồ thị Tri thức (Knowledge Graphs - KG), Truy hồi Tăng cường Tạo sinh (Retrieval-Augmented Generation - RAG) và đặc biệt là Hệ Đa Tác tử Tự chủ (Autonomous Multi-Agent Systems - MAS) đã tái định hình căn bản cách con người tiếp cận việc xây dựng các hệ thống tính toán thông minh.")
    p_body(doc, "Tuy nhiên, trong thực tiễn nghiên cứu học thuật và triển khai ứng dụng công nghiệp, một khoảng cách lớn thường xuyên tồn tại: các nhà nghiên cứu thường xem xét các kỹ thuật trên một cách rời rạc, phân mảnh. Kỹ sư dữ liệu tập trung vào học máy bảng truyền thống (Tabular Machine Learning); chuyên gia thị giác máy tính tách biệt trong không gian CNN; chuyên gia tài chính định lượng chỉ nghiên cứu mô hình chuỗi thời gian RNN/LSTM; trong khi các nhà phát triển hệ thống hiện đại lại nhảy thẳng vào gọi API từ các mô hình ngôn ngữ lớn (LLMs) mà bỏ qua hoàn toàn nền tảng toán học, cơ chế lan truyền ngược (backpropagation), thiên kiến quy nạp (inductive bias) và các ràng buộc về độ tin cậy của mô hình.")
    p_body(doc, "Xuất phát từ tư tưởng cốt lõi xuyên suốt chương trình đào tạo của PGS. TS. Trần Đình Quế: 'Hiểu bản chất hệ thống, biểu diễn tường minh thông tin, học mối quan hệ từ dữ liệu thực tế và biến mô hình thành ứng dụng hoàn chỉnh có thể kiểm chứng được', đề tài tiểu luận này được xây dựng nhằm mục tiêu kết nối toàn diện và liền mạch toàn bộ các tầng bậc tiến hóa của Trí tuệ Nhân tạo. Thông qua hai miền ứng dụng thực tiễn mang tính sống còn và đòi hỏi độ chính xác khắt khe bậc nhất của xã hội hiện đại: (1) Y tế thông minh và Bệnh lý chuyển hóa mạn tính (Healthcare & Metabolic Disorders) và (2) Tài chính thông minh và Đầu tư định lượng (Quantitative Finance & Risk Management), tiểu luận sẽ chứng minh tính tổng quát, khả năng chuyển giao liên miền và triết lý toán học thống nhất của toàn bộ hệ thống thông minh.")

    h_sec(doc, "2. Mục tiêu nghiên cứu")
    p_body(doc, "Đề tài hướng tới các mục tiêu cụ thể và chuẩn mực sau:")
    p_bullet(doc, "Làm chủ trọn vẹn nền tảng lý thuyết và bản chất toán học từ các thuật toán Học máy cơ bản (Linear/Logistic Regression, Tree-based, SVM, PCA, K-Means), Mạng nơ-ron tích chập (CNN), Mạng nơ-ron hồi quy (RNN, LSTM, GRU) đến Đồ thị tri thức (KG), Học sâu trên đồ thị (Deep Graph - GNN, GCN, GraphSAGE, GAT) và Hệ đa tác tử (MAS).", "Về mặt lý thuyết:")
    p_bullet(doc, "Thực hiện cài đặt độc lập và kiểm chứng chéo (parity verification) trên ba nền tảng: Scratch thuần (NumPy/Python từ đầu), Keras/TensorFlow và PyTorch, đảm bảo gradient đạo hàm và sai số suy luận sai lệch dưới ngưỡng máy tính số học ($< 10^{-7}$).", "Về mặt cài đặt thuật toán:")
    p_bullet(doc, "Thực nghiệm nghiêm ngặt trên các bộ dữ liệu thật đa dạng: dữ liệu bảng y tế NHANES/Pima, dữ liệu bảng tài chính LendingClub/Housing, ảnh y tế võng mạc RetinaMNIST, ảnh MNIST, chuỗi thời gian đường huyết CGM Shanghai, chuỗi giá cổ phiếu AAPL/VN-Index, đồ thị trích dẫn Pubmed/Cora và đồ thị tương quan tài chính.", "Về mặt thực nghiệm dữ liệu:")
    p_bullet(doc, "Xây dựng các hệ thống hỏi đáp có căn cứ (Grounded Q&A) kết hợp RAG, Đồ thị Tri thức và Tool-Use, khắc phục triệt để hiện tượng ảo giác (hallucination) và dữ liệu lỗi thời của các mô hình ngôn ngữ lớn.", "Về mặt tri thức biểu tượng:")
    p_bullet(doc, "Xây dựng các hệ đa tác tử phối hợp (Cooperative MAS) và học tăng cường đa tác tử (MARL) có cơ chế phân xử đồng thuận (Consensus Gate) và chốt an toàn (Guardrails) đa tầng.", "Về mặt hệ tác tử tự chủ:")
    p_bullet(doc, "Đóng gói toàn bộ các mô hình và luồng suy luận thành giao diện Web tương tác trực quan (Localhost Demo), cho phép người dùng kiểm tra, kiểm thử và tái lập toàn bộ quy trình.", "Về mặt triển khai ứng dụng:")

    h_sec(doc, "3. Câu hỏi nghiên cứu (Research Questions)")
    p_body(doc, "Tiểu luận được thiết kế để trả lời 6 câu hỏi nghiên cứu nền tảng:")
    p_bullet(doc, "Bản chất toán học của quá trình học biểu diễn (representation learning) thay đổi như thế nào khi chuyển dịch từ dữ liệu bảng (1D), dữ liệu ảnh (2D), dữ liệu chuỗi thời gian (tuần tự) sang dữ liệu đồ thị (phi Euclid) và tri thức ngữ nghĩa?", "RQ1 (Về biểu diễn dữ liệu):")
    p_bullet(doc, "Liệu việc cài đặt thủ công từ đầu (Scratch thuần) với đạo hàm giải tích giải bằng tay có đạt được sự tương đồng hoàn toàn về độ chính xác và đường cong tối ưu so với các framework công nghiệp hiện đại (Keras, PyTorch) hay không?", "RQ2 (Về kiểm chứng tương đương):")
    p_bullet(doc, "Mạng tích chập CNN và cơ chế giải thích Grad-CAM có thực sự học được các đặc trưng ngữ nghĩa mang ý nghĩa lâm sàng/kinh tế hay chỉ học tương quan giả ngẫu nhiên?", "RQ3 (Về tính giải thích của CNN):")
    p_bullet(doc, "Cơ chế cổng của LSTM và GRU giải quyết sự suy giảm gradient (vanishing gradient) như thế nào trong bài toán dự báo chuỗi thời gian so với SimpleRNN, và làm thế nào để loại bỏ triệt để hiện tượng nhìn trước tương lai (lookahead bias)?", "RQ4 (Về mô hình hóa chuỗi tuần tự):")
    p_bullet(doc, "Sự kết hợp giữa Đồ thị Tri thức (Knowledge Graph) và RAG (GraphRAG) cải thiện độ trung thực (Faithfulness) và khả năng suy luận đa bước (Multi-hop Reasoning) như thế nào so với RAG vector thuần túy?", "RQ5 (Về tích hợp tri thức và RAG):")
    p_bullet(doc, "Hệ đa tác tử (Multi-Agent System) gồm nhiều chuyên gia phân vai có thực sự vượt trội hơn một tác tử đơn lẻ (Single-Agent) hoặc một lời nhắc Prompt LLM duy nhất trong các nhiệm vụ phức tạp đòi hỏi thẩm định chéo hay không?", "RQ6 (Về hiệu năng đa tác tử):")

    h_sec(doc, "4. Đối tượng và Phạm vi nghiên cứu")
    p_body(doc, "Để đảm bảo tính nghiêm cẩn khoa học và chiều sâu thực nghiệm, tiểu luận lựa chọn tiếp cận song song hai miền bài toán đại diện tiêu biểu (Dual Domains Strategy):")
    p_bullet(doc, "Tập trung vào bệnh lý đái tháo đường (Diabetes) — một căn bệnh mạn tính toàn cầu với đầy đủ các dạng thái dữ liệu: (i) Bảng lâm sàng và xét nghiệm sinh hóa (Pima Indians, NHANES 2011–2018); (ii) Ảnh y tế chụp đáy mắt đáy võng mạc (RetinaMNIST); (iii) Chuỗi thời gian theo dõi đường huyết liên tục (CGM Shanghai T1DM/T2DM); (iv) Đồ thị tri thức y học và hướng dẫn điều trị của Bộ Y tế / MedQuAD; (v) Mạng lưới bài báo nghiên cứu y sinh học (Pubmed-Diabetes).", "Miền 1 — Y tế Chuyển hóa Lâm sàng:")
    p_bullet(doc, "Tập trung vào phân tích định lượng thị trường tài chính và rủi ro: (i) Bảng dữ liệu tín dụng và rủi ro vỡ nợ (LendingClub / Housing valuation); (ii) Biểu đồ nến kỹ thuật (Candlestick charts / Gramian Angular Fields); (iii) Chuỗi giá cổ phiếu và lợi suất chuỗi thời gian (Apple AAPL, S&P 500, VN-Index 30); (iv) Đồ thị tri thức tài chính doanh nghiệp và báo cáo tài chính (FinQA / SEC filings); (v) Mạng lưới tương quan lợi suất đa biến giữa các nhóm ngành cổ phiếu.", "Miền 2 — Kinh tế Định lượng & Phân tích Tài chính:")

    h_sec(doc, "5. Phương pháp nghiên cứu")
    p_body(doc, "Nghiên cứu áp dụng phương pháp luận khoa học thực nghiệm đối chứng đa chiều:")
    p_bullet(doc, "Thiết lập các công thức giải tích chuẩn mực cho hàm mất mát, gradient đạo hàm, phép tích chập, phương trình lan truyền ngược qua thời gian, biến đổi Fourier trên đồ thị và phương trình tối ưu Bellman.", "Phương pháp hình thức toán học:")
    p_bullet(doc, "Áp dụng chiến lược chia tập nghiêm ngặt (Train / Validation / Test) độc lập, chuẩn hóa dữ liệu sau khi chia để chống rò rỉ thông tin (Data Leakage), áp dụng Walk-forward split cho chuỗi thời gian, và 10-Fold Cross-Validation cho dữ liệu bảng.", "Phương pháp thực nghiệm kiểm soát:")
    p_bullet(doc, "Tiến hành phân tích cô lập (Ablation Study) để bóc tách đóng góp của từng thành phần kiến trúc (ví dụ: tác động của Batch Normalization trong CNN, tác động của cổng quên Forget Gate trong LSTM, tác động của phép gộp trong GCN, tác động của Critic Agent trong MAS).", "Phương pháp bóc tách thành phần:")
    p_bullet(doc, "Đánh giá bằng hệ thống chỉ số toàn diện: Accuracy, Precision, Recall, Specificity, F1-macro, ROC-AUC, PR-AUC, MSE, RMSE, MAE, R², Sharpe Ratio, Maximum Drawdown, Hit@k, MRR, Faithfulness, Answer Relevance.", "Hệ thống đo lường đa tiêu chí:")

    h_sec(doc, "6. Đóng góp nổi bật của bài tiểu luận")
    p_body(doc, "Công trình tiểu luận đóng góp 10 giá trị khoa học và kỹ thuật cốt lõi:")
    p_bullet(doc, "Xây dựng bức tranh toàn cảnh xuyên suốt từ lịch sử 1950 tới 2026, thực nghiệm đối đầu 4 thế hệ mô hình trên cùng bài toán.", "1. Tổng quan lịch sử toàn diện:")
    p_bullet(doc, "Hiện thực hóa trọn vẹn 3 bản cài đặt độc lập (Scratch thuần NumPy, Keras, PyTorch) cho các kiến trúc mạng nơ-ron nhiều lớp (MLP), mạng tích chập (CNN) và mạng hồi quy (RNN/LSTM).", "2. Bộ ba cài đặt chuẩn mực:")
    p_bullet(doc, "Cung cấp bảng đối chiếu sai lệch gradient đạo hàm (Parity Check) đạt độ chính xác số học tới $10^{-7}$, chứng minh tính đúng đắn tuyệt đối của mã nguồn Scratch.", "3. Bằng chứng kiểm chứng tương đương:")
    p_bullet(doc, "Biểu diễn toàn bộ các mô hình học sâu phức tạp (MLP, CNN, RNN, GCN, Multi-Agent) dưới dạng hàm hợp toán học tường minh $f(x) = (f_L \circ f_{L-1} \circ \dots \circ f_1)(x)$.", "4. Lý thuyết hàm hợp xuyên suốt:")
    p_bullet(doc, "Triển khai kỹ thuật Grad-CAM trên CNN giúp soi rọi các nơ-ron lớp tích chập cuối, minh chứng trực quan vùng tổn thương đáy mắt và mô hình đảo chiều giá.", "5. Tính giải thích trực quan với Grad-CAM:")
    p_bullet(doc, "Áp dụng Walk-forward backtest trên chuỗi thời gian, đo lường các hệ số tài chính chuyên sâu (Sharpe ratio, Maximum Drawdown) và phân tích sai số theo dải glucose lâm sàng.", "6. Đánh giá chuỗi thời gian không nhìn trước:")
    p_bullet(doc, "Hiện thực hóa hệ thống GraphRAG kết hợp cơ sở tri thức đồ thị bộ ba (SPO triples) và truy hồi lai (BM25 + Dense + RRF), nâng cao vượt bậc chất lượng hỏi đáp.", "7. Hệ thống Hybrid GraphRAG:")
    p_bullet(doc, "Thực nghiệm học sâu trên đồ thị (GNN, GCN, GraphSAGE, GAT) trên cả mạng trích dẫn khoa học và mạng lưới tương quan tài chính, phân tích định lượng hiện tượng over-smoothing.", "8. Khám phá sâu sắc Deep Graph:")
    p_bullet(doc, "Xây dựng song song hai hệ đa tác tử: Hệ học tăng cường (MARL) Mèo đuổi chuột trong môi trường lưới đối kháng và Hệ Hội đồng Đa tác tử LLM có cơ chế đồng thuận Consensus Gate.", "9. Hệ Đa tác tử tự chủ và cơ chế phòng vệ:")
    p_bullet(doc, "Toàn bộ 7 chương đều đi kèm ứng dụng Web Demo (Localhost Dashboard) tương tác trực quan thời gian thực, minh chứng tính sẵn sàng ứng dụng thực tiễn.", "10. Hệ thống Demo Web đa chương trình:")

    h_sec(doc, "7. Cấu trúc của bài tiểu luận")
    p_body(doc, "Báo cáo tiểu luận được tổ chức thành 7 chương chuyên môn, phần kết luận và các phụ lục kỹ thuật:")
    
    headers = ["Chương", "Tên chương", "Nội dung trọng tâm & Bộ dữ liệu thực nghiệm", "Sản phẩm triển khai"]
    rows = [
        ["Chương 1", "Lịch sử phát triển của Trí tuệ Nhân tạo", "7 giai đoạn lịch sử (1950–2026), AI y tế và tài chính; Thực nghiệm 4 thế hệ mô hình trên bộ Pima Diabetes", "Bảng đối chiếu 4 thế hệ"],
        ["Chương 2", "Các kỹ thuật Học máy cơ bản", "Cơ sở toán học, 9 thuật toán kinh điển, 3 bộ dữ liệu (Diabetes, Housing, Customer); Cài đặt 3 cách (Scratch, Keras, PyTorch); Parity Check", "Web Demo Tabular ML"],
        ["Chương 3", "Mạng nơ-ron tích chập (CNN)", "Toán tích chập 2D, Pooling, BatchNorm, ResNet, Grad-CAM; Dữ liệu RetinaMNIST, MNIST, Fashion; Cài đặt 3 cách", "Web Demo CNN & Grad-CAM"],
        ["Chương 4", "Mạng nơ-ron hồi quy (RNN–LSTM)", "Dữ liệu chuỗi, BPTT, Toán cổng LSTM/GRU, Bẫy chuỗi; Dữ liệu CGM Shanghai, Cổ phiếu AAPL, Doanh thu bán lẻ; Cài đặt 3 cách", "Web Demo Time-Series Forecasting"],
        ["Chương 5", "Knowledge Graph và RAG", "Đồ thị tri thức, Hybrid RAG (BM25 + Dense + RRF), GraphRAG, Tri-framework Ragas; Dữ liệu Y tế & FinQA; ToolAgent", "Web Demo Q&A Grounded RAG"],
        ["Chương 6", "Học sâu trên đồ thị (Deep Graph)", "Dữ liệu phi Euclid, MPNN, Spectral GCN, GraphSAGE, GAT, Over-smoothing test, 1-WL; Dữ liệu Pubmed, Cora, Tương quan tài chính", "Web Demo GCN Graph Explorer"],
        ["Chương 7", "Hệ đa tác tử (Multi-Agent Systems)", "PEAS; Bài 1: MARL Mèo đuổi chuột Gridworld; Bài 2: Hội đồng Đa tác tử LLM, Consensus Gate, Guardrails; So sánh Single vs MAS", "Web Demo Multi-Agent Council"],
    ]
    add_table_data(doc, headers, rows, widths=[0.9, 1.8, 2.7, 1.4], caption="Bảng M.1. Tổng quan cấu trúc nội dung và các mốc thực nghiệm trong tiểu luận")
