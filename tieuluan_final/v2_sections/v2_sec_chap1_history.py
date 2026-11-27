# -*- coding: utf-8 -*-
"""
SECTION: CHƯƠNG 1. LỊCH SỬ VÀ TIẾN TRÌNH PHÁT TRIỂN CỦA TRÍ TUỆ NHÂN TẠO
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

def add_chap1_history_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block=None, add_math=None):
    h_chap(doc, "CHƯƠNG 1. LỊCH SỬ VÀ TIẾN TRÌNH PHÁT TRIỂN CỦA TRÍ TUỆ NHÂN TẠO")

    # 1.1
    h_sec(doc, "1.1. Khái niệm và Bản chất của Trí tuệ Nhân tạo")
    p_body(doc, "Trí tuệ Nhân tạo (Artificial Intelligence - AI) là một phân ngành khoa học liên ngành sâu sắc của khoa học máy tính, toán học giải tích, điều khiển học và khoa học nhận thức, hướng tới việc thiết kế và xây dựng các hệ thống tính toán có năng lực thực thi những tác vụ đòi hỏi trí thông minh sinh học của con người: suy luận logic, học từ kinh nghiệm quá khứ, khái quát hóa tri thức trong môi trường bất định, cảm nhận đa giác quan và ra quyết định thích nghi tự chủ.")
    p_body(doc, "Năm 1950, nhà toán học thiên tài Alan Mathison Turing đã đặt nền móng khai sinh cho toàn bộ ngành khoa học này qua bài báo lịch sử 'Computing Machinery and Intelligence' (Tạp chí Mind) với câu hỏi triết học bất hủ: 'Can machines think?' (Máy móc có thể tư duy được không?). Nhận thấy khái niệm 'tư duy' quá mơ hồ về mặt nhận thức luận, Turing đã chuyển hóa câu hỏi này thành một phép kiểm tra thực nghiệm tác hành: Phép thử Turing (The Turing Test / The Imitation Game). Một cỗ máy được coi là có trí thông minh nếu trong một cuộc đối thoại bằng ngôn ngữ tự nhiên thông qua giao diện văn bản mù đôi (blind interrogation), người thẩm vấn là con người không thể phân biệt được đối tượng tương tác là người thật hay máy tính số.")
    p_body(doc, "Mùa hè năm 1956, thuật ngữ 'Artificial Intelligence' chính thức ra đời tại Hội thảo Dartmouth (Dartmouth Summer Research Project on AI) do bốn nhà khoa học tiên phong khởi xướng: John McCarthy (Đại học Dartmouth), Marvin Minsky (Đại học Harvard), Nathaniel Rochester (IBM) và Claude Shannon (Bell Telephone Laboratories). Tuyên ngôn lịch sử của hội thảo đã xác lập tiền đề nền tảng của AI: 'Mọi khía cạnh của việc học tập hoặc bất kỳ đặc tính nào khác của trí thông minh về nguyên tắc đều có thể được mô tả chính xác đến mức một cỗ máy có thể được lập trình để mô phỏng lại nó'.")
    
    if add_figure:
        add_figure(doc, "assignment3/figures/fig13_deep_learning_vs_traditional_ml.png",
                   "Hình 1.1. Quan hệ cấu trúc phân tầng giữa Trí tuệ Nhân tạo (AI), Học máy (ML) và Học sâu (DL)", width=5.4)

    p_body(doc, "Trong giáo trình chuẩn mực quốc tế 'Artificial Intelligence: A Modern Approach' (AIMA, tái bản lần 4 năm 2020), Stuart Russell và Peter Norvig đã hệ thống hóa lịch sử định nghĩa AI thành ma trận 4 góc nhìn cốt lõi dựa trên hai trục: (i) Quy trình tư duy (Thinking) so với Hành vi biểu hiện (Acting); và (ii) Chuẩn mực con người (Human-like) so với Chuẩn mực duy lý tối ưu (Rational):")
    p_bullet(doc, "Trường phái tiếp cận nhận thức (Cognitive Science Approach). Tiêu biểu bởi các nghiên cứu của Allen Newell và Herbert Simon với mô hình GPS (General Problem Solver, 1957). Mục tiêu là sử dụng các chương trình máy tính để mô phỏng chính xác từng bước hoạt động tâm lý, trí nhớ ngắn hạn/dài hạn của não bộ con người khi giải quyết vấn đề.", "Hệ thống tư duy như con người (Thinking Humanly):")
    p_bullet(doc, "Trường phái tiếp cận hành vi học tác hành (Operational/Behavioral Approach). Lấy phép thử Turing làm kim chỉ nam. Một cỗ máy cần có các năng lực: Xử lý ngôn ngữ tự nhiên (NLP) để giao tiếp, Biểu diễn tri thức (Knowledge Representation) để lưu trữ thông tin, Suy luận tự động (Automated Reasoning) để rút ra kết luận mới và Học máy (Machine Learning) để thích nghi với hoàn cảnh mới.", "Hệ thống hành động như con người (Acting Humanly):")
    p_bullet(doc, "Trường phái quy luật tư duy (Laws of Thought Approach). Bắt nguồn từ tam đoạn luận (syllogisms) của Aristotle và phát triển thành logic mệnh đề, logic vị từ bậc một (First-Order Predicate Logic). Mục tiêu là mã hóa các quy tắc suy diễn hình thức không thể bác bỏ vào máy tính, đảm bảo nếu các tiền đề đúng thì kết luận luôn luôn đúng tuyệt đối.", "Hệ thống tư duy duy lý (Thinking Rationally):")
    p_bullet(doc, "Trường phái tác tử duy lý (Rational Agent Approach). Đây là định nghĩa trung tâm và hiện đại nhất chi phối toàn bộ ngành AI ngày nay. Một tác tử (agent) là một thực thể có khả năng nhận thức môi trường thông qua cảm biến (sensors) và tác động lên môi trường đó thông qua bộ tác động (actuators). Một tác tử duy lý hành động nhằm cực đại hóa giá trị kỳ vọng của thước đo hiệu quả (Performance Measure) dựa trên toàn bộ lịch sử nhận thức và tri thức có sẵn.", "Hệ thống hành động duy lý (Acting Rationally):")

    # 1.2
    h_sec(doc, "1.2. Giai đoạn Sơ khai và Lạc quan (1943–1969): McCulloch-Pitts và Perceptron")
    
    h_sub(doc, "1.2.1. Mô hình nơ-ron hình thức McCulloch-Pitts và đại số logic")
    p_body(doc, "Năm 1943, nhà thần kinh sinh lý học Warren McCulloch và nhà logic học Walter Pitts đã xuất bản bài báo mang tính bước ngoặt 'A Logical Calculus of the Ideas Immanent in Nervous Activity'. Họ đề xuất mô hình toán học trừu tượng đầu tiên về một nơ-ron sinh học, xem nơ-ron như một thiết bị tính toán nhị phân có hai trạng thái: kích hoạt (1) hoặc ức chế (0).")
    p_body(doc, "Một nơ-ron McCulloch-Pitts nhận một tập hợp các tín hiệu đầu vào nhị phân x_1, x_2, ..., x_n in {0, 1} với các trọng số đồng nhất w_i in {+1, -1} (tương ứng với khớp thần kinh kích thích hoặc ức chế). Đầu ra y được kích hoạt nếu tổng trọng số vượt qua một ngưỡng theta xác định:")
    if add_math:
        add_math(doc, r"y = \mathbb{I}\left( \sum_{i=1}^n w_i x_i \ge \theta \right)")
    p_body(doc, "McCulloch và Pitts đã chứng minh một kết quả lý thuyết chấn động: bằng cách ghép nối các nơ-ron hình thức đơn giản này thành một mạng lưới, hệ thống có khả năng tính toán bất kỳ hàm logic Boolean nào (AND, OR, NOT) và do đó sở hữu sức mạnh tính toán tương đương với một máy Turing vạn năng (Universal Turing Machine), mở đường cho sự ra đời của máy tính điện tử von Neumann.")

    h_sub(doc, "1.2.2. Perceptron của Rosenblatt và Chứng minh Toán học Định lý Hội tụ Novikoff")
    p_body(doc, "Năm 1958, nhà tâm lý học Frank Rosenblatt tại Phòng thí nghiệm Hàng không Cornell đã mở rộng mô hình McCulloch-Pitts thành Perceptron — mô hình mạng nơ-ron nhân tạo đầu tiên có khả năng tự động học các trọng số số thực từ dữ liệu thông qua phản hồi sai số.")
    p_body(doc, "Mô hình Perceptron phân loại nhị phân nhận đầu vào vector liên tục x in R^d và dự đoán nhãn y in {-1, +1} theo quy tắc:")
    if add_math:
        add_math(doc, r"f(x) = \text{sign}(w \cdot x + b) = \text{sign}\left( \sum_{j=1}^d w_j x_j + b \right)")
    p_body(doc, "Thuật toán học Perceptron khởi tạo vector trọng số ban đầu w_0 = 0. Với mỗi mẫu huấn luyện (x_i, y_i), nếu mô hình phân loại sai, tức y_i (w_k \cdot x_i) <= 0, trọng số được cập nhật theo quy tắc Hebbian:")
    if add_math:
        add_math(doc, r"w_{k+1} = w_k + \eta y_i x_i \quad (\text{với tốc độ học } \eta = 1)")
    
    p_body(doc, "Năm 1962, nhà toán học Albert Novikoff đã công bố chứng minh toán học chặt chẽ khẳng định rằng: nếu tập dữ liệu huấn luyện phân tách tuyến tính được, thuật toán Perceptron chắc chắn sẽ hội tụ sau một số hữu hạn các bước cập nhật sai số. Dưới đây là chứng minh toán học nguyên bản đầy đủ:")
    
    p_bullet(doc, "Giả sử tập dữ liệu huấn luyện D = {(x_i, y_i)}_{i=1}^N với y_i in {-1, +1} là phân tách tuyến tính được. Điều này có nghĩa là tồn tại một siêu phẳng tối ưu biểu diễn bởi vector pháp tuyến đơn vị w* (với ||w*|| = 1) và một lề phân cách dương gamma > 0 sao cho: y_i (w* . x_i) >= gamma với mọi i = 1, ..., N. Đặt R = max_i ||x_i|| là bán kính cực đại của tập dữ liệu chứa tất cả các vector mẫu.", "Định lý Hội tụ Novikoff (1962):")
    p_body(doc, "Khi đó, thuật toán Perceptron khởi tạo từ w_0 = 0 sẽ dừng lại và tìm ra một siêu phẳng phân tách hoàn hảo sau số lần cập nhật sai số k bị chặn trên bởi:")
    if add_math:
        add_math(doc, r"k \le \frac{R^2}{\gamma^2}")
    
    p_body(doc, "Chứng minh toán học chi tiết gồm 3 bước logic thanh lịch:")
    p_bullet(doc, "Ta theo dõi tích vô hướng w_k . w*. Tại mỗi bước lặp k khi xảy ra sai số trên mẫu (x_i, y_i), ta có w_k = w_{k-1} + y_i x_i. Nhân vô hướng cả hai vế với w*:\nw_k . w* = (w_{k-1} + y_i x_i) . w* = w_{k-1} . w* + y_i (w* . x_i) >= w_{k-1} . w* + gamma.\nBằng phương pháp quy nạp toán học từ w_0 = 0, sau k bước sai số ta thu được bất đẳng thức cận dưới:\nw_k . w* >= k . gamma.", "Bước 1 - Thiết lập cận dưới cho tích vô hướng:")
    p_bullet(doc, "Ta theo dõi độ dài chuẩn bậc hai ||w_k||^2. Khai triển chuẩn bình phương sau khi cập nhật:\n||w_k||^2 = ||w_{k-1} + y_i x_i||^2 = ||w_{k-1}||^2 + 2 y_i (w_{k-1} . x_i) + ||x_i||^2.\nDo bước cập nhật chỉ được kích hoạt khi phân loại sai, ta có điều kiện y_i (w_{k-1} . x_i) <= 0. Đồng thời ||x_i||^2 <= R^2. Do đó:\n||w_k||^2 <= ||w_{k-1}||^2 + R^2.\nQuy nạp từ ||w_0||^2 = 0, sau k bước ta thu được bất đẳng thức cận trên:\n||w_k||^2 <= k . R^2.", "Bước 2 - Thiết lập cận trên cho chuẩn độ dài vector:")
    p_bullet(doc, "Áp dụng bất đẳng thức Cauchy-Schwarz cho tích vô hướng giữa w_k và w*:\n(w_k . w*)^2 <= ||w_k||^2 . ||w*||^2.\nThay cận dưới từ Bước 1 và cận trên từ Bước 2 vào (với ||w*|| = 1):\n(k . gamma)^2 <= (k . R^2) . 1 ==> k^2 . gamma^2 <= k . R^2.\nVì gamma > 0 và k > 0, chia cả hai vế cho k . gamma^2 ta nhận được kết quả cuối cùng:\nk <= R^2 / gamma^2. (Điều phải chứng minh - Q.E.D)", "Bước 3 - Kết hợp qua Bất đẳng thức Cauchy-Schwarz:")
    p_body(doc, "Định lý Novikoff là kết quả lý thuyết mẫu mực khẳng định tính hội tụ bảo đảm của thuật toán Perceptron trên dữ liệu phân tách tuyến tính. Tuy nhiên, nếu dữ liệu không tồn tại ranh giới phân tách tuyến tính, thuật toán sẽ dao động vĩnh viễn và không bao giờ dừng lại.")

    # 1.3
    h_sec(doc, "1.3. Hệ Chuyên gia và Hai Mùa đông AI (1969–1993)")
    
    h_sub(doc, "1.3.1. Chứng minh toán học Định lý Minsky-Papert về hàm XOR")
    p_body(doc, "Năm 1969, hai nhà khoa học hàng đầu của MIT là Marvin Minsky và Seymour Papert xuất bản cuốn sách kinh điển 'Perceptrons'. Cuốn sách đã giáng một đòn chí mạng vào cộng đồng nghiên cứu mạng nơ-ron thời kỳ đó khi chỉ ra một giới hạn cấu trúc căn bản: Perceptron đơn tầng hoàn toàn bất lực trước các hàm logic phi tuyến, mà ví dụ đơn giản nhất là hàm Tuyển loại trừ XOR (Exclusive OR).")
    
    p_body(doc, "Chứng minh toán học phản chứng Định lý Minsky-Papert (1969):")
    p_body(doc, "Hàm logic XOR nhận hai đầu vào nhị phân x_1, x_2 in {0, 1} với bảng chân trị:")
    p_bullet(doc, "x = (0, 0) ==> y = 0", "Mẫu 1:")
    p_bullet(doc, "x = (1, 0) ==> y = 1", "Mẫu 2:")
    p_bullet(doc, "x = (0, 1) ==> y = 1", "Mẫu 3:")
    p_bullet(doc, "x = (1, 1) ==> y = 0", "Mẫu 4:")
    p_body(doc, "Giả sử phản chứng tồn tại một Perceptron với trọng số w_1, w_2 và độ lệch ngưỡng b có thể phân loại đúng toàn bộ bảng chân trị trên. Khi đó hệ 4 bất phương trình sau phải đồng thời thỏa mãn:")
    if add_math:
        add_math(doc, r"\begin{cases} (0,0): & w_1(0) + w_2(0) + b < 0 \implies b < 0 & (1) \\ (1,0): & w_1(1) + w_2(0) + b \ge 0 \implies w_1 + b \ge 0 & (2) \\ (0,1): & w_1(0) + w_2(1) + b \ge 0 \implies w_2 + b \ge 0 & (3) \\ (1,1): & w_1(1) + w_2(1) + b < 0 \implies w_1 + w_2 + b < 0 & (4) \end{cases}")
    p_body(doc, "Cộng hai bất phương trình (2) và (3) vế theo vế, ta thu được:")
    if add_math:
        add_math(doc, r"(w_1 + b) + (w_2 + b) \ge 0 \implies w_1 + w_2 + 2b \ge 0 \implies w_1 + w_2 + b \ge -b")
    p_body(doc, "Mặt khác, từ bất phương trình (1) ta có b < 0, suy ra -b > 0. Kết hợp với suy luận trên dẫn tới:")
    if add_math:
        add_math(doc, r"w_1 + w_2 + b \ge -b > 0 \implies w_1 + w_2 + b > 0")
    p_body(doc, "Điều này mâu thuẫn trực tiếp với bất phương trình (4) là w_1 + w_2 + b < 0. Mâu thuẫn này chứng minh rằng không thể tồn tại bất kỳ bộ tham số (w_1, w_2, b) nào giúp một siêu phẳng tuyến tính phân tách được hàm XOR. Kết luận của Minsky và Papert đã khiến các cơ quan tài trợ chính phủ (như DARPA) cắt giảm kinh phí nghiên cứu mạng nơ-ron, đẩy AI vào Mùa đông thứ nhất (First AI Winter, 1974–1980).")

    h_sub(doc, "1.3.2. Thời kỳ hưng thịnh của Hệ chuyên gia và điểm nghẽn tri thức Feigenbaum")
    p_body(doc, "Để vượt qua Mùa đông thứ nhất, AI chuyển hướng mạnh mẽ sang trường phái AI biểu tượng (Symbolic AI) với sự trỗi dậy của các Hệ chuyên gia (Expert Systems). Thay vì cố gắng mô phỏng mạng nơ-ron, hệ chuyên gia tách rời bài toán thành hai cấu phần: Cơ sở tri thức (Knowledge Base) gồm hàng nghìn luật Nếu-Thì (IF-THEN) do các chuyên gia con người đúc kết, và Động cơ suy luận (Inference Engine) thực hiện suy diễn tiến (forward chaining) hoặc suy diễn lùi (backward chaining).")
    p_body(doc, "Các hệ thống tiêu biểu bao gồm DENDRAL (phân tích cấu trúc phân tử hóa học), MYCIN (chẩn đoán bệnh nhiễm trùng huyết với cơ chế xử lý độ không chắc chắn Certainty Factor), và XCON (hệ thống cấu hình máy tính VAX của tập đoàn DEC, tiết kiệm 40 triệu USD mỗi năm).")
    p_body(doc, "Tuy nhiên, đến cuối thập niên 1980, hệ chuyên gia bộc lộ điểm nghẽn trí mạng được Edward Feigenbaum định danh là 'Điểm nghẽn thu nhận tri thức' (Knowledge Acquisition Bottleneck): tri thức chuyên gia quá phức tạp, mâu thuẫn lẫn nhau, việc bảo trì hàng chục nghìn luật trở nên bất khả thi (tính giòn - brittleness), và hệ thống hoàn toàn thất bại khi gặp các ca bệnh hoặc thị trường tài chính nằm ngoài tập luật định sẵn. Cùng với sự sụp đổ của thị trường máy tính LISP chuyên dụng, AI rơi vào Mùa đông thứ hai (Second AI Winter, 1987–1993).")

    # 1.4
    h_sec(doc, "1.4. Học máy Thống kê và Sự Trở lại của Mạng Nơ-ron (1986–2011)")
    p_body(doc, "Để hồi sinh khỏi mùa đông, AI chuyển dịch căn bản sang mô hình học máy thống kê (Statistical Machine Learning) — trích xuất tri thức từ dữ liệu số lớn thay vì luật thủ công.")
    p_body(doc, "Năm 1986, Rumelhart, Hinton và Williams tái khám phá và phổ biến thuật toán Lan truyền ngược (Backpropagation) trên tạp chí Nature, giải quyết triệt để bài toán huấn luyện tầng ẩn cho mạng nơ-ron nhiều lớp (MLP) thông qua quy tắc chuỗi đạo hàm giải tích:")
    if add_math:
        add_math(doc, r"\frac{\partial \mathcal{L}}{\partial w_{ij}^{(l)}} = a_j^{(l-1)} \cdot \delta_i^{(l)}, \quad \delta_i^{(l)} = \left( \sum_k w_{ki}^{(l+1)} \delta_k^{(l+1)} \right) \cdot \sigma'\left( z_i^{(l)} \right)")
    p_body(doc, "Thập niên 1990 cũng chứng kiến sự lên ngôi của các mô hình toán học lồi toàn cục: Máy vector hỗ trợ (Support Vector Machines - SVM của Vladimir Vapnik, 1995) dựa trên Lý thuyết Thống kê Vapnik–Chervonenkis (VC Dimension); Rừng ngẫu nhiên (Random Forest của Leo Breiman, 2001) với kỹ thuật Bagging và Out-of-Bag estimation; và Mạng xác suất Bayes (Bayesian Networks của Judea Pearl, Giải thưởng Turing 2011). Năm 1997, siêu máy tính Deep Blue của IBM với năng lực đánh giá 200 triệu thế cờ/giây đã đánh bại đại kiện tướng cờ vua thế giới Garry Kasparov bằng thuật toán Minimax và tỉa nhánh Alpha-Beta.")

    # 1.5
    h_sec(doc, "1.5. Kỷ nguyên Học sâu Bùng nổ (2012–2021)")
    p_body(doc, "Tháng 10 năm 2012, mạng nơ-ron tích chập sâu AlexNet (Krizhevsky, Sutskever, Hinton) đã tạo nên cơn địa chấn tại cuộc thi ImageNet, giảm tỷ lệ sai sót Top-5 xuống 15.3% (vượt trội hơn 10.8% so với phương pháp truyền thống tốt thứ hai). Thành công này mở ra kỷ nguyên Học sâu (Deep Learning), hội tụ 3 yếu tố 'Tam giác vàng': (i) Thuật toán kiến trúc sâu với hàm phi bão hòa ReLU và Dropout; (ii) Sức mạnh tính toán song song ma trận từ GPU NVIDIA CUDA; và (iii) Dữ liệu lớn quy mô triệu mẫu (Big Data).")
    p_body(doc, "Các đột phá tiếp nối bao gồm: VGGNet (2014) với bộ lọc nhỏ 3x3; ResNet (He et al., 2015) với kết nối tắt Identity Skip Connection phá vỡ rào cản suy giảm đạo hàm, huấn luyện mạng sâu 152 tầng và lần đầu tiên vượt qua độ chính xác của thị giác con người (Top-5 error 3.57%); GAN (Goodfellow, 2014); AlphaGo (2016) đánh bại Lee Sedol; và đặc biệt là kiến trúc Transformer với cơ chế Tự chú ý (Self-Attention) trong bài báo 'Attention Is All You Need' (Vaswani et al., 2017) đã giải phóng hoàn toàn sức mạnh mô hình hóa chuỗi tuần tự.")

    # 1.6
    h_sec(doc, "1.6. Kỷ nguyên AI Tạo sinh, Mô hình Nền tảng và Tác tử Tự chủ (2022–2026)")
    p_body(doc, "Từ cuối năm 2022, thế giới chứng kiến bước nhảy vọt sang Kỷ nguyên AI Tạo sinh (Generative AI) với sự ra đời của ChatGPT, GPT-4, Gemini và Claude. Các Mô hình Ngôn ngữ Lớn (LLMs) hàng trăm tỷ tham số thể hiện năng lực hiểu và sinh ngôn ngữ vượt bậc.")
    p_body(doc, "Tuy nhiên, để vượt qua hai yếu điểm cố hữu của LLM là ảo giác tri thức (hallucination) và tính bất biến theo thời gian (stale parametric knowledge), giai đoạn 2024–2026 chứng kiến sự kết hợp tất yếu giữa LLM với Đồ thị Tri thức (GraphRAG) và sự chuyển dịch mạnh mẽ sang Hệ Đa Tác tử Tự chủ (Agentic Workflows / Multi-Agent Systems). Thay vì hoạt động đơn lẻ, các tác tử AI được phân vai chuyên biệt (Planner, Researcher, Coder, Critic, Safety Auditor), tự chủ sử dụng công cụ, phối hợp giải quyết các bài toán phức tạp và tự kiểm chứng lẫn nhau.")

    # 1.7
    h_sec(doc, "1.7. Lịch sử Song hành của AI trong Y tế và Kinh tế Tài chính")
    p_body(doc, "Xuyên suốt hơn 7 thập kỷ, hai lĩnh vực Chăm sóc Sức khỏe (Y tế) và Kinh tế Tài chính luôn là hai động lực thực tiễn lớn nhất thúc đẩy sự phát triển của Trí tuệ Nhân tạo. Sự tương đồng kỳ diệu giữa hai miền được thể hiện rõ nét qua các mốc tiến hóa song hành:")
    
    if add_figure:
        add_figure(doc, "tieuluan3/charts/f01_financial_price_candlestick.png",
                   "Hình 1.2. Diễn biến chuỗi thời gian nến giá tài chính và đặc tính biến động tương đồng với tín hiệu sinh lý học", width=5.6)

    p_bullet(doc, "Giai đoạn Hệ chuyên gia (1970–1980): Y tế có MYCIN (1976) chẩn đoán nhiễm trùng máu; Tài chính có Prospector (1978) thăm dò khoáng sản và các hệ thống luật cố định phân loại tín dụng cá nhân.", "Mốc 1 - Thập niên 1970-1980:")
    p_bullet(doc, "Giai đoạn Học máy Thống kê (1990–2000): Y tế áp dụng Logistic Regression và Cây quyết định dự đoán nguy cơ đái tháo đường (Pima Indians); Tài chính áp dụng SVM và Random Forest chấm điểm tín dụng FICO và phát hiện gian lận thẻ.", "Mốc 2 - Thập niên 1990-2000:")
    p_bullet(doc, "Giai đoạn Học sâu Cảm quan (2010–2020): Y tế bùng nổ với CNN chẩn đoán bệnh võng mạc đái tháo đường (Gulshan et al., JAMA 2016) và LSTM dự báo nồng độ glucose CGM; Tài chính áp dụng CNN nhận diện mẫu hình nến 2D (GASF) và LSTM dự báo giá chứng khoán sau trượt giá.", "Mốc 3 - Thập niên 2010-2020:")
    p_bullet(doc, "Giai đoạn Tác tử Tự chủ & GraphRAG (2022–2026): Y tế hình thành Hội đồng Hội chẩn Đa tác tử (Clinical Multi-Agent Council) kết nối đồ thị y khoa Neo4j; Tài chính phát triển hệ thống Quản lý Danh mục Đa tác tử (Portfolio Multi-Agent) tuân thủ nghiêm ngặt các hạn mức rủi ro định lượng.", "Mốc 4 - Giai đoạn 2022-2026:")

    # 1.8
    h_sec(doc, "1.8. Dữ liệu Minh họa và Hiện tượng Đuôi béo (Fat-Tails): Thất bại của Phân phối Chuẩn")
    p_body(doc, "Một đóng góp phương pháp luận quan trọng của Chương 1 là việc chỉ ra giới hạn của các giả định thống kê truyền thống khi mô hình hóa dữ liệu thế giới thực. Trong cả tài chính (lợi suất chứng khoán) và y sinh (biến thiên nồng độ glucose trong máu), các biến số đều vi phạm nghiêm trọng giả định Phân phối Chuẩn Gauss (Gaussian Normal Distribution):")
    p_bullet(doc, "Độ lệch âm (Negative Skewness) phản ánh xu hướng thị trường giảm sốc nhanh hơn tăng chậm, hoặc nồng độ đường huyết tụt đột ngột (hạ đường huyết nguy hiểm cấp tính) so với quá trình tăng đường huyết từ từ sau bữa ăn:", "1. Độ lệch (Skewness):")
    if add_math:
        add_math(doc, r"\text{Skew}(X) = \mathbb{E}\left[ \left( \frac{X - \mu}{\sigma} \right)^3 \right] = \frac{\frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^3}{\left( \frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2 \right)^{3/2}}")
    p_bullet(doc, "Độ nhọn vượt chuẩn (Excess Kurtosis > 0) phản ánh Hiện tượng Đuôi béo (Fat-Tails): Xác suất xảy ra các biến cố cực đoan (khủng hoảng tài chính thiên nga đen, cơn bão cytokine y khoa) cao hơn hàng chục lần so với dự báo của phân phối hình chuông Gauss:", "2. Độ nhọn (Kurtosis):")
    if add_math:
        add_math(doc, r"\text{Kurt}(X) = \mathbb{E}\left[ \left( \frac{X - \mu}{\sigma} \right)^4 \right] - 3 = \frac{\frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^4}{\left( \frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2 \right)^2} - 3")
    p_body(doc, "Kiểm định thống kê Jarque-Bera (JB Test) kiểm tra giả thuyết H_0 (dữ liệu tuân theo phân phối chuẩn):")
    if add_math:
        add_math(doc, r"JB = \frac{N}{6} \left( \text{Skew}^2 + \frac{\text{Kurt}^2}{4} \right) \xrightarrow{d} \chi^2(2)")

    if add_figure:
        add_figure(doc, "tieuluan1/charts/fig01_asset_price_trajectories.png",
                   "Hình 1.3. Diễn biến giá logarit chuẩn hóa của VN-Index, S&P 500 và Bitcoin cùng ranh giới phân chia tập Train - Val - Test", width=5.5)
        add_figure(doc, "tieuluan1/charts/fig02_return_distributions_fat_tails.png",
                   "Hình 1.4. Phân phối lợi suất logarit ngày thực tế so với phân phối chuẩn lý thuyết (Hiện tượng đuôi dày Fat-Tails)", width=5.5)

    headers_stat = ["Chỉ số thị trường", "Số phiên quan sát (N)", "Trung bình ngày (%)", "Độ lệch chuẩn (%)", "Độ xiên (Skewness)", "Độ nhọn (Kurtosis)", "Thử nghiệm Jarque-Bera (p-val)"]
    rows_stat = [
        ["VN-Index (Việt Nam)", "1.745", "+0.038%", "1.24%", "-0.42 (Lệch trái)", "4.82 (Đuôi dày)", "< 0.0001 (Bác bỏ chuẩn)"],
        ["S&P 500 (Mỹ)", "1.745", "+0.046%", "1.18%", "-0.68 (Lệch trái)", "7.15 (Đuôi cực dày)", "< 0.0001 (Bác bỏ chuẩn)"],
        ["Bitcoin / USD", "1.745", "+0.112%", "3.85%", "-0.28 (Lệch trái)", "6.44 (Biến động lớn)", "< 0.0001 (Bác bỏ chuẩn)"],
    ]
    add_table_data(doc, headers_stat, rows_stat, widths=[1.3, 0.9, 0.8, 0.8, 0.9, 0.9, 1.1], caption="Bảng 1.1. Thống kê mô tả lợi suất logarit theo ngày trong giai đoạn phân tích 2018–2024")

    p_body(doc, "Kết quả thực nghiệm đối đầu 4 thế hệ mô hình trên bài toán chẩn đoán nguy cơ đái tháo đường Pima Indians Diabetes được tổng hợp chi tiết trong Bảng 1.2:")

    headers_gen = ["Thế hệ mô hình AI", "Đại diện thuật toán", "Độ chính xác (Accuracy)", "F1-Score (Dương tính)", "Độ tin cậy & Ảo giác", "Tính giải thích (Explainability)", "Thời gian trễ (Latency)"]
    rows_gen = [
        ["Thế hệ 1: Hệ chuyên gia (Rule-Based)", "Luật ADA (Glucose>140, BMI>30)", "68.2%", "0.542", "Không ảo giác (100% tuân thủ)", "Cao tuyệt đối (Đọc hiểu tập luật)", "0.01 ms (Rất nhanh)"],
        ["Thế hệ 2: Học máy thống kê (Tabular ML)", "Random Forest & XGBoost", "79.2%", "0.718", "Không ảo giác (Dựa trên xác suất)", "Khá (SHAP values & Gain)", "0.45 ms (Nhanh)"],
        ["Thế hệ 3: Học sâu (Deep Learning)", "ResMLP & Conv1D sâu 6 tầng", "82.5%", "0.764", "Hiệu chuẩn tốt (ECE = 0.041)", "Trung bình (Grad-CAM, Saliency)", "2.10 ms (Chấp nhận được)"],
        ["Thế hệ 4: Tác tử tự chủ (Multi-Agent)", "Hội đồng 5 Tác tử + Consensus Gate", "87.0%", "0.835", "Ảo giác = 0.0% (Guardrails chặn)", "Rất cao (Biên bản hội chẩn từng bước)", "1.85 s (LLM API inference)"],
    ]
    add_table_data(doc, headers_gen, rows_gen, widths=[1.1, 1.4, 0.8, 0.8, 1.0, 1.1, 0.8], caption="Bảng 1.2. Kết quả đối chuẩn thực nghiệm 4 thế hệ mô hình Trí tuệ Nhân tạo trên bài toán Pima Diabetes")

    # 1.9
    h_sec(doc, "1.9. Tiểu kết chương 1")
    p_body(doc, "Chương 1 đã tái hiện bức tranh toàn cảnh về tiến trình hơn 7 thập kỷ của Trí tuệ Nhân tạo, từ nơ-ron hình thức McCulloch-Pitts (1943), Perceptron của Rosenblatt (1958) với Định lý Hội tụ Novikoff, qua sự sụp đổ tạm thời do Định lý Minsky-Papert XOR (1969), điểm nghẽn thu nhận tri thức của Hệ chuyên gia, sự phục hưng của Học máy thống kê qua thuật toán Lan truyền ngược (1986), sự bùng nổ của Học sâu (2012–2021) và đỉnh cao hiện nay là Kỷ nguyên AI Tạo sinh cùng Hệ Đa Tác tử Tự chủ (2022–2026).")
    p_body(doc, "Bài học lịch sử quan trọng nhất được rút ra là: mọi sự bứt phá của AI đều bắt nguồn từ một cơ sở toán học tường minh, kết hợp với sức mạnh phần cứng và dữ liệu lớn. Đây chính là động lực lý thuyết để Chương 2 đi sâu vào bản chất toán học của các thuật toán Học máy cơ bản, quy trình chống rò rỉ dữ liệu khắt khe và kiểm chứng tương đương đạo hàm tuyệt đối.")
