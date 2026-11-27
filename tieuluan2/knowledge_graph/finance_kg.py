"""
finance_kg.py
Đồ thị Tri thức Tài chính Việt Nam (VietnamFinanceKG): Các kênh truyền dẫn vĩ mô,
chính sách tiền tệ Fed & NHNN, tỷ giá USD/VND, biến động VN30 (FPT, HPG, VCB, VIC)
và thị trường vàng SJC theo Nghị định 24/2012 và Nghị định 232/2025.
"""
from .ontology import Ontology, Predicate
from .kg_base import KnowledgeGraph

def build_vietnam_finance_ontology() -> Ontology:
    onto = Ontology("VietnamFinanceOntology")

    classes = [
        ("FinanceEntity", "Thing"),
        ("MacroFactor", "FinanceEntity"),
        ("GlobalFactor", "MacroFactor"),
        ("DomesticFactor", "MacroFactor"),
        ("PolicyEvent", "FinanceEntity"),
        ("MarketAsset", "FinanceEntity"),
        ("Stock", "MarketAsset"),
        ("GoldAsset", "MarketAsset"),
        ("MarketIndex", "MarketAsset"),
        ("CapitalFlow", "FinanceEntity")
    ]
    for child, parent in classes:
        onto.add_class(child, parent)

    preds = [
        Predicate("TAC_DONG_TICH_CUC", "FinanceEntity", "FinanceEntity", "tác động cùng chiều (tăng → tăng) tới"),
        Predicate("TAC_DONG_TIEU_CUC", "FinanceEntity", "FinanceEntity", "tác động ngược chiều (tăng → giảm) tới"),
        Predicate("SUA_DOI_BO_SUNG", "PolicyEvent", "PolicyEvent", "sửa đổi, nới lỏng cơ chế của"),
        Predicate("THANH_PHAN_CUA", "MarketAsset", "MarketIndex", "là cổ phiếu thành phần trụ cột của"),
        Predicate("CAU_THANH_GIA", "FinanceEntity", "GoldAsset", "là biến số định giá trực tiếp của")
    ]
    for p in preds:
        onto.add_predicate(p)

    return onto

def build_vietnam_finance_kg() -> KnowledgeGraph:
    onto = build_vietnam_finance_ontology()
    kg = KnowledgeGraph("VietnamFinanceKG", onto)

    # 1. Global Factors
    kg.add_node("Lai_Suat_Fed", "GlobalFactor", "Lãi suất quỹ liên bang Fed (Fed Funds Rate)", ["fed", "lãi suất fed", "fed rate", "fomc"])
    kg.add_node("Chi_So_DXY", "GlobalFactor", "Chỉ số sức mạnh đồng USD (DXY)", ["dxy", "chỉ số usd", "usd index"])
    kg.add_node("XAU_USD", "GlobalFactor", "Giá vàng thế giới giao ngay (XAU/USD)", ["vàng thế giới", "xau", "xau/usd", "gold price"])
    kg.add_node("Bat_On_Dia_Chinh_Tri", "GlobalFactor", "Căng thẳng địa chính trị quốc tế", ["địa chính trị", "chiến tranh", "xung đột"])

    # 2. Domestic Factors & Capital Flows
    kg.add_node("Ty_Gia_USD_VND", "DomesticFactor", "Tỷ giá hối đoái USD/VND", ["tỷ giá", "tỷ giá usd/vnd", "usdvnd", "đô la mỹ"])
    kg.add_node("Lai_Suat_NHNN", "DomesticFactor", "Lãi suất điều hành Ngân hàng Nhà nước", ["lãi suất nhnn", "lãi suất điều hành", "sbv"])
    kg.add_node("Khoi_Ngoai_Ban_Rong", "CapitalFlow", "Dòng vốn khối ngoại bán ròng trên HOSE", ["khối ngoại", "khối ngoại bán ròng", "rút vốn"])

    # 3. Policy Events
    kg.add_node("Nghi_Dinh_24", "PolicyEvent", "Nghị định 24/2012/NĐ-CP (Độc quyền vàng miếng SJC)", ["nghị định 24", "nd24"])
    kg.add_node("Nghi_Dinh_232_2025", "PolicyEvent", "Nghị định 232/2025/NĐ-CP (Xóa độc quyền SJC, khơi thông cung)", ["nghị định 232", "nd232", "sửa nghị định 24"])

    # 4. Gold Assets
    kg.add_node("Vang_Quy_Doi", "GoldAsset", "Giá vàng thế giới quy đổi (VND/lượng)", ["vàng quy đổi", "giá vàng thế giới quy đổi"])
    kg.add_node("Vang_Mieng_SJC", "GoldAsset", "Giá vàng miếng SJC trong nước", ["vàng sjc", "sjc", "vàng miếng"])
    kg.add_node("Chenh_Lech_SJC", "GoldAsset", "Phần bù chênh lệch vàng SJC so với thế giới", ["phần bù sjc", "chênh lệch sjc", "premium sjc"])
    kg.add_node("Vang_Nhan_9999", "GoldAsset", "Giá vàng nhẫn trơn 9999", ["vàng nhẫn", "vàng nhẫn 9999", "nhẫn trơn"])

    # 5. Stocks & Indexes
    kg.add_node("FPT", "Stock", "CTCP FPT (FPT)", ["fpt", "cổ phiếu fpt", "xuất khẩu phần mềm"])
    kg.add_node("HPG", "Stock", "Tập đoàn Hòa Phát (HPG)", ["hpg", "hòa phát", "thép hòa phát", "cổ phiếu hpg"])
    kg.add_node("VCB", "Stock", "Vietcombank (VCB)", ["vcb", "vietcombank", "ngân hàng vcb"])
    kg.add_node("VIC", "Stock", "Tập đoàn Vingroup (VIC)", ["vic", "vingroup", "cổ phiếu vic"])
    kg.add_node("VN30", "MarketIndex", "Chỉ số cổ phiếu VN30", ["vn30", "chỉ số vn30", "thị trường chứng khoán"])

    # --- Facts & Causal Edges ---
    # Global to Domestic
    kg.add_fact("Lai_Suat_Fed", "TAC_DONG_TICH_CUC", "Chi_So_DXY", source="f03-fed", sign=1, mechanism="Chênh lệch lãi suất thu hút dòng vốn đổ vào USD")
    kg.add_fact("Lai_Suat_Fed", "TAC_DONG_TIEU_CUC", "XAU_USD", source="f03-fed", sign=-1, mechanism="Chi phí cơ hội nắm giữ vàng không sinh lãi tăng")
    kg.add_fact("Bat_On_Dia_Chinh_Tri", "TAC_DONG_TICH_CUC", "XAU_USD", source="f02-vang", sign=1, mechanism="Nhu cầu tài sản trú ẩn an toàn toàn cầu bùng nổ")

    kg.add_fact("Chi_So_DXY", "TAC_DONG_TICH_CUC", "Ty_Gia_USD_VND", source="f01-ty-gia", sign=1, mechanism="Đồng USD mạnh gây áp lực mất giá lên tiền đồng VND")
    kg.add_fact("Ty_Gia_USD_VND", "TAC_DONG_TICH_CUC", "Khoi_Ngoai_Ban_Rong", source="f03-fed", sign=1, mechanism="Lợi suất chuyển đổi sang USD bị xói mòn kích hoạt rút vốn")
    kg.add_fact("Ty_Gia_USD_VND", "TAC_DONG_TICH_CUC", "Lai_Suat_NHNN", source="f01-ty-gia", sign=1, mechanism="NHNN phải nâng lãi suất điều hành để bảo vệ dự trữ ngoại hối và tiền đồng")

    # Impact on Stocks
    kg.add_fact("Ty_Gia_USD_VND", "TAC_DONG_TICH_CUC", "FPT", source="f01-ty-gia", sign=1, mechanism="Doanh thu xuất khẩu phần mềm bằng USD quy đổi sang VND tăng vượt trội so với chi phí nội tệ")
    kg.add_fact("Ty_Gia_USD_VND", "TAC_DONG_TIEU_CUC", "HPG", source="f01-ty-gia", sign=-1, mechanism="Chi phí nhập khẩu quặng sắt/than cốc bằng USD đội lên và gánh nặng lỗ tỷ giá nợ vay")
    kg.add_fact("Lai_Suat_NHNN", "TAC_DONG_TIEU_CUC", "VIC", source="f01-ty-gia", sign=-1, mechanism="Chi phí lãi vay nợ tài chính bất động sản tăng cao và dòng tiền người mua bị siết")
    kg.add_fact("Lai_Suat_NHNN", "TAC_DONG_TIEU_CUC", "VN30", source="f03-fed", sign=-1, mechanism="Mặt bằng chiết khấu dòng tiền WACC tăng làm nén hệ số P/E toàn thị trường")
    kg.add_fact("Khoi_Ngoai_Ban_Rong", "TAC_DONG_TIEU_CUC", "VN30", source="f03-fed", sign=-1, mechanism="Áp lực cung bán ròng từ quỹ ngoại ép điểm số các mã vốn hóa lớn")

    kg.add_fact("Lai_Suat_NHNN", "TAC_DONG_TICH_CUC", "VCB", source="f01-ty-gia", sign=1, mechanism="Biên lãi thuần NIM ngân hàng lớn được bảo toàn và vị thế ngoại tệ sinh lời")

    # Gold Pricing Channel
    kg.add_fact("XAU_USD", "CAU_THANH_GIA", "Vang_Quy_Doi", source="f02-vang", sign=1, mechanism="Quy đổi = XAU * USD/VND * 1.2057")
    kg.add_fact("Ty_Gia_USD_VND", "CAU_THANH_GIA", "Vang_Quy_Doi", source="f02-vang", sign=1, mechanism="Tỷ giá tăng đẩy giá quy đổi tiền đồng tăng tương ứng")
    kg.add_fact("Vang_Quy_Doi", "TAC_DONG_TICH_CUC", "Vang_Nhan_9999", source="f02-vang", sign=1, mechanism="Vàng nhẫn bám sát 98% giá thế giới quy đổi")
    kg.add_fact("Vang_Quy_Doi", "TAC_DONG_TICH_CUC", "Vang_Mieng_SJC", source="f02-vang", sign=1, mechanism="Giá thế giới là giá sàn gốc cấu thành vàng miếng")

    kg.add_fact("Nghi_Dinh_24", "TAC_DONG_TICH_CUC", "Chenh_Lech_SJC", source="f02-vang", sign=1, mechanism="Độc quyền nguồn cung vàng miếng làm dội phần bù chênh lệch lên 15-20 triệu/lượng")
    kg.add_fact("Nghi_Dinh_232_2025", "SUA_DOI_BO_SUNG", "Nghi_Dinh_24", source="f02-vang", mechanism="Xóa bỏ độc quyền, cấp phép nhập khẩu nguyên liệu mới")
    kg.add_fact("Nghi_Dinh_232_2025", "TAC_DONG_TIEU_CUC", "Chenh_Lech_SJC", source="f02-vang", sign=-1, mechanism="Tăng nguồn cung bình ổn làm bốc hơi phần bù bất hợp lý về dưới 5%")
    kg.add_fact("Chenh_Lech_SJC", "TAC_DONG_TICH_CUC", "Vang_Mieng_SJC", source="f02-vang", sign=1, mechanism="Giá SJC = Giá thế giới quy đổi + Phần bù chênh lệch")

    return kg

if __name__ == "__main__":
    kg = build_vietnam_finance_kg()
    print(f"Built VietnamFinanceKG: {len(kg.G.nodes)} nodes, {len(kg.G.edges)} edges.")
