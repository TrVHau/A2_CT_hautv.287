"""
Chapter 2: Xây dựng Đồ thị Tri thức Y tế và Tài chính
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP2_DATA = {
    "chapter_num": 2,
    "chapter_title": "CHƯƠNG 2: XÂY DỰNG ĐỒ THỊ TRI THỨC Y TẾ VÀ TÀI CHÍNH",
    "intro_text": """
Chương này trình bày toàn bộ quy trình thiết kế bản thể học (Ontology), mô hình dữ liệu bộ ba RDF, chứng minh toán học định lý hội tụ của thuật toán suy diễn tiến (Forward Chaining) RDFS/OWL, đại số quan hệ truy vấn SPARQL, và đường ống chuyển đổi dữ liệu dạng bảng lớn thành Đồ thị Tri thức hoàn chỉnh cho hai miền nghiệp vụ: VietnamDiabetesKG và VietnamFinanceKG.
""",
    "sections": [
        {
            "num": "2.1",
            "title": "2.1 Các Thành phần Cấu tạo của Knowledge Graph",
            "text": """
Một Đồ thị Tri thức hoàn chỉnh trong hệ thống được cấu thành từ ba thành phần cơ bản theo đặc tả chuẩn W3C:
1. **Nút Thực thể (Entity Nodes)**: Đại diện cho các đối tượng hoặc khái niệm trừu tượng trong thế giới thực. Mỗi thực thể được gán một Định danh Tài nguyên Đồng nhất (URI), ví dụ `http://ptit.edu.vn/med/Metformin` hoặc `http://ptit.edu.vn/fin/SJC_Gold`. Điều này đảm bảo tính duy nhất trên toàn cầu, tránh sự trùng lặp hoặc hiểu nhầm giữa các khái niệm có cùng tên gọi trong các bối cảnh khác nhau.
2. **Nút Giá trị Hằng số (Literal Nodes)**: Biểu thị các giá trị định lượng hoặc thuộc tính nguyên tử gắn liền với thực thể, bao gồm chuỗi ký tự mô tả, các ngưỡng số học lâm sàng (ví dụ: ngưỡng HbA1c 6.5%, ngưỡng eGFR 30 mL/phút/1.73m^2), hoặc các mức giá đóng cửa thị trường (ví dụ: giá đóng cửa FPT 135.000 đồng). Các literal đều được gắn thẻ kiểu dữ liệu XML Schema (`xsd:string`, `xsd:float`, `xsd:integer`).
3. **Cạnh Quan hệ Ngữ nghĩa (Semantic Relation Edges)**: Nối giữa hai nút thực thể hoặc giữa một nút thực thể với một nút literal. Mỗi cạnh mang một nhãn vị từ (Predicate) xác định ý nghĩa của mối liên kết, tuân thủ nghiêm ngặt theo các tiên đề bản thể học.
"""
        },
        {
            "num": "2.2",
            "title": "2.2 Mô hình Biểu diễn Bộ ba RDF (Resource Description Framework)",
            "text": """
Toàn bộ tri thức của hệ thống được chuẩn hóa theo đặc tả W3C RDF 1.1. Mỗi đơn vị tri thức là một bộ ba (Triple) gồm ba thành phần theo cấu trúc ngữ pháp hình thức:
$$(s, p, o) \\in (\\text{Subject}, \\text{Predicate}, \\text{Object})$$

Trong đó:
- **Chủ từ (Subject - $s$)**: Là thực thể tài nguyên được mô tả, bắt buộc phải là một URI hoặc một nút ẩn danh (Blank Node).
- **Vị từ (Predicate - $p$)**: Là mối quan hệ ngữ nghĩa có hướng từ chủ từ sang đối từ, bắt buộc phải là một URI.
- **Đối từ (Object - $o$)**: Có thể là một thực thể tài nguyên khác (URI), một nút ẩn danh, hoặc một giá trị dữ liệu cụ thể (Literal).

Hệ thống định nghĩa các không gian tên (Namespaces) chuyên biệt:
- `rdf:` (`http://www.w3.org/1999/02/22-rdf-syntax-ns#`): Cung cấp các từ vựng cơ bản như `rdf:type`.
- `rdfs:` (`http://www.w3.org/2000/01/rdf-schema#`): Cung cấp quan hệ kế thừa `rdfs:subClassOf`, `rdfs:subPropertyOf`, định nghĩa miền xác định `rdfs:domain` và miền giá trị `rdfs:range`.
- `owl:` (`http://www.w3.org/2002/07/owl#`): Hỗ trợ các quan hệ bản thể nâng cao như tương đương `owl:equivalentClass` hoặc đối nghịch `owl:disjointWith`.
- `med:` (`http://ptit.edu.vn/med/`): Không gian tên chuyên ngành Y tế Đái tháo đường Típ 2 Việt Nam.
- `fin:` (`http://ptit.edu.vn/fin/`): Không gian tên chuyên ngành Tài chính và Kinh tế Vĩ mô Việt Nam.

Ví dụ về định dạng Turtle chuẩn của một bộ ba thể hiện tương tác nguy hiểm trong y tế:
```turtle
@prefix med: <http://ptit.edu.vn/med/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

med:Metformin med:interactsWith med:Ethanol ;
              med:hasLethalRisk med:LacticAcidosis ;
              rdfs:label "Metformin tương tác nguy hiểm với Rượu bia sinh toan lactic"@vi .
```
"""
        },
        {
            "num": "2.2.1",
            "title": "2.2.1 Ngữ nghĩa Hình thức của Không gian Tên và Phân cấp Thực thể",
            "text": """
Cơ chế Định danh Tài nguyên Đồng nhất (URI) trong đồ thị tri thức đóng vai trò sống còn trong việc ngăn chặn hiện tượng đa nghĩa (Polysemy) và đồng âm khác nghĩa. Trong môi trường y tế và tài chính, một từ viết tắt có thể mang nhiều tầng ý nghĩa trái ngược nhau. Ví dụ: từ "CAP" trong y tế có thể chỉ "Viêm phổi mắc phải tại cộng đồng" (Community-Acquired Pneumonia), trong khi trong tài chính lại chỉ "Giới hạn trần lãi suất" (Interest Rate Cap) hoặc "Vốn hóa thị trường" (Market Capitalization). Nhờ cơ chế không gian tên phân định rõ ràng `med:CAP` và `fin:MarketCap`, hệ thống triệt tiêu hoàn toàn sự nhập nhằng khái niệm ở mức biểu diễn hình thức.

Phân cấp thực thể trong hệ thống được thiết lập theo logic mô tả $\\mathcal{SROIQ}(\\mathcal{D})$:
- Tiên đề Bao hàm Khái niệm (Concept Inclusion Axiom): $C \\sqsubseteq D$ biểu diễn rằng mọi cá thể thuộc lớp $C$ đều là cá thể thuộc lớp $D$. Ví dụ: $\\text{med:Biguanide} \\sqsubseteq \\text{med:Drug}$.
- Tiên đề Không giao nhau (Disjointness Axiom): $C \\sqcap D = \\bot$ biểu diễn hai lớp triệt tiêu lẫn nhau, không thể có thực thể nào đồng thời thuộc cả hai lớp. Ví dụ: $\\text{med:AcuteComplication} \\sqcap \\text{med:ChronicComplication} = \\bot$.
- Tiên đề Giới hạn Thuộc tính (Role Quantification): Khai báo miền xác định $\\exists R.\\top \\sqsubseteq C$ và miền giá trị $\\top \\sqsubseteq \\forall R.D$, đảm bảo quan hệ vị từ $R$ chỉ được phép nối từ thực thể kiểu $C$ sang thực thể kiểu $D$.
"""
        },
        {
            "num": "2.3",
            "title": "2.3 Bản thể học (Ontology) và Biểu diễn Tri thức Hình thức",
            "text": """
Bản thể học đóng vai trò là "bộ luật định nghĩa ngữ nghĩa" cho đồ thị tri thức. Nó xác định các lớp đối tượng được phép tồn tại, mối quan hệ kế thừa hình cây giữa các lớp, và các ràng buộc logic áp đặt lên các thuộc tính dựa trên logic mô tả Description Logic.

**1. Bản thể học Y tế (VietnamDiabetesKG)**:
Hệ thống xây dựng 23 lớp bản thể phân cấp chặt chẽ, xếp dưới lớp gốc `med:MedicalEntity`:
- `med:Disease`: Lớp bệnh lý (thực thể tiêu biểu: `med:Type2Diabetes`, `med:Prediabetes`).
- `med:Symptom`: Lớp triệu chứng (ví dụ: `med:Polyuria` - tiểu nhiều, `med:Polydipsia` - khát nhiều, `med:Polyphagia` - ăn nhiều, `med:WeightLoss` - sụt cân).
- `med:DrugClass`: Lớp nhóm thuốc dược lý (gồm `med:Biguanide`, `med:SGLT2Inhibitor`, `med:DPP4Inhibitor`, `med:Sulfonylurea`, `med:Thiazolidinedione`, `med:GLP1RA`, `med:InsulinRegimen`).
- `med:Drug`: Lớp dược chất cụ thể (thực thể: `med:Metformin`, `med:Dapagliflozin`, `med:Empagliflozin`, `med:Gliclazide`, `med:Sitagliptin`, `med:Linagliptin`).
- `med:Complication`: Lớp biến chứng lâm sàng (chia thành biến chứng cấp tính `med:AcuteComplication` gồm hạ đường huyết, nhiễm toan lactic; và biến chứng mạn tính `med:ChronicComplication` như bệnh thận ĐTĐ, bệnh thần kinh ngoại biên, biến chứng mắt võng mạc, bàn chân ĐTĐ).
- `med:LabTest`: Lớp xét nghiệm cận lâm sàng (thực thể: `med:HbA1cTest`, `med:FPGTest`, `med:OGTTTest`, `med:eGFRTest`, `med:CreatinineTest`, `med:UACRTest`).
- `med:Contraindication`: Lớp tình trạng chống chỉ định lâm sàng tuyệt đối và tương đối.
- `med:FoodItem`: Lớp thực phẩm trong chế độ dinh dưỡng (thực thể: `med:ChickenBreast`, `med:WhiteRice`, `med:BrownRice`, `med:EthanolBeverage`).
- `med:ClinicalTarget`: Lớp mục tiêu kiểm soát (ví dụ: mục tiêu HbA1c < 7.0%, đường huyết đói 80-130 mg/dL).
- `med:PatientProfile`: Lớp hồ sơ bệnh nhân điện tử.

Mạng lưới quan hệ y tế gồm **17 vị từ chính**: `med:indicatedFor`, `med:contraindicatedWith`, `med:hasSideEffect`, `med:interactsWith`, `med:requiresRenalAdjustment`, `med:targetHbA1c`, `med:prescribedInStep`, `med:hasNutritionalComposition`, `med:contraindicatedWhenEGFRBelow`, `med:hasLethalRisk`, `med:interactionSeverity`, `med:clinicalWarning`, `med:hasCardioRenalBenefit`, `med:diagnosticCutoff`, `med:belongsToClass`, `med:hasComplication`, `med:lifestyleAdvice`.

**2. Bản thể học Tài chính (VietnamFinanceKG)**:
Gồm 16 lớp thực thể tài chính vĩ mô và doanh nghiệp phân cấp dưới `fin:FinancialEntity`:
- `fin:MonetaryPolicy`: Chính sách tiền tệ (lãi suất điều hành, cung tiền M2, can thiệp bán ngoại hối).
- `fin:MacroIndicator`: Chỉ số vĩ mô (chỉ số DXY, lạm phát CPI, tỷ giá USD/VND, lãi suất liên ngân hàng O/N).
- `fin:CommodityAsset`: Lớp hàng hóa kim loại quý (thực thể: `fin:SJC_Bullion`, `fin:World_Gold_Ounce`).
- `fin:StockEquity`: Lớp cổ phiếu doanh nghiệp niêm yết (thực thể: `fin:FPT`, `fin:VNM`, `fin:HPG`, `fin:VCB`).
- `fin:MarketIndex`: Chỉ số thị trường (thực thể: `fin:VN30_Index`, `fin:VN_Index`).
- `fin:RegulatoryDecree`: Văn bản quy phạm pháp luật (thực thể: `fin:Decree_24_2012`, `fin:Decree_232_2025`).

Các quan hệ tài chính được thiết kế đặc thù là các quan hệ nhân quả có hướng có dấu:
- `fin:causesPositive`: Tác động cùng chiều (A tăng làm B tăng, A giảm làm B giảm, trọng số dấu $+1$).
- `fin:causesNegative`: Tác động ngược chiều (A tăng làm B giảm, A giảm làm B tăng, trọng số dấu $-1$).
- `fin:regulates`: Quan hệ điều tiết pháp lý của cơ quan quản lý nhà nước.
- `fin:benchmarks`: Quan hệ định chuẩn tham chiếu giá quy đổi.
- `fin:affectsCostOfCapital`: Quan hệ tác động chi phí vốn doanh nghiệp.
- `fin:influencesEarnings`: Quan hệ ảnh hưởng biên lợi nhuận ròng.
"""
        },
        {
            "num": "2.3.1",
            "title": "2.3.1 Thuật toán Suy diễn Tiến trên RDF và Chứng minh Định lý Hội tụ",
            "text": """
Một trong những ưu thế vượt trội nhất của Đồ thị Tri thức so với cơ sở dữ liệu quan hệ truyền thống là khả năng suy luận tự động nhằm phát hiện ra các tri thức mới chưa từng được khai báo tường minh trong cơ sở dữ liệu ban đầu. Hệ thống triển khai động cơ suy diễn tiến (Forward Chaining Engine) áp dụng 4 quy tắc bao hàm chuẩn của W3C RDF Schema:

1. **Quy tắc Miền xác định (rdfs2 - Domain Entailment)**:
   $$\\frac{(p, \\text{rdfs:domain}, C), \\quad (x, p, y)}{(x, \\text{rdf:type}, C)}$$
2. **Quy tắc Miền giá trị (rdfs3 - Range Entailment)**:
   $$\\frac{(p, \\text{rdfs:range}, C), \\quad (x, p, y)}{(y, \\text{rdf:type}, C)}$$
3. **Quy tắc Bắc cầu của Thuộc tính con (rdfs7 - SubProperty Entailment)**:
   $$\\frac{(p_1, \\text{rdfs:subPropertyOf}, p_2), \\quad (x, p_1, y)}{(x, p_2, y)}$$
4. **Quy tắc Kế thừa Lớp (rdfs9 - SubClass Entailment)**:
   $$\\frac{(C_1, \\text{rdfs:subClassOf}, C_2), \\quad (x, \\text{rdf:type}, C_1)}{(x, \\text{rdf:type}, C_2)}$$

**Chứng minh Toán học Định lý Hội tụ Điểm Bất động (Fixed-Point Convergence Theorem)**:
- *Bổ đề*: Cho không gian các đồ thị con $\\mathcal{P}(\\mathcal{U})$ trên vũ trụ bộ ba Herbrand hữu hạn $\\mathcal{U} = (\\mathcal{E} \\cup \\mathcal{B}) \\times \\mathcal{R} \\times (\\mathcal{E} \\cup \\mathcal{B} \\cup \\mathcal{L})$. Định nghĩa toán tử suy diễn tiến $\\mathcal{T}: \\mathcal{P}(\\mathcal{U}) \\to \\mathcal{P}(\\mathcal{U})$:
  $$\\mathcal{T}(\\mathcal{G}) = \\mathcal{G} \\cup \\{t \\in \\mathcal{U} \\mid \\mathcal{G} \\vdash_{\\text{RDFS}} t\\}$$
- *Tính Đơn điệu (Monotonicity)*: Dễ thấy với mọi $\\mathcal{G}_A \\subseteq \\mathcal{G}_B$, nếu một bộ ba $t$ được suy ra từ $\\mathcal{G}_A$ bởi các tiền đề của rdfs2, rdfs3, rdfs7, rdfs9 thì các tiền đề đó cũng tồn tại trong $\\mathcal{G}_B$. Do đó $\\mathcal{T}(\\mathcal{G}_A) \\subseteq \\mathcal{T}(\\mathcal{G}_B)$.
- *Tính Bị chặn trên (Boundedness)*: Vì vũ trụ thực thể $|\\mathcal{V}| = N$ và số vị từ $|\\mathcal{R}| = M$ là hữu hạn, tổng số bộ ba tối đa có thể tồn tại trong vũ trụ là $|\text{Triples}| \\le N^2 \\cdot M < \\infty$.
- *Kết luận*: Theo Định lý Điểm Bất động Knaster-Tarski, dãy lặp:
  $$\\mathcal{G}_0 \\subseteq \\mathcal{G}_1 = \\mathcal{T}(\\mathcal{G}_0) \\subseteq \\mathcal{G}_2 = \\mathcal{T}(\\mathcal{G}_1) \\subseteq \\dots$$
  chắc chắn phải dừng sau một số bước hữu hạn $k \\le N^2 \\cdot M$, tại đó $\\mathcal{T}(\\mathcal{G}_k) = \\mathcal{G}_k = \\mathcal{G}^*$. Trạng thái $\\mathcal{G}^*$ là bao đóng suy diễn đóng kín (Deductive Closure) duy nhất của đồ thị tri thức.
"""
        },
        {
            "num": "2.3.2",
            "title": "2.3.2 Truy vấn SPARQL và Đại số Quan hệ Đồ thị",
            "text": """
Hệ thống sử dụng ngôn ngữ truy vấn SPARQL (SPARQL Protocol and RDF Query Language) tiêu chuẩn để trích xuất tri thức hình thức. Cốt lõi của SPARQL là phép so khớp mẫu đồ thị cơ sở (Basic Graph Pattern - BGP Matching) trên đại số quan hệ đồ thị:
- Toán tử BGP: Ánh xạ một tập các biến số $\\mu: \\text{Vars} \\to \\mathcal{E} \\cup \\mathcal{L}$ thỏa mãn toàn bộ các bộ ba trong mẫu đồ thị.
- Toán tử Join ($\\bowtie$): Kết hợp hai phép so khớp có chung biến số.
- Toán tử Filter ($\\sigma_R$): Giữ lại các bộ lời giải thỏa mãn biểu thức logic $R$.

Dưới đây là 5 truy vấn SPARQL chuyên sâu đại diện cho các tác vụ nghiệp vụ quan trọng trong hệ thống:
1. **Truy vấn Q1 (Lethal Drug Interaction)**: Phát hiện tương tác chết người giữa Metformin và Ethanol thông qua việc truy vết vị từ `med:hasLethalRisk` và lọc điều kiện `FILTER (?drugA = med:Metformin && ?drugB = med:Ethanol)`.
2. **Truy vấn Q2 (Dual Therapy Selection)**: Tìm kiếm các thuốc kết hợp bước 2 có lợi ích kép bảo vệ tim mạch và thận khi HbA1c vượt mục tiêu.
3. **Truy vấn Q3 (Renal Contraindications)**: Quét toàn bộ danh mục thuốc có thuộc tính `med:requiresRenalAdjustment true`, sắp xếp giảm dần theo ngưỡng lọc cầu thận an toàn `med:contraindicatedWhenEGFRBelow`.
4. **Truy vấn Q4 (Fed Rate Shock Propagation)**: Khám phá chuỗi truyền dẫn đa chặng từ chính sách tiền tệ Mỹ đến phần bù giá vàng SJC trong nước.
5. **Truy vấn Q5 (Exchange Rate Impact)**: Phân tích mức độ tổn thương của các mã cổ phiếu xuất nhập khẩu (FPT, HPG, VNM) trước biến động của tỷ giá USD/VND.
"""
        },
        {
            "num": "2.3.3",
            "title": "2.3.3 Kiểm tra Ràng buộc và Tính Nhất quán Lâm sàng / Kinh tế",
            "text": """
Đồ thị Tri thức giải quyết dứt điểm các lỗi logic ngớ ngẩn thường gặp của mô hình ngôn ngữ thông qua hệ thống Ràng buộc Nhất quán (Consistency Constraint Validator):
1. **Ràng buộc Lâm sàng Tuyệt đối (Absolute Clinical Constraints)**:
   - *Ràng buộc Thận đối với Metformin*: Nếu hồ sơ bệnh nhân ghi nhận $\\text{eGFR} < 30\\text{ mL/phút/1.73m}^2$, hệ thống kích hoạt ràng buộc cứng:
     $$\\forall p \\in \\text{Patients}: (p, \\text{hasEGFR}, v) \\land (v < 30) \\implies \\neg (p, \\text{prescribedWith}, \\text{Metformin})$$
     Mọi kế hoạch điều trị vi phạm ràng buộc này đều bị hệ thống chặn đứng ở tầng logic trước khi chuyển sang bước tổng hợp ngôn ngữ.
   - *Ràng buộc Thận đối với thuốc ức chế SGLT2*: Nếu $\\text{eGFR} < 20\\text{ mL/phút/1.73m}^2$, hệ thống ngăn chặn chỉ định mới của Dapagliflozin / Empagliflozin do hiệu quả hạ đường huyết của thuốc qua đường bài tiết nước tiểu bị mất hoàn toàn tại ngưỡng này.
2. **Ràng buộc Tính Nhất quán Kinh tế Vĩ mô**:
   - Mọi chu trình nhân quả trong VietnamFinanceKG đều được kiểm tra tính triệt tiêu hoặc cộng hưởng dấu. Nếu một chuỗi suy luận tạo ra mâu thuẫn dấu (ví dụ: lãi suất tăng đồng thời dẫn đến chi phí vốn rẻ hơn), hệ thống sẽ cảnh báo lỗi cấu trúc bản thể để chuyên gia hiệu chỉnh lại quan hệ.
"""
        },
        {
            "num": "2.3.4",
            "title": "2.3.4 Bản thể học Mở rộng: Đa dạng Sinh học và Đồng chuyển hóa trong Y tế",
            "text": """
Trong thực tiễn điều trị tại các bệnh viện Việt Nam, bệnh nhân đái tháo đường típ 2 hiếm khi xuất hiện như một bệnh lý đơn lẻ thuần túy mà thường nằm trong bối cảnh phức tạp của **Hội chứng Chuyển hóa (Metabolic Syndrome)** với các bệnh đồng mắc (Co-morbidities) nghiêm trọng:
- Tăng huyết áp nguyên phát (`med:Hypertension`): Chiếm hơn 70% bệnh nhân đái tháo đường tại Việt Nam, làm gia tăng gấp đôi nguy cơ đột quỵ và biến cố tim mạch.
- Rối loạn lipid máu (`med:Dyslipidemia`): Đặc trưng bởi tăng triglycerid, giảm HDL-C và tăng các hạt LDL-C nhỏ đậm đặc gây xơ vữa động mạch sớm.
- Bệnh gan thoái hóa mỡ không do rượu (`med:NAFLD`): Thúc đẩy tình trạng đề kháng insulin tại gan trầm trọng hơn.
- Bệnh thận mạn tính do đái tháo đường (`med:DiabeticKidneyDisease - DKD`): Là nguyên nhân hàng đầu dẫn tới suy thận giai đoạn cuối phải chạy thận nhân tạo chu kỳ.

Bản thể học VietnamDiabetesKG mã hóa các mối quan hệ đồng mắc này thông qua vị từ `med:hasComorbidityRisk` và `med:sharedRiskFactor`. Nhờ đó, khi tác tử đánh giá một bệnh nhân, nó không chỉ nhìn vào một chỉ số HbA1c đơn lẻ mà thực hiện một đánh giá toàn diện về nguy cơ tim mạch - thận - chuyển hóa (Cardio-Renal-Metabolic Continuum) để đưa ra khuyến nghị phối hợp thuốc tối ưu.
"""
        },
        {
            "num": "2.3.5",
            "title": "2.3.5 Bản thể học Mở rộng: Cấu trúc Rổ Chỉ số VN30 và Trọng số Vốn hóa",
            "text": """
Chỉ số VN30 là chỉ số giá đại diện cho 30 doanh nghiệp niêm yết có giá trị vốn hóa và thanh khoản hàng đầu trên Sở Giao dịch Chứng khoán TP.HCM (HOSE), chiếm hơn 75% giá trị vốn hóa và 60% giá trị giao dịch của toàn thị trường chứng khoán Việt Nam.

Công thức tính chỉ số VN30 được mã hóa trong VietnamFinanceKG tuân thủ quy tắc định lượng:
$$\\text{VN30-Index}_t = \\frac{\\sum_{i=1}^{30} P_{i, t} \\times Q_{i, t} \\times f_{i, t} \\times c_{i, t}}{\\text{Hệ số chia cơ sở } D_t} \\times 1000$$
Trong đó:
- $P_{i, t}$ là giá thị trường của cổ phiếu $i$ tại thời điểm $t$.
- $Q_{i, t}$ là khối lượng cổ phiếu đang lưu hành của doanh nghiệp $i$.
- $f_{i, t}$ là tỷ lệ cổ phiếu tự do chuyển nhượng (Free-float Ratio), loại bỏ các cổ phiếu bị hạn chế chuyển nhượng do Nhà nước hoặc cổ đông sáng lập nắm giữ dài hạn.
- $c_{i, t} = 10\\%$ là hệ số giới hạn tỷ trọng vốn hóa (Capping Ratio), nhằm đảm bảo không có bất kỳ một cổ phiếu đơn lẻ nào (như VCB hay HPG) có thể thao túng hoặc chi phối quá 10% biến động của toàn bộ rổ chỉ số.
- $D_t$ là hệ số chia được điều chỉnh kỹ thuật khi có các sự kiện doanh nghiệp (chia tách cổ phiếu, trả cổ tức bằng cổ phiếu, phát hành thêm) để đảm bảo tính liên tục của đường chỉ số.
"""
        },
        {
            "num": "2.4",
            "title": "2.4 Xây dựng Cơ sở Tri thức (KB) và Đồ thị (KG) từ Dữ liệu Bảng Lớn",
            "text": """
Thách thức lớn trong thực tiễn là dữ liệu nghiệp vụ thường nằm ở dạng bảng quan hệ hoặc file CSV (hồ sơ bệnh án điện tử, dữ liệu phiên giao dịch chứng khoán). Để đưa vào đồ thị tri thức, hệ thống thiết kế đường ống ETL (Extract - Transform - Load) bán tự động:

- **Chuyển đổi 96.128 Hồ sơ Bệnh nhân**: Mỗi dòng trong file `diabetes_prediction_dataset.csv` đại diện cho một cá thể bệnh nhân duy nhất. Một thuật toán sinh đồ thị tự động chuyển đổi mỗi hàng thành một thực thể `med:PatientProfile_XXXXX`, sau đó liên kết các đặc trưng thành các bộ ba RDF:
  - `(PatientProfile_XXXXX, rdf:type, med:PatientProfile)`
  - `(PatientProfile_XXXXX, med:hasAge, "55"^^xsd:integer)`
  - `(PatientProfile_XXXXX, med:hasBMI, "27.4"^^xsd:float)`
  - `(PatientProfile_XXXXX, med:hasHbA1c, "7.2"^^xsd:float)`
  - `(PatientProfile_XXXXX, med:hasSmokingHistory, "former"^^xsd:string)`
  Quá trình này tạo ra hơn **961.280 bộ ba RDF** định lượng, cho phép hệ thống thực hiện các truy vấn thống kê dân số học hoặc tìm các bệnh nhân tương đồng bằng ngôn ngữ SPARQL chuẩn.
- **Chuyển đổi 2.932 Phiên Giao dịch Thị trường (2015 - 2026)**: Tương tự, dữ liệu chuỗi thời gian OHLCV của 7 tài sản được ánh xạ thành các nút sự kiện phiên giao dịch `fin:TradingSession_YYYYMMDD`, lưu giữ giá đóng cửa, khối lượng, tỷ lệ biến động và mối liên hệ chéo giữa các chỉ số vĩ mô.
"""
        },
        {
            "num": "2.5",
            "title": "2.5 So sánh Chi tiết: Graph Database và Vector Database",
            "text": """
Hiện nay trong cộng đồng kỹ thuật AI có nhiều tranh luận về việc nên sử dụng Cơ sở Dữ liệu Đồ thị (Graph Database) hay Cơ sở Dữ liệu Vector (Vector Database). Nghiên cứu này khẳng định: Đây không phải là hai công nghệ đối đầu triệt tiêu nhau, mà là hai mặt bổ trợ của cùng một vấn đề:

- **Bản chất lưu trữ**: Graph DB lưu trữ các thực thể và quan hệ rõ ràng dưới dạng bộ ba hoặc nút/cạnh có nhãn. Vector DB lưu trữ các mảng số thực nhiều chiều (Embeddings) đại diện cho tọa độ ngữ nghĩa của đoạn văn bản.
- **Khả năng suy luận đa bước (Multi-hop Reasoning)**: Graph DB có khả năng duyệt đường đi nhiều chặng ($k$-hops) với độ chính xác tuyệt đối thông qua phép toán duyệt đồ thị BFS/DFS hoặc câu truy vấn Cypher/SPARQL. Trong khi đó, Vector DB chỉ có thể tìm kiếm độ tương đồng cục bộ quanh một điểm vector, hoàn toàn bất lực khi cần suy luận bắc cầu qua 3-4 nút trung gian.
- **Tính giải thích được (Explainability)**: Kết quả của Graph DB là một đường đi hình học minh bạch gồm các thực thể và vị từ rõ ràng. Kết quả của Vector DB là một con số tương đồng cosin trừu tượng không thể giải thích tại sao hai đoạn văn lại gần nhau.
- **Chi phí cập nhật**: Graph DB cập nhật với chi phí $O(1)$ cho mỗi cạnh mới. Vector DB đòi hỏi phải chạy qua mô hình nhúng nơ-ron để sinh vector mới và tái cấu trúc cây chỉ mục xấp xỉ lân cận (HNSW/IVF).

Hệ thống giải quyết bài toán này bằng cách **hợp nhất cả hai**: Sử dụng Graph DB làm bộ xương sống logic kiểm soát tính đúng đắn và suy luận quan hệ, đồng thời sử dụng Vector DB làm công cụ tìm kiếm ngữ nghĩa linh hoạt trên văn bản phi cấu trúc.
"""
        }
    ]
}
