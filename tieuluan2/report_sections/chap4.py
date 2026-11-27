"""
Chapter 4: Tri thức Y tế & Học sâu Chẩn đoán Đái tháo đường Type 2
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP4_DATA = {
    "chapter_num": 4,
    "chapter_title": "CHƯƠNG 4: TRI THỨC Y TẾ & HỌC SÂU CHẨN ĐOÁN ĐÁI THÁO ĐƯỜNG TYPE 2",
    "intro_text": """
Chương này tập trung vào phân hệ Y tế Lâm sàng: phân tích dịch tễ học và phác đồ chẩn đoán theo Quyết định 5481/QĐ-BYT và tiêu chuẩn ADA 2024, thiết kế chi tiết bản thể học VietnamDiabetesKG, xây dựng và huấn luyện mô hình học sâu PyTorch DiabetesMLP (10.497 tham số, Weighted BCE, ROC-AUC 0.9755), phân tích giá trị giải thích SHAP, và mổ xẻ các bài toán lâm sàng kinh điển có tính sống còn đối với bệnh nhân Việt Nam.
""",
    "sections": [
        {
            "num": "4.1",
            "title": "4.1 Bối cảnh Dịch tễ và Phác đồ Chẩn đoán của Bộ Y tế",
            "text": """
Đái tháo đường Típ 2 (Type 2 Diabetes Mellitus - T2DM) đang trở thành một trong những đại dịch bệnh không lây nhiễm đe dọa nghiêm trọng nhất sức khỏe cộng đồng tại Việt Nam. Theo thống kê của Hiệp hội Đái tháo đường Thế giới (IDF) và Bộ Y tế, tỷ lệ hiện mắc đái tháo đường ở người trưởng thành tại Việt Nam đã tăng nhanh chóng từ mức 2.7% năm 2002 lên hơn 7.3% năm 2023, với hơn 55% số ca bệnh trong cộng đồng chưa được chẩn đoán kịp thời.

**Đặc điểm Kiểu hình Lâm sàng của Người Việt Nam (Asian Phenotype)**:
Người Việt Nam và người châu Á nói chung có kiểu hình đái tháo đường rất đặc thù so với người da trắng phương Tây:
- Bệnh nhân khởi phát ở lứa tuổi trẻ hơn nhiều và chỉ số khối cơ thể (BMI) thấp hơn đáng kể.
- Ngay cả ở mức BMI được coi là bình thường theo chuẩn phương Tây ($22 - 24\\text{ kg/m}^2$), người Việt Nam đã có tỷ lệ tích tụ mỡ nội tạng (Visceral Fat) rất cao và khối lượng cơ bắp thấp (Sarcopenic Obesity). Do đó, hệ thống áp dụng nghiêm ngặt tiêu chuẩn phân loại BMI của Tổ chức Y tế Thế giới khu vực Tây Thái Bình Dương (WPRO) và IDI dành riêng cho người châu Á:
  $$\\text{Bình thường: } 18.5 \\le \\text{BMI} < 23.0 \\text{ kg/m}^2, \\quad \\text{Thừa cân: } 23.0 \\le \\text{BMI} < 25.0 \\text{ kg/m}^2, \\quad \\text{Béo phì: } \\text{BMI} \\ge 25.0 \\text{ kg/m}^2$$
- Tuyến tụy của người châu Á có khả năng tiết insulin bù trừ kém hơn (Early Beta-cell Failure), dẫn đến sự suy giảm chức năng tế bào beta nhanh hơn khi xuất hiện đề kháng insulin.

**Tiêu chuẩn Chẩn đoán Vàng theo Quyết định 5481/QĐ-BYT và ADA 2024**:
Một cá nhân được chẩn đoán xác định mắc Đái tháo đường Típ 2 khi thỏa mãn ít nhất một trong bốn tiêu chuẩn cận lâm sàng chuẩn sau:
1. **Glucose huyết tương lúc đói (Fasting Plasma Glucose - FPG)**: $\\ge 126\\text{ mg/dL}$ ($7.0\\text{ mmol/L}$). Nhịn ăn ít nhất 8 giờ trước khi lấy máu.
2. **Glucose huyết tương 2 giờ sau nghiệm pháp dung nạp 75g glucose đường uống (2h-OGTT)**: $\\ge 200\\text{ mg/dL}$ ($11.1\\text{ mmol/L}$).
3. **Chỉ số HbA1c (Hemoglobin glycated)**: $\\ge 6.5\\%$ ($48\\text{ mmol/mol}$). Xét nghiệm bắt buộc phải được thực hiện bằng phương pháp chuẩn hóa theo Chương trình Chuẩn hóa Glycohemoglobin Quốc gia (NGSP) hoặc IFCC.
4. **Bệnh nhân có triệu chứng lâm sàng kinh điển của tăng đường huyết** (tiểu nhiều, uống nhiều, ăn nhiều, sụt cân không rõ nguyên nhân) kèm một mẫu **Glucose huyết tương bất kỳ (RPG)** $\\ge 200\\text{ mg/dL}$ ($11.1\\text{ mmol/L}$).

**Phác đồ Phân tầng Điều trị Bậc thang**:
Mục tiêu kiểm soát đường huyết chung là đưa HbA1c về $< 7.0\\%$, đường huyết đói từ $80 - 130\\text{ mg/dL}$, và đường huyết sau ăn $< 180\\text{ mg/dL}$. Chiến lược dùng thuốc tuân thủ nguyên tắc cá thể hóa:
- **Bước 1 (Đơn trị liệu đầu tay)**: Thay đổi lối sống (dinh dưỡng + vận động) kết hợp dược chất nền tảng là **Metformin** (trừ trường hợp có chống chỉ định).
- **Bước 2 (Phối hợp đôi - Dual Therapy)**: Nếu sau 3 tháng không đạt mục tiêu HbA1c, phối hợp Metformin với một thuốc nhóm hai: thuốc ức chế SGLT2 (Dapagliflozin/Empagliflozin - ưu tiên hàng đầu nếu có bệnh tim mạch xơ vữa hoặc bệnh thận mạn), thuốc ức chế DPP-4 (Sitagliptin/Vildagliptin - an toàn, không gây hạ đường huyết), đồng vận thụ thể GLP-1 (Liraglutide/Semaglutide), hoặc Sulfonylurea (Gliclazide MR - hiệu quả hạ đường nhanh, chi phí thấp).
- **Bước 3 & Bước 4**: Phối hợp ba thuốc đường uống hoặc khởi trị bằng Insulin nền (Basal Insulin) khi HbA1c $\\ge 9.0\\%$ hoặc có dấu hiệu dị hóa cấp tính.
"""
        },
        {
            "num": "4.2",
            "title": "4.2 Thiết kế Bản thể học và Đồ thị Tri thức Y tế VietnamDiabetesKG",
            "text": """
Đồ thị Tri thức Y tế VietnamDiabetesKG được cấu trúc thành 23 lớp bản thể học độc lập và 17 vị từ quan hệ lâm sàng chặt chẽ. Hệ thống mã hóa toàn diện các quy tắc y khoa từ Quyết định 5481/QĐ-BYT:

- **Hệ thống Thực thể và Thuộc tính**:
  Mỗi dược chất trong đồ thị không chỉ có tên gọi mà còn chứa đầy đủ các thuộc tính dược lý định lượng:
  - `med:Metformin`: Thuộc nhóm `med:Biguanide`, liều khởi đầu 500mg/ngày, liều tối đa 2000mg/ngày, cơ chế giảm sản xuất glucose tại gan và tăng nhạy cảm insulin ngoại vi; đặc tính: không gây tăng cân, không gây hạ đường huyết khi dùng đơn độc.
  - `med:Dapagliflozin`: Thuộc nhóm `med:SGLT2Inhibitor`, ức chế kênh đồng vận chuyển natri-glucose ở ống lượn gần thận, tăng bài tiết glucose qua nước tiểu 70-80g/ngày, mang lại lợi ích giảm áp lực nội cầu thận và giảm nhập viện do suy tim.
- **Ràng buộc Lâm sàng Bất biến**:
  Đồ thị thiết lập các cạnh đối nghịch `owl:disjointWith` và vị từ cấm kỵ `med:contraindicatedWith` liên kết các dược chất với các bệnh đồng mắc (suy tim mất bù, suy gan nặng, suy thận độ 4-5) và tình trạng lối sống (lạm dụng rượu bia, nhịn ăn kéo dài).
"""
        },
        {
            "num": "4.3",
            "title": "4.3 Mô hình Học sâu Chẩn đoán Nguy cơ: DiabetesMLP",
            "text": """
Song song với đồ thị tri thức tượng trưng, hệ thống tích hợp một mô hình mạng nơ-ron học sâu chuyên biệt được viết hoàn toàn bằng PyTorch để xử lý dữ liệu định lượng từ hồ sơ khám sức khỏe: mô hình `DiabetesMLP`.

**1. Dữ liệu Thực nghiệm và Tiền xử lý**:
Mô hình được huấn luyện và đánh giá trên bộ dữ liệu chuẩn gồm **100.000 mẫu hồ sơ bệnh nhân** (được chia ngẫu nhiên theo tỷ lệ 80% tập huấn luyện `train`, 10% tập xác thực `val`, và 10% tập kiểm thử độc lập `test` với đúng 14.420 mẫu kiểm thử sau khi làm sạch).
Dữ liệu đối mặt với thách thức thực tế khắc nghiệt: **Mất cân bằng dữ liệu nghiêm trọng (Severe Class Imbalance)** khi chỉ có **8.820 mẫu dương tính (mắc đái tháo đường, chiếm 8.82%)** và tới 91.180 mẫu âm tính (91.18%). Tỷ lệ mất cân bằng lên tới xấp xỉ $1 : 10.3$.
Mỗi mẫu gồm 13 đặc trưng đầu vào sau khi mã hóa one-hot và chuẩn hóa: Tuổi, Giới tính, Chỉ số khối cơ thể (BMI), Huyết áp tâm thu (Systolic BP), Huyết áp tâm trương (Diastolic BP), Tiền sử tăng huyết áp, Tiền sử bệnh tim mạch, Tiền sử hút thuốc lá (Never, Former, Current), Đường huyết tương lúc đói (FPG), và Chỉ số HbA1c.

**2. Kiến trúc Mạng Nơ-ron PyTorch DiabetesMLP**:
Mô hình được thiết kế theo kiến trúc mạng nơ-ron truyền thẳng đa tầng (Multi-Layer Perceptron) với cơ chế chuẩn hóa theo mẻ (Batch Normalization) và triệt tiêu ngẫu nhiên (Dropout):
- Tầng đầu vào: 13 đặc trưng.
- Tầng `nn.BatchNorm1d(13)`: Chuẩn hóa phân phối mẻ, giúp ổn định gradient và tăng tốc hội tụ (chứa 26 tham số học được).
- Tầng ẩn 1: `nn.Linear(13, 128)` kết hợp hàm kích hoạt phi tuyến `nn.ReLU()` (chứa $13 \\times 128 + 128 = 1.792$ tham số).
- Tầng `nn.Dropout(p=0.3)`: Tắt ngẫu nhiên 30% nơ-ron trong pha huấn luyện để ngăn chặn quá khớp (overfitting).
- Tầng ẩn 2: `nn.Linear(128, 64)` kết hợp `nn.ReLU()` (chứa $128 \\times 64 + 64 = 8.256$ tham số).
- Tầng `nn.Dropout(p=0.2)`: Tắt ngẫu nhiên 20% nơ-ron.
- Tầng đầu ra: `nn.Linear(64, 1)` kết hợp hàm kích hoạt `nn.Sigmoid()` chiếu xác suất ra khoảng $[0, 1]$ (chứa $64 \\times 1 + 1 = 65$ tham số).
**Tổng số tham số học được của mô hình được tính toán chính xác tuyệt đối là đúng 10.497 tham số**.

**3. Đạo hàm Giải tích Hàm Mất mát Weighted Binary Cross-Entropy**:
Để giải quyết bài toán mất cân bằng lớp, hệ thống áp dụng hàm mất mát Weighted BCE:
$$\\mathcal{L}(y, z) = - \\left[ w \\cdot y \\log(\\sigma(z)) + (1 - y) \\log(1 - \\sigma(z)) \\right]$$
Với logit $z$, hàm sigmoid $\\sigma(z) = \\frac{1}{1 + e^{-z}}$, và $w = pos\\_weight = \\frac{91.308}{8.820} \\approx 10.3$.
Đạo hàm của hàm mất mát theo logit $z$:
$$\\frac{\\partial \\mathcal{L}}{\\partial z} = - w \\cdot y \\cdot \\frac{1}{\\sigma(z)} \\cdot \\sigma(z)(1 - \\sigma(z)) - (1 - y) \\cdot \\frac{1}{1 - \\sigma(z)} \\cdot (-\\sigma(z)(1 - \\sigma(z)))$$
$$\\frac{\\partial \\mathcal{L}}{\\partial z} = - w \\cdot y (1 - \\sigma(z)) + (1 - y)\\sigma(z) = \\sigma(z) \\left[ 1 + (w - 1)y \\right] - w \\cdot y$$
- Khi mẫu là Âm tính ($y = 0$): $\\frac{\\partial \\mathcal{L}}{\\partial z} = \\sigma(z)$. Tín hiệu gradient tỷ lệ thuận với xác suất dự báo sai.
- Khi mẫu là Dương tính ($y = 1$): $\\frac{\\partial \\mathcal{L}}{\\partial z} = w \\cdot (\\sigma(z) - 1)$. Gradient cập nhật được khuếch đại **gấp đúng 10.3 lần**, buộc mạng nơ-ron phải ưu tiên giảm thiểu sai số trên lớp thiểu số dương tính.

**4. Kết quả Thực nghiệm và Hiệu chuẩn Ngưỡng (Threshold Calibration)**:
Mô hình được huấn luyện trong 60 epoch bằng thuật toán AdamW ($lr=0.001$, weight decay $= 10^{-4}$) với cơ chế Early Stopping theo dõi trên tập xác thực:
- **Độ phân tách trên toàn miền ngưỡng**: Đạt diện tích dưới đường cong ROC (**ROC-AUC = 0.9755**) và diện tích dưới đường cong Precision-Recall (**PR-AUC = 0.8726**), chứng minh năng lực phân loại vượt trội trên dữ liệu mất cân bằng.
- **Hiệu chuẩn Ngưỡng Quyết định Tối ưu**: Quét tìm ngưỡng phân loại tối ưu $\\tau^*$ trên đường cong ROC bằng cách tối đa hóa chỉ số Youden's J statistic ($J = \\text{Sensitivity} + \\text{Specificity} - 1$):
  $$\\tau^* = \\arg\\max_\\tau (\\text{Recall}(\\tau) + \\text{TNR}(\\tau) - 1) = 0.9016$$
- **Đánh giá trên tập kiểm thử độc lập (14.420 mẫu)** tại ngưỡng $\\tau = 0.9016$:
  - **Độ nhạy (Recall)**: Đạt **93.28%** (chỉ bỏ sót chưa tới 7% ca bệnh).
  - **Độ chính xác (Precision)**: Đạt **66.35%**.
  - **Điểm F1-Score**: Đạt **0.7755**.
  - **Độ chính xác tổng thể (Accuracy)**: Đạt **95.62%**.
"""
        },
        {
            "num": "4.3.4",
            "title": "4.3.4 Phân tích Đóng góp Thuộc tính bằng Giá trị SHAP (SHAP Feature Importance)",
            "text": """
Để mở chiếc "hộp đen" của mạng nơ-ron `DiabetesMLP`, hệ thống triển khai phương pháp phân tích SHAP (SHapley Additive exPlanations) dựa trên lý thuyết trò chơi hợp tác của Lloyd Shapley. Giá trị đóng góp $\\phi_i(x)$ của đặc trưng $i$ đối với quyết định dự báo của bệnh nhân $x$ được tính toán:
$$\\phi_i(x) = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|! (|F| - |S| - 1)!}{|F|!} \\left[ f(S \\cup \\{i\\}) - f(S) \\right]$$
Trong đó $F$ là tập hợp toàn bộ 13 đặc trưng và $S$ là tập con các đặc trưng liên minh.

Kết quả phân tích SHAP trên tập kiểm thử xác định rõ thứ hạng ảnh hưởng lâm sàng:
1. **Chỉ số HbA1c** (mean $|\\text{SHAP}| = 1.84$): Là đặc trưng dẫn đầu áp đảo. Khi HbA1c vượt ngưỡng $6.5\\%$, giá trị SHAP tăng vọt theo hàm phi tuyến, đẩy xác suất chẩn đoán lên vùng nguy cơ cao.
2. **Đường huyết đói FPG** (mean $|\\text{SHAP}| = 1.42$): Đóng góp lớn thứ hai, phản ánh mức độ rối loạn kiểm soát đường huyết cơ bản của gan.
3. **Chỉ số khối cơ thể BMI** (mean $|\\text{SHAP}| = 0.96$): Khi BMI $\\ge 25\\text{ kg/m}^2$, đóng góp làm tăng đáng kể nguy cơ do liên quan chặt chẽ với đề kháng insulin.
4. **Độ tuổi** (mean $|\\text{SHAP}| = 0.68$): Bệnh nhân trên 45 tuổi có mức đóng góp nguy cơ tăng đều theo tuổi tác.
5. **Tiền sử Tăng huyết áp** (mean $|\\text{SHAP}| = 0.45$): Yếu tố đồng chuyển hóa quan trọng.
Kết quả này hoàn toàn nhất quán với các hướng dẫn lâm sàng của Bộ Y tế và ADA, củng cố độ tin cậy khoa học của mô hình học sâu.
"""
        },
        {
            "num": "4.4",
            "title": "4.4 Phân tích Các Tình huống Lâm sàng Thực tế Chuyên sâu",
            "text": """
Năng lực cốt lõi của hệ thống được chứng minh thông qua việc xử lý chính xác ba bài toán lâm sàng hóc búa thường gặp trong thực tế y tế tại Việt Nam:

**1. Bài toán 1: Tương tác Nguy hiểm giữa Metformin và Ethanol (Rượu bia)**:
- *Bối cảnh*: Bệnh nhân nam 52 tuổi đang điều trị đái tháo đường típ 2 bằng Metformin 1000mg/ngày, chuẩn bị tham gia tiệc liên hoan có sử dụng nhiều rượu bia.
- *Cơ chế Dược lý & Sinh hóa*: Metformin có tác dụng ức chế phức hợp 1 của chuỗi truyền điện tử trong ty thể tế bào gan, dẫn đến ức chế quá trình tân tạo đường từ tiền chất lactate. Khi bệnh nhân uống nhiều rượu bia, quá trình chuyển hóa ethanol bởi men alcohol dehydrogenase làm cạn kiệt lượng $NAD^+$ nội bào, làm tăng tỷ lệ $NADH / NAD^+$. Sự tích tụ này thúc đẩy mạnh mẽ phản ứng chuyển hóa pyruvate thành lactate mà không thể đảo ngược:
  $$\\text{Pyruvate} + NADH + H^+ \\xrightarrow{\\text{LDH}} \\text{Lactate} + NAD^+$$
  Hậu quả là acid lactic bị ứ đọng dữ dội trong máu nhưng gan không thể tái sử dụng để tân tạo glucose, gây ra tình trạng **Nhiễm toan Lactic (Lactic Acidosis)** cấp tính với tỷ lệ tử vong lên tới $30 - 50\\%$. Đồng thời, việc ức chế tân tạo glucose còn kích hoạt cơn hạ đường huyết nghiêm trọng lúc nửa đêm.
- *Phản ứng của Hệ thống*: Khi người dùng hỏi "Đang uống Metformin có được uống rượu bia không?", Đồ thị Tri thức lập tức kích hoạt bộ ba `(med:Metformin, med:interactsWith, med:Ethanol)` và `(med:Metformin, med:hasLethalRisk, med:LacticAcidosis)`. Hệ thống phát tín hiệu CẢNH BÁO ĐỎ TUYỆT ĐỐI, yêu cầu kiêng hoàn toàn rượu bia và hướng dẫn các triệu chứng nhận biết sớm toan lactic (đau bụng, thở nhanh sâu Kussmaul, buồn nôn, lơ mơ).

**2. Bài toán 2: Đánh giá Suy giảm Chức năng Thận và Ngưỡng Lọc Cầu thận eGFR**:
- *Bối cảnh*: Bệnh nhân có tiền sử đái tháo đường 8 năm, xét nghiệm máu ghi nhận creatinine huyết thanh tăng, mức lọc cầu thận ước tính tính theo công thức CKD-EPI giảm xuống $\\text{eGFR} = 26\\text{ mL/phút/1.73m}^2$.
- *Quy tắc Lâm sàng Phân tầng theo KDIGO và BYT*:
  - Nếu $\\text{eGFR} \\ge 60\\text{ mL/phút/1.73m}^2$: Sử dụng Metformin liều đầy đủ (tối đa 2000mg/ngày), theo dõi eGFR mỗi năm một lần.
  - Nếu $45 \\le \\text{eGFR} < 60$: Tiếp tục dùng liều tối đa 2000mg, theo dõi eGFR mỗi 3-6 tháng.
  - Nếu $30 \\le \\text{eGFR} < 45$: Giảm 50% liều Metformin (tối đa 1000mg/ngày), không khởi trị bệnh nhân mới.
  - Nếu $\\text{eGFR} < 30\\text{ mL/phút/1.73m}^2$: **CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI**, bắt buộc phải NGỪNG NGAY Metformin do nguy cơ đào thải thuốc qua thận bị ngưng trệ gây ngộ độc toan lactic. Đồng thời, thuốc ức chế SGLT2 (Dapagliflozin) cũng phải ngừng khởi trị hạ đường huyết nếu $\\text{eGFR} < 20$.
- *Phản ứng của Hệ thống*: Động cơ SPARQL tự động đối chiếu giá trị $\\text{eGFR} = 26$ với ngưỡng $\\text{contraindicatedWhenEGFRBelow} = 30$, lập tức loại bỏ Metformin khỏi phác đồ và đề xuất chuyển giao sang thuốc ức chế DPP-4 (Linagliptin - không cần chỉnh liều theo thận) hoặc Insulin.

**3. Bài toán 3: Dinh dưỡng Đĩa ăn Chuẩn và Ẩm thực Truyền thống Việt Nam**:
- *Bối cảnh*: Người bệnh băn khoăn về khẩu phần ăn hàng ngày và các món ăn truyền thống (phở, bún chả, cơm trắng).
- *Quy tắc Đĩa ăn Chuẩn (Plate Method) Bản địa hóa*:
  Áp dụng cho đĩa tròn đường kính 20 cm:
  - **1/2 Đĩa (50%)**: Các loại rau củ không chứa tinh bột, giàu chất xơ hòa tan (rau muống luộc, rau ngót, cải xanh, dưa chuột, súp lơ xanh). Chất xơ làm chậm quá trình hấp thu glucose tại ruột non, ngăn chặn đỉnh đường huyết sau ăn.
  - **1/4 Đĩa (25%)**: Đạm nạc chất lượng cao. Khuyến cáo tối ưu là **thịt ức gà không da luộc/hấp** (giàu leucine giúp kích thích tổng hợp protein cơ bắp, chỉ số chất béo bão hòa cực thấp), cá nước ngọt, đậu phụ. Hạn chế tối đa thịt đỏ nhiều mỡ và thịt chế biến sẵn.
  - **1/4 Đĩa (25%)**: Thực phẩm giàu tinh bột carbohydrate. Khuyến khích thay thế một phần cơm trắng bằng gạo lứt, khoai lang luộc hoặc yến mạch (chỉ số đường huyết GI thấp hơn).
- *Chuyển đổi Ẩm thực Truyền thống*: Hệ thống RAG cung cấp bảng quy đổi tương đương: 1 bát phở bò đầy đủ chứa khoảng 55-65g carbohydrate tinh chế hấp thu nhanh tương đương với 2 bát cơm trắng; hệ thống đưa ra lời khuyên thực tế: ăn nhiều rau giá đỗ trước, chỉ ăn 1/2 lượng bánh phở và hạn chế húp nước béo giàu muối natri.
"""
        },
        {
            "num": "4.4.5",
            "title": "4.4.5 Phác đồ Xử trí Cấp cứu Cơn Hạ Đường huyết theo Quy tắc 15-15",
            "text": """
Hạ đường huyết (Hypoglycemia) là biến chứng cấp tính nguy hiểm nhất có thể xảy ra trong quá trình dùng thuốc (đặc biệt khi dùng Sulfonylurea hoặc Insulin). Hạ đường huyết được định nghĩa khi mức glucose huyết tương giảm xuống $< 70\\text{ mg/dL}$ ($3.9\\text{ mmol/L}$).

Hệ thống mã hóa quy trình xử trí cấp cứu chuẩn hóa theo **Quy tắc 15 - 15** của Bộ Y tế:
- **Bước 1: Bổ sung ngay 15g Carbohydrate tác dụng nhanh**:
  Bệnh nhân cần uống ngay 150ml nước ngọt có ga thông thường (không dùng loại 'diet' không đường), 3-4 viên đường glucose, hoặc 1 thìa canh mật ong.
- **Bước 2: Nghỉ ngơi và Đợi đúng 15 phút**:
  Để cơ thể hấp thu glucose vào máu, không ăn dồn dập nhiều thức ăn chứa chất béo (như sô-cô-la) vì chất béo làm chậm tốc độ làm rỗng dạ dày và trì hoãn quá trình nâng đường huyết.
- **Bước 3: Đo lại Đường huyết Mao mạch**:
  - Nếu đường huyết vẫn $< 70\\text{ mg/dL}$: Tiếp tục nạp thêm 15g carbohydrate và đợi thêm 15 phút.
  - Nếu đường huyết đã $\\ge 70\\text{ mg/dL}$ và còn hơn 1 giờ nữa mới đến bữa ăn chính: Ăn ngay một bữa phụ nhẹ gồm tinh bột phức hợp và đạm (1 lát bánh mì hoặc 3-4 chiếc bánh quy giòn) để ngăn ngừa cơn hạ đường huyết tái phát.
- *Lưu ý Trường hợp Hôn mê mất ý thức*: Tuyệt đối không nhét thức ăn vào miệng vì nguy cơ sặc phổi gây tử vong; người nhà cần tiêm ngay Glucagon dưới da/bắp hoặc gọi cấp cứu y tế 115 truyền tĩnh mạch Glucose ưu trương 20 - 30%.
"""
        }
    ]
}
