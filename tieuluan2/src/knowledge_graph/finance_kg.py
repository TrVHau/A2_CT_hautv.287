"""
VietnamFinanceKG: Macroeconomic and Multi-Asset Causal Knowledge Graph for Vietnam
- 16 formal classes and 6 predicates (including signed causal relations)
- Empirical and theoretical transmission channels: Fed Rate -> DXY -> USD/VND -> Gold SJC / Stocks (FPT, VNM, HPG, VCB)
- Signed edge algebra (+1 / -1), path polarity multiplication, and shock propagation
"""

from typing import Dict, List, Any, Optional
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL
from .ontology import Ontology, Predicate
from .reasoning import CausalGraphReasoner


EX = Namespace("http://ptit.edu.vn/tieuluan2/finance/")


def build_finance_ontology() -> Ontology:
    """Builds the 16-class financial ontology with 6 predicates."""
    ont = Ontology("VietnamFinanceOntology")

    classes = [
        ("FinancialEntity", "Entity"),
        ("MacroIndicator", "FinancialEntity"),
        ("InterestRate", "MacroIndicator"),
        ("FedRate", "InterestRate"),
        ("SBVRate", "InterestRate"),
        ("ExchangeRate", "MacroIndicator"),
        ("DollarIndexDXY", "MacroIndicator"),
        ("Asset", "FinancialEntity"),
        ("CommodityAsset", "Asset"),
        ("PreciousMetal", "CommodityAsset"),
        ("WorldGoldXAU", "PreciousMetal"),
        ("DomesticGoldSJC", "PreciousMetal"),
        ("EquityAsset", "Asset"),
        ("StockVN30", "EquityAsset"),
        ("StockIndexVN30", "EquityAsset"),
        ("CorporateCostFactor", "FinancialEntity")
    ]
    for c, p in classes:
        ont.add_class(c, p)

    # 6 Predicates
    predicates = [
        Predicate("tang_dan_toi", "FinancialEntity", "FinancialEntity", polarity=1, description="Tác động nhân quả đồng chiều (+)"),
        Predicate("giam_dan_toi", "FinancialEntity", "FinancialEntity", polarity=-1, description="Tác động nhân quả ngược chiều (-)"),
        Predicate("thanh_phan_dinh_gia", "FinancialEntity", "FinancialEntity", description="Thành phần cấu thành giá"),
        Predicate("chi_phoi_boi_chinh_sach", "FinancialEntity", "MacroIndicator", description="Chịu sự điều tiết của chính sách"),
        Predicate("co_phan_trong_chi_so", "StockVN30", "StockIndexVN30", description="Cổ phiếu thành viên rổ VN30"),
        Predicate("tuong_quan_thuc_nghiem", "Asset", "Asset", symmetric=True, description="Tương quan thống kê lịch sử")
    ]
    for p in predicates:
        ont.add_predicate(p)

    return ont


class VietnamFinanceKG:
    """Vietnam Finance Causal Knowledge Graph implementation."""
    def __init__(self):
        self.ontology = build_finance_ontology()
        self.graph = Graph()
        self.graph.bind("ex", EX)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.causal_engine = CausalGraphReasoner()
        self.triples_raw: List[Dict[str, Any]] = []
        self._populate_knowledge()

    def _add_entity(self, eid: str, name_vi: str, cls: str, properties: Optional[Dict] = None):
        self.entities[eid] = {
            "id": eid,
            "name": name_vi,
            "class": cls,
            "properties": properties or {}
        }
        self.causal_engine.add_node(eid, name_vi, cls, properties)
        uri = EX[eid]
        self.graph.add((uri, RDF.type, EX[cls]))
        self.graph.add((uri, RDFS.label, Literal(name_vi, lang="vi")))

    def _add_causal_edge(self, s_id: str, t_id: str, sign: int, mechanism: str, source_doc: str):
        rel = "tang_dan_toi" if sign > 0 else "giam_dan_toi"
        self.causal_engine.add_edge(s_id, t_id, sign, rel, mechanism, source_doc)
        
        triple = {
            "subject": s_id,
            "subject_name": self.entities[s_id]["name"],
            "predicate": rel,
            "object": t_id,
            "object_name": self.entities[t_id]["name"],
            "sign": sign,
            "mechanism": mechanism,
            "source_doc": source_doc
        }
        self.triples_raw.append(triple)
        self.graph.add((EX[s_id], EX[rel], EX[t_id]))

    def _populate_knowledge(self):
        # 1. Macro Indicators
        self._add_entity("FED_RATE", "Lãi suất điều hành Fed (Federal Funds Rate)", "FedRate", {"country": "US", "instrument": "FFR"})
        self._add_entity("DXY", "Chỉ số sức mạnh đồng Đô la Mỹ (US Dollar Index)", "DollarIndexDXY")
        self._add_entity("USD_VND", "Tỷ giá hối đoái USD/VND (Thị trường liên ngân hàng)", "ExchangeRate")
        self._add_entity("SBV_RATE", "Lãi suất điều hành NHNN và Lãi suất liên ngân hàng VND", "SBVRate")
        
        # 2. Precious Metals / Gold
        self._add_entity("XAU_USD", "Giá vàng thế giới giao ngay (USD/troy oz)", "WorldGoldXAU")
        self._add_entity("GOLD_VND", "Giá vàng thế giới quy đổi (triệu VND/lượng)", "PreciousMetal")
        self._add_entity("SJC_PREMIUM", "Phần bù khan hiếm độc quyền thương hiệu vàng SJC", "MacroIndicator")
        self._add_entity("GOLD_SJC", "Giá vàng miếng SJC trong nước (triệu VND/lượng)", "DomesticGoldSJC")

        # 3. Equities / Stocks
        self._add_entity("VN30", "Chỉ số đại diện cổ phiếu vốn hóa lớn VN30 Index", "StockIndexVN30")
        self._add_entity("FPT", "Cổ phiếu CTCP FPT (HOSE: FPT) - Xuất khẩu CNTT & Chuyển đổi số", "StockVN30", {"beta": 0.75, "pe_ratio": 22.5})
        self._add_entity("VNM", "Cổ phiếu CTCP Sữa Việt Nam (HOSE: VNM) - Tiêu dùng thiết yếu", "StockVN30", {"beta": 0.52, "div_yield": "5.2%"})
        self._add_entity("HPG", "Cổ phiếu CTCP Tập đoàn Hòa Phát (HOSE: HPG) - Thép cuộn cán nóng", "StockVN30", {"beta": 1.35, "cycle": "High Cyclical"})
        self._add_entity("VCB", "Cổ phiếu NHTMCP Ngoại thương Việt Nam (HOSE: VCB) - Trụ cột ngân hàng", "StockVN30", {"beta": 0.88, "nim": "3.3%"})

        # 4. Input Cost Factors
        self._add_entity("RAW_MILK_COST", "Chi phí sữa bột nguyên liệu nhập khẩu tính bằng USD", "CorporateCostFactor")
        self._add_entity("FX_LOAN_EXPENSE", "Chi phí lỗ chênh lệch tỷ giá vay nợ USD của Hòa Phát", "CorporateCostFactor")

        # Macro Causal Links
        # Link 1: FED_RATE (+) -> DXY
        self._add_causal_edge("FED_RATE", "DXY", 1, "Fed thắt chặt tiền tệ thu hút dòng vốn toàn cầu, tăng sức mạnh đồng USD", "D10_Lai_Suat_Fed_Va_Dong_Von_Toan_Cau.txt")

        # Link 2: DXY (+) -> USD_VND
        self._add_causal_edge("DXY", "USD_VND", 1, "USD mạnh lên tạo áp lực tăng tỷ giá USD/VND qua kênh carry trade và chênh lệch lãi suất", "D09_Dieu_Hanh_Ty_Gia_USD_VND_Va_Chinh_Sach_Tien_Te.txt")

        # Link 3: USD_VND (+) -> SBV_RATE
        self._add_causal_edge("USD_VND", "SBV_RATE", 1, "NHNN phát hành tín phiếu hút tiền hoặc tăng lãi suất điều hành để bảo vệ tỷ giá và dự trữ ngoại hối", "D09_Dieu_Hanh_Ty_Gia_USD_VND_Va_Chinh_Sach_Tien_Te.txt")

        # Link 4: SBV_RATE (-) -> VN30
        self._add_causal_edge("SBV_RATE", "VN30", -1, "Lãi suất trong nước tăng làm tăng chi phí vốn vay và nâng lãi suất chiết khấu định giá cổ phiếu", "D11_Tong_Quan_Chi_So_VN30_Va_Co_Cau_Nganh.txt")

        # Link 5: FED_RATE (-) -> XAU_USD
        self._add_causal_edge("FED_RATE", "XAU_USD", -1, "Lãi suất thực tế của Mỹ tăng làm tăng chi phí cơ hội nắm giữ vàng vô sinh lợi", "D16_Chênh_Lech_Gia_Vang_Va_Ty_Gia_Quy_Doi.txt")

        # Link 6: XAU_USD (+) -> GOLD_VND
        self._add_causal_edge("XAU_USD", "GOLD_VND", 1, "Giá vàng thế giới là thành phần cơ sở của công thức quy đổi giá vàng nội địa", "D16_Chênh_Lech_Gia_Vang_Va_Ty_Gia_Quy_Doi.txt")

        # Link 7: USD_VND (+) -> GOLD_VND
        self._add_causal_edge("USD_VND", "GOLD_VND", 1, "Tỷ giá USD/VND tăng làm tăng giá quy đổi VND của mỗi ounce vàng nhập khẩu", "D16_Chênh_Lech_Gia_Vang_Va_Ty_Gia_Quy_Doi.txt")

        # Link 8: GOLD_VND (+) -> GOLD_SJC
        self._add_causal_edge("GOLD_VND", "GOLD_SJC", 1, "Giá vàng quy đổi truyền dẫn trực tiếp vào giá vàng miếng SJC", "D07_Nghi_Dinh_24_Quan_Ly_Thi_Truong_Vang.txt")

        # Link 9: SJC_PREMIUM (+) -> GOLD_SJC
        self._add_causal_edge("SJC_PREMIUM", "GOLD_SJC", 1, "Độc quyền nguồn cung SJC tạo chênh lệch giá cộng thêm vào giá vật chất", "D07_Nghi_Dinh_24_Quan_Ly_Thi_Truong_Vang.txt")

        # Stock Specific Links
        # FPT: USD_VND (+) -> FPT (+) Natural Hedge (Doanh thu USD/JPY xuất khẩu phần mềm)
        self._add_causal_edge("USD_VND", "FPT", 1, "FPT hưởng lợi từ doanh thu xuất khẩu phần mềm bằng ngoại tệ trong khi chi phí nhân sự bằng VND", "D12_Phan_Tich_Co_Ban_Co_Phieu_FPT.txt")

        # VNM: USD_VND (+) -> RAW_MILK_COST (+) -> VNM (-)
        self._add_causal_edge("USD_VND", "RAW_MILK_COST", 1, "Tỷ giá tăng đẩy giá vốn nhập khẩu nguyên liệu bột sữa từ New Zealand", "D13_Phan_Tich_Co_Ban_Co_Phieu_VNM.txt")
        self._add_causal_edge("RAW_MILK_COST", "VNM", -1, "Chi phí nguyên liệu tăng làm xói mòn biên lợi nhuận gộp của Vinamilk", "D13_Phan_Tich_Co_Ban_Co_Phieu_VNM.txt")

        # HPG: USD_VND (+) -> FX_LOAN_EXPENSE (+) -> HPG (-)
        self._add_causal_edge("USD_VND", "FX_LOAN_EXPENSE", 1, "HPG vay nợ USD để mua máy móc Dung Quất, tỷ giá tăng làm tăng chi phí lỗ tỷ giá", "D14_Phan_Tich_Co_Ban_Co_Phieu_HPG.txt")
        self._add_causal_edge("FX_LOAN_EXPENSE", "HPG", -1, "Khoản lỗ chênh lệch tỷ giá ăn mòn trực tiếp lợi nhuận sau thuế của Hòa Phát", "D14_Phan_Tich_Co_Ban_Co_Phieu_HPG.txt")

        # VN30 Market Beta Channels
        self._add_causal_edge("VN30", "VCB", 1, "VCB là cổ phiếu vốn hóa lớn nhất chỉ số, hưởng lợi khi thanh khoản dòng tiền thị trường dồi dào", "D15_Phan_Tich_Co_Ban_Co_Phieu_VCB.txt")
        self._add_causal_edge("VN30", "HPG", 1, "HPG có hệ số beta 1.35, biến động khuếch đại theo chu kỳ chung của VN30", "D14_Phan_Tich_Co_Ban_Co_Phieu_HPG.txt")
        self._add_causal_edge("VN30", "VNM", 1, "VNM chịu ảnh hưởng bởi xu hướng dòng tiền khối ngoại và quỹ ETF ngoại", "D13_Phan_Tich_Co_Ban_Co_Phieu_VNM.txt")
        self._add_causal_edge("VN30", "FPT", 1, "FPT là thành phần công nghệ duy nhất trong rổ VN30, dẫn dắt đà tăng trưởng", "D12_Phan_Tich_Co_Ban_Co_Phieu_FPT.txt")

    def query_transmission_path(self, origin: str, target: str) -> Dict[str, Any]:
        """Queries multi-step causal reasoning between two financial variables."""
        return self.causal_engine.calculate_net_effect(origin, target)

    def query_shock_propagation(self, origin: str, direction: int = 1) -> Dict[str, Any]:
        """Queries network-wide shock propagation starting from a macro variable."""
        return self.causal_engine.propagate_shock(origin, direction)

    def get_summary_statistics(self) -> Dict[str, Any]:
        return {
            "name": "VietnamFinanceKG",
            "classes_count": len(self.ontology.classes),
            "predicates_count": len(self.ontology.predicates),
            "entities_count": len(self.entities),
            "causal_edges_count": len(self.triples_raw)
        }
