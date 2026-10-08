#!/usr/bin/env python3
"""Build the course term paper from the verified assignment artifacts."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "tieuluan01CT09_TranVanHau.docx"
FIG4 = ROOT / "assignment4" / "report" / "screenshots"
FIG6 = ROOT / "assignment6" / "figures"
LOGO = ROOT / "assignment3" / "report" / "ptit_logo.png"

NAVY = RGBColor(30, 58, 138)
BLUE = RGBColor(37, 99, 235)
TEXT = RGBColor(30, 41, 59)
MUTED = RGBColor(100, 116, 139)


def shade(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def set_cell(cell, text, bold=False, color=TEXT, size=9.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell(t.rows[0].cells[i], h, True, RGBColor(255, 255, 255), 9)
        shade(t.rows[0].cells[i], "1E3A8A")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, value in enumerate(row):
            set_cell(cells[i], value, False, TEXT, 8.8)
            if ri % 2:
                shade(cells[i], "F1F5F9")
    if widths:
        for row in t.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def p(doc, text, bold=False, italic=False):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.first_line_indent = Inches(0.3)
    para.paragraph_format.line_spacing = 1.15
    para.paragraph_format.space_after = Pt(5)
    run = para.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = TEXT
    run.font.bold = bold
    run.font.italic = italic
    return para


def bullet(doc, text):
    para = doc.add_paragraph(style="List Bullet")
    para.paragraph_format.line_spacing = 1.1
    para.paragraph_format.space_after = Pt(3)
    run = para.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = TEXT


def heading(doc, text, level=1):
    h = doc.add_heading(text, level)
    for run in h.runs:
        run.font.name = "Times New Roman"
        run.font.color.rgb = NAVY if level == 1 else BLUE
        run.font.size = Pt(15 if level == 1 else 12.5)
    return h


def page_title(doc, text):
    doc.add_page_break()
    heading(doc, text, 1)


def figure(doc, path, caption, width=5.9):
    if not path.exists():
        return
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(str(path), width=Inches(width))
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(6)
    for run in cap.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = MUTED


def code(doc, text):
    para = doc.add_paragraph()
    para.paragraph_format.left_indent = Inches(0.25)
    para.paragraph_format.right_indent = Inches(0.25)
    para.paragraph_format.space_after = Pt(6)
    for line in text.strip("\n").splitlines():
        run = para.add_run(line + "\n")
        run.font.name = "Consolas"
        run.font.size = Pt(8.2)
        run.font.color.rgb = RGBColor(15, 23, 42)


def field(paragraph, instruction):
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), instruction)
    run._r.append(fld)


def configure(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
    sec.top_margin = sec.bottom_margin = Inches(0.8)
    sec.left_margin, sec.right_margin = Inches(1.0), Inches(0.8)
    styles = doc.styles
    styles["Normal"].font.name = "Times New Roman"
    styles["Normal"].font.size = Pt(11)
    for name in ("Heading 1", "Heading 2", "Heading 3"):
        styles[name].font.name = "Times New Roman"
    for section in doc.sections:
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.add_run("Tiểu luận môn học - Trần Văn Hậu - B23DCCN287 | Trang ")
        field(footer, "PAGE")


def cover(doc):
    if LOGO.exists():
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.add_run().add_picture(str(LOGO), width=Inches(1.25))
    for text, size, bold in [
        ("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", 15, True),
        ("KHOA CÔNG NGHỆ THÔNG TIN", 13, True),
        ("", 12, False),
        ("TIỂU LUẬN MÔN HỌC", 19, True),
        ("LỊCH SỬ AI, MACHINE LEARNING, CNN VÀ RNN", 15, True),
        ("", 12, False),
        ("Từ biểu diễn dữ liệu đến mô hình học sâu triển khai được", 12, False),
    ]:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(9)
        run = para.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = NAVY
    table(doc, ["Thông tin", "Chi tiết"], [
        ("Sinh viên", "Trần Văn Hậu"),
        ("Mã sinh viên", "B23DCCN287"),
        ("Nhóm lớp", "CT"),
        ("Nhóm tiểu luận", "09"),
        ("Giảng viên", "PGS. TS. Trần Đình Quế"),
        ("Thời gian", "Tháng 10/2026"),
    ], [1.8, 3.6])
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(55)
    run = para.add_run("Hà Nội - 2026")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    doc.add_page_break()


def build():
    doc = Document()
    configure(doc)
    cover(doc)

    heading(doc, "MỤC LỤC", 1)
    toc = doc.add_paragraph()
    field(toc, 'TOC \\o "1-3" \\h \\z \\u')
    p(doc, "Mục lục được cập nhật trong Microsoft Word bằng thao tác Update Field sau khi mở báo cáo.", italic=True)

    page_title(doc, "MỞ ĐẦU")
    p(doc, "Trí tuệ nhân tạo (Artificial Intelligence - AI) đã chuyển từ một hướng nghiên cứu hàn lâm thành nền tảng của nhiều hệ thống thực tế như chẩn đoán hỗ trợ, tìm kiếm, nhận dạng ảnh, dự báo và trợ lý thông minh. Sự phát triển này đến từ khả năng biểu diễn dữ liệu bằng vector, học tham số từ dữ liệu và triển khai mô hình thành dịch vụ có thể sử dụng.")
    p(doc, "Tiểu luận này tổng hợp tiến trình từ lịch sử AI đến các kỹ thuật Machine Learning cơ bản, sau đó đi sâu vào CNN và RNN. Phần thực nghiệm tận dụng các dataset và chương trình đã được xây dựng trong những assignment trước, giúp báo cáo có dữ liệu thật, kết quả đo được và quy trình tái lập.")
    heading(doc, "1. Mục tiêu", 2)
    bullet(doc, "Hệ thống hóa các mốc lịch sử và khái niệm nền tảng của AI, ML và Deep Learning.")
    bullet(doc, "Mô tả dữ liệu, phân bố, tiền xử lý và cách đánh giá trên nhiều miền dữ liệu.")
    bullet(doc, "Cài đặt các mô hình theo ba cách: scratch, Keras/TensorFlow và PyTorch.")
    bullet(doc, "So sánh kết quả, phân tích giới hạn và trình bày phương án deploy.")
    heading(doc, "2. Phạm vi và phương pháp", 2)
    p(doc, "Chương 2 dùng dữ liệu bảng, văn bản và hồi quy; Chương 3 dùng ảnh MNIST và Dogs vs Cats; Chương 4 dùng chuỗi thời gian cổ phiếu AAPL và giao dịch bán lẻ. Các kết quả được trích từ artifact trong assignment3, assignment4 và assignment6; các con số được ghi rõ là kết quả của cấu hình và lần chạy tương ứng, không khẳng định mô hình nào luôn tốt nhất.")
    heading(doc, "3. Bố cục", 2)
    p(doc, "Chương 1 trình bày lịch sử AI. Chương 2 giới thiệu ML cơ bản và thí nghiệm dữ liệu bảng. Chương 3 trình bày CNN, các phép toán tích chập và thực nghiệm ảnh. Chương 4 trình bày RNN/LSTM, dự báo chuỗi thời gian và triển khai web.")

    page_title(doc, "CHƯƠNG 1. LỊCH SỬ PHÁT TRIỂN AI")
    p(doc, "Lịch sử AI không phát triển theo một đường thẳng. Các giai đoạn luân phiên giữa kỳ vọng cao, giới hạn tính toán và những đột phá về dữ liệu, thuật toán. Việc nhìn lại lịch sử giúp lựa chọn mô hình phù hợp thay vì xem Deep Learning là lời giải cho mọi bài toán.")
    heading(doc, "1.1. Giai đoạn hình thành", 2)
    p(doc, "Ý tưởng về máy có khả năng suy luận xuất hiện cùng sự phát triển của logic hình thức, xác suất và máy tính điện tử. Năm 1950, Alan Turing đề xuất câu hỏi liệu máy có thể biểu hiện hành vi thông minh và đưa ra phép thử đối thoại. Năm 1956, hội thảo Dartmouth phổ biến thuật ngữ Artificial Intelligence, đặt nền móng cho một lĩnh vực nghiên cứu độc lập.")
    heading(doc, "1.2. AI biểu tượng và hệ chuyên gia", 2)
    p(doc, "Trong giai đoạn đầu, các nhà nghiên cứu biểu diễn tri thức bằng luật IF-THEN, logic vị từ, cây tìm kiếm và hệ suy diễn. Hệ chuyên gia có thể đạt kết quả tốt trong miền hẹp khi tri thức được viết thủ công. Nhược điểm là chi phí thu nhận tri thức lớn, khó thích nghi và khó xử lý dữ liệu nhiễu.")
    heading(doc, "1.3. Machine Learning và xác suất", 2)
    p(doc, "Machine Learning chuyển trọng tâm từ viết luật sang học quy luật từ ví dụ. Các phương pháp như hồi quy tuyến tính, logistic regression, cây quyết định, SVM và ensemble cung cấp các mô hình mạnh trên dữ liệu bảng. Tiền xử lý, chọn đặc trưng và thiết kế phép đánh giá trở thành phần quan trọng không kém thuật toán.")
    heading(doc, "1.4. Deep Learning và kỷ nguyên dữ liệu lớn", 2)
    p(doc, "Mạng nơ-ron nhiều tầng có thể tự học biểu diễn phân cấp. GPU, dữ liệu lớn, các hàm kích hoạt tốt hơn, khởi tạo và tối ưu hiện đại đã giúp CNN đạt kết quả cao trên ảnh; RNN/LSTM xử lý chuỗi; Transformer mở rộng khả năng mô hình hóa ngôn ngữ và đa phương thức.")
    heading(doc, "1.5. AI tạo sinh và hệ thống hiện đại", 2)
    p(doc, "Các mô hình nền tảng, mô hình ngôn ngữ lớn, RAG và hệ đa Agent đang mở rộng AI từ dự đoán sang sinh nội dung và phối hợp công cụ. Tuy nhiên, hệ thống hiện đại vẫn cần kiểm soát dữ liệu, đánh giá hallucination, bảo vệ thông tin và giám sát khi triển khai.")
    table(doc, ["Giai đoạn", "Đặc trưng", "Giới hạn chính"], [
        ("1950-1960", "Logic, tìm kiếm, AI biểu tượng", "Không linh hoạt với dữ liệu thực"),
        ("1970-1980", "Hệ chuyên gia, luật suy diễn", "Nút thắt thu nhận tri thức"),
        ("1990-2000", "ML thống kê, SVM, cây", "Phụ thuộc thiết kế đặc trưng"),
        ("2010-2019", "Deep Learning, GPU, dữ liệu lớn", "Cần dữ liệu/tài nguyên, khó giải thích"),
        ("2020-nay", "Transformer, RAG, Agent, AI tạo sinh", "An toàn, chi phí, độ tin cậy"),
    ])

    page_title(doc, "CHƯƠNG 2. CÁC KỸ THUẬT MACHINE LEARNING CƠ BẢN")
    p(doc, "Machine Learning học một hàm fθ từ dữ liệu. Với dữ liệu huấn luyện {(xi, yi)}, mục tiêu thường là cực tiểu hóa rủi ro thực nghiệm: J(θ)=1/N Σ L(fθ(xi), yi)+λΩ(θ). Thành phần mất mát đo sai số; regularization hạn chế mô hình quá phức tạp.")
    heading(doc, "2.1. Phân loại, hồi quy và quy trình chuẩn", 2)
    p(doc, "Phân loại dự đoán nhãn rời rạc; hồi quy dự đoán giá trị liên tục. Một pipeline đáng tin cậy gồm khám phá dữ liệu, làm sạch, chia train/validation/test, fit biến đổi trên train, huấn luyện, đánh giá trên test và đóng gói tiền xử lý cùng model.")
    heading(doc, "2.2. Các mô hình cơ bản", 2)
    bullet(doc, "Logistic Regression: xác suất lớp qua sigmoid, phù hợp baseline tuyến tính.")
    bullet(doc, "Decision Tree: chia không gian theo điều kiện, dễ giải thích nhưng dễ overfit.")
    bullet(doc, "Random Forest: trung bình nhiều cây ngẫu nhiên, thường mạnh trên dữ liệu bảng.")
    bullet(doc, "Ridge Regression: hồi quy tuyến tính có L2 regularization.")
    bullet(doc, "Naive Bayes: giả định độc lập có điều kiện, hiệu quả và nhanh cho văn bản.")
    heading(doc, "2.3. Ba cách cài đặt", 2)
    p(doc, "Bản scratch dùng NumPy để minh họa forward, loss và gradient descent. Keras/TensorFlow cung cấp API huấn luyện và callback. PyTorch cho phép định nghĩa Module, vòng lặp tối ưu và kiểm soát tensor chi tiết. Ba cách giúp phân biệt bản chất toán học với tiện ích framework.")
    code(doc, """
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))

for epoch in range(epochs):
    prob = sigmoid(X_train @ w + b)
    grad_w = X_train.T @ (prob - y_train) / len(y_train)
    grad_b = np.mean(prob - y_train)
    w -= learning_rate * grad_w
    b -= learning_rate * grad_b
""")
    heading(doc, "2.4. Dataset 1: Diabetes Prediction", 2)
    p(doc, "Nguồn cục bộ: assignment3/diabetes/data/diabetes_prediction_dataset.csv. Dataset có các trường gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level và diabetes. Đây là phân loại nhị phân, có mất cân bằng lớp nên Accuracy phải đi kèm Precision, Recall, F1 và ROC-AUC.")
    table(doc, ["Thuộc tính", "Vai trò", "Xử lý"], [
        ("age, bmi", "Đặc trưng số", "StandardScaler"),
        ("HbA1c_level, blood_glucose_level", "Chỉ dấu chuyển hóa", "StandardScaler"),
        ("gender, smoking_history", "Đặc trưng phân loại", "One-hot/encoding"),
        ("hypertension, heart_disease", "Bệnh nền nhị phân", "Giữ dạng số"),
        ("diabetes", "Nhãn 0/1", "Stratified split"),
    ])
    p(doc, "Kết quả test trong assignment3: Logistic Regression đạt Accuracy 0.8846, F1 0.5716, AUC 0.9591; Decision Tree đạt Accuracy 0.8988, F1 0.6041, AUC 0.9712; Random Forest đạt Accuracy 0.9191, F1 0.6515, AUC 0.9740. Random Forest tốt nhất trong ba baseline trên cấu hình này.")
    heading(doc, "2.5. Dataset 2: Vietnam Housing", 2)
    p(doc, "File assignment3/house_price/data/VN_housing_dataset.csv chứa thông tin ngày đăng, địa chỉ, quận/huyện, loại hình, giấy tờ pháp lý, số tầng, số phòng ngủ, diện tích và giá/m². Bài toán là hồi quy; giá có ngoại lệ lớn nên MAE, RMSE và R² cần được đọc cùng nhau.")
    heading(doc, "2.6. Dataset 3: Women’s Clothing Reviews", 2)
    p(doc, "File assignment3/customer_behavior/data/Womens Clothing E-Commerce Reviews.csv chứa văn bản đánh giá, rating, Recommended IND, nhóm sản phẩm và phản hồi tích cực. Văn bản được biểu diễn bằng TF-IDF. Cần tránh để review trùng hoặc thông tin nhãn lọt vào feature.")
    table(doc, ["Mô hình", "Diabetes F1", "Diabetes AUC", "Nhận xét"], [
        ("Logistic Regression", "0.5716", "0.9591", "Baseline tuyến tính"),
        ("Decision Tree", "0.6041", "0.9712", "Dễ diễn giải"),
        ("Random Forest", "0.6515", "0.9740", "Tốt nhất trong bảng"),
    ])
    heading(doc, "2.7. Nhận xét và triển khai", 2)
    p(doc, "Các model cần được lưu cùng scaler, encoder và thứ tự feature. API nên kiểm tra kiểu dữ liệu, trường bắt buộc và giới hạn hợp lệ; không được fit lại preprocessing trên dữ liệu request. Những nguyên tắc này đã được áp dụng trong các web demo của assignment3.")

    page_title(doc, "CHƯƠNG 3. MẠNG NƠ-RON TÍCH CHẬP CNN")
    p(doc, "CNN khai thác cấu trúc không gian cục bộ của ảnh. Thay vì nối mọi pixel với mọi neuron, kernel dùng chung trọng số quét qua ảnh để học cạnh, góc, texture rồi ghép thành đặc trưng cấp cao.")
    heading(doc, "3.1. Các phép toán nền tảng", 2)
    p(doc, "Với ảnh X và kernel K, tích chập tạo feature map bằng tổng tích từng phần tử trong receptive field. Padding giữ kích thước; stride điều khiển bước trượt. ReLU g(z)=max(0,z) tạo phi tuyến. MaxPooling giảm kích thước bằng cách giữ cực đại trong vùng cục bộ. Cuối cùng, Flatten và Dense thực hiện phân loại.")
    code(doc, """
def conv2d(image, kernel):
    h, w = image.shape
    kh, kw = kernel.shape
    output = np.zeros((h-kh+1, w-kw+1))
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            output[i, j] = np.sum(image[i:i+kh, j:j+kw] * kernel)
    return output
""")
    heading(doc, "3.2. Dataset và phân bố", 2)
    p(doc, "MNIST gồm ảnh xám 28×28 chữ số viết tay, phù hợp kiểm tra pipeline cơ bản. Dogs vs Cats là ảnh màu với bối cảnh đa dạng, khó hơn và dễ overfit. Hai archive được lưu tại assignment4/dogandcat/train.zip, test.zip; MNIST nằm tại assignment4/MNIST.")
    table(doc, ["Dataset", "Đầu vào", "Bài toán", "Đặc điểm"], [
        ("MNIST", "28×28×1", "10 lớp", "Nét chữ đơn giản, nền tương đối sạch"),
        ("Dogs vs Cats", "Ảnh màu resize", "2 lớp", "Nhiễu nền, tư thế và ánh sáng đa dạng"),
    ])
    figure(doc, FIG4 / "mnist_comparison.png", "Hình 3.1. So sánh kết quả CNN trên MNIST")
    figure(doc, FIG4 / "dogcat_comparison.png", "Hình 3.2. So sánh kết quả CNN trên Dogs vs Cats")
    heading(doc, "3.3. Scratch, Keras và PyTorch", 2)
    p(doc, "Bản NumPy minh họa Conv2D, ReLU, pooling, flatten, softmax và cập nhật tham số. Keras dùng Sequential/Conv2D/MaxPooling2D/Dense; PyTorch dùng nn.Conv2d, nn.MaxPool2d và DataLoader. Hai framework tự động tính gradient và hỗ trợ GPU.")
    code(doc, """
class SimpleCNN(nn.Module):
    def __init__(self, classes):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2), nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(), nn.MaxPool2d(2))
        self.classifier = nn.Linear(32 * 16 * 16, classes)

    def forward(self, x):
        return self.classifier(torch.flatten(self.features(x), 1))
""")
    heading(doc, "3.4. Kết quả", 2)
    table(doc, ["Dataset", "NumPy CNN", "Keras CNN", "PyTorch CNN"], [
        ("Dogs vs Cats - Accuracy", "0.9281", "0.9894", "0.9867"),
        ("MNIST - Accuracy", "0.5445", "0.6331", "0.6061"),
    ])
    p(doc, "Kết quả trên cho thấy Keras/PyTorch có lợi thế về tối ưu và pipeline dữ liệu trong lần chạy cũ. Tuy nhiên Accuracy MNIST thấp bất thường so với một CNN MNIST chuẩn; vì vậy không nên kết luận chất lượng CNN từ con số này mà cần kiểm tra thêm preprocessing, số epoch, kích thước tập con và cấu hình huấn luyện. Đây là điểm cần minh bạch khi sử dụng kết quả thực nghiệm.")
    heading(doc, "3.5. Các hướng phát triển", 2)
    bullet(doc, "Batch Normalization giúp phân phối kích hoạt ổn định hơn.")
    bullet(doc, "Data augmentation tăng tính đa dạng ảnh và giảm overfitting.")
    bullet(doc, "Transfer learning với ResNet/MobileNet phù hợp dataset ảnh thực tế nhỏ.")
    bullet(doc, "Dropout, weight decay và early stopping kiểm soát độ phức tạp.")
    heading(doc, "3.6. Deploy", 2)
    p(doc, "Model được lưu cùng kích thước ảnh, normalization và mapping nhãn. Endpoint nhận file ảnh, resize đúng pipeline, trả nhãn và xác suất. Cần giới hạn kích thước file, từ chối MIME không hợp lệ và không tin cậy tên file từ người dùng.")

    page_title(doc, "CHƯƠNG 4. MẠNG NƠ-RON HỒI QUY RNN")
    p(doc, "RNN xử lý dữ liệu có thứ tự bằng cách truyền hidden state qua từng thời điểm. Với chuỗi y1,...,yT, mô hình học quan hệ giữa quá khứ và mục tiêu tương lai. Khác dữ liệu bảng, phép chia train/test phải giữ thứ tự thời gian.")
    heading(doc, "4.1. RNN và LSTM", 2)
    p(doc, "RNN cơ bản cập nhật ht=tanh(Wxxt+Whht-1+bh), sau đó dự đoán yt=Wyh_t+by. Khi chuỗi dài, đạo hàm có thể biến mất hoặc bùng nổ. LSTM thêm cell state và các cổng forget, input, output để kiểm soát thông tin dài hạn.")
    code(doc, """
def recurrent_step(value, hidden, wx, wh, bias):
    hidden = torch.tanh(value @ wx + hidden @ wh + bias)
    return hidden

model = nn.Sequential(
    nn.LSTM(input_size=1, hidden_size=32, batch_first=True),
    nn.Linear(32, 1)
)
""")
    figure(doc, FIG6 / "rnn_vs_lstm_cell.png", "Hình 4.1. So sánh RNN và LSTM")
    figure(doc, FIG6 / "lstm_architecture_diagram.png", "Hình 4.2. Kiến trúc LSTM many-to-one")
    heading(doc, "4.2. Dataset 1: cổ phiếu AAPL", 2)
    p(doc, "File assignment6/data/all_stocks_5yr.csv.zip gồm dữ liệu nhiều mã cổ phiếu với date, open, high, low, close, volume và Name. Pipeline lọc AAPL, sắp xếp date, dùng close làm biến mục tiêu. Sau lọc có 1.259 phiên từ 2013-02-08 đến 2018-02-07. 80% đầu train, 20% cuối test; cửa sổ 30 phiên dự đoán phiên tiếp theo.")
    table(doc, ["Chỉ số AAPL close", "Giá trị"], [
        ("Mean", "109.0667"), ("Std", "30.5568"), ("Min", "55.7899"),
        ("Median", "109.0100"), ("Max", "179.2600"), ("Skewness", "0.2899"),
    ])
    figure(doc, FIG6 / "aapl_time_series.png", "Hình 4.3. Chuỗi giá AAPL và ranh giới train/test")
    heading(doc, "4.3. Dataset 2: Online Retail II", 2)
    p(doc, "File assignment6/data/online_retail_II.csv.zip chứa Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID và Country. Pipeline loại invoice hủy, quantity/price không hợp lệ, sau đó tổng hợp số invoice khác nhau theo ngày. Đây là chuỗi nhu cầu bán lẻ có xu hướng và biến động theo thời gian.")
    figure(doc, FIG6 / "retail_time_series.png", "Hình 4.4. Chuỗi số invoice theo ngày")
    figure(doc, FIG6 / "retail_distribution.png", "Hình 4.5. Phân bố số invoice theo ngày")
    heading(doc, "4.4. Thiết kế và kết quả", 2)
    p(doc, "Cả hai dataset dùng LSTM(32) -> Dense(16, ReLU) -> Dense(1), cửa sổ 30, chuẩn hóa MinMaxScaler chỉ fit trên train. Metrics được inverse-transform về đơn vị gốc. Keras và PyTorch dùng cùng cách đặt bài toán để so sánh công bằng.")
    table(doc, ["Framework", "Dataset", "MAE", "RMSE", "MAPE", "Thời gian (s)"], [
        ("Keras", "AAPL", "6.8849", "8.1645", "4.2579%", "12.61"),
        ("PyTorch", "AAPL", "47.4643", "48.5066", "30.1820%", "3.71"),
        ("Keras", "Transactions", "15.3181", "19.8245", "24.5338%", "8.58"),
        ("PyTorch", "Transactions", "23.7989", "29.8393", "31.1915%", "1.11"),
    ])
    figure(doc, FIG6 / "metrics_comparison_bar.png", "Hình 4.6. So sánh metrics giữa hai framework")
    p(doc, "Trong lần chạy này Keras có sai số thấp hơn, còn PyTorch chạy nhanh hơn. Chênh lệch AAPL khá lớn nên cần kiểm tra seed, số epoch, scaler, khởi tạo và điều kiện hội tụ trước khi khẳng định nguyên nhân do framework. Kết luận phù hợp nhất là Keras thắng về sai số trong cấu hình đã chạy; PyTorch thắng về thời gian.")
    heading(doc, "4.5. Deploy FastAPI", 2)
    p(doc, "Assignment6 có hai service web: web/pytorch_app.py và web/keras_app.py. Có thể chạy PyTorch ở port 8001 và Keras ở port 8002 bằng Uvicorn. Endpoint /health phục vụ kiểm tra trạng thái; /docs cung cấp Swagger. Người dùng chọn dataset, nhập 30 giá trị hoặc dùng cửa sổ cuối để dự đoán bước kế tiếp.")
    code(doc, """
uvicorn web.pytorch_app:app --app-dir assignment6 --reload --port 8001
uvicorn web.keras_app:app --app-dir assignment6 --reload --port 8002
""")
    heading(doc, "4.6. Hạn chế", 2)
    bullet(doc, "Dự báo một bước và univariate chưa khai thác OHLCV hoặc yếu tố lịch.")
    bullet(doc, "Giá cổ phiếu chịu ảnh hưởng của sự kiện ngoài dữ liệu; không dùng kết quả làm tư vấn đầu tư.")
    bullet(doc, "Chuỗi bán lẻ có thể có mùa vụ, ngày nghỉ và missing date cần mô hình hóa cẩn thận.")
    bullet(doc, "Cần baseline naive, nhiều seed và walk-forward validation để đánh giá chắc chắn hơn.")

    page_title(doc, "KẾT LUẬN")
    p(doc, "Tiểu luận đã nối một quy trình hoàn chỉnh từ lịch sử AI, biểu diễn dữ liệu, mô hình ML cơ bản đến CNN và RNN. Thực nghiệm trên dữ liệu bảng, ảnh và chuỗi thời gian cho thấy đặc trưng của dữ liệu quyết định kiến trúc: Random Forest mạnh trên dữ liệu bảng; CNN khai thác không gian ảnh; LSTM xử lý phụ thuộc theo thời gian.")
    p(doc, "Các kết quả cũng cho thấy cần đánh giá nhiều chỉ số, tránh chỉ nhìn Accuracy, và cần kiểm soát leakage trong preprocessing. Deploy không chỉ là lưu model mà còn bao gồm kiểm tra input, giữ đúng pipeline, endpoint health check, version hóa artifact và giới hạn rủi ro.")
    p(doc, "Hướng phát triển gồm kiểm định lại thí nghiệm CNN MNIST, bổ sung augmentation/transfer learning, dùng walk-forward validation cho RNN, mở rộng sang Transformer, Knowledge Graph, RAG và hệ đa Agent ở các chương tiếp theo của tiểu luận.")

    page_title(doc, "TÀI LIỆU THAM KHẢO VÀ NGUỒN")
    refs = [
        "Russell, S. & Norvig, P. Artificial Intelligence: A Modern Approach.",
        "Goodfellow, I., Bengio, Y. & Courville, A. Deep Learning. MIT Press.",
        "LeCun, Y., Bengio, Y. & Hinton, G. (2015). Deep learning. Nature.",
        "Turing, A. M. (1950). Computing Machinery and Intelligence.",
        "Kaggle - Diabetes Prediction Dataset: https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset",
        "Kaggle - S&P 500 Stock Data: https://www.kaggle.com/datasets/camnugent/sandp500",
        "UCI Online Retail II: https://archive.ics.uci.edu/dataset/502/online+retail+ii",
        "TensorFlow/Keras documentation: https://www.tensorflow.org/guide/keras",
        "PyTorch documentation: https://pytorch.org/docs/",
        "Nguồn code và dataset cục bộ: assignment3, assignment4, assignment6 trong repository A2_CT_hautv.287.",
    ]
    for i, ref in enumerate(refs, 1):
        p(doc, f"[{i}] {ref}")

    page_title(doc, "PHỤ LỤC. CẤU TRÚC MÃ NGUỒN VÀ TÁI LẬP")
    p(doc, "Các file liên quan nằm trong repository theo cấu trúc sau:")
    code(doc, """
assignment3/
  diabetes/, house_price/, customer_behavior/
  report/
assignment4/
  notebook/1_dog_cat_cnn.ipynb
  dogandcat/, MNIST/, report/
assignment6/
  notebook/assignment6_rnn_real_data.ipynb
  train_pytorch.py, train_keras.py
  web/pytorch_app.py, web/keras_app.py
tieuluan/
  require.md
  build_tieuluan_docx.py
""")
    p(doc, "Để chạy lại báo cáo, dùng môi trường Conda assignment2 với Python 3.11 và chạy script build_tieuluan_docx.py. Sau khi mở DOCX, cập nhật mục lục bằng Update Field. Các notebook cần được chạy từ trên xuống dưới nếu muốn tái tạo hoàn toàn các bảng và hình thực nghiệm.")

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
