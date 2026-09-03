# BÁO CÁO MÔN HỌC
## PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH (INTELLIGENT SYSTEM DEVELOPMENT)
### Assignment 02 – End-to-End Machine Learning System Development

> **Học viện Công nghệ Bưu chính Viễn thông – Khoa Công nghệ Thông tin 1**  
> **Họ và tên sinh viên**: Trần Văn Hậu  
> **Mã sinh viên**: B23DCCN287  
> **Lớp**: D23CQCN01-B  
> **Giảng viên hướng dẫn**: PGS. TS. Trần Đình Quế  

---

ASSIGNMENT 02

From Data Representation to Deployable Intelligent Systems

Hà Nội – 2026


# TÓM TẮT

Báo cáo xây dựng ba ứng dụng học máy gồm dự đoán tiểu đường, dự đoán giá nhà và dự đoán khả năng khách hàng khuyến nghị sản phẩm. Mỗi ứng dụng được xây dựng từ dữ liệu lịch sử, biểu diễn dữ liệu phù hợp với bài toán, so sánh nhiều mô hình và triển khai dưới dạng REST API kết hợp giao diện Web và Mobile.



| Application | Prediction/Task | Main Representation |
| --- | --- | --- |
| Diabetes | Phân loại nguy cơ/ kết quả bị tiểu đường | Vector gồm 5 đặc trưng số |
| House Price | Hồi quy giá nhà | Vector đặc trưng số và biến phân loại đã mã hoá |
| Customer Behavior | Phân loại khả năng khuyến nghị sản phẩm | Vector TF – IDF từ Title và Review Text |


Diabetes

Dataset: Pima Indians Diabetes Dataset, gồm 768 quan sát về thông tin sức khỏe và nhãn Outcome

Problem: Bài toán phân loại nhị phân, dự đoán bệnh nhân có khả năng thuộc lớp tiểu đường (1) hay không (0).

Representation: Mỗi bệnh nhân được biểu diễn bằng 5 đặc trưng: Glucose, BMI, Age, Pregnancies và DiabetesPedigreeFunction.

Selected model: Decision Tree.

Main evaluation result: Mô hình đạt Accuracy xấp xỉ 80%, Precision khoảng 71%, Recall khoảng 72%, F1-score khoảng 71% và ROC-AUC khoảng 0.83. Decision Tree được chọn vì có Recall và F1-score tốt nhất trong các mô hình thử nghiệm.

Deployment method: Flask REST API, giao diện Web và ứng dụng Mobile Flutter. Người dùng nhập các chỉ số sức khỏe và hệ thống trả về dự đoán.

House Price

Dataset: Dữ liệu giá nhà với 30,229 quan sát, bao gồm thông tin về diện tích, số phòng, số tầng, tình trạng nội thất, khả năng tiếp cận đường và giá nhà.

Problem: Bài toán hồi quy, dự đoán giá bán nhà.

Representation: Vector đặc trưng gồm Area, Access Road, Floors, Bedrooms, Bathrooms và Furniture state; các biến phân loại được mã hóa trước khi huấn luyện.

Selected model: Random Forest Regressor.

Main evaluation result: Random Forest đạt MAE = 1.4607, RMSE = 1.8478 và R² = 0.2997 trên tập kiểm tra; đây là mô hình có sai số thấp nhất trong các mô hình được so sánh.

Deployment method: Flask REST API, giao diện Web và ứng dụng Mobile Flutter. Người dùng nhập thông tin căn nhà và nhận giá dự đoán.

Customer Behavior

Dataset: Women’s E-Commerce Clothing Reviews Dataset. Sau khi loại các review thiếu nội dung, dữ liệu được dùng để dự đoán nhãn Recommended IND

Problem: Bài toán phân loại nhị phân, dự đoán review có khả năng khuyến nghị sản phẩm (1) hoặc không khuyến nghị (0).

Representation: Ghép Title và Review Text, làm sạch văn bản, sau đó biểu diễn bằng TF-IDF với unigram và bigram.

Selected model: Logistic Regression với class_weight="balanced".

Main evaluation result: Mô hình đạt Accuracy = 87.88%, Precision = 96.31%, Recall = 88.60%, F1-score = 92.29% và ROC-AUC = 0.9403. Mô hình được chọn nhờ ROC-AUC cao nhất, khả năng phân biệt hai lớp tốt và có thể giải thích bằng trọng số từ khóa.

Deployment method: Flask REST API, giao diện Web và ứng dụng Mobile Flutter. Người dùng nhập tiêu đề và nội dung review; hệ thống trả về “Có khả năng khuyến nghị sản phẩm” hoặc “Có khả năng không khuyến nghị sản phẩm”, kèm màu xanh/đỏ để dễ nhận biết.


## Biểu diễn dữ liệu

Ba ứng dụng sử dụng ba dạng dữ liệu khác nhau, nhưng đều tuân theo nguyên tắc: đối tượng thực tế được thu thập thành dữ liệu thô, được làm sạch và chuyển thành biểu diễn số trước khi đưa vào mô hình học máy. Mô hình không xử lý trực tiếp CSV hay câu review; mô hình chỉ nhận vector hoặc ma trận số.



| Ứng dụng | Một quan sát | Dữ liệu thô | Biểu diễn số / đầu vào model |
| --- | --- | --- | --- |
| Diabetes | Một bệnh nhân | CSV gồm các chỉ số lâm sàng | X ∈ R^(768×5): 5 chỉ số số sau tiền xử lý |
| House Price | Một tin/căn nhà | CSV gồm số và category | X: 5 biến số + Furniture state đã one-hot encode |
| Customer Behavior | Một review sản phẩm | Title và Review Text | TF-IDF unigram/bigram; train 18,112×3,500, test 4,529×3,500 |


Với Diabetes, một vector đầu vào có dạng xᵢ = [Glucose, BMI, Age, Pregnancies, DiabetesPedigreeFunction].

Với House Price, các đặc trưng số được xử lý bằng imputation và RobustScaler, còn Furniture state được one-hot encoding.

Với Customer Behavior, Title và Review Text được ghép, chuyển về chữ thường, loại ký tự không phải chữ cái, rồi TF-IDF biến mỗi review thành vector 3,500 trọng số từ/cụm từ.


## Ứng dụng 1 - Dự đoán tiểu đường


### Link github notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/diabetes/notebook/diabetes_prediction.ipynb
Link Kaggle Dataset: https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset


### Mô tả bài toán và dữ liệu

Mục tiêu của ứng dụng là dự đoán bệnh nhân có thuộc lớp Outcome = 1 (có kết quả tiểu đường trong bộ dữ liệu) hay Outcome = 0. Đây là bài toán phân loại nhị phân có giám sát; dự đoán chỉ hỗ trợ sàng lọc và không thay thế chẩn đoán y khoa.



| Thuộc tính | Kiểu | Vai trò / ý nghĩa |
| --- | --- | --- |
| Glucose | Số | Chỉ số glucose; đầu vào |
| BMI | Số | Chỉ số khối cơ thể; đầu vào |
| Age | Số nguyên | Tuổi bệnh nhân; đầu vào |
| Pregnancies | Số nguyên | Số lần mang thai; đầu vào |
| DiabetesPedigreeFunction | Số thực | Chỉ số tiền sử gia đình; đầu vào |
| Outcome | Nhị phân | Target: 0 hoặc 1 |


Nguồn dữ liệu là Pima Indians Diabetes Dataset trên Kaggle. Notebook xác định 768 quan sát, 8 đặc trưng ban đầu và một nhãn Outcome. Sau EDA, năm đặc trưng trên được chọn cho mô hình; Insulin không được chọn vì có nhiều giá trị 0 và mức liên hệ hữu ích thấp hơn trong phân tích của notebook.


### Làm sạch, biểu diễn và EDA

Notebook đã trình bày chi tiết kiểm tra kiểu dữ liệu, giá trị thiếu, bản ghi lặp, phân phối và các giá trị không hợp lý. Các giá trị 0 ở Glucose và BMI không có ý nghĩa sinh lý được xem là thiếu trong pipeline, sau đó được xử lý bằng preprocessor đã lưu. Dữ liệu được chia train/test theo stratification; scaler/imputer chỉ fit trên train để tránh data leakage.


*Hình: Phân phối nhãn Outcome trong bộ dữ liệu Diabetes.*

Quan sát: số bệnh nhân Outcome = 0 lớn hơn Outcome = 1. Hàm ý ML: Accuracy không đủ để đánh giá; Recall và F1-score của lớp tiểu đường cần được xem trọng vì bỏ sót người thuộc lớp 1 có ý nghĩa rủi ro cao.

Biểu diễn dữ liệu

Dữ liệu được chuyển theo luồng: Raw CSV → DataFrame → chọn 5 feature → thay giá trị 0 không hợp lý ở Glucose và BMI thành NaN → median imputation → StandardScaler → X.

Mỗi bệnh nhân i được biểu diễn bởi vector: xᵢ = [Glucoseᵢ, BMIᵢ, Ageᵢ, Pregnanciesᵢ, DiabetesPedigreeFunctionᵢ]ᵀ.

Do đó, trước khi chia dữ liệu: X ∈ R^(768 × 5), y ∈ {0, 1}^768. Mỗi hàng là một bệnh nhân và mỗi cột là một chỉ số sức khỏe.

Sau khi chia stratified 80/20 và áp dụng pipeline chỉ fit trên train: X_train ∈ R^(614 × 5), X_test ∈ R^(154 × 5). Output notebook xác nhận cả train và test đều không còn giá trị NaN. Ma trận này là đầu vào cho toàn bộ model phân loại.


### Phát triển, đánh giá và chọn mô hình

Các mô hình được so sánh trên cùng tập test là Logistic Regression, KNN (K=11), SVM Linear, SVM RBF, Decision Tree và Dummy Classifier làm baseline. Các chỉ số Accuracy, Precision, Recall, F1-score và ROC-AUC được báo cáo theo yêu cầu của bài toán phân loại.



| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Decision Tree | 0.799 | 0.709 | 0.722 | 0.716 | 0.825 |
| SVM RBF | 0.727 | 0.643 | 0.500 | 0.562 | 0.794 |
| KNN (K=11) | 0.714 | 0.614 | 0.500 | 0.551 | 0.794 |
| Logistic Regression | 0.701 | 0.587 | 0.500 | 0.540 | 0.810 |
| SVM Linear | 0.695 | 0.578 | 0.481 | 0.525 | 0.810 |
| Dummy baseline | 0.649 | 0.000 | 0.000 | 0.000 | 0.500 |



*Hình: Kết quả so sánh các mô hình Diabetes trên tập test.*

Decision Tree được chọn để deploy vì có Accuracy, Recall và F1-score cao nhất trong các mô hình được thử nghiệm, đồng thời ROC-AUC = 0.825. Recall 0.722 nghĩa là mô hình nhận diện được khoảng 72.2% bệnh nhân thực sự thuộc lớp Outcome = 1; tuy vậy vẫn cần theo dõi các false negative trong sử dụng thực tế.


### Triển khai

Model và preprocessor được lưu tại thư mục model dưới dạng .sav. Flask API nạp lại preprocessor.sav và Decision Tree trước khi suy luận; endpoint POST /diabetes/v1/predict nhận năm chỉ số và trả về prediction_class, risk_level và confidence khi model hỗ trợ xác suất. Giao diện Web và Mobile Flutter thu thập đúng năm đầu vào này, kiểm tra giá trị hợp lệ rồi gọi REST API.


## Ứng dụng 2 - Dự đoán giá nhà


### Link github notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/house_price/notebook/house_price_prediction.ipynb
Link Kaggle Dataset: https://www.kaggle.com/datasets/ladcva/vietnam-housing-dataset-hanoi/data


### Mô tả bài toán, dữ liệu và biểu diễn

Mỗi hàng của bộ dữ liệu biểu diễn một bất động sản/tin nhà; Price là biến mục tiêu liên tục nên đây là bài toán hồi quy, khác với phân loại Diabetes. Notebook sử dụng dữ liệu house_prices.csv gồm 30,229 quan sát và 12 cột. Sau EDA và chọn feature, đầu vào mô hình gồm Area, Access Road, Floors, Bedrooms, Bathrooms và Furniture state.



| Nhóm | Đặc trưng | Xử lý trong pipeline |
| --- | --- | --- |
| Numerical | Area, Access Road, Floors, Bedrooms, Bathrooms | Median imputation và RobustScaler |
| Categorical | Furniture state | Mode imputation và OneHotEncoder |
| Target | Price | Số liên tục; không encode |


Pipeline chỉ fit median, scaler và encoder trên tập train. Vì Furniture state là biến category, one-hot encoding chuyển trạng thái nội thất thành các chỉ báo 0/1 để có thể ghép cùng các biến số trong feature matrix.

Biểu diễn dữ liệu

Dữ liệu được chuyển theo luồng: Raw CSV → DataFrame → chọn 5 biến số và Furniture state → median imputation + RobustScaler cho biến số → mode imputation + One-Hot Encoding cho Furniture state → X.

Trước preprocessing, X_raw ∈ R^(30229 × 6), y ∈ R^30229. Sáu feature là Area, Access Road, Floors, Bedrooms, Bathrooms và Furniture state; y là Price.

Furniture state có hai giá trị Basic và Full. One-Hot Encoding chuyển feature này thành Furniture state_Basic và Furniture state_Full; vì vậy vector cuối cùng gồm 5 feature số + 2 cột one-hot = 7 chiều.

Kích thước thực tế in từ notebook sau preprocessing là: X_train ∈ R^(24183 × 7), X_test ∈ R^(6046 × 7). Ví dụ vector đã xử lý: [-0.125, 3.0, 1.5, 1.0, 2.0, 0, 1]. Không còn NaN sau preprocessing.


### EDA và ý nghĩa


*Hình: Mối quan hệ giữa diện tích (Area) và giá nhà (Price).*

Quan sát: biểu đồ scatter cho thấy Area có quan hệ dương với Price nhưng các điểm phân tán đáng kể. Diễn giải: diện tích quan trọng nhưng không đủ để quyết định giá nhà. Hàm ý ML: cần kết hợp số tầng, số phòng, khả năng tiếp cận đường và trạng thái nội thất; mô hình phi tuyến có thể phù hợp hơn mô hình tuyến tính đơn giản.


### Phát triển, đánh giá và chọn mô hình

Các mô hình hồi quy được so sánh trên tập test: Linear Regression, Ridge Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor và Dummy Regressor baseline. MAE, MSE và RMSE càng thấp càng tốt; R² càng cao càng tốt.



| Model | MAE | MSE | RMSE | R² | Thời gian (s) |
| --- | --- | --- | --- | --- | --- |
| Random Forest Regressor | 1.4607 | 3.4144 | 1.8478 | 0.2997 | 1.4253 |
| Gradient Boosting Regressor | 1.4933 | 3.4346 | 1.8533 | 0.2956 | 3.9962 |
| Decision Tree Regressor | 1.5069 | 3.6170 | 1.9018 | 0.2582 | 0.0842 |
| Linear Regression | 1.6189 | 3.9102 | 1.9774 | 0.1981 | 0.0168 |
| Ridge Regression | 1.6190 | 3.9103 | 1.9774 | 0.1980 | 0.0090 |
| Dummy baseline | 1.8438 | 4.8760 | 2.2082 | 0.0000 | 0.0015 |



*Hình: So sánh hiệu năng các mô hình hồi quy giá nhà.*

Random Forest Regressor được chọn vì có MAE và RMSE thấp nhất, đồng thời R² cao nhất trong các mô hình so sánh. R² = 0.2997 cho thấy mô hình còn nhiều biến thiên giá chưa giải thích được; kết quả phù hợp để tham khảo nhưng chưa phải định giá chính thức.


### Triển khai

Preprocessor và năm model hồi quy được lưu dưới dạng .sav. Endpoint POST /house-price/v1/predict nhận năm giá trị số và Furniture state, chạy preprocessor đã lưu rồi trả predicted_price. Web và Mobile Flutter sử dụng cùng tập trường đầu vào, hiển thị giá ước lượng và thông báo đây chỉ là giá tham khảo.


## Ứng dụng 3 - Hành vi khách hàng thương mại điện tử


### Link github notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/customer_behavior/notebook/customer_behavior.ipynb
Link Kaggle Dataset: https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews


### Bài toán, dữ liệu và target

Bộ dữ liệu Womens Clothing E-Commerce Reviews gồm 23,486 review. Mỗi quan sát là một review sản phẩm, không phải hồ sơ dài hạn của một khách hàng vì dữ liệu không có Customer ID. Bài toán có giám sát được chọn là dự đoán Recommended IND: review có khả năng khuyến nghị sản phẩm (1) hoặc không khuyến nghị (0).



| Trường | Vai trò trong bài toán |
| --- | --- |
| Title, Review Text | Nguồn text cho mô hình TF-IDF |
| Recommended IND | Target nhị phân 0/1 |
| Rating, Positive Feedback Count, Age | Dùng để EDA và diễn giải hành vi |
| Division/Department/Class Name | Category dùng để phân tích danh mục |



### Làm sạch, biểu diễn văn bản và EDA

Cột index Unnamed: 0 đã được loại vì không mang ý nghĩa hành vi. Các dòng thiếu Review Text bị loại trước khi huấn luyện; Title thiếu được thay bằng chuỗi rỗng khi ghép văn bản. Sau làm sạch có 22,641 mẫu: lớp khuyến nghị 18,540 mẫu (81.9%) và lớp không khuyến nghị 4,101 mẫu (18.1%), tương ứng tỷ lệ mất cân bằng xấp xỉ 4.6:1.


*Hình: Phân phối nhãn Recommended IND trong E-commerce reviews.*

Hàm ý ML: mô hình chỉ tối ưu Accuracy có thể thiên về lớp khuyến nghị. Notebook áp dụng class_weight='balanced' cho các mô hình phù hợp và báo cáo thêm Precision, Recall, F1-score, ROC-AUC cùng confusion matrix.

Chuỗi biến đổi text là: Title + Review Text → lower-case → loại ký tự không phải chữ cái → chuẩn hóa khoảng trắng → TF-IDF (unigram và bigram). Vectorizer được fit trên train 18,112 review, tạo ma trận 18,112×3,500; test gồm 4,529×3,500. Mỗi chiều là trọng số TF-IDF của một unigram hoặc bigram trong từ điển 3,500 feature.

Biểu diễn dữ liệu văn bản

Dữ liệu được chuyển theo luồng: Title + Review Text → Full_Text → lower-case → loại ký tự không phải chữ cái → chuẩn hóa khoảng trắng → TF-IDF unigram/bigram → X.

Sau khi loại các review thiếu Review Text, dữ liệu có 22,641 mẫu. Mỗi review i được biểu diễn bởi vector TF-IDF: xᵢ = [wᵢ₁, wᵢ₂, ..., wᵢ₃₅₀₀], trong đó wᵢⱼ là trọng số TF-IDF của unigram/bigram thứ j.

Ma trận và target có dạng: X ∈ R^(22641 × 3500), y ∈ {0, 1}^22641. Nhãn 1 là review khuyến nghị sản phẩm; nhãn 0 là review không khuyến nghị.

Notebook chia stratified 80/20 và fit TF-IDF chỉ trên train, tạo X_train ∈ R^(18112 × 3500) và X_test ∈ R^(4529 × 3500). Đây là ma trận thưa 3,500 chiều đưa vào Logistic Regression, Naive Bayes, SVM, SGD, Decision Tree và Random Forest.


### Phát triển, đánh giá và chọn mô hình

Sáu mô hình được so sánh: Logistic Regression Balanced, Linear SVM Balanced, Multinomial Naive Bayes, SGD Classifier Balanced Log, Decision Tree và Random Forest Balanced. Multinomial Naive Bayes có F1-score và Recall lớp khuyến nghị cao nhất; Logistic Regression được chọn cho triển khai vì ROC-AUC cao nhất và có hệ số TF-IDF diễn giải được.



| Model | Accuracy (%) | Precision (%) | Recall (%) | F1 (%) | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Multinomial Naive Bayes | 88.05 | 89.40 | 96.90 | 93.00 | 0.9322 |
| Random Forest Balanced | 87.57 | 93.53 | 91.13 | 92.31 | 0.9091 |
| Logistic Regression Balanced | 87.88 | 96.31 | 88.60 | 92.29 | 0.9403 |
| SGD Classifier Balanced Log | 87.75 | 96.41 | 88.33 | 92.19 | 0.9402 |
| Linear SVM Balanced | 86.97 | 94.70 | 89.08 | 91.80 | 0.9233 |
| Decision Tree | 78.01 | 91.09 | 81.07 | 85.79 | 0.7038 |



*Hình: So sánh F1-score, Recall và ROC của sáu mô hình Customer Behavior.*

Với Logistic Regression Balanced, confusion matrix trên test cho thấy mô hình dự đoán đúng 694/820 review không khuyến nghị và 3,286/3,709 review khuyến nghị. Do đó, mô hình có Recall khoảng 84.6% cho lớp 0 và 88.6% cho lớp 1; kết quả vẫn cần được theo dõi vì precision của lớp không khuyến nghị thấp hơn lớp khuyến nghị.


*Hình: Các từ khóa TF-IDF có trọng số dương và âm cao của Logistic Regression.*

Các hệ số không phải là cảm xúc tuyệt đối của từ. Hệ số dương làm tăng log-odds dự đoán lớp khuyến nghị, còn hệ số âm làm giảm log-odds đó. Các từ liên quan return/returned/returning xuất hiện trong nhóm âm, gợi ý trải nghiệm hoàn trả hoặc không hài lòng là tín hiệu hữu ích cho lớp không khuyến nghị.


### Diễn giải nghiệp vụ và triển khai

EDA cho thấy Rating liên hệ rất mạnh với hành vi khuyến nghị: tỷ lệ recommend tăng rõ khi rating tăng. Các Department/Class có nhiều review nhất phản ánh mức quan tâm trong phạm vi dữ liệu review, không phải doanh số. Positive Feedback Count có phân phối lệch phải; các review cực trị có thể là phản hồi quan trọng nên không bị xóa tự động.

API lưu và nạp tfidf_vectorizer.sav cùng logistic_regression.sav. Endpoint POST /recommendation/v1/predict nhận Title (tùy chọn) và Review Text (bắt buộc), áp dụng đúng hàm clean_text khi inference, rồi trả về thông điệp 'Có khả năng khuyến nghị sản phẩm' hoặc 'Có khả năng không khuyến nghị sản phẩm' cùng probability khi có. Web/Mobile hiển thị kết quả theo màu xanh/đỏ để dễ hiểu.


## So sánh ba hệ thống thông minh



| Khía cạnh | Diabetes | House Price | Customer Behavior |
| --- | --- | --- | --- |
| Loại bài toán | Phân loại nhị phân | Hồi quy | Phân loại nhị phân |
| Một quan sát | Bệnh nhân | Căn nhà/tin nhà | Review sản phẩm |
| Target | Outcome | Price | Recommended IND |
| Dạng dữ liệu | Số dạng bảng | Số + categorical | Text + metadata |
| Biểu diễn | 5 feature số | Encoded/scaled feature vector | TF-IDF 3,500 chiều |
| Model deploy | Decision Tree | Random Forest Regressor | Logistic Regression Balanced |
| Metric chính | Recall, F1, ROC-AUC | MAE, RMSE, R² | F1, Recall, ROC-AUC |
| Hạn chế | Dữ liệu nhỏ; false negative | R² thấp; thiếu feature vị trí | Mất cân bằng lớp; không có Customer ID |


Ba bộ dữ liệu khác nhau như thế nào?

Diabetes là dữ liệu y tế dạng bảng, mỗi dòng là một bệnh nhân với các chỉ số lâm sàng.

House Price là dữ liệu bất động sản, mỗi dòng là một căn nhà/tin đăng với đặc trưng vật lý và trạng thái nội thất.

Customer Behavior là dữ liệu review thương mại điện tử, mỗi dòng là một review sản phẩm gồm metadata và văn bản. Vì vậy, Customer Behavior có dữ liệu text phức tạp hơn hai bộ dữ liệu còn lại.

Biểu diễn dữ liệu khác nhau như thế nào?

Diabetes được biểu diễn bằng vector gồm 5 đặc trưng số: Glucose, BMI, Age, Pregnancies và DiabetesPedigreeFunction.

House Price được biểu diễn bằng vector kết hợp biến số đã scale với Furniture state đã one-hot encoding.

Customer Behavior ghép Title và Review Text, làm sạch văn bản rồi chuyển thành vector TF-IDF 3,500 chiều; đây là ma trận thưa có số chiều cao hơn đáng kể.

Những bước tiền xử lý nào là chung?

Cả ba ứng dụng đều kiểm tra kiểu dữ liệu, giá trị thiếu, bản ghi trùng lặp, giá trị không hợp lệ và outlier. Dữ liệu đều được chia train/test trước khi fit các bước tiền xử lý. Preprocessor hoặc vectorizer chỉ được fit trên tập train, sau đó lưu lại và tái sử dụng trong API để tránh data leakage và bảo đảm inference nhất quán.

Những bước tiền xử lý nào mang tính riêng cho từng ứng dụng?

Diabetes xử lý các giá trị 0 không hợp lý về mặt sinh lý, đặc biệt ở Glucose và BMI.

House Price dùng median imputation, RobustScaler cho biến số và one-hot encoding cho Furniture state.

Customer Behavior loại review thiếu Review Text, thay Title thiếu bằng chuỗi rỗng, chuẩn hóa chữ thường/khoảng trắng, loại ký tự không cần thiết và dùng TF-IDF unigram–bigram; đồng thời dùng class_weight='balanced' do nhãn bị mất cân bằng.

Vì sao biểu diễn target khác nhau?

Diabetes và Customer Behavior có target rời rạc gồm hai lớp nên là bài toán phân loại: Outcome ∈ {0,1} và Recommended IND ∈ {0,1}.

House Price có target Price là giá trị số liên tục nên là bài toán hồi quy. Sự khác biệt này quyết định loại model và metric: phân loại dùng Accuracy, Precision, Recall, F1-score, ROC-AUC; hồi quy dùng MAE, MSE, RMSE và R².

Vì sao cần các metric đánh giá khác nhau?

Diabetes và Customer Behavior là bài toán phân loại nên cần Accuracy, Precision, Recall, F1-score và ROC-AUC để đánh giá khả năng phân biệt từng lớp. Với Diabetes, Recall đặc biệt quan trọng vì cần giảm số bệnh nhân có nguy cơ bị dự đoán nhầm là không mắc bệnh. Với Customer Behavior, dữ liệu mất cân bằng nên Accuracy đơn lẻ không phản ánh đầy đủ hiệu năng; F1-score, Recall và ROC-AUC cần được xem xét thêm.

House Price là bài toán hồi quy với target liên tục nên dùng MAE, MSE, RMSE và R². MAE/RMSE đo mức sai lệch giữa giá thực tế và giá dự đoán, còn R² đo mức độ biến thiên của giá được mô hình giải thích.

Hệ thống nào dễ triển khai nhất?

Diabetes là hệ thống dễ triển khai nhất. Đầu vào chỉ gồm năm biến số, pipeline xử lý đơn giản gồm thay giá trị không hợp lý, imputation và scaling; mô hình Decision Tree có chi phí suy luận thấp và kết quả dễ diễn giải. Giao diện Web/Mobile cũng đơn giản vì người dùng chỉ cần nhập các chỉ số sức khỏe.

House Price cần xử lý thêm category Furniture state, còn Customer Behavior cần làm sạch văn bản và chạy TF-IDF trước khi dự đoán, nên phức tạp hơn.

Hệ thống nào đòi hỏi tính toán nhiều nhất?

Customer Behavior là hệ thống đòi hỏi tính toán nhiều nhất. Mỗi review được chuyển thành vector TF-IDF 3,500 chiều; tập train có kích thước 18,112 x 3,500. Việc xây dựng từ điển TF-IDF, biến đổi text và huấn luyện trên ma trận thưa cao chiều tốn tài nguyên hơn các feature vector nhỏ của Diabetes.

House Price có số quan sát lớn hơn (30,229) và Random Forest gồm nhiều cây cũng cần thời gian huấn luyện đáng kể, nhưng đầu vào sau preprocessing chỉ có 7 chiều. Diabetes có 768 quan sát và 5 feature nên có chi phí tính toán thấp nhất.


## Kiến trúc triển khai và suy luận

Cả ba ứng dụng đều triển khai theo cùng một luồng suy luận:

Người dùng → Web/Mobile UI → Flask REST API → Validation → Preprocessor/TF-IDF đã lưu → Model .sav → JSON response → Giao diện



| Ứng dụng | Endpoint | Artifact đã lưu | Kết quả trả về |
| --- | --- | --- | --- |
| Diabetes | POST /diabetes/v1/predict | preprocessor.sav + decision_tree.sav | Lớp dự đoán, mức rủi ro, confidence |
| House Price | POST /house-price/v1/predict | preprocessor.sav + random_forest_regressor.sav | Predicted price |
| Customer | POST /recommendation/v1/predict | tfidf_vectorizer.sav + logistic_regression.sav | Khuyến nghị/không khuyến nghị, probability |


Việc nạp đúng preprocessor/vectorizer đã fit ở giai đoạn train là bắt buộc. Nếu fit lại scaler, encoder hoặc TF-IDF trên input người dùng hay test set, biểu diễn sẽ khác với giai đoạn huấn luyện và tạo data leakage hoặc kết quả suy luận không nhất quán.

Ví dụ:

Request:

POST /recommendation/v1/predict

Content-Type: application/json

{

"Title": "Love this dress",

"Review Text": "I love this dress. It fits perfectly and the fabric is comfortable."

}

Response:

{

"message": "Kết quả được dự đoán từ nội dung review và chỉ mang tính tham khảo.",

"model": "logistic_regression",

"model_label": "Logistic Regression (khuyến nghị)",

"prediction_class": 1,

"recommendation": "Có khả năng khuyến nghị sản phẩm",

"recommendation_probability": 98.61,

"result_level": "positive"

}


## Web Application


### Web Application — Diabetes

Framework: Flask REST API + HTML/CSS/JavaScript

Endpoint: POST /diabetes/v1/predict

Input: Glucose, BMI, Age, Pregnancies, DiabetesPedigreeFunction; model là tùy chọn và mặc định là decision_tree.

Validation rules: JSON phải là object; không thiếu trường bắt buộc; các giá trị phải là số hữu hạn; Glucose, BMI và Age > 0; Pregnancies và DiabetesPedigreeFunction ≥ 0.

Preprocessing used: convert_invalid_zero_to_nan cho Glucose/BMI → median imputation → StandardScaler, bằng preprocessor.sav đã fit trên train.

Loaded model: preprocessor.sav + decision_tree.sav.

Output: model, model_label, prediction_class, risk_level, prediction và confidence.

Example request:

{
  "Glucose": 140,
  "BMI": 32,
  "Age": 45,
  "Pregnancies": 2,
  "DiabetesPedigreeFunction": 0.5
}

Example response:

{
  "prediction_class": 0,
  "risk_level": "low",
  "prediction": "Nguy cơ thấp tiểu đường theo mô hình",
  "confidence": 54.76
}


*Hình: Giao diện nhập chỉ số sức khoẻ*


*Hình: Giao diện kết quả dự đoán*


*Hình: Giao diện kết quả dự đoán*


### Web Application — House Price

Framework: Flask REST API + HTML/CSS/JavaScript

Endpoint: POST /house-price/v1/predict

Input: Area, Access Road, Floors, Bedrooms, Bathrooms, Furniture state; model là tùy chọn và mặc định là random_forest_regressor.

Validation rules: JSON phải là object; không thiếu trường bắt buộc; năm feature số phải hữu hạn và > 0; Furniture state chỉ nhận Basic hoặc Full; model phải thuộc danh sách model đã nạp.

Preprocessing used: median imputation + RobustScaler cho năm feature số; most-frequent imputation + OneHotEncoder cho Furniture state, bằng preprocessor.sav đã fit trên train.

Loaded model: preprocessor.sav + random_forest_regressor.sav.

Output: model, model_label, predicted_price, predicted_price_display và message.

Example request:

{
  "Area": 80,
  "Access Road": 3,
  "Floors": 2,
  "Bedrooms": 3,
  "Bathrooms": 2,
  "Furniture state": "Full"
}

Example response:

{
  "model": "random_forest_regressor",
  "predicted_price": 4.6875,
  "predicted_price_display": "4.69 tỷ VNĐ",
  "message": "Giá dự đoán chỉ mang tính tham khảo, không phải giá thẩm định chính thức."
}


*Hình: Giao diện nhập đặc trưng căn nhà*


*Hình: Giao diện kết quả giá dự đoán*


### Web Application — Customer Behavior

Framework: Flask REST API + HTML/CSS/JavaScript

Endpoint: POST /recommendation/v1/predict

Input: Title là tùy chọn; Review Text là bắt buộc; model là tùy chọn và mặc định là logistic_regression.

Validation rules: JSON phải là object; Review Text không được trống; model phải hợp lệ; nội dung sau clean_text phải còn ký tự chữ cái hợp lệ.

Preprocessing used: Ghép Title và Review Text → lower-case → loại ký tự không phải chữ cái → chuẩn hóa khoảng trắng → tfidf_vectorizer.sav.transform().

Loaded model: tfidf_vectorizer.sav + logistic_regression.sav.

Output: model, model_label, prediction_class, recommendation, result_level, recommendation_probability và message.

Example request:

{
  "Title": "Love this dress",
  "Review Text": "I love this dress. It fits perfectly and the fabric is comfortable."
}

Example response:

{
  "prediction_class": 1,
  "recommendation": "Có khả năng khuyến nghị sản phẩm",
  "result_level": "positive",
  "recommendation_probability": 98.61
}


*Hình: Giao diện nhập Title và Review*


*Hình: Giao diện kết quả dự đoán*


## Mobile Application


### Mobile Application — Diabetes

Framework: Flutter (Dart), sử dụng package http để gọi REST API.

Platform: Android. Khi chạy Android Emulator, base URL mặc định là http://10.0.2.2:5000; khi chạy trên điện thoại thật, người dùng thay bằng LAN IP của máy chạy Flask.

Input screen: Glucose, BMI, Tuổi, Số lần mang thai, Diabetes Pedigree Function và lựa chọn mô hình.

API endpoint: POST /diabetes/v1/predict.

Validation: kiểm tra biểu mẫu trước khi gửi; Glucose, BMI và Tuổi phải > 0; Pregnancies và Diabetes Pedigree Function phải >= 0.

Prediction display: Card màu đỏ cho nguy cơ cao hoặc xanh cho nguy cơ thấp; hiển thị nhãn dự đoán, mô hình và confidence.


*Hình: Giao diện nhập thông tin*


*Hình: Giao diện kết quả*


### Mobile Application — House Price

Framework: Flutter (Dart), sử dụng package http để gọi REST API.

Platform: Android. Base URL mặc định trên Android Emulator là http://10.0.2.2:5000; điện thoại thật sử dụng LAN IP của máy chạy Flask.

Input screen: Area, Access Road, Floors, Bedrooms, Bathrooms, Furniture state và lựa chọn mô hình.

API endpoint: POST /house-price/v1/predict.

Validation: năm đầu vào số phải là số hợp lệ và > 0; Furniture state chỉ nhận Basic hoặc Full.

Prediction display: Card màu xanh hiển thị giá dự đoán theo tỷ VNĐ và tên mô hình đã dùng.


*Hình: Giao diện nhập thông tin*


*Hình: Giao diện kết quả dự đoán*


### Mobile Application — Customer Behavior

Framework: Flutter (Dart), sử dụng package http để gọi REST API.

Platform: Android. Base URL mặc định trên Android Emulator là http://10.0.2.2:5000; điện thoại thật sử dụng LAN IP của máy chạy Flask.

Input screen: Title (tùy chọn), Review Text (bắt buộc) và lựa chọn mô hình.

API endpoint: POST /recommendation/v1/predict.

Validation: Review Text không được rỗng trước khi gửi request; lỗi API được hiển thị trên giao diện.

Prediction display: Card xanh cho “Có khả năng khuyến nghị sản phẩm”, đỏ cho “Có khả năng không khuyến nghị sản phẩm”; hiển thị mô hình và xác suất khuyến nghị.


*Hình: Giao diện nhập thông tin*


*Hình: Giao diện dự đoán kết quả*


## Khả năng tái lập, thảo luận và hạn chế

Các notebook cố định random_state = 42 ở các bước chính, lưu model/preprocessor/vectorizer, và mã nguồn API, Web, Mobile được tổ chức theo từng ứng dụng trong thư mục Assigned_2. Để tái lập, cần dùng đúng CSV nguồn Kaggle, chạy notebook theo thứ tự để tạo artifact .sav, sau đó chạy REST_API.py và mở Web/Mobile client.

Diabetes: dataset nhỏ và mô hình có thể bỏ sót một phần người thuộc lớp Outcome = 1; không dùng kết quả thay cho khám chuyên khoa.

House Price: R² của model tốt nhất còn thấp; cần thêm thông tin vị trí, pháp lý, mặt tiền và đặc trưng thị trường để cải thiện dự đoán.

Customer Behavior: target là hành vi ở cấp review, không phải hồ sơ khách hàng theo thời gian; nhãn mất cân bằng và text có thể chứa thiên lệch ngôn ngữ.

Nếu có thêm thời gian, hướng cải thiện gồm thu thập dữ liệu mới hơn, tuning siêu tham số bằng validation/cross-validation, theo dõi hiệu năng sau triển khai, thêm ảnh chụp kiểm thử Web/Mobile vào phần phụ lục và đánh giá fairness/robustness của hệ thống.


## Final Comparative Discussion

Phần “So sánh ba hệ thống thông minh” ở trên đã trả lời các câu hỏi chung về sự khác biệt dữ liệu, biểu diễn, tiền xử lý, target, metric, khả năng triển khai và chi phí tính toán. Bảng dưới đây chỉ tổng hợp các kết quả đó theo cùng một khuôn so sánh và bổ sung các điểm còn cần nêu rõ.


### Chất lượng dữ liệu khác nhau trực tiếp dẫn đến rủi ro khác nhau:

Diabetes cần nhận diện số 0 không có ý nghĩa sinh lý

House Price chịu ảnh hưởng bởi missing values, outlier và thiếu biến vị trí

Customer Behavior chịu ảnh hưởng bởi review thiếu, dữ liệu text nhiễu và mất cân bằng nhãn. Vì vậy, không thể dùng một pipeline tiền xử lý duy nhất cho cả ba ứng dụng.


### Model tốt nhất không chỉ được chọn theo một con số.

Decision Tree được chọn cho Diabetes vì có ROC-AUC cao nhất trong thí nghiệm và dễ diễn giải;

Random Forest Regressor có MAE/RMSE thấp nhất cho House Price;

Logistic Regression Balanced có ROC-AUC cao nhất cho Customer Behavior và còn cho phép giải thích trọng số từ TF-IDF.

Cả ba model đều được lưu cùng preprocessor/vectorizer đã fit trên train để API suy luận nhất quán.


### Đặc tính triển khai không hoàn toàn trùng với hiệu năng dự đoán.

Diabetes là đơn giản nhất vì chỉ nhận năm biến số.

House Price cần xử lý thêm biến phân loại

Customer Behavior khó nhất vì phải kiểm tra review, làm sạch text và biến đổi thành vector TF-IDF trước khi dự đoán.

Tuy vậy, ba ứng dụng đều dùng chung mô hình triển khai Flutter/Web → Flask REST API → artifact đã lưu → JSON response.

Data leakage được tránh bằng cách chia train/test trước khi fit imputer, scaler, encoder hoặc TF-IDF; ở giai đoạn triển khai chỉ gọi transform bằng artifact đã lưu, không fit lại trên input người dùng. Các hạn chế riêng và hướng cải thiện tiếp theo đã được trình bày ở phần “Khả năng tái lập, thảo luận và hạn chế” ngay trước mục này.


## Kết luận

Ba ứng dụng minh họa rằng một hệ thống thông minh không chỉ là một mô hình đạt metric tốt. Giá trị của hệ thống đến từ toàn bộ pipeline: dữ liệu được hiểu và làm sạch, biểu diễn thành vector/matrix phù hợp, model được đánh giá đúng metric, artifact được lưu và được dùng nhất quán trong API, Web và Mobile. Kết quả thực nghiệm chọn Decision Tree cho Diabetes, Random Forest Regressor cho House Price và Logistic Regression Balanced cho Customer Behavior; mỗi lựa chọn phản ánh mục tiêu và dạng biểu diễn dữ liệu riêng của bài toán.

Qua quá trình xây dựng ba ứng dụng Diabetes, House Price và Customer Behavior, bài học quan trọng nhất là một hệ thống thông minh không chỉ là mô hình có chỉ số tốt, mà là toàn bộ chuỗi Raw Data → Clean → Represent → Learn → Evaluate → Persist → Deploy. Giá trị thực tế chỉ xuất hiện khi dữ liệu được xử lý phù hợp, biểu diễn đúng cho mô hình, kết quả được đánh giá bằng metric phù hợp và model có thể được sử dụng nhất quán trên Web/Mobile.

Thách thức kỹ thuật quan trọng nhất là bảo đảm pipeline huấn luyện và suy luận giống nhau. Các bước imputation, scaling, one-hot encoding và TF-IDF đều chỉ được fit trên tập train, sau đó lưu thành artifact .sav để API gọi lại khi dự đoán. Điều này giúp tránh data leakage và tránh việc biểu diễn input khi deploy khác với lúc huấn luyện.

Vấn đề biểu diễn dữ liệu quan trọng nhất là mỗi loại dữ liệu cần một cách biểu diễn riêng. Diabetes sử dụng vector gồm các đặc trưng số đã được làm sạch và scale; House Price kết hợp các biến số đã scale với biến nội thất được one-hot encoding; Customer Behavior cần chuyển Title và Review Text thành ma trận TF-IDF thưa 3.500 chiều. Vì vậy, không thể dùng cùng một cách tiền xử lý hoặc cùng một mô hình cho mọi bài toán.

Bài học machine learning quan trọng nhất là lựa chọn model phải dựa trên loại target, cấu trúc dữ liệu và metric đánh giá, không chỉ dựa vào Accuracy. Decision Tree phù hợp cho Diabetes nhờ ROC-AUC tốt và dễ diễn giải; Random Forest Regressor cho sai số thấp nhất ở House Price; Logistic Regression Balanced đạt ROC-AUC cao nhất ở Customer Behavior và có thể giải thích ảnh hưởng của từ khóa. Với dữ liệu mất cân bằng, như Customer Behavior, cần xem thêm F1-score, Recall và ROC-AUC thay vì chỉ dùng Accuracy.

Bài học triển khai quan trọng nhất là API, Web và Mobile phải dùng đúng artifact đã được lưu từ notebook. Các giao diện chỉ thu thập và kiểm tra input, gửi JSON đến Flask REST API, nhận JSON response rồi hiển thị kết quả dễ hiểu cho người dùng. Điều này tách rõ phần giao diện, xử lý dữ liệu và mô hình; đồng thời giúp hệ thống dễ bảo trì và tái sử dụng.

Trong tương lai, hướng cải thiện quan trọng là bổ sung dữ liệu và đặc trưng có ý nghĩa hơn. Với House Price, cần có vị trí chi tiết, thông tin thị trường và đặc trưng công trình để cải thiện R²; với Diabetes cần dữ liệu lớn hơn và đánh giá kỹ hơn các trường hợp nguy cơ bị bỏ sót; với Customer Behavior cần dữ liệu khách hàng theo thời gian hoặc Customer ID để phân tích hành vi dài hạn. Ngoài ra, có thể tuning siêu tham số, cross-validation và theo dõi hiệu năng sau triển khai để kiểm tra độ ổn định của các hệ thống.
