import os

EXTRA_KG_SECTION = """- Đồ thị tri thức Y khoa Đa nguồn & Graph-RAG (Knowledge Graph 56 Nodes, 59 Edges):
  + Tệp lưu trữ Neo4j Cypher : project01/knowledge_graph/DB_diabet.cypher (Kèm DB_diabet.cypher & diabetes_kg_neo4j.cypher)
  + Tệp JSON Đồ thị          : project01/knowledge_graph/diabetes_knowledge_graph_expanded.json
  + Danh mục đường dẫn (URLs) chính thức được nhúng trực tiếp trong từng Node của tệp Cypher:
    1. Hiệp hội Đái tháo đường Hoa Kỳ (ADA Standards of Care 2024):
       * Cổng tổng quan toàn văn : https://diabetesjournals.org/care/issue/47/Supplement_1
       * Tiêu chuẩn chẩn đoán    : https://doi.org/10.2337/dc24-S002
       * Tiền đái tháo đường     : https://doi.org/10.2337/dc24-S003
       * Lối sống & Dinh dưỡng   : https://doi.org/10.2337/dc24-S005
       * Béo phì & Cân nặng      : https://doi.org/10.2337/dc24-S008
       * Tiếp cận Dược lý        : https://doi.org/10.2337/dc24-S009
       * Tim mạch & Suy tim      : https://doi.org/10.2337/dc24-S010
       * Bệnh thận mạn tính (CKD): https://doi.org/10.2337/dc24-S011
       * Võng mạc & Thần kinh    : https://doi.org/10.2337/dc24-S012
       * Cấp cứu DKA / HHS       : https://doi.org/10.2337/dc24-S016
    2. Bộ Y tế Việt Nam (Quyết định số 5481/QĐ-BYT):
       * Cục Quản lý Khám chữa bệnh: https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html
       * Thư viện Pháp luật      : https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Quyet-dinh-5481-QD-BYT-2020-tai-lieu-chuyen-mon-Huong-dan-chan-doan-dieu-tri-dai-thao-duong-tip-2-461324.aspx
    3. Hiệp hội Thận học Quốc tế (KDIGO 2023):
       * Khuyến cáo KDIGO        : https://kdigo.org/guidelines/diabetes-ckd/
       * Kidney International DOI: https://doi.org/10.1016/j.kint.2023.08.014
    4. Bệnh viện Đa khoa Quốc tế Vinmec (Chuẩn JCI):
       * Chẩn đoán & Điều trị ĐTĐ: https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/
       * Đĩa thức ăn người Việt  : https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/dinh-duong/che-do-an-uong-cho-nguoi-tieu-duong-loai-2/
       * Chăm sóc bàn chân ĐTĐ   : https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/huong-dan-cham-soc-ban-chan-cho-nguoi-benh-tieu-duong/
       * Sàng lọc võng mạc đáy mắt: https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/mat/sang-loc-benh-vong-mac-dai-thao-duong/
       * Chỉ số ABI mạch máu     : https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/tim-mach/y-nghia-cua-chi-so-abi-trong-chan-doan-benh-dong-mach-ngoai-bien/
       * Tập luyện thể dục       : https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/bai-tap-the-duc-cho-nguoi-tieu-duong-tot-nhat/
       * Cai thuốc lá tuyệt đối  : https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/vi-sao-nguoi-benh-tieu-duong-can-cai-thuoc-la-ngay-lap-tuc/
    5. Hệ thống Nhà thuốc FPT Long Châu:
       * Quy tắc 15-15 hạ đường huyết: https://nhathuoclongchau.com.vn/bai-viet/quy-tac-15-15-trong-xu-tri-ha-duong-huyet-o-nguoi-benh-tieu-duong-61389.html
       * Hướng dẫn uống Metformin : https://nhathuoclongchau.com.vn/bai-viet/uong-metformin-luc-nao-tot-nhat-huong-dan-dung-thuoc-dung-cach-62145.html
       * Trajenta Linagliptin 5mg: https://nhathuoclongchau.com.vn/thuoc/trajenta-5mg-boehringer-3x10-18454.html
       * Jardiance Empagliflozin : https://nhathuoclongchau.com.vn/thuoc/jardiance-10mg-boehringer-3x10-18451.html
       * Forxiga Dapagliflozin   : https://nhathuoclongchau.com.vn/thuoc/forxiga-10mg-astrazeneca-2x14-17799.html
       * Kỹ thuật tiêm bút Insulin: https://nhathuoclongchau.com.vn/bai-viet/huong-dan-cach-tiem-insulin-bang-but-tiem-dung-chuan-57989.html
       * Bút tiêm Lantus SoloStar: https://nhathuoclongchau.com.vn/thuoc/lantus-solostar-100iu-ml-sanofi-hop-5-but-tiem-2015.html
       * Thuốc Diamicron MR 30mg : https://nhathuoclongchau.com.vn/thuoc/diamicron-mr-30mg-les-laboratoires-servier-industrie-2-vi-x-30-vien-2811.html
       * Thuốc Januvia 100mg     : https://nhathuoclongchau.com.vn/thuoc/januvia-100mg-msd-2x14-610.html
       * Hoạt chất Semaglutide   : https://nhathuoclongchau.com.vn/thanh-phan/semaglutide
    6. Tổ chức Y tế Thế giới (WHO):
       * Fact Sheet Đái tháo đường: https://www.who.int/news-room/fact-sheets/detail/diabetes
       * Tiêu chuẩn chẩn đoán WHO: https://www.who.int/publications/i/item/9789241516594
       * Chuẩn BMI Châu Á (WPRO) : https://www.who.int/westernpacific/health-topics/obesity
"""

target_files = [
    "DANH_SACH_DATASET_VA_MODEL.txt",
    os.path.join("project01", "DANH_SACH_DATASET_VA_MODEL.txt")
]

for tf in target_files:
    if os.path.exists(tf):
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        
        old_part = "- Đồ thị tri thức Y khoa Đa nguồn & Graph-RAG (Knowledge Graph 56 Nodes, 59 Edges):\n  + Tệp lưu trữ : project01/knowledge_graph/diabetes_knowledge_graph_expanded.json & diabetes_kg_neo4j.cypher\n  + Nguồn y văn : ADA Standards of Care 2024, KDIGO 2023, Bệnh viện Vinmec, Nhà thuốc FPT Long Châu, Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)."
        
        if old_part in content:
            new_content = content.replace(old_part, EXTRA_KG_SECTION.strip())
            with open(tf, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {tf}")
        else:
            print(f"Old pattern not found in {tf}")
