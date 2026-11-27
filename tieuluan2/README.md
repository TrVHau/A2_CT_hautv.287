# DỰ ÁN TIỂU LUẬN 2: HỆ THỐNG TRI THỨC VÀ AI ĐA MIỀN (KNOWLEDGE GRAPH, RAG & DEEP LEARNING)

**Học phần**: Phát triển Hệ thống Thông minh  
**Học viện**: Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Sinh viên thực hiện**: **Trần Văn Hậu** | **MSV**: **B23DCCN287** | **Lớp**: **D23CTPM01**  
**Giảng viên hướng dẫn**: **PGS.TS. Trần Đình Quế**  

---

## 1. Giới thiệu Dự án

Dự án nghiên cứu và triển khai hệ thống Trí tuệ Nhân tạo đa miền kết hợp giữa:
1. **Đồ thị Tri thức (Knowledge Graph - KG)**:
   - `VietnamDiabetesKG`: Bản thể học 23 lớp, 17 vị từ, phác đồ Bộ Y tế & ADA 2024, cảnh báo tương tác Metformin + Rượu bia (Nhiễm toan Lactic), mô hình dinh dưỡng Đĩa ăn cân bằng (Thịt gà GI=0, cơm trắng GI cao).
   - `VietnamFinanceKG`: Bản thể học 16 lớp, 6 vị từ, các kênh truyền dẫn nhân quả mang dấu (+ / -) từ Lãi suất Fed -> DXY -> USD/VND -> VN30/Vàng SJC (Nghị định 24/232), thuật toán lan truyền cú sốc BFS.
   - Động cơ suy diễn tiến (Forward Chaining) RDFS/OWL tới điểm bất động (Fixed Point).
   - Động cơ truy vấn SPARQL chuẩn hóa (Q1 - Q5).
2. **Retrieval-Augmented Generation (RAG) Đa tầng**:
   - 5 Chiến lược phân mảnh văn bản (Fixed-size, Overlap, Sentence, Semantic, Hierarchical).
   - Truy xuất lai (Hybrid Retrieval) BM25 Okapi + Dense Vectors qua Reciprocal Rank Fusion (RRF $k=60$).
   - Mạng xếp hạng lại thần kinh Cross-Encoder Reranker ($nDCG@10 = 0.94$).
   - GraphRAG: Phân cụm cộng đồng Louvain, tóm tắt cộng đồng và tìm kiếm hai chế độ Local Search / Global Search.
   - Ma trận đối chuẩn thực nghiệm 25 tổ hợp RAG.
3. **Mô hình Học sâu Chuyên biệt (PyTorch)**:
   - `DiabetesMLP`: Mạng nơ-ron 13 đặc trưng (128 -> 64 -> 1), Weighted BCE Loss ($pos\_weight = 10.3$), đạt ROC-AUC = 0.9755 và PR-AUC = 0.8726 trên 100.000 hồ sơ bệnh nhân.
   - `SeqForecaster` (BiLSTM): Mạng hồi quy hai chiều 2 tầng (64 nơ-ron/chiều) dự báo lợi suất phiên kế tiếp, Huber loss ($\delta=1.0$), 200 lượt Monte Carlo Dropout thiết lập dải quạt tin cậy 90% lượng hóa độ bất định.
4. **Hệ thống Suy luận Tất định & Bộ Kiểm chứng (Grounded Verifier)**:
   - Vòng lặp ReAct (Thought -> Action -> Observation) với bộ lập kế hoạch tất định.
   - Bộ kiểm chứng độ trung thực số học (Numerical Faithfulness $\ge 85\%$) và tính hợp lệ của trích dẫn `[n]`, chống triệt để hiện tượng ảo giác.
5. **Giao diện Web Ứng dụng Tương tác (FastAPI + Cytoscape.js)**:
   - Trực quan hóa đồ thị tri thức mạng lưới, dự báo rủi ro y tế thời gian thực, dự báo tài chính đa tài sản và ma trận đánh giá RAG.

---

## 2. Hướng dẫn Chạy Kiểm thử & Khởi động Hệ thống

### Bước 1: Chạy kiểm thử tự động toàn bộ 6 module
```powershell
python tieuluan2/tests/test_system.py
```

### Bước 2: Khởi động máy chủ Web Demo
```powershell
python -m uvicorn tieuluan2.src.web.app:app --host 127.0.0.1 --port 8000 --reload
```
Mở trình duyệt truy cập: `http://127.0.0.1:8000/`

### Bước 3: Xem Báo cáo Word & Markdown
- **Báo cáo Word Hoàn chỉnh (3.72 MB)**: [`tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx`](file:///c:/code/A2_CT_hautv.287/tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx)
- **Báo cáo Markdown Học thuật Chi tiết**: [`tieuluan2/BAO_CAO_TIEU_LUAN_2_NANG_CAP.md`](file:///c:/code/A2_CT_hautv.287/tieuluan2/BAO_CAO_TIEU_LUAN_2_NANG_CAP.md)
