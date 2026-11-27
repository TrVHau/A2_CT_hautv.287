# PROJECT 01: HỆ SINH THÁI Y TẾ SỐ HỘI CHẨN ĐA TÁC TỬ & ĐA MÔ HÌNH HỌC MÁY / HỌC SÂU / REINFORCEMENT LEARNING QUẢN LÝ BỆNH ĐÁI THÁO ĐƯỜNG CẤP DOANH NGHIỆP
## (Enterprise Multi-Agent Clinical Council & Multi-Model ML/DL/D3QN Decision Support System for Diabetes Mellitus)

**Môn học:** Phát triển các hệ thống thông minh (Intelligent Systems Development)  
**Học viên thực hiện:** **Trần Văn Hậu** – MSV: **B23DCCN287**  
**Lớp:** **D23CQCN01-B / D23CTPM01-B** — Nhóm môn học: **CT_09**  
**Giảng viên hướng dẫn:** **PGS. TS. Trần Đình Quế**  
**Khoa:** Khoa Công nghệ Thông tin 1 – **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**  
**Kho lưu trữ GitHub:** [https://github.com/TrVHau/A2_CT_hautv.287](https://github.com/TrVHau/A2_CT_hautv.287)  

---

## 📌 1. TỔNG QUAN DỰ ÁN (EXECUTIVE SUMMARY)

Project 01 phát triển một giải pháp y tế số thông minh toàn diện chuyên biệt cho sàng lọc, chẩn đoán, phân tầng nguy cơ và phác đồ điều trị cá nhân hóa bệnh **Đái tháo đường (Diabetes Mellitus)** dựa trên chiến lược **Đa Cohort Lâm Sàng (Multi-Cohort Clinical Framework)** với hơn 100.000 hồ sơ bệnh án chuẩn hóa quốc tế. Hệ thống tích hợp 6 trụ cột công nghệ AI y sinh tiên tiến nhất hiện nay:

1. **Bộ Đôi Cơ Sở Dữ Liệu Lâm Sàng Mở Quốc Tế (Dual-Cohort Provenance)**:
   - **Cohort 2 (Dân số hiện đại - 100.000 hồ sơ)**: Trích xuất từ hồ sơ bệnh án điện tử (EHR) gồm 8 đặc trưng nhân khẩu học và xét nghiệm sinh hóa cốt lõi. Nguồn: [Kaggle Diabetes Prediction Dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset).
   - **Cohort 1 (Dân tộc Pima - 768 hồ sơ)**: Tập dữ liệu chuẩn mực của Viện NIDDK với 8 chỉ số dung nạp glucose và nồng độ insulin huyết thanh. Nguồn: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/34/pima+indians+diabetes) (DOI: `10.24432/C5059P`) & [Kaggle Pima Indians Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database).
   - **Đối chuẩn Cơ sở (Reference Baseline)**: Khảo sát phỏng vấn hành vi CDC BRFSS (253.680 quan sát) qua [Kaggle CDC BRFSS Indicators](https://www.kaggle.com/datasets/alexteb/diabetes-health-indicators-dataset).
2. **Suite 9 Kiến Trúc Mô Hình AI & Đối Chuẩn Độc Lập**:
   - Triển khai và đối chuẩn 9 mô hình: **TabResNet Attention** (Đạt đỉnh ROC-AUC **0.9793**), **Super Stacking Meta-Learner** (ROC-AUC **0.9790**), **Gradient Tree Boosting** (GBDT), **Random Forest** (100 cây), **Deep Learning MLP**, **1D-CNN Biomarker Filter**, **Recurrent LSTM**, **Decision Tree** và **Logistic Regression**.
   - Chứng minh toán học đẳng hình qua thuật toán **Pure NumPy Scratch MLP** đối chuẩn chéo với PyTorch & Scikit-Learn với sai số hội tụ tuyệt đối $\Delta = 0.0025 < 0.0050$.
3. **Huấn Luyện Tăng Cường Can Thiệp Lối Sống (Reinforcement Learning Lifestyle Coach)**:
   - Kiến trúc mạng nơ-ron học tăng cường kép sâu **Dueling Double Deep Q-Network (D3QN)** kết hợp bộ nhớ ưu tiên **Prioritized Experience Replay (PER)** và **Tabular Q-Learning**.
   - Không gian hành động gồm 24 quyết định can thiệp dinh dưỡng (giảm calo, kiểm soát carbohydrate) và thể lực, tối ưu hàm thưởng cân bằng giữa giảm $\text{HbA1c}$ và mức độ tuân thủ của bệnh nhân.
4. **Đồ Thị Tri Thức Y Khoa ADA 2024 & Graph-RAG**:
   - Đồ thị tri thức chuẩn hóa 44 thực thể và 45 mối quan hệ lâm sàng đa chiều tuân thủ tiêu chuẩn ADA 2024 / KDIGO / ACC/AHA (biến chứng võng mạc, thận mạn CKD, tim mạch ASCVD, phác đồ Metformin, SGLT2i, GLP-1 RA, Insulin và chống chỉ định eGFR).
   - Cơ chế truy hồi tăng cường đồ thị (Graph-RAG) đạt độ chính xác thực tế **94.2%**, vượt trội so với tìm kiếm vector đơn thuần (**68.4%**).
5. **Hội Đồng Lâm Sàng 12 Tác Tử Y Khoa (DiaMulti-Agent Council)**:
   - Mô hình điều phối tuần tự kết hợp song song giữa 12 tác tử chuyên biệt, phản biện tự động (Self-Evaluation Reflection Critic), kiểm toán công bằng nhân khẩu học (Fairness Auditor) và dược lý gen cá nhân hóa (Pharmacogenomics).
6. **Báo Cáo Khoa Học & Ấn Phẩm Trực Quan 36 Biểu Đồ (300 DPI)**:
   - Toàn bộ 36 biểu đồ trực quan hóa y sinh độ phân giải cao 300 DPI được nhúng trực tiếp trong báo cáo khoa học Word (`Bao_Cao_Project01_CT_09_Hautv.287.docx` dung lượng 6.07 MB) và báo cáo Markdown chi tiết.

---

## 🏛️ 2. HỘI ĐỒNG LÂM SÀNG 12 TÁC TỬ (12-AGENT COUNCIL ARCHITECTURE)

Hội đồng lâm sàng phối hợp 12 tác tử chuyên biệt thông qua điều phối viên `DiaCouncilCoordinator`:

| STT | Tác tử (Agent Name) | Vai trò lâm sàng & Chức năng kỹ thuật | Đầu vào chính | Đầu ra / Khuyến nghị |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `DiaTriage-Agent` | Tiếp đón, phân loại lâm sàng ban đầu & phát hiện nguy cơ cấp cứu | Dấu hiệu sinh tồn, Glucose cấp, Tuổi | Tầng ưu tiên (Cấp cứu/Cao/Vừa/Thấp) |
| **2** | `DiaDiagnostic-Agent` | Chẩn đoán đồng thuận từ 9 mô hình AI & trích xuất xác suất | 8-9 chỉ số sinh hóa & nhân khẩu | Xác suất mắc bệnh, Mô hình đồng thuận |
| **3** | `DiaGraph-Agent` | Tra cứu phác đồ ADA 2024 & phát hiện chống chỉ định qua KG | Bệnh nền, Chỉ số thận eGFR | Khuyến nghị thuốc bậc 1/2, Chống chỉ định |
| **4** | `DiaTherapy-Agent` | Thiết lập phác đồ dược lý và dinh dưỡng lâm sàng (MNT) | Chẩn đoán, Mục tiêu HbA1c, Dị ứng | Đơn thuốc cá nhân hóa, Chế độ ăn MNT |
| **5** | `DiaCritic-Agent` | Phản biện, thẩm định an toàn đa chiều (Self-Evaluation Critic) | Đề xuất từ Tác tử 2, 3, 4 | Phê duyệt / Bác bỏ / Điều chỉnh liều |
| **6** | `DiaSafetyRules-Agent` | Hàng rào 12 quy tắc an toàn tất định (R1-R12, Hard Guardrails) | Mức đường huyết, Chức năng thận | Cảnh báo hạ đường huyết, Suy thận cấp |
| **7** | `DiaFairnessAuditor-Agent` | Kiểm toán công bằng nhân khẩu học & hiệu chuẩn xác suất (ECE) | Giới tính, Nhóm tuổi, Dự báo AI | Điểm tin cậy, Đánh giá sai lệch nhóm |
| **8** | `DiaLongitudinalTracker-Agent`| Theo dõi quỹ đạo bệnh án 4 tuần & cảnh báo biến thiên | Lịch sử HbA1c & Glucose theo tuần | Xu hướng tiến triển, Điều chỉnh mục tiêu |
| **9** | `DiaPharmacogenomics-Agent` | Phân tích dược lý gen (CYP2C9, OCT1) & chuyển hóa thuốc | Hồ sơ gen, Kiểu chuyển hóa enzyme | Cảnh báo tương tác gen-thuốc, Liều tối ưu |
| **10** | `DiaCounterfactual-Agent` | Lập luận phản thực tế tối thiểu (Actionable Recourse) | Trọng số mô hình, Ngưỡng quyết định | Can thiệp tối thiểu đưa nguy cơ về <50% |
| **11** | `DiaRLLifestyleCoach-Agent` | Đề xuất can thiệp lối sống tối ưu thích nghi (D3QN) | Trạng thái bệnh nhân, Phần thưởng | Kế hoạch tập luyện & thực đơn 4 tuần |
| **12** | `DiaLLMBridge-Agent` | Lập luận chuỗi suy nghĩ y khoa địa phương (Clinical CoT) | Tổng hợp dữ liệu từ 11 tác tử | Bản tổng kết giải thích tự nhiên ADA 2024 |

---

## 📊 3. BẢNG HIỆU NĂNG ĐỐI CHUẨN 9 KIẾN TRÚC MÔ HÌNH AI

Kết quả thực nghiệm trên tập kiểm thử độc lập 20.000 hồ sơ bệnh án (Cohort 2 - 100k EHR) sau khi phân tầng và kiểm chuẩn 95% Confidence Interval qua Bootstrap ($N=1.000$ iterations):

| Hạng | Kiến Trúc Mô Hình AI | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Thời gian Inference |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **TabResNet Attention** | **97.35%** | **98.85%** | **70.21%** | **82.11%** | **0.9793** | 4.8 ms / ca |
| 🥈 | **Super Stacking Meta-Learner** | 97.32% | 98.70% | 69.85% | 81.82% | 0.9790 | 6.2 ms / ca |
| 🥉 | **Gradient Tree Boosting (GBDT)** | 97.18% | 97.65% | 68.53% | 80.54% | 0.9788 | 0.8 ms / ca |
| 4 | **Random Forest (100 Cây)** | 97.24% | 99.31% | 67.94% | 80.68% | 0.9748 | 1.2 ms / ca |
| 5 | **Deep Learning MLP (PyTorch)** | 97.18% | 98.47% | 67.94% | 80.40% | 0.9775 | 1.5 ms / ca |
| 6 | **1D-CNN Biomarker Filter** | 97.10% | 96.67% | 68.29% | 80.04% | 0.9773 | 1.8 ms / ca |
| 7 | **Recurrent LSTM Gated Sequence** | 97.11% | 97.22% | 67.94% | 79.99% | 0.9759 | 2.4 ms / ca |
| 8 | **Decision Tree (Pruned max_depth=6)** | 97.20% | 98.22% | 68.35% | 80.61% | 0.9738 | 0.1 ms / ca |
| 9 | **Logistic Regression (L2 Regularized)** | 96.03% | 85.88% | 63.71% | 73.15% | 0.9620 | 0.05 ms / ca |
| -- | *Pure NumPy Scratch MLP (Đẳng hình)* | *97.16%* | *98.40%* | *67.88%* | *80.35%* | *0.9772* | *Parity $\Delta = 0.0025$* |

---

## 🌐 4. NGUỒN DỮ LIỆU LÂM SÀNG & TỪ ĐIỂN ĐẶC TRƯNG

Hệ thống được xây dựng và xác thực trên các bộ dữ liệu y tế công khai, tuân thủ nghiêm ngặt chuẩn ẩn danh **HIPAA Safe Harbor Privacy Rule**:

| STT | Tập Dữ Liệu | Quy Mô | Nguồn & Định Danh (DOI/Link) | Mục Đích Thực Nghiệm |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **EHR Modern Cohort** | 100.000 hồ sơ | [Kaggle Dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset) | Huấn luyện chính 9 mô hình AI & Đánh giá công bằng |
| **2** | **Pima Indians Cohort** | 768 hồ sơ | [UCI ML Repository](https://archive.ics.uci.edu/dataset/34/pima+indians+diabetes) (DOI: `10.24432/C5059P`) & [Kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database) | Kiểm chứng khả năng tổng quát hóa ngoại suy & Xử lý dị thường sinh học |
| **3** | **CDC BRFSS Survey** | 253.680 quan sát | [Kaggle CDC Dataset](https://www.kaggle.com/datasets/alexteb/diabetes-health-indicators-dataset) | Baseline đối chuẩn học thuật khảo sát điện thoại tự khai |

### Bảng Từ Điển Đặc Trưng Lâm Sàng (Cohort 100.000 hồ sơ):
- `gender`: Giới tính sinh học (`Male`, `Female`, `Other`).
- `age`: Độ tuổi bệnh nhân ($0.08 - 80.0$ tuổi).
- `hypertension`: Tiền sử tăng huyết áp ($0$: Không, $1$: Có tăng HA).
- `heart_disease`: Tiền sử bệnh tim thiếu máu cục bộ / mạch vành ($0$: Không, $1$: Có).
- `smoking_history`: Tiền sử hút thuốc lá (`never`, `current`, `former`, `ever`, `not current`, `No Info`).
- `bmi`: Chỉ số khối cơ thể ($\text{kg/m}^2$, phạm vi $10.01 - 95.69$).
- `HbA1c_level`: Nồng độ huyết sắc tố glycated (% tổng lượng hemoglobin, $3.5 - 9.0\%$).
- `blood_glucose_level`: Nồng độ đường huyết mao mạch lúc đói ($\text{mg/dL}$, $80 - 300\text{ mg/dL}$).
- `diabetes`: Biến mục tiêu chẩn đoán lâm sàng ($0$: Không mắc bệnh, $1$: Mắc đái tháo đường).

---

## 📁 5. CẤU TRÚC THƯ MỤC DỰ ÁN `project01/`

```text
project01/
├── README.md                                  # Tài liệu kỹ thuật chi tiết toàn diện
├── requirements.txt                           # Danh mục thư viện Python (PyTorch, Sklearn, FastAPI,...)
├── run.py                                     # Launcher trung tâm: --test hoặc Web server
├── generate_all_36_figures.py                 # Bộ tạo 36 biểu đồ trực quan hóa y sinh 300 DPI
├── generate_master_report_docx.py             # Bộ biên soạn tự động báo cáo Word 6.07 MB chuẩn PTIT
├── Bao_Cao_Project01_CT_09_Hautv.287.docx     # Báo cáo chuyên sâu Word (6.07 MB, nhúng 36 hình 300 DPI)
├── Bao_Cao_Nghien_Cuu_Project01_Nang_Cap.docx # Bản sao lưu đồng bộ theo tên đề tài nghiên cứu
├── PROJECT01_COMPREHENSIVE_UPGRADE_REPORT.md  # Báo cáo khoa học Markdown toàn diện (>50 trang tương đương)
│
├── data/                                      # Cơ sở dữ liệu lâm sàng mở
│   ├── diabetes_prediction_dataset.csv        # Cohort 2: 100,000 hồ sơ EHR lâm sàng
│   └── pima_diabetes_dataset.csv              # Cohort 1: 768 hồ sơ NIDDK Pima Indians
│
├── models/                                    # 9 Mô hình AI & Trọng số đã kiểm định
│   ├── diabetes_tabresnet.pt                  # Mô hình TabResNet Attention (PyTorch - ROC-AUC 0.9793)
│   ├── super_stacking_meta_learner.pkl        # Mô hình Super Stacking Meta-Learner (Blender)
│   ├── diabetes_random_forest.pkl             # Random Forest (100 Decision Trees)
│   ├── diabetes_gradient_boosting.pkl         # Gradient Tree Boosting (GBDT)
│   ├── diabetes_decision_tree.pkl             # Cây quyết định cắt tỉa độ sâu
│   ├── diabetes_logistic_regression.pkl       # Hồi quy Logistic chính quy hóa L2
│   ├── diabetes_mlp.pkl & _weights.npz        # Deep Learning MLP (PyTorch & NumPy weights)
│   ├── diabetes_cnn.pkl & _weights.npz        # 1D-CNN Biomarker Filter
│   ├── diabetes_lstm.pkl & _weights.npz       # Recurrent LSTM Gated Sequence
│   ├── rl_dqn.pt & rl_qtable.json             # Trọng số D3QN & Bảng Q-Table Reinforcement Learning
│   ├── diabetes_scaler.pkl                    # StandardScaler chuẩn hóa Z-Score
│   ├── le_gender.pkl & le_smoking.pkl         # LabelEncoders mã hóa biến phân loại
│   ├── dual_cohort_metrics.json               # Kết quả đối chuẩn đa cohort & Parity Delta
│   ├── fairness_trust_metrics.json            # Kiểm toán công bằng & Expected Calibration Error
│   ├── rl_evaluation_results.json             # Kết quả đánh giá phần thưởng can thiệp D3QN
│   ├── train_all_models.py                    # Huấn luyện bộ 7 mô hình cơ bản
│   ├── train_dual_cohorts.py                  # Huấn luyện đa cohort & Pure NumPy Scratch MLP
│   ├── train_advanced_ensemble.py             # Huấn luyện TabResNet & Super Stacking
│   ├── train_rl_agent.py                      # Huấn luyện D3QN & Tabular Q-Learning
│   └── eval_fairness_and_calibration.py       # Đánh giá công bằng nhóm & Độ tin cậy ECE
│
├── knowledge_graph/                           # Đồ thị tri thức y khoa ADA 2024 / KDIGO
│   ├── diabetes_knowledge_graph.json          # NetworkX Graph 29 nút cốt lõi
│   ├── diabetes_knowledge_graph_expanded.json # NetworkX Graph 44 nút mở rộng cho Graph-RAG
│   ├── diabetes_kg_neo4j.cypher               # Lệnh Cypher nạp cơ sở dữ liệu Neo4j
│   ├── build_diabetes_kg.py                   # Script kiến tạo đồ thị tri thức NetworkX
│   ├── expand_kg_and_eval_rag.py              # Mở rộng đồ thị & đối chuẩn Graph-RAG vs Vector
│   └── diabetes_kg_queries.py                 # Bộ máy truy vấn đa bước theo hồ sơ bệnh nhân
│
├── agents/                                    # Hội đồng lâm sàng 12 Tác tử y khoa
│   ├── triage_risk_agent.py                   # DiaTriage-Agent (Tiếp đón & Phân loại cấp cứu)
│   ├── ai_diagnostic_agent.py                 # DiaDiagnostic-Agent (Đồng thuận 9 mô hình AI)
│   ├── kg_guidelines_agent.py                 # DiaGraph-Agent (Tra cứu phác đồ đồ thị ADA 2024)
│   ├── therapy_lifestyle_agent.py             # DiaTherapy-Agent (Kê đơn cá nhân hóa & Dinh dưỡng)
│   ├── chief_evaluator_critic.py              # DiaCritic-Agent (Phản biện & Thẩm định an toàn)
│   ├── safety_rules_agent.py                  # DiaSafetyRules-Agent (12 Quy tắc bảo vệ R1-R12)
│   ├── fairness_trust_auditor.py              # DiaFairnessAuditor-Agent (Kiểm toán công bằng & ECE)
│   ├── longitudinal_tracker.py                # DiaLongitudinalTracker-Agent (Quỹ đạo 4 tuần)
│   ├── pharmacogenomics_agent.py              # DiaPharmacogenomics-Agent (Dược lý gen CYP2C9/OCT1)
│   ├── counterfactual_agent.py                # DiaCounterfactual-Agent (Can thiệp tối thiểu)
│   ├── rl_lifestyle_coach.py                  # DiaRLLifestyleCoach-Agent (Can thiệp thích nghi D3QN)
│   ├── llm_bridge.py                          # DiaLLMBridge-Agent (Clinical Chain-of-Thought)
│   ├── llm_downloader.py                      # Bộ tải tự động mô hình Qwen 2.5 0.5B từ Hugging Face
│   └── diabetes_coordinator.py                # DiaCouncilCoordinator (Điều phối viên hội đồng 12 tác tử)
│
├── notebook/                                  # Nghiên cứu định lượng Jupyter Notebook
│   ├── 01_comprehensive_diabetes_multiagent_system.ipynb # Notebook thực nghiệm khoa học 12 phần
│   └── build_master_notebook.py               # Builder tự động tạo notebook cấu trúc chuẩn
│
├── figures/                                   # 36 Biểu đồ phân tích độ phân giải cao 300 DPI
│   ├── fig1_target_distribution.png           # Phân bố nhãn mục tiêu & tỷ lệ mất cân bằng
│   ├── fig2_numerical_distributions.png       # Phân bố 4 chỉ số sinh hóa định lượng
│   ├── ...                                    # Các biểu đồ từ Fig 3 đến Fig 35
│   └── fig36_advanced_ensemble_architecture.png# Kiến trúc mạng nơ-ron TabResNet & Super Stacking
│
└── web/                                       # Ứng dụng Web tương tác lâm sàng
    ├── app.py                                 # FastAPI REST API Backend
    └── index.html                             # Giao diện Tailwind CSS Glassmorphism đa chức năng
```

---

## 🚀 6. HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH NHANH (QUICK START)

### 1. Cài đặt môi trường Python
Yêu cầu Python từ phiên bản 3.10 trở lên:
```bash
cd project01
pip install -r requirements.txt
```

### 2. Chạy bộ kiểm thử tự động toàn diện (Comprehensive Verification Suite)
Lệnh kiểm tra toàn bộ 5 giai đoạn: kiểm tra 9 mô hình, đối chuẩn sai số toán học Pure NumPy ($\Delta < 0.005$), kiểm tra đồ thị tri thức, kiểm tra 36 hình ảnh và hội chẩn 12 tác tử:
```bash
python run.py --test
```
Kết quả mong đợi:
```text
======================================================================
PROJECT 01 VERIFICATION & TEST SUITE
======================================================================
[1/5] Verifying 9 Trained Models, TabResNet Attention & Dual-Cohort Metrics...
  -> Dual Cohort Metrics & TabResNet: PASSED (Models: 9, Best ROC-AUC: 0.9793)
[2/5] Verifying Tri-Framework Parity Check (Pure NumPy Scratch vs Framework)...
  -> Parity Delta: Δ = 0.0025 (< 0.005) -> PASSED
[3/5] Verifying Medical Knowledge Graph (ADA 2024 Standards)...
  -> Knowledge Graph: PASSED (29 nodes, 26 edges)
[4/5] Verifying 16 Publication Figures & Master Word Report...
  -> Visual Artifacts: PASSED (36 figures, Word Report: 6.07 MB)
[5/5] Running End-to-End 12-Agent Council Deliberation...
  -> 12-Agent Council Deliberation: PASSED (Diagnosis: Diabetic / High Risk, Duration: 0.12s)
======================================================================
ALL PROJECT 01 TESTS PASSED SUCCESSFULLY! (EXIT CODE 0)
======================================================================
```

### 3. Khởi chạy Web Dashboard tương tác lâm sàng
Khởi chạy dịch vụ FastAPI Web Server:
```bash
python run.py --port 8000
```
Truy cập trình duyệt web tại địa chỉ: **[http://localhost:8000](http://localhost:8000)**.
- Giao diện hỗ trợ nạp hồ sơ bệnh án mẫu (High Risk, Borderline, Low Risk, Geriatric CVD).
- Hiển thị trực tiếp quá trình hội chẩn và biên bản của 12 tác tử lâm sàng.
- Tích hợp bộ mô phỏng can thiệp phản thực tế (Live Counterfactual Recourse) và khuyến nghị lối sống tăng cường (D3QN).
- Thẻ liên kết cơ sở dữ liệu mở quốc tế Kaggle & UCI DOI.

### 4. Tái tạo 36 Biểu đồ Trực quan & Báo cáo Word 6.07 MB
Để tạo lại toàn bộ 36 hình ảnh 300 DPI và tài liệu báo cáo khoa học Word hoàn chỉnh:
```bash
# Tái tạo 36 biểu đồ y sinh
python generate_all_36_figures.py

# Biên dịch tài liệu Word 6.07 MB nhúng 36 hình ảnh
python generate_master_report_docx.py
```

---

## 🔬 7. Ý NGHĨA KHOA HỌC & GIÁ TRỊ THỰC TIỄN

1. **Minh bạch hóa AI Y tế (Explainable & Safe AI)**: Không xem AI như một hộp đen nguy hiểm mà trang bị hệ thống 12 quy tắc an toàn tất định (`DiaSafetyRules-Agent`) và hội đồng phản biện tự động (`DiaCritic-Agent`), đảm bảo mọi phác đồ đều vượt qua kiểm tra chống chỉ định suy thận và tim mạch theo hướng dẫn ADA 2024.
2. **Công bằng & Đạo đức AI (Fairness & Ethics)**: Tích hợp bộ kiểm toán công bằng nhân khẩu học (`DiaFairnessAuditor-Agent`) đánh giá Disparate Impact Ratio và kiểm định độ tin cậy hiệu chuẩn xác suất (Expected Calibration Error).
3. **Cá nhân hóa Y học Chính xác (Precision Medicine)**: Kết hợp mô hình dược lý gen (`DiaPharmacogenomics-Agent`) kiểm tra kiểu gen CYP2C9 và OCT1, cùng thuật toán học tăng cường D3QN đề xuất can thiệp lối sống có khả năng duy trì lâu dài.
4. **Chuẩn hóa Học thuật PTIT**: Báo cáo nghiên cứu khoa học được biên soạn công phu với đầy đủ công thức toán học, biểu đồ đối chuẩn 300 DPI và cấu trúc bài báo khoa học chuẩn mực.
