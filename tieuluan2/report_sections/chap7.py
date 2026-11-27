"""
Chapter 7: Kết luận và Hướng phát triển
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP7_DATA = {
    "chapter_num": 7,
    "chapter_title": "CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN",
    "intro_text": """
Chương cuối cùng tổng kết các thành tựu nghiên cứu và triển khai thực nghiệm đạt được của đề tài, phân tích sâu sắc các giá trị học thuật và công nghệ đóng góp cho lĩnh vực AI tại Việt Nam, đánh giá khách quan các hạn chế kỹ thuật hiện tại, và định hình 4 hướng phát triển chiến lược trong tương lai.
""",
    "sections": [
        {
            "num": "7.1",
            "title": "7.1 Kết luận và Đóng góp Then chốt của Đề tài",
            "text": r"""
Báo cáo tiểu luận môn học "Phát triển các Hệ thống Thông minh" đã hoàn thành trọn vẹn và xuất sắc các mục tiêu nghiên cứu, thiết kế kiến trúc và triển khai thực nghiệm một Hệ thống Thông minh Đa miền tích hợp chuyên sâu cho hai lĩnh vực trọng yếu tại Việt Nam là Y tế Lâm sàng và Phân tích Đầu tư Tài chính.

Công trình này đại diện cho một nghiên cứu tiên phong trong việc hiện thực hóa mô hình Trí tuệ Nhân tạo Thần kinh - Tượng trưng (Neuro-Symbolic AI) tại Việt Nam với 5 đóng góp khoa học và kỹ thuật cốt lõi:

1. **Xây dựng Hệ thống Bản thể học Hình thức và Đồ thị Tri thức Đa miền Chuẩn W3C**:
   Thiết kế hoàn chỉnh hai đồ thị tri thức RDF: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp bản thể, 6 vị từ quan hệ nhân quả có hướng có dấu). Hiện thực động cơ suy diễn tiến (Forward Chaining) RDFS/OWL đến điểm bất động có chứng minh toán học và 5 nhóm truy vấn đại số quan hệ SPARQL chuyên sâu, giải quyết trọn vẹn các bài toán rà soát chống chỉ định thuốc và lan truyền cú sốc kinh tế vĩ mô.

2. **Thiết lập Khung Thực nghiệm và Ma trận Đối chuẩn 25 Cấu hình RAG Đầy đủ**:
   Xây dựng kho ngữ liệu chuẩn hóa gồm 17 tài liệu quy chuẩn kỹ thuật tiếng Việt (D01 - D17) và bộ 30 câu hỏi benchmark đa tầng. Đối chuẩn toàn diện ma trận 25 cấu hình kết hợp giữa 5 chiến lược phân mảnh văn bản (Fixed-size, Sliding Window, Sentence, Semantic Markdown, Parent-Child) với 5 bộ truy xuất (BM25 Okapi, Dense Cosine, Hybrid RRF k=60, Cross-Encoder Reranker, và GraphRAG Louvain). Xác định cấu hình tối ưu vượt trội là Parent-Child kết hợp Hybrid RRF và Cross-Encoder đạt Hit@1 = 90.00%, Hit@3 = 100.00% và NDCG@5 = 0.9634.

3. **Hiện thực Hai Mô hình Mạng Nơ-ron PyTorch Chuyên biệt Đạt Chuẩn Công nghiệp**:
   - Mô hình `DiabetesMLP`: Gồm đúng 10.497 tham số học được, áp dụng hàm mất mát Weighted Binary Cross-Entropy với hệ số $pos\\_weight = 10.3$ giải quyết dứt điểm vấn đề mất cân bằng dữ liệu y tế (chỉ 8.82% ca bệnh), hiệu chuẩn ngưỡng quyết định Youden J $\\tau = 0.9016$, đạt ROC-AUC = 0.9755 và Độ nhạy lâm sàng Recall = 93.28% trên tập kiểm thử độc lập 14.420 mẫu bệnh nhân.
   - Mô hình `BiLSTM SeqForecaster`: Gồm đúng 140.865 tham số, cấu trúc 2 tầng BiLSTM 64 chiều, tối ưu hóa bằng Huber Loss $\\delta=1.0$ chống ngoại lai thị trường, tích hợp 200 lượt suy luận Monte Carlo Dropout để lượng hóa độ bất định vị kỷ Bayes và sinh Dải quạt tin cậy 90% (Fan Chart) hỗ trợ quản trị rủi ro đầu tư chuyên nghiệp.

4. **Hiện thực Tác tử Lập luận ReAct Tất định và Bộ Kiểm chứng Độ trung thực Số liệu ($\ge 85\%$)**:
   Kiên quyết loại bỏ cơ chế đa tác tử tự phát thiếu kiểm soát, thay vào đó xây dựng Tác tử ReAct điều phối tuần tự 6 công cụ chuyên trách theo đồ thị thực thi có định hướng (DAG). Triển khai thuật toán Grounded Verifier tự động kiểm tra trích dẫn nguồn `[Dxx]` (đạt 100%) và kiểm toán độ trung thực số liệu $\\ge 85\\%$ (thực tế đạt 97.4%), triệt tiêu hoàn toàn hiện tượng ảo giác nghiệp vụ (tỷ lệ ảo giác giảm từ 37.5% ở LLM đơn lẻ về 0.0%).

5. **Cung cấp Hệ thống Toàn vẹn Có Thể Vận hành Ngay (Production-Grade) kèm Giao diện Web Trực quan**:
   Toàn bộ mã nguồn được tổ chức module hóa chuyên nghiệp, vượt qua 100% các bài kiểm thử tự động đa tầng, và đi kèm một ứng dụng Web Dashboard FastAPI tích hợp thư viện đồ họa mạng lưới Cytoscape.js hiện đại, bảng tính nguy cơ lâm sàng và đồ thị nến dải quạt tin cậy thời gian thực.
"""
        },
        {
            "num": "7.2",
            "title": "7.2 Đánh giá Khách quan Các Hạn chế Kỹ thuật",
            "text": r"""
Mặc dù đã đạt được những kết quả rất ấn tượng, đề tài vẫn còn tồn tại một số hạn chế kỹ thuật khách quan cần tiếp tục hoàn thiện:
- **Phạm vi Dữ liệu và Bản thể học**: Đồ thị tri thức y tế hiện tại mới tập trung sâu vào bệnh Đái tháo đường Típ 2, chưa mở rộng sang toàn bộ các bệnh lý rối loạn chuyển hóa phức tạp đi kèm (như hội chứng Cushing, suy giáp). Tương tự, đồ thị tài chính tập trung vào 4 cổ phiếu trụ cột đại diện và vàng SJC, chưa bao phủ toàn bộ 1.600 mã chứng khoán trên các sàn giao dịch Việt Nam.
- **Tài nguyên Tính toán Phần cứng**: Các thử nghiệm của đề tài được tối ưu hóa để vận hành mượt mà trên môi trường CPU tiêu chuẩn. Do đó, việc triển khai các mô hình ngôn ngữ lớn nguồn mở cục bộ (On-premise LLMs) có quy mô trên 14 tỷ tham số gặp phải nút thắt cổ chai về tốc độ sinh token.
- **Tính Động của Tri thức Pháp lý**: Quy trình trích xuất bộ ba từ văn bản pháp luật mới vẫn đòi hỏi sự rà soát và phê duyệt ở bước cuối cùng bởi chuyên gia con người (Human-in-the-loop) để đảm bảo không xảy ra sai sót ngữ nghĩa pháp lý.
"""
        },
        {
            "num": "7.3",
            "title": "7.3 Bốn Hướng Phát triển và Ứng dụng Thực tiễn trong Tương lai",
            "text": r"""
Trong các giai đoạn nghiên cứu tiếp theo, hệ thống có thể được tiếp tục mở rộng theo 4 hướng chiến lược:
1. **Tích hợp Mô hình Ngôn ngữ Lớn Tiếng Việt Chuyên biệt Cục bộ**: Triển khai các mô hình mã nguồn mở tối ưu cho tiếng Việt (như PhoGPT, Vistral, Qwen-2.5-7B) chạy suy luận tăng tốc với vLLM hoặc Ollama trên hạ tầng máy chủ GPU chuyên dụng, đảm bảo tính bảo mật dữ liệu y tế và tài chính tuyệt đối nội bộ.
2. **Mở rộng Đồ thị Tri thức Đa tầng (Multi-layered Ontology)**: Mở rộng VietnamDiabetesKG kết nối với các kho tri thức y học mở toàn cầu (UMLS, SNOMED CT, DrugBank); mở rộng VietnamFinanceKG bao phủ toàn bộ thị trường trái phiếu doanh nghiệp, thị trường bất động sản và chuỗi cung ứng liên ngành.
3. **Ứng dụng Trợ lý Sức khỏe Cá thể hóa Thời gian Thực**: Phát triển ứng dụng di động cho bệnh nhân đái tháo đường, kết nối trực tiếp với các thiết bị đo đường huyết liên tục (Continuous Glucose Monitoring - CGM) thông qua giao thức IoT, tự động phân tích đồ thị đường huyết và đề xuất chế độ ăn uống bản địa hóa theo thời gian thực.
4. **Hệ thống Quản lý Danh mục Đầu tư Định lượng Tự động**: Tích hợp mô hình BiLSTM Monte Carlo Dropout vào các thuật toán tối ưu hóa danh mục đầu tư Markowitz và Black-Litterman, tự động tái cân bằng danh mục tài sản dựa trên mức độ rủi ro vĩ mô được suy luận từ đồ thị tri thức.
"""
        }
    ]
}
