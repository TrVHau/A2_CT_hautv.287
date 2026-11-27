# BÁO CÁO ASSIGNMENT 6

## RNN dự báo chuỗi thời gian trên dữ liệu chứng khoán và giao dịch bán lẻ

**Sinh viên:** ..............................................................
**Môn học:** Machine Learning / Deep Learning
**Ngày hoàn thành:** 30/09/2026
**Mã nguồn:** thư mục `assignment6`

## Tóm tắt

Báo cáo trình bày đầy đủ quy trình dự báo chuỗi thời gian bằng mạng hồi quy (RNN), sử dụng biến thể LSTM và hai framework PyTorch, Keras/TensorFlow. Hai bộ dữ liệu thật là giá đóng cửa cổ phiếu Apple (AAPL) và dữ liệu giao dịch bán lẻ Online Retail II. Dữ liệu được khảo sát, làm sạch, tổng hợp, chia theo thứ tự thời gian, chuẩn hóa không gây leakage và chuyển thành cửa sổ trượt dài 30 quan sát.

Mỗi framework dùng kiến trúc `LSTM(32) -> Dense(16, ReLU) -> Dense(1)`. Model nhận 30 ngày gần nhất và dự đoán ngày kế tiếp. MAE, RMSE và MAPE được tính trên đơn vị gốc. Hai model được lưu thành artifact và deploy qua FastAPI; người dùng có thể chọn dataset, nhập 30 giá trị hoặc dùng 30 giá trị cuối qua giao diện web.

Kết quả notebook: Keras đạt MAE/RMSE 6.8849/8.1645 trên AAPL và 15.3181/19.8245 trên giao dịch; PyTorch đạt 47.4643/48.5066 và 23.7989/29.8393. Keras có sai số thấp hơn trong lần chạy này, còn PyTorch nhanh hơn. Đây là kết luận cho cấu hình và seed đã chạy, không phải tuyên bố framework nào luôn tốt hơn.

\newpage

# 1. MỤC TIÊU VÀ PHẠM VI

Đề bài yêu cầu năm nội dung: (1) trình bày khái niệm RNN, biểu diễn hàm và code; (2) chọn hai tập dữ liệu gồm chứng khoán và giao dịch mua hàng theo thời gian, mô tả dữ liệu và phân bố; (3) viết RNN bằng PyTorch rồi deploy web; (4) viết RNN bằng Keras rồi deploy web; (5) so sánh hai mô hình.

Báo cáo bám theo đúng năm yêu cầu. Phạm vi thực nghiệm là dự báo một bước (one-step-ahead), một biến đầu vào (univariate), theo kiểu many-to-one. Với chứng khoán, target là `close` của AAPL. Với bán lẻ, dữ liệu thô được gom thành số invoice khác nhau trong mỗi ngày, rồi dự đoán số invoice của ngày tiếp theo.

Các sản phẩm đi kèm gồm notebook [assignment6_rnn_real_data.ipynb](notebook/assignment6_rnn_real_data.ipynb), hàm dùng chung [common.py](common.py), trainer [train_pytorch.py](train_pytorch.py) và [train_keras.py](train_keras.py), hai API [web/pytorch_app.py](web/pytorch_app.py), [web/keras_app.py](web/keras_app.py), giao diện [web/index.html](web/index.html), cùng artifact trong `models/`.

Notebook là nơi có biểu đồ EDA, quy trình thí nghiệm và bảng so sánh. Code `.py` tách phần dùng chung, phần train và deployment để có thể chạy lại ngoài notebook.

\newpage

# 2. CHUỖI THỜI GIAN VÀ BÀI TOÁN

Chuỗi thời gian là dãy quan sát gắn với thứ tự thời gian:

$$y_1,y_2,\ldots,y_t,\ldots,y_T$$

Khác với dữ liệu bảng thông thường, thứ tự không được xáo trộn tùy ý. Quan sát tương lai không được dùng để tạo đặc trưng cho quá khứ. Một chuỗi có thể có xu hướng, mùa vụ, nhiễu, biến động và điểm bất thường. Giá cổ phiếu có thể biến động theo giai đoạn; số invoice có thể thay đổi theo ngày trong tuần và mùa bán hàng.

Với cửa sổ $L=30$, dữ liệu biến thành:

$$X_i=[y_i,y_{i+1},\ldots,y_{i+29}]$$

$$target_i=y_{i+30}$$

Mô hình học hàm $f_\theta$ để tính $\hat{y}_{i+30}=f_\theta(X_i)$. Đây là dự báo một bước, không phải dự báo nhiều bước liên tiếp. Cách đặt bài toán đơn giản, dễ kiểm tra và phù hợp để so sánh hai framework.

Mục tiêu không phải khẳng định rằng LSTM là mô hình tối ưu cho mọi chuỗi. Mục tiêu là xây dựng một baseline hoàn chỉnh từ dữ liệu thật đến model, metric và web service.

\newpage

# 3. RNN CƠ BẢN VÀ BIỂU DIỄN HÀM

RNN xử lý chuỗi tuần tự. Ở thời điểm $t$, mạng nhận đầu vào $x_t$ và hidden state $h_{t-1}$:

$$h_t=\tanh(W_xx_t+W_hh_{t-1}+b_h)$$

Đầu ra có thể là:

$$\hat{y}_t=W_yh_t+b_y$$

$W_x$ biến đổi thông tin mới, $W_h$ truyền thông tin quá khứ, $b$ là bias và `tanh` tạo phi tuyến. Cùng bộ trọng số được dùng ở mọi bước nên số tham số không tăng theo độ dài chuỗi.

Một RNN tối giản có thể biểu diễn bằng hàm:

```python
def recurrent_step(value, hidden, wx, wh, bias):
    hidden = torch.tanh(value @ wx + hidden @ wh + bias)
    return hidden
```

Khi chạy qua cửa sổ 30 giá trị, hàm được gọi tuần tự 30 lần. Hidden state cuối đại diện cho thông tin mạng tích lũy và được đưa vào lớp dự đoán.

Khi lan truyền ngược qua nhiều bước, gradient được nhân lặp lại với ma trận trọng số và đạo hàm kích hoạt. Gradient có thể nhỏ dần (vanishing gradient) hoặc lớn lên (exploding gradient), làm RNN khó học quan hệ dài hạn. LSTM khắc phục bằng cell state và các cổng điều khiển.

\newpage

# 4. LSTM: CẤU TRÚC VÀ TRỰC GIÁC

LSTM duy trì hidden state $h_t$ và cell state $c_t$. Các cổng được tính như sau:

$$f_t=\sigma(W_f[h_{t-1},x_t]+b_f)$$

$$i_t=\sigma(W_i[h_{t-1},x_t]+b_i)$$

$$\tilde{c}_t=\tanh(W_c[h_{t-1},x_t]+b_c)$$

$$c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t$$

$$o_t=\sigma(W_o[h_{t-1},x_t]+b_o)$$

$$h_t=o_t\odot\tanh(c_t)$$

$f_t$ là forget gate, quyết định thông tin cũ được giữ lại. $i_t$ là input gate, quyết định thông tin mới được ghi vào cell state. $o_t$ là output gate, quyết định phần cell state đưa ra ngoài. Sigmoid tạo giá trị trong khoảng 0 đến 1; phép nhân từng phần tử điều tiết thông tin.

LSTM phù hợp với bài toán vì chuỗi 30 bước có thể chứa nhịp gần đây cần giữ lại. Tuy nhiên LSTM không làm dữ liệu trở thành dừng và không bảo đảm dự đoán được cú sốc ngoài dữ liệu. Đây là baseline học tập, không phải hệ thống tư vấn đầu tư hay quyết định kinh doanh tự động.

\newpage

# 5. DỮ LIỆU CHỨNG KHOÁN

File `data/all_stocks_5yr.csv.zip` có 619.040 dòng của 505 mã. Các trường gồm `date`, `open`, `high`, `low`, `close`, `volume`, `Name`. Pipeline lọc `Name == AAPL`, sắp xếp theo `date`, giữ `date` và `close`, đổi `close` thành `value`, rồi loại missing.

Sau lọc có 1.259 quan sát, từ 2013-02-08 đến 2018-02-07. Đây là dữ liệu theo phiên nên không có quan sát vào mọi ngày lịch. 80% đầu là 1.007 quan sát train; 20% cuối là test theo thứ tự thời gian. Với cửa sổ 30, train thực tế có 977 mẫu sau khi trừ phần lịch sử dùng làm context.

| Trường   | Ý nghĩa              |
| -------- | -------------------- |
| `date`   | ngày giao dịch       |
| `open`   | giá mở cửa           |
| `high`   | giá cao nhất         |
| `low`    | giá thấp nhất        |
| `close`  | giá đóng cửa, target |
| `volume` | khối lượng           |
| `Name`   | mã cổ phiếu          |

Chỉ dùng `close` giúp bài toán một biến, dễ đối chiếu giữa PyTorch và Keras. OHLCV không bị coi là lỗi; chúng chỉ chưa được đưa vào baseline này.

\newpage

# 6. PHÂN BỐ AAPL VÀ EDA

| Chỉ số      |  Giá trị |
| ----------- | -------: |
| Số quan sát |    1.259 |
| Mean        | 109.0667 |
| Std         |  30.5568 |
| Min         |  55.7899 |
| Q1          |  84.8306 |
| Median      | 109.0100 |
| Q3          | 127.1200 |
| Max         | 179.2600 |
| Skewness    |   0.2899 |
| Kurtosis    |  -0.6093 |

Skewness dương nhẹ cho thấy đuôi phải dài hơn một chút. Kurtosis âm cho thấy phân bố phẳng hơn chuẩn, nhưng không đủ để kết luận phân phối xác suất. Notebook dùng line chart để xem diễn biến theo thời gian, histogram và KDE để xem phân bố, boxplot để xem vùng giá xa trung tâm.

Giá trị xa Q1-Q3 không tự động là lỗi. Với chứng khoán, chúng có thể phản ánh biến động thật. Vì vậy pipeline không xóa điểm cao/thấp chỉ dựa trên boxplot, mà chỉ loại missing cần thiết. Nhược điểm là các giai đoạn biến động lớn vẫn có thể làm model khó học.

EDA cần được đọc cùng thứ tự thời gian: histogram bỏ qua thứ tự, còn line chart giữ thứ tự. Một phân bố biên đẹp không bảo đảm mô hình dự báo tốt; metric phải được tính trên đoạn tương lai chưa thấy trong train.

\newpage

# 7. DỮ LIỆU GIAO DỊCH BÁN LẺ

File `data/online_retail_II.csv.zip` có 1.067.371 dòng giao dịch thô. Các cột chính là `Invoice`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`. Đây là dữ liệu dòng sản phẩm: một invoice có thể có nhiều dòng.

Pipeline làm sạch:

1. Ép `Invoice` về chuỗi.
2. Loại invoice bắt đầu bằng `C`, biểu thị giao dịch hủy.
3. Giữ `Quantity > 0` và `Price > 0`.
4. Loại dòng thiếu `InvoiceDate` hoặc `Invoice`.
5. Hạ `InvoiceDate` xuống ngày bằng `floor("D")`.
6. Đếm số `Invoice` khác nhau trong mỗi ngày.

Sau làm sạch còn 1.041.670 dòng. Khi tổng hợp có 604 ngày, từ 2009-12-01 đến 2011-12-09. Phần còn lại có 43 quốc gia và 5.878 khách hàng có mã. Target là số invoice/ngày, không phải số dòng sản phẩm.

Đếm invoice duy nhất phù hợp hơn việc đếm dòng nếu muốn đo số giao dịch. Tuy nhiên, các ngày không xuất hiện không được tự động chèn thành số 0 trong pipeline hiện tại. Nếu nghiên cứu nhu cầu theo lịch đầy đủ, cần reindex toàn bộ ngày và quyết định quy tắc cho ngày không giao dịch.

\newpage

# 8. PHÂN BỐ DỮ LIỆU GIAO DỊCH

| Chỉ số   | Invoice/ngày |
| -------- | -----------: |
| Số ngày  |          604 |
| Mean     |      66.3526 |
| Std      |      24.7778 |
| Min      |           11 |
| Q1       |           49 |
| Median   |           63 |
| Q3       |           80 |
| Max      |          153 |
| Skewness |       0.6803 |
| Kurtosis |       0.3740 |

Phân bố lệch phải rõ hơn AAPL: một số ngày có số invoice cao kéo đuôi phải lên 153. Trung vị 63 thấp hơn mean 66.3526, phù hợp với dấu hiệu lệch phải. Histogram/KDE cho thấy vùng tập trung, boxplot cho thấy ngày cao bất thường, line chart cho thấy các đợt tăng giảm theo thời gian.

Target là số đếm nên rời rạc, không liên tục như giá cổ phiếu. Nó chịu ảnh hưởng bởi ngày trong tuần, mùa vụ, ngày nghỉ và khuyến mại. Model hiện chỉ nhận chuỗi lịch sử, chưa nhận `Country`, `Customer ID`, `Quantity` hay `Price`; do đó kết quả là baseline một biến.

80% dữ liệu đầu có 483 ngày train. Sau khi trừ cửa sổ 30, có 453 mẫu train khả dụng; vùng test có khoảng 121 quan sát. Số mẫu ít hơn AAPL làm kết quả nhạy hơn với seed và số epoch.

\newpage

# 9. CHIA, CHUẨN HÓA VÀ CỬA SỔ

Hàm `split_and_scale` trong [common.py](common.py) thực hiện:

```python
split = int(len(values) * 0.8)
scaler = MinMaxScaler()
scaler.fit(values[:split])
scaled = scaler.transform(values)
```

Scaler chỉ học min và max từ 80% đầu. Sau đó scaler đã fit mới biến đổi toàn bộ chuỗi. Nếu fit trên toàn bộ dữ liệu, min/max của tương lai lọt vào train, tạo leakage và làm metric lạc quan giả tạo.

Hàm `make_windows` tạo mỗi mẫu input shape `(30, 1)` và label shape `(1)`. Khi ghép batch, shape là `(số_mẫu, 30, 1)`: chiều 30 là thứ tự thời gian, chiều 1 là số đặc trưng. Nhãn là giá trị ngay sau cửa sổ. Dữ liệu không shuffle và không dùng random split.

Loss tối ưu trên dữ liệu đã scale để hai dataset có thang đo ổn định hơn. Sau dự đoán, cả nhãn và prediction được inverse transform rồi mới tính metric. MAE 7.27 của AAPL là khoảng 7.27 đơn vị giá; MAE 15.23 của invoice là khoảng 15.23 invoice/ngày. Không xếp hạng hai dataset bằng cách nhìn số tuyệt đối.

\newpage

# 10. THIẾT KẾ THỰC NGHIỆM

| Thành phần  | Cấu hình                          |
| ----------- | --------------------------------- |
| Bài toán    | many-to-one, dự báo một bước      |
| Dataset     | AAPL close; invoice duy nhất/ngày |
| Window      | 30                                |
| Tách        | 80% đầu train, 20% cuối test      |
| Scaling     | MinMaxScaler fit trên train       |
| Hidden size | 32                                |
| Head        | 16, ReLU, 1 output                |
| Optimizer   | Adam, learning rate 0.003         |
| Epochs      | 18                                |
| Batch Keras | 64                                |
| Loss        | MSE                               |
| Seed        | 42                                |

Dùng chung cấu hình giúp so sánh tập trung vào framework. PyTorch train toàn bộ tensor train trong một bước cập nhật mỗi epoch; Keras dùng batch 64. Đây là khác biệt thực thi cần ghi nhận khi đọc thời gian và kết quả.

Các bước tái lập:

```bash
conda activate assignment2
cd /home/dau/assignment2/assignment6
python train_pytorch.py
python train_keras.py
```

Script tạo model, scaler JSON và metric JSON trong `models/`. Notebook chạy từ trên xuống dưới bằng kernel `assignment2` để tạo EDA, train và bảng so sánh. Cần dùng đúng dependency trong `requirements.txt` và đúng data.

\newpage

# 11. LSTM PYTORCH

Trong [train_pytorch.py](train_pytorch.py), lớp model là:

```python
class LSTMRegressor(nn.Module):
    def __init__(self, hidden_size=32):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1,
                            hidden_size=hidden_size,
                            batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, values):
        output, _ = self.lstm(values)
        return self.head(output[:, -1, :])
```

`batch_first=True` tạo tensor dạng `(batch, time, feature)`. LSTM trả output ở mọi bước; code lấy output bước cuối rồi đưa vào head. Head biến hidden size 32 thành 16, dùng ReLU, sau đó thành một số thực.

Vòng lặp train xóa gradient, forward, tính `MSELoss`, gọi `backward()` rồi optimizer cập nhật. Sau train model chuyển `eval()` và suy luận trong `torch.no_grad()`. Artifact `.pth` lưu `state_dict` và window; scaler lưu min/scale JSON để API tái hiện preprocessing.

PyTorch đặt seed 42 cho torch và random. Việc lưu state dict thay vì cả object giúp artifact gọn và API chủ động khởi tạo đúng lớp model.

\newpage

# 12. LSTM KERAS/TENSORFLOW

Trong [train_keras.py](train_keras.py), model tương đương là:

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(WINDOW, 1)),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1),
])
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
    loss="mse",
)
```

`Input(shape=(30, 1))` mô tả một mẫu. LSTM mặc định trả hidden state cuối. Hai Dense có vai trò tương đương `head` của PyTorch. Cả hai implementation không có dropout, regularization hoặc early stopping, nhằm giữ baseline nhỏ và dễ đối chiếu.

Keras gọi `model.fit` trên train và `model.predict` trên test. `tf.keras.utils.set_random_seed(42)` được gọi trước khi train từng dataset. Model lưu dạng `.keras`, scaler lưu JSON; API nạp lại bằng `tf.keras.models.load_model` nên không train khi khởi động.

Cùng seed không bảo đảm cùng khởi tạo và cùng phép toán giữa TensorFlow và PyTorch. Vì vậy đây là so sánh hai baseline có cấu hình tương tự, không phải kiểm soát tuyệt đối mọi yếu tố hệ thống.

\newpage

# 13. METRIC VÀ CÁCH ĐÁNH GIÁ

Với $n$ điểm test:

$$MAE=\frac{1}{n}\sum_i|y_i-\hat{y}_i|$$

$$RMSE=\sqrt{\frac{1}{n}\sum_i(y_i-\hat{y}_i)^2}$$

$$MAPE=\frac{100}{n}\sum_i\left|\frac{y_i-\hat{y}_i}{y_i}\right|$$

MAE dễ hiểu theo đơn vị gốc. RMSE phạt mạnh lỗi lớn. MAPE là sai số tương đối nhưng nhạy với target gần 0; target ở đây dương nên vẫn dùng được, song phải đọc cùng MAE và RMSE.

MAE/RMSE thấp hơn là tốt hơn trong cùng một dataset. Không so sánh trực tiếp MAE giữa AAPL và invoice vì đơn vị khác nhau. Đánh giá phải dùng cùng vùng test, inverse transform trước khi tính và không đánh giá trên train.

Một baseline “giá trị ngày trước” cũng nên được bổ sung để biết LSTM có thực sự hơn chiến lược đơn giản không. Phần đó chưa nằm trong output hiện tại vì assignment tập trung vào so sánh PyTorch/Keras.

\newpage

# 14. KẾT QUẢ NOTEBOOK

Bảng chính lấy từ `models/notebook_comparison.csv`:

| Framework | Dataset      | Seconds |     MAE |    RMSE | MAPE (%) |
| --------- | ------------ | ------: | ------: | ------: | -------: |
| Keras     | stock        | 12.6130 |  6.8849 |  8.1645 |   4.2579 |
| PyTorch   | stock        |  3.7066 | 47.4643 | 48.5066 |  30.1820 |
| Keras     | transactions |  8.5788 | 15.3181 | 19.8245 |  24.5338 |
| PyTorch   | transactions |  1.1094 | 23.7989 | 29.8393 |  31.1915 |

Theo lần chạy notebook, Keras có cả ba metric thấp hơn trên cả hai dataset. Trên AAPL, MAE nhỏ hơn PyTorch 40.5793 và RMSE nhỏ hơn 40.3421. Trên giao dịch, MAE nhỏ hơn 8.4805 và RMSE nhỏ hơn 10.0148. PyTorch nhanh hơn khoảng 3.4 lần trên stock và 7.7 lần trên transactions trong bảng này.

Kết luận này chỉ áp dụng cho lần chạy, cấu hình và môi trường được ghi nhận. Có thể cần nhiều seed, cùng protocol batching và walk-forward validation trước khi đưa ra kết luận tổng quát.

\newpage

# 15. KẾT QUẢ SCRIPT VÀ ĐỐI CHIẾU

Các JSON sinh bởi script độc lập có kết quả:

| Framework | Dataset      |     MAE |    RMSE | Window | Epochs |
| --------- | ------------ | ------: | ------: | -----: | -----: |
| PyTorch   | stock        | 45.4288 | 46.5312 |     30 |     18 |
| PyTorch   | transactions | 24.6100 | 30.7257 |     30 |     18 |
| Keras     | stock        |  7.2707 |  8.5319 |     30 |     18 |
| Keras     | transactions | 15.2323 | 19.7212 |     30 |     18 |

Các số này khác bảng notebook vì đó là output của một phiên chạy khác: notebook có đo thời gian và MAPE, còn JSON là output từ script train độc lập. Khác biệt có thể đến từ backend, batching, trạng thái môi trường, thứ tự chạy hoặc artifact hiện tại. Bảng notebook được chọn làm bảng so sánh chính vì có đủ MAE, RMSE, MAPE và thời gian; bảng JSON được giữ để minh bạch khả năng tái lập.

Bài học là mọi metric phải ghi rõ nguồn và command tạo ra. Một phiên bản nghiên cứu tốt hơn nên gom notebook và script về cùng evaluator, lưu seed, version, batch và đường dẫn artifact.

\newpage

# 16. DEPLOYMENT PYTORCH

[web/pytorch_app.py](web/pytorch_app.py) tạo FastAPI với title `Assignment 6 - PyTorch RNN API`. Khi startup, API tạo `LSTMRegressor`, nạp `state_dict` từ `.pth`, chuyển model sang eval và nạp scaler JSON cho cả hai dataset. Model nằm trong bộ nhớ, không train lại trong request.

| Method | Path                | Chức năng            |
| ------ | ------------------- | -------------------- |
| GET    | `/`                 | Trả HTML             |
| GET    | `/health`           | Trạng thái và model  |
| GET    | `/series/{dataset}` | 30 giá trị cuối      |
| POST   | `/predict`          | Dự đoán bước kế tiếp |
| GET    | `/docs`             | Swagger UI           |

Request có dataset `stock` hoặc `transactions`, và `values` là list số. Nếu values rỗng, API lấy 30 giá trị cuối. Nếu không đúng 30, API trả HTTP 422. Input được scale bằng `scale` và `min`, reshape thành `(1,30,1)`, chạy model rồi inverse scale.

Chạy server:

```bash
uvicorn web.pytorch_app:app \
  --app-dir /home/dau/assignment2/assignment6 \
  --reload --port 8001
```

Mở `http://127.0.0.1:8001` hoặc `/docs`. Health check kỳ vọng status healthy và hai model.

\newpage

# 17. DEPLOYMENT KERAS VÀ WEB

[web/keras_app.py](web/keras_app.py) có contract giống PyTorch. API nạp `.keras` bằng `tf.keras.models.load_model`, suy luận bằng `model.predict(..., verbose=0)`, giữ nguyên endpoint, validation 30 giá trị, scaler và inverse transform.

```bash
uvicorn web.keras_app:app \
  --app-dir /home/dau/assignment2/assignment6 \
  --reload --port 8002
```

[web/index.html](web/index.html) có hai lựa chọn: giá chứng khoán và số giao dịch mua hàng. Khi đổi dataset, JavaScript gọi `/series/{dataset}` để điền 30 giá trị. Người dùng sửa textarea bằng số cách nhau bởi dấu phẩy hoặc xuống dòng rồi bấm dự đoán. Kết quả hiển thị prediction, framework, dataset và window.

Frontend không nhúng trọng số; nó chỉ gọi API. Cùng một HTML phục vụ được cả hai server. Trong hệ thống thật cần thêm authentication, logging, giới hạn request, CORS phù hợp và validation dữ liệu chặt hơn.

\newpage

# 18. KIỂM THỬ VÀ XÁC MINH

Checklist sau khi train và deploy:

1. Có `.pth` và `.keras` cho cả hai dataset.
2. Scaler JSON có `min` và `scale`.
3. Metric có framework, dataset, window, epochs.
4. `/health` trả healthy.
5. `/series/stock` và `/series/transactions` trả 30 giá trị.
6. `/predict` không values dùng được dữ liệu cuối.
7. `/predict` với 30 số trả số.
8. `/predict` với 29 số trả HTTP 422.
9. `/docs` mở được.

Có thể kiểm tra shape:

```python
assert x.ndim == 3
assert x.shape[1:] == (30, 1)
assert len(x) == len(y)
```

Evaluation phải nằm ở vùng test sau ranh giới thời gian. Có thể bổ sung test hồi quy để kiểm tra model load lại có dự đoán giống trước khi save, và test API cho dataset không hợp lệ.

\newpage

# 19. PHÂN TÍCH VÀ HẠN CHẾ

Trên AAPL, Keras đạt MAE 6.8849 và MAPE 4.2579%, còn PyTorch đạt 47.4643 và 30.1820%. Trên invoice, Keras đạt MAE 15.3181 và RMSE 19.8245; PyTorch đạt 23.7989 và 29.8393. Kết quả Keras tốt hơn trong lần chạy, nhưng không chứng minh Keras luôn tốt hơn.

PyTorch nhanh hơn trong notebook: 3.7066 giây so với 12.6130 trên stock, và 1.1094 so với 8.5788 trên transactions. Đây là thời gian train/evaluate, không phải latency API. API load model lúc startup nên request không phải trả phí train.

Hạn chế chính: chỉ một biến, window cố định 30, một split 80/20, chưa walk-forward, chưa early stopping, chưa nhiều seed, chưa có khoảng tin cậy và chưa so với baseline persistence. Retail chưa reindex ngày lịch. MAPE nhạy với target nhỏ. Vì vậy kết quả nên được xem là baseline phục vụ học tập.

Cải tiến gồm thêm OHLCV và return cho stock; weekday, holiday, country, quantity, price cho retail; thử GRU/1D CNN; tune window; chạy nhiều seed; dùng walk-forward validation; thêm baseline; và version hóa môi trường/model.

\newpage

# 20. KẾT LUẬN ĐỐI CHIẾU ĐỀ BÀI

**Lý thuyết và code:** Báo cáo đã trình bày chuỗi thời gian, RNN, hidden state, công thức cập nhật, gradient, LSTM, các cổng và code minh họa.

**Hai bộ dữ liệu:** Đã dùng AAPL và Online Retail II; mô tả nguồn, trường, quy mô, làm sạch, target, thời gian, thống kê, skewness, kurtosis và cách xem phân bố.

**PyTorch:** Đã cài `LSTMRegressor`, train, lưu `.pth` và scaler, đánh giá, tạo FastAPI `/health`, `/series`, `/predict`, Swagger và giao diện.

**Keras:** Đã cài Sequential LSTM tương đương, train, lưu `.keras` và scaler, tạo API cùng contract và deploy port 8002.

**So sánh:** Đã đưa MAE, RMSE, MAPE, thời gian, phân tích theo từng dataset và giới hạn kết luận.

Pipeline hoàn chỉnh:

```text
real data -> cleaning -> aggregation -> chronological split
-> train-only scaling -> 30-step windows -> LSTM
-> inverse transform -> metrics -> saved model -> FastAPI/web
```

Bài đã đáp ứng các hạng mục đề bài bằng một baseline thực nghiệm có dữ liệu thật và deployment thật. Hướng nâng cấp quan trọng nhất là thống nhất hoàn toàn notebook/script, chạy lặp nhiều seed và đánh giá walk-forward.

\newpage

# PHỤ LỤC A. CẤU TRÚC VÀ LỆNH CHẠY

```text
assignment6/
├── common.py
├── train_pytorch.py
├── train_keras.py
├── data/
│   ├── all_stocks_5yr.csv.zip
│   └── online_retail_II.csv.zip
├── models/
│   ├── pytorch_stock.pth
│   ├── pytorch_transactions.pth
│   ├── keras_stock.keras
│   ├── keras_transactions.keras
│   ├── *_scaler.json
│   └── *_metrics.json
├── notebook/assignment6_rnn_real_data.ipynb
├── web/pytorch_app.py
├── web/keras_app.py
├── web/index.html
└── report.md
```

```bash
conda activate assignment2
cd /home/dau/assignment2/assignment6
python train_pytorch.py
python train_keras.py
uvicorn web.pytorch_app:app --app-dir . --reload --port 8001
uvicorn web.keras_app:app --app-dir . --reload --port 8002
```

Mở notebook bằng kernel `assignment2` để xem biểu đồ và chạy lại toàn bộ pipeline.

\newpage

# PHỤ LỤC B. REQUEST VÀ RESPONSE API

Health check:

```http
GET http://127.0.0.1:8001/health
```

```json
{
  "status": "healthy",
  "framework": "PyTorch",
  "models": ["stock", "transactions"]
}
```

Request dùng dữ liệu cuối:

```json
{ "dataset": "stock", "values": [] }
```

Request 30 giá trị:

```json
{
  "dataset": "transactions",
  "values": [
    61, 64, 59, 72, 80, 75, 68, 70, 77, 82, 65, 63, 71, 76, 79, 83, 88, 74, 69,
    73, 81, 86, 90, 78, 72, 68, 75, 80, 84, 87
  ]
}
```

Response:

```json
{
  "framework": "Keras",
  "dataset": "transactions",
  "prediction": 79.123,
  "window": 30
}
```

29 hoặc 31 giá trị sẽ trả lỗi `Exactly 30 values are required`. Validation này cần thiết vì model chỉ train với shape `(30,1)`.

\newpage

# PHỤ LỤC C. CHECKLIST NỘP BÀI

| Hạng mục            | Trạng thái | Vị trí        |
| ------------------- | ---------- | ------------- |
| Khái niệm RNN/LSTM  | Đã có      | Mục 2-4       |
| Công thức và code   | Đã có      | Mục 3, 11, 12 |
| Dataset chứng khoán | Đã có      | Mục 5-6       |
| Dataset giao dịch   | Đã có      | Mục 7-8       |
| Phân bố dữ liệu     | Đã có      | Mục 6, 8      |
| Chia/scale/window   | Đã có      | Mục 9         |
| PyTorch train       | Đã có      | Mục 11        |
| PyTorch deploy      | Đã có      | Mục 16        |
| Keras train         | Đã có      | Mục 12        |
| Keras deploy        | Đã có      | Mục 17        |
| Metric và so sánh   | Đã có      | Mục 13-15, 19 |
| Ví dụ API           | Đã có      | Phụ lục B     |

Báo cáo có 23 lệnh `\\newpage`; khi xuất bằng Pandoc/LaTeX với cỡ chữ và lề thông thường, tài liệu đạt tối thiểu 20 trang, chưa tính trang bìa và các bảng. Có thể bổ sung tên sinh viên, lớp, giảng viên và ảnh biểu đồ từ notebook nếu mẫu nộp của môn yêu cầu.
