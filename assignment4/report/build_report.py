import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd
import numpy as np

# Load data
df_dog = pd.read_csv('/home/dau/assignment2/assignment4/dogcat_results.csv')
df_mnist = pd.read_csv('/home/dau/assignment2/assignment4/notebook/mnist_results.csv')

df_dog['parameters'] = df_dog['parameters'].fillna(0)
df_mnist['parameters'] = df_mnist['parameters'].fillna(0)

def create_plot(filename, title, df):
    plt.figure(figsize=(6, 4))
    plt.bar(df['model'], df['test_accuracy'], color=['#4C78A8', '#F58518', '#54A24B'])
    plt.title(title, fontsize=12)
    plt.ylabel('Test Accuracy', fontsize=10)
    plt.ylim(0, 1)
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(filename)
    plt.close()

# Tạo biểu đồ
create_plot('/home/dau/assignment2/assignment4/report/screenshots/dogcat_comparison.png', 'So sánh độ chính xác: Dog/Cat', df_dog)
create_plot('/home/dau/assignment2/assignment4/report/screenshots/mnist_comparison.png', 'So sánh độ chính xác: MNIST', df_mnist)

doc = Document()

# Cover
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN\n\n')
run.bold = True
run.font.size = Pt(14)
doc.add_heading('BÁO CÁO BÀI TẬP LỚN: MẠNG NƠ-RON CNN VÀ KHẢO SÁT FRAMEWORK', 0)
doc.add_paragraph('\n\n\n')
doc.add_paragraph('Sinh viên thực hiện: Trần Văn Hậu')
doc.add_paragraph('Mã sinh viên: B23DCCN287')
doc.add_paragraph('Lớp: D23CTPM01-B')
doc.add_page_break()

# 1. Giới thiệu
doc.add_heading('1. Giới thiệu và phương pháp tiếp cận', level=1)
doc.add_paragraph('Thị giác máy tính (Computer Vision) đã chứng kiến sự thăng tiến vượt bậc nhờ sự ra đời của Mạng nơ-ron tích chập (CNN). Trong bài tập lớn số 04 này, mục đích cốt lõi là thấu hiểu từng "mạch máu" của thuật toán. Thay vì chỉ gọi các API bậc cao, phương pháp thực nghiệm được triển khai từ việc lập trình hoàn chỉnh một mạng CNN từ con số 0 (from scratch) bằng NumPy. Toàn bộ logic của Forward Propagation (Lan truyền thuận) và Backward Propagation (Lan truyền ngược) được tự định nghĩa chặt chẽ.')
doc.add_paragraph('Báo cáo phân tích trên hai tập dữ liệu đại diện cho hai cấp độ khó khác nhau: tập ảnh xám chữ số viết tay MNIST (cơ bản) và tập ảnh màu phức tạp Dogs vs Cats (nhiễu cao). Các framework deep learning phổ biến như Keras và PyTorch cũng được triển khai song song để thiết lập hệ quy chiếu so sánh về tốc độ, năng lực hội tụ và mức độ tiện lợi khi viết mã.')

# 2. Lý thuyết
doc.add_heading('2. Phân tích nền tảng kiến trúc CNN', level=1)
doc.add_paragraph('Các mạng nhiều lớp fully-connected thông thường yêu cầu làm phẳng (flatten) dữ liệu ảnh ngay từ đầu, điều này làm cản trở việc học các thuộc tính không gian lân cận và làm bùng nổ số lượng tham số. CNN giải quyết vấn đề này qua các khối logic:')

doc.add_heading('2.1. Lớp trích xuất đặc trưng (Conv2D)', level=2)
doc.add_paragraph('Lớp Conv2D giữ nguyên cấu trúc 2 chiều của ảnh. Bằng cách sử dụng các ma trận trọng số (kernel) trượt dọc theo không gian 2D, lớp này tính toán tích chập trên vùng nhận diện cục bộ (receptive field). Kỹ thuật dùng chung trọng số (weight sharing) trên toàn bộ ma trận ảnh giúp CNN học được các đặc trưng độc lập với vị trí (dù con vật nằm ở góc nào trong ảnh).')

doc.add_heading('2.2. Lớp kích hoạt ReLU phi tuyến', level=2)
doc.add_paragraph('Sau tầng trích xuất Conv, đặc trưng thô được đi qua hàm kích hoạt ReLU: f(x) = max(0, x). Dưới góc độ lan truyền ngược, ReLU cho phép truyền nguyên vẹn giá trị gradient nếu như neuron được kích hoạt (>0) và triệt tiêu hoàn toàn nếu (<0). Điều này giải quyết bài toán giảm dần đạo hàm (vanishing gradient) vốn là trở ngại trên các mô hình truyền thống.')

doc.add_heading('2.3. Lớp gộp miền không gian (MaxPool2D)', level=2)
doc.add_paragraph('Nhằm giảm kích thước độ phân giải, Max Pooling sẽ rà soát các ô cục bộ và giữ lại giá trị cực đại. Không chỉ tối ưu bộ nhớ cho tham số, pooling còn mang lại lợi ích "translation invariance", mô hình bớt nhạy cảm hơn khi vật thể bị dịch chuyển một vài pixel.')

doc.add_heading('2.4. Đạo hàm chuỗi và cập nhật bằng Adam', level=2)
doc.add_paragraph('Quá trình học tối ưu hóa diễn ra trong giai đoạn backpropagation. Để mô phỏng được PyTorch/Keras, lớp NumPy CNN tự tính đạo hàm theo quy tắc chuỗi cho từng lớp. Bộ tối ưu Adam kết hợp hai cơ chế Gradient Momentum (quán tính hướng đi) và RMSProp (bình phương gradient) để hội tụ vượt trội so với Gradient Descent thuần.')

# 3. Thực nghiệm
doc.add_heading('3. Thiết kế thực nghiệm và Số liệu', level=1)

doc.add_heading('3.1. Bài toán phân loại ảnh Chó/Mèo', level=2)
doc.add_paragraph('Tập dữ liệu yêu cầu mô hình phân tích nhiễu phức tạp từ bối cảnh, hậu cảnh. Toàn bộ ảnh được thay đổi kích thước đồng bộ về 64x64 pixel. Với NumPy, kích thước tensor và tài nguyên tính toán không tận dụng được kiến trúc tăng tốc vật lý. Dưới đây là kết quả kiểm thử trên các file dữ liệu độc lập:')
doc.add_picture('/home/dau/assignment2/assignment4/report/screenshots/dogcat_comparison.png', width=Inches(5))

table = doc.add_table(rows=1, cols=4)
table.style = 'Table Grid'
for i, col in enumerate(['Khung lập trình (Model)', 'Độ chính xác (Accuracy)', 'Hàm mất mát (Loss)', 'Tham số']): table.rows[0].cells[i].text = col
for _, row in df_dog.iterrows():
    r = table.add_row().cells
    r[0].text = str(row['model']); r[1].text = f"{row['test_accuracy']:.4f}"; r[2].text = f"{row['test_loss']:.4f}"; r[3].text = f"{int(row['parameters']):,}"

doc.add_heading('3.2. Bài toán phân loại chữ số MNIST', level=2)
doc.add_paragraph('Đây là tập hình thái đối tượng cơ bản gồm nét đen và nền trắng. Biến thể duy nhất là hình dáng viết tay. Do đó không cần tới kiến trúc phức tạp, các mô hình nhanh chóng hội tụ đạt trên 98% chỉ sau một vài epochs huấn luyện:')
doc.add_picture('/home/dau/assignment2/assignment4/report/screenshots/mnist_comparison.png', width=Inches(5))

table = doc.add_table(rows=1, cols=4)
table.style = 'Table Grid'
for i, col in enumerate(['Khung lập trình (Model)', 'Độ chính xác (Accuracy)', 'Hàm mất mát (Loss)', 'Tham số']): table.rows[0].cells[i].text = col
for _, row in df_mnist.iterrows():
    r = table.add_row().cells
    r[0].text = str(row['model']); r[1].text = f"{row['test_accuracy']:.4f}"; r[2].text = f"{row['test_loss']:.4f}"; r[3].text = f"{int(row['parameters']):,}"

# 4. Thảo luận
doc.add_heading('4. Thảo luận và Đánh giá tổng quan', level=1)
doc.add_paragraph('Từ thực tế triển khai bài toán, sinh viên đúc kết được các luận điểm đánh giá sau đây:')
doc.add_paragraph('Thứ nhất, tính chất của Dữ liệu quyết định độ chuyên sâu mô hình. Bài toán Dog/Cat thể hiện giới hạn cứng của một CNN truyền thống không có Batch Normalization hay chiến lược Data Augmentation. Accuracy chỉ đạt mức trung bình thấp cho thấy cấu trúc Conv-Pool thông thường dễ dàng chịu lỗi Overfitting trên tập ảnh nhiễu đa dạng.')
doc.add_paragraph('Thứ hai, giá trị của việc viết code thủ công (from scratch). Phương pháp NumPy from scratch tuy có tốc độ thực thi rất chậm do không dùng GPU nhưng là kỹ năng bắt buộc để một kỹ sư AI thực thụ nắm được ma trận gradient (Backprop) di chuyển bên trong các layer như thế nào.')
doc.add_paragraph('Thứ ba, sự khác nhau căn bản giữa các Framework. TensorFlow/Keras đóng gói các mô hình phức tạp thành một API thân thiện, rút ngắn thời gian phát triển với hàm .fit() đơn giản. Ngược lại, PyTorch cung cấp phương pháp tiếp cận hướng đối tượng, buộc kỹ sư phải tự viết vòng lặp Loss-Backward-Step. Tuy dài hơn về lượng code, điều kiện này lại mở ra khả năng tùy biến vô hạn trong các trung tâm học thuật và nghiên cứu.')

doc.save('/home/dau/assignment2/assignment4/report/Assignment4_Report_ver2.docx')
print('Đã tạo Assignment4_Report_ver2.docx chi tiết dựa theo phong cách báo cáo học thuật!')
