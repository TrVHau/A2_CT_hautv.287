"""
build_documents_corpus.py
Tạo kho văn bản tài liệu chuẩn hóa miền Y tế (Bộ Y Tế) và Tài chính (NHNN, TTCK) phục vụ RAG.
"""
import os

DOCUMENTS = {
    "h01_chan_doan_dai_thao_duong.txt": """# QUYẾT ĐỊNH 5481/QĐ-BYT: HƯỚNG DẪN CHẨN ĐOÁN VÀ ĐIỀU TRỊ ĐÁI THÁO ĐƯỜNG TÍP 2
Bộ Y Tế ban hành ngày 30/12/2020.

## 1. Tiêu chuẩn chẩn đoán Đái tháo đường
Đái tháo đường (ĐTĐ) được chẩn đoán dựa trên 1 trong 4 tiêu chuẩn lâm sàng và cận lâm sàng sau:
1. Glucose huyết tương lúc đói (Fasting Plasma Glucose - FPG) >= 126 mg/dL (tương đương >= 7.0 mmol/L). Nhịn ăn ít nhất 8 giờ.
2. Glucose huyết tương ở thời điểm 2 giờ sau khi làm nghiệm pháp dung nạp glucose đường uống (OGTT 75g) >= 200 mg/dL (>= 11.1 mmol/L).
3. HbA1c >= 6.5% (48 mmol/mol), thực hiện tại phòng xét nghiệm được chuẩn hóa theo phương pháp NGSP.
4. Bệnh nhân có triệu chứng kinh điển của tăng glucose máu (tiểu nhiều, uống nhiều, sụt cân không rõ nguyên nhân) kèm theo glucose huyết tương ngẫu nhiên >= 200 mg/dL (>= 11.1 mmol/L).

Nếu không có triệu chứng kinh điển của tăng glucose máu cấp tính, xét nghiệm tiêu chuẩn 1, 2, 3 phải được lặp lại lần hai vào một ngày khác để khẳng định chẩn đoán.

## 2. Tiêu chuẩn chẩn đoán Tiền đái tháo đường (Pre-diabetes)
Tiền đái tháo đường bao gồm:
- Rối loạn glucose máu lúc đói (IFG): Glucose huyết tương lúc đói từ 100 đến 125 mg/dL (5.6 đến 6.9 mmol/L).
- Rối loạn dung nạp glucose (IGT): Glucose huyết tương ở thời điểm 2 giờ sau nghiệm pháp OGTT từ 140 đến 199 mg/dL (7.8 đến 11.0 mmol/L).
- HbA1c nằm trong khoảng 5.7% đến 6.4% (39 đến 47 mmol/mol).
Tiền đái tháo đường làm gia tăng mạnh mẽ nguy cơ tiến triển thành đái tháo đường típ 2 thực sự và các biến chứng tim mạch sớm. Khuyến cáo can thiệp lối sống tích cực: giảm ít nhất 7% cân nặng và hoạt động thể lực tối thiểu 150 phút/tuần.
""",

    "h02_thuoc_dieu_tri_va_chong_chi_dinh.txt": """# HƯỚNG DẪN SỬ DỤNG THUỐC HẠ GLUCOSE MÁU VÀ CÁC CHỐNG CHỈ ĐỊNH ĐẶC BIỆT
Căn cứ theo Hướng dẫn của Bộ Y Tế và Hiệp hội Đái tháo đường Hoa Kỳ (ADA).

## 1. Thuốc hàng đầu (First-line): Metformin (Biguanide)
- Cơ chế: Giảm sản xuất glucose ở gan, tăng tính nhạy cảm của thụ thể insulin tại mô ngoại vi, không gây hạ đường huyết khi dùng đơn trị và không làm tăng cân.
- Liều khởi đầu: 500 mg - 850 mg x 1-2 lần/ngày, uống trong hoặc sau bữa ăn để giảm tác dụng phụ trên đường tiêu hóa.
- Chống chỉ định tuyệt đối:
  + Bệnh nhân có mức lọc cầu thận ước tính eGFR < 30 mL/phút/1.73 m2 (suy thận nặng giai đoạn 4-5).
  + Bệnh nhân suy gan nặng, sốc nhiễm trùng, thiếu oxy mô cấp (suy tim cấp mất bù, nhồi máu cơ tim cấp).
- Cân nhắc giảm liều: Nếu eGFR trong khoảng 30 - 44 mL/phút/1.73 m2, tối đa không quá 1000 mg/ngày.
- Tương tác đặc biệt nguy hiểm với RƯỢU BIA (Ethanol): Metformin ức chế tân tạo glucose ở gan từ lactate. Khi uống rượu bia, quá trình chuyển hóa alcohol cạnh tranh NAD+ ở gan làm tích tụ acid lactic nghiêm trọng, dẫn đến nguy cơ toan acid lactic máu (Lactic Acidosis) có tỷ lệ tử vong lên đến 50%. Khuyến cáo: Tuyệt đối tránh uống rượu bia khi đang sử dụng thuốc Metformin.

## 2. Thuốc ức chế kênh đồng vận Natri - Glucose 2 (SGLT2 inhibitors)
- Hoạt chất tiêu biểu: Empagliflozin, Dapagliflozin, Canagliflozin.
- Cơ chế: Ức chế tái hấp thu glucose tại ống lượn gần của thận, bài tiết glucose qua nước tiểu.
- Lợi ích vượt trội: Ưu tiên chỉ định hàng đầu ở bệnh nhân đái tháo đường típ 2 có suy tim phân suất tống máu giảm (HFrEF) hoặc bảo tồn (HFpEF) hoặc bệnh thận mạn (CKD), giúp giảm tỷ lệ tử vong tim mạch và nhập viện vì suy tim.

## 3. Thuốc nhóm Thiazolidinediones (TZD - Pioglitazone)
- Cơ chế: Kích hoạt PPAR-gamma tăng nhạy cảm insulin ở mô mỡ và cơ.
- Chống chỉ định đặc biệt: Chống chỉ định ở bệnh nhân có tiền sử hoặc đang bị suy tim (NYHA I-IV) do thuốc gây phù, ứ trệ dịch tuần hoàn làm nặng thêm tình trạng suy tim.

## 4. Nhóm Sulfonylureas (Gliclazide, Glimepiride) và Insulin
- Cơ chế: Kích thích tế bào beta đảo tụy tiết insulin (độc lập với nồng độ glucose).
- Nguy cơ chính: Hạ đường huyết (Hypoglycemia, glucose máu < 70 mg/dL hoặc < 3.9 mmol/L).
- Xử trí hạ đường huyết cấp: Áp dụng quy tắc 15-15: Uống ngay 15g carbohydrate tác dụng nhanh (1/2 ly nước ngọt có đường, 3-4 viên kẹo đường hoặc 1 thìa canh đường pha nước), nghỉ ngơi 15 phút rồi đo lại đường huyết. Nếu vẫn < 70 mg/dL tiếp tục bổ sung thêm 15g.
""",

    "h03_dinh_duong_va_chi_so_gi.txt": """# NGUYÊN TẮC DINH DƯỠNG LÂM SÀNG VÀ CHỈ SỐ ĐƯỜNG HUYẾT CỦA THỰC PHẨM (GI)
Tài liệu hướng dẫn dinh dưỡng cho người bệnh đái tháo đường của Viện Dinh Dưỡng Quốc Gia.

## 1. Phân loại chỉ số đường huyết của thực phẩm (Glycemic Index - GI)
- GI thấp (<= 55): Tiêu hóa và hấp thu chậm, không làm tăng vọt glucose máu sau ăn. Khuyến nghị sử dụng chính.
  Ví dụ: Gạo lứt (GI ~ 50), yến mạch (GI ~ 55), đậu đỗ (GI ~ 28-35), rau xanh hầu hết (GI < 15), táo, bưởi, ổi.
- GI trung bình (56 - 69): Sử dụng ở mức vừa phải.
- GI cao (>= 70): Hấp thu nhanh, làm đường huyết tăng vọt sau ăn, bắt tụy tiết insulin ồ ạt.
  Ví dụ: Cơm trắng (GI ~ 73-83), xôi nếp (GI ~ 85-93), bánh mì trắng (GI ~ 75), khoai tây nướng, nước ngọt.

## 2. Lời khuyên cụ thể về các món ăn truyền thống Việt Nam
- Cơm trắng: Người đái tháo đường không nhất thiết phải kiêng tuyệt đối cơm trắng nhưng cần định lượng chặt chẽ (1/2 đến 2/3 bát mỗi bữa). Nên ăn theo thứ tự: ăn rau xanh trước -> ăn đạm thịt/cá -> ăn cơm cuối cùng. Thứ tự này giúp chất xơ làm chậm tốc độ rỗng dạ dày và làm phẳng đỉnh đường huyết sau ăn.
- Thịt gà: Thịt gà (đặc biệt là ức gà bỏ da) là nguồn protein nạc chất lượng cao (GI = 0), không chứa carbohydrate, cung cấp amino acid thiết yếu mà không làm tăng đường huyết. Bệnh nhân đái tháo đường hoàn toàn ăn được, nên ưu tiên gà luộc hoặc hấp, tránh chiên rán ngập dầu mỡ hoặc tẩm bột.
- Xôi nếp và bánh chưng: Có thành phần amylopectin rất cao, GI lên tới 85-95. Cần hạn chế tối đa, nếu ăn phải giảm khẩu phần cơm tương ứng và tăng lượng rau xanh.
""",

    "f01_co_che_ty_gia_va_xuat_nhap_khau.txt": """# CƠ CHẾ TRUYỀN DẪN TỶ GIÁ USD/VND VÀ TÁC ĐỘNG ĐẾN CÁC NGÀNH TRÊN THỊ TRƯỜNG CHỨNG KHOÁN
Báo cáo Phân tích Chiến lược Vĩ mô Thị trường Tài chính Việt Nam.

## 1. Kênh truyền dẫn vĩ mô của tỷ giá USD/VND
Khi chỉ số USD Index (DXY) hoặc lãi suất điều hành của Cục Dự trữ Liên bang Mỹ (Fed) duy trì ở mức cao, chênh lệch lãi suất USD-VND nới rộng gây áp lực làm tỷ giá USD/VND tăng giá (tiền đồng Việt Nam mất giá so với đô la Mỹ).

## 2. Tác động phân hóa theo từng nhóm doanh nghiệp niêm yết
- Doanh nghiệp Xuất khẩu ròng (Hưởng lợi - Tác động TÍCH CỰC (+)):
  + Tiêu biểu: CTCP FPT (Mã: FPT). Doanh thu mảng xuất khẩu phần mềm sang các thị trường quốc tế (Mỹ, Nhật, châu Âu) thu về bằng ngoại tệ USD/JPY/EUR, trong khi phần lớn chi phí nhân sự và vận hành hạch toán bằng VND. Khi tỷ giá USD/VND tăng, doanh thu quy đổi sang VND tăng trưởng mạnh hơn tốc độ tăng chi phí, biên lợi nhuận ròng được mở rộng rõ rệt.
  + Doanh nghiệp dệt may, thủy sản có tỷ trọng xuất khẩu cao.

- Doanh nghiệp Nhập khẩu nguyên vật liệu & Nợ vay USD lớn (Bất lợi - Tác động TIÊU CỰC (-)):
  + Tiêu biểu: CTCP Tập đoàn Hòa Phát (Mã: HPG). Hòa Phát phải nhập khẩu lượng lớn quặng sắt và than cốc luyện thép từ thị trường quốc tế với hóa đơn thanh toán định giá bằng USD. Đồng thời công ty duy trì dư nợ vay bằng USD để tài trợ cho các dự án mở rộng như Dung Quất 2. Khi tỷ giá USD/VND tăng, chi phí nguyên liệu đầu vào tăng cao và doanh nghiệp phải ghi nhận khoản lỗ chênh lệch tỷ giá tài chính lớn, bào mòn lợi nhuận.

- Nhóm Bất động sản và Tiêu dùng (VIC):
  + Tiêu biểu: Tập đoàn Vingroup (Mã: VIC). Tỷ giá tăng gây áp lực lên chi phí lãi vay trái phiếu quốc tế định danh USD, đồng thời Ngân hàng Nhà nước có thể phải thắt chặt thanh khoản để ổn định tỷ giá, làm tăng mặt bằng lãi suất trong nước và gây trở ngại cho thị trường bất động sản.

- Nhóm Ngân hàng (VCB):
  + Tiêu biểu: Vietcombank (Mã: VCB). VCB có vị thế ngoại hối mạnh và nguồn tiền gửi kiều hối dồi dào, thu nhập từ kinh doanh ngoại hối tăng khi tỷ giá biến động, tuy nhiên rủi ro nợ xấu có thể gia tăng ở các khách hàng vay có cơ cấu tài chính nhạy cảm với tỷ giá.
""",

    "f02_thi_truong_vang_va_nghi_dinh.txt": """# THỊ TRƯỜNG VÀNG VIỆT NAM: CƠ CHẾ ĐỊNH GIÁ, PHẦN BÙ SJC VÀ BỐI CẢNH NGHỊ ĐỊNH 232/2025/NĐ-CP
Nghiên cứu thị trường vàng vật chất và chính sách quản lý ngoại hối của Ngân hàng Nhà nước Việt Nam.

## 1. Công thức quy đổi giá vàng thế giới sang giá vàng trong nước
Giá vàng quốc tế niêm yết theo chuẩn XAU/USD (USD trên mỗi ounce troy).
Đơn vị tính trong nước là "lượng" (cây vàng), tương đương 37.5 gram (hoặc 10 chỉ).
Hệ số quy đổi vật lý: 1 ounce troy = 31.1034768 gram => 1 lượng = 37.5 / 31.1034768 ≈ 1.205653 ounce.

Công thức quy đổi chuẩn:
Giá vàng thế giới quy đổi (Triệu VNĐ/lượng) = (Giá XAU/USD * Tỷ giá USD/VND * 1.205653) / 1,000,000

Ví dụ thực nghiệm: Nếu XAU/USD = 2,650 USD/oz và USD/VND = 25,400:
Giá quy đổi = (2,650 * 25,400 * 1.205653) / 1,000,000 ≈ 81.15 Triệu VNĐ/lượng.

## 2. Phần bù chênh lệch vàng miếng SJC và Tác động thể chế
- Giai đoạn 2012 - 2024 (Nghị định 24/2012/NĐ-CP): Nhà nước độc quyền sản xuất vàng miếng và chọn thương hiệu SJC làm vàng miếng quốc gia. Việc không cấp phép dập thêm vàng miếng trong suốt 12 năm khiến nguồn cung SJC bị cô lập cục bộ so với nhu cầu trú ẩn gia tăng, dẫn đến hiện tượng "phần bù SJC" tăng vọt lên mức kỷ lục 15 - 20 triệu đồng/lượng (cao hơn 18-24% so với giá thế giới quy đổi).
- Giai đoạn 2025 trở đi (Nghị định 232/2025/NĐ-CP): Sửa đổi bổ sung Nghị định 24 nhằm xóa bỏ độc quyền vàng miếng SJC, cấp phép cho các doanh nghiệp đủ điều kiện nhập khẩu vàng nguyên liệu và sản xuất vàng thương hiệu khác. Chính sách này tăng nguồn cung hợp pháp, làm phần bù chênh lệch giữa giá vàng SJC và giá vàng thế giới quy đổi co hẹp mạnh mẽ về vùng an toàn (dưới 5-8%).
- Khuyến nghị đầu tư: Vàng nhẫn 9999 bám sát giá thế giới quy đổi hơn, ít chịu rủi ro bốc hơi phần bù chính sách so với vàng miếng SJC khi nguồn cung được khơi thông.
""",

    "f03_lai_suat_fed_va_dong_von.txt": """# TÁC ĐỘNG CỦA LÃI SUẤT CỤC DỰ TRỮ LIÊN BANG MỸ (FED) ĐẾN DÒNG VỐN VÀ THỊ TRƯỜNG CHỨNG KHOÁN VIỆT NAM
Tài liệu Tổng luận Nghiên cứu Kinh tế Vĩ mô & Ngân hàng Trung ương.

## 1. Chu kỳ chính sách tiền tệ của Fed
Khi Fed tăng lãi suất quỹ liên bang (Fed Funds Rate), lợi suất trái phiếu chính phủ Mỹ tăng cao, thúc đẩy dòng vốn toàn cầu rút khỏi các thị trường mới nổi (Emerging Markets) và cận biên (Frontier Markets) để quay trở về các tài sản định danh bằng đồng USD an toàn. Chỉ số USD Index (DXY) mạnh lên.

## 2. Cơ chế lan truyền cú sốc tới Việt Nam
- Khối ngoại bán ròng: Khi chênh lệch lãi suất USD/VND duy trì mức âm sâu (lãi suất USD cao hơn VND), khối ngoại đẩy mạnh rút vốn, bán ròng cổ phiếu trên sàn HOSE và chuyển đổi vốn sang USD.
- Áp lực tỷ giá và dự trữ ngoại hối: Ngân hàng Nhà nước (NHNN) đứng trước áp lực phải bán ngoại tệ can thiệp hoặc tăng lãi suất điều hành (lãi suất tái cấp vốn, tái chiết khấu) để bảo vệ giá trị đồng nội tệ.
- Thị trường chứng khoán (VN30): Định giá P/E của thị trường chịu áp lực điều chỉnh giảm do chi phí vốn (WACC) tăng. Tuy nhiên, khi Fed kết thúc chu kỳ thắt chặt và bắt đầu cắt giảm lãi suất (chu kỳ nới lỏng tiền tệ), áp lực tỷ giá hạ nhiệt, dòng vốn ngoại có xu hướng đảo chiều mua ròng trở lại, tạo động lực phục hồi mạnh mẽ cho các cổ phiếu trụ cột như VCB, FPT, HPG.
"""
}

def write_documents(base_dir="tieuluan2/data/documents"):
    os.makedirs(base_dir, exist_ok=True)
    for fname, content in DOCUMENTS.items():
        fpath = os.path.join(base_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Wrote {fpath} ({len(content)} chars)")

if __name__ == "__main__":
    write_documents()
