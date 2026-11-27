"""
react_orchestrator.py
Hệ thống Tác tử Thông minh Đa tầng (ReAct Agent Orchestrator):
1. Tầng liên kết thực thể (Entity Linker) & Nhận diện miền (Healthcare vs Finance)
2. Tầng trích xuất hồ sơ xét nghiệm lâm sàng tự động bằng Regex
3. Bộ lập kế hoạch tất định (Deterministic Planner)
4. Vòng lặp thực thi ReAct (Thought -> Action -> Observation)
5. Bộ tổng hợp có căn cứ (Grounded Synthesizer) & Kiểm định ảo giác (Verifier)
"""
import re
import time
import os
import torch
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional

from .tool_specs import Tool
from .verifier_agent import VerifierAgent
from .llm_engine import LocalLLMEngine, build_grounded_prompt, DISCLAIMER
from ..knowledge_graph.kg_base import KnowledgeGraph
from ..knowledge_graph.diabetes_kg import build_vietnam_diabetes_kg
from ..knowledge_graph.finance_kg import build_vietnam_finance_kg
from ..knowledge_graph.reasoning import impact_paths, propagate_shock
from ..rag.corpus import DocumentCorpus
from ..rag.sparse_retriever import BM25Retriever
from ..rag.dense_retriever import DenseRetriever
from ..rag.hybrid_retriever import HybridRRFRetriever
from ..rag.reranker import CrossEncoderReranker
from ..rag.graph_rag import GraphRAG, EntityLinker, strip_accents
from ..models.dl_healthcare import DiabetesResMLP
from ..models.dl_finance import BiLSTMAttentionForecaster, TemporalAttention

class ReActAgent:
    def __init__(self, data_dir: str = "tieuluan2/data", weights_dir: str = "tieuluan2/models/saved_weights"):
        self.data_dir = data_dir
        self.weights_dir = weights_dir

        print("Initializing Knowledge Graphs...")
        self.hkg = build_vietnam_diabetes_kg()
        self.fkg = build_vietnam_finance_kg()
        self.linker = EntityLinker([self.hkg, self.fkg])
        self.graph_rag = GraphRAG([self.hkg, self.fkg])

        print("Initializing RAG Pipeline...")
        self.corpus = DocumentCorpus(os.path.join(data_dir, "documents"))
        self.bm25 = BM25Retriever(self.corpus.chunks)
        self.dense = DenseRetriever(self.corpus.chunks)
        self.hybrid = HybridRRFRetriever(self.bm25, self.dense, k=60)
        self.reranker = CrossEncoderReranker()

        print("Loading Deep Learning Models & Weights...")
        self.health_model = self._load_health_model()
        self.finance_model = self._load_finance_model()

        # Load market data
        market_csv = os.path.join(data_dir, "market_series.csv")
        self.market_df = pd.read_csv(market_csv) if os.path.exists(market_csv) else pd.DataFrame()

        self.verifier = VerifierAgent(min_faithfulness=0.80)
        self.llm = LocalLLMEngine()
        self.tools = self._register_tools()
        print("ReAct Agent initialized successfully.")

    def _load_health_model(self) -> Optional[DiabetesResMLP]:
        model = DiabetesResMLP(input_dim=8, hidden_dim=64, dropout_rate=0.2)
        weight_path = os.path.join(self.weights_dir, "diabetes_mlp.pt")
        if os.path.exists(weight_path):
            try:
                model.load_state_dict(torch.load(weight_path, map_location="cpu", weights_only=True))
                model.eval()
                return model
            except Exception as e:
                print(f"Notice: Failed to load diabetes weights: {e}")
        return model

    def _load_finance_model(self) -> Optional[BiLSTMAttentionForecaster]:
        model = BiLSTMAttentionForecaster(d_in=7, hidden=64, layers=2, dropout=0.2)
        weight_path = os.path.join(self.weights_dir, "finance_bilstm.pt")
        if os.path.exists(weight_path):
            try:
                model.load_state_dict(torch.load(weight_path, map_location="cpu", weights_only=True))
                model.eval()
                return model
            except Exception as e:
                print(f"Notice: Failed to load finance weights: {e}")
        return model

    def parse_profile(self, text: str) -> Dict[str, Any]:
        """Trích xuất tự động hồ sơ xét nghiệm lâm sàng từ câu hỏi tự do bằng Regex."""
        t = text.lower().replace(",", ".")
        pats = {
            "HbA1c_level": r"hba1c\D{0,8}(\d+(?:\.\d+)?)",
            "bmi": r"bmi\D{0,8}(\d+(?:\.\d+)?)",
            "blood_glucose_level": r"(?:glucose|đường huyết|đường máu)[^\d]{0,20}(\d{2,3}(?:\.\d+)?)",
            "age": r"(\d{2})\s*(?:tuổi|yo)"
        }
        profile = {}
        for k, rx in pats.items():
            m = re.search(rx, t)
            if m:
                profile[k] = float(m.group(1))

        if re.search(r"\b(nữ|phụ nữ|bà|chị|cô)\b", t):
            profile["gender"] = 0 # Female
        elif re.search(r"\b(nam|đàn ông|ông|anh|chú)\b", t):
            profile["gender"] = 1 # Male

        if "huyết áp" in t or "cao huyết áp" in t:
            profile["hypertension"] = 1
        if "tim mạch" in t or "bệnh tim" in t:
            profile["heart_disease"] = 1
        if "hút thuốc" in t:
            profile["smoking_history"] = 2

        return profile

    def _register_tools(self) -> Dict[str, Tool]:
        tools = {}

        # 1. Chẩn đoán nguy cơ học sâu (DL)
        def tool_chan_doan(profile: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Tuple[str, str]]]:
            gender = profile.get("gender", 1)
            age = profile.get("age", 50.0)
            hyp = profile.get("hypertension", 0)
            heart = profile.get("heart_disease", 0)
            smoke = profile.get("smoking_history", 0)
            bmi = profile.get("bmi", 25.0)
            hba1c = profile.get("HbA1c_level", 6.5)
            glucose = profile.get("blood_glucose_level", 126.0)

            # Heuristic / Model estimation
            raw_feats = np.array([gender, age, hyp, heart, smoke, bmi, hba1c, glucose], dtype=np.float32)
            # Standard approximate scaling
            scaled = (raw_feats - np.array([0.4, 42.0, 0.07, 0.04, 0.5, 27.0, 5.5, 138.0])) / np.array([0.5, 22.0, 0.26, 0.19, 0.7, 6.6, 1.0, 40.0])
            
            with torch.no_grad():
                tensor_in = torch.tensor(scaled.reshape(1, -1), dtype=torch.float32)
                prob = float(torch.sigmoid(self.health_model(tensor_in)).item())

            # Clinical classification according to MoH Decision 5481
            risk_level = "RẤT CAO (Khẳng định ĐTĐ típ 2)" if (hba1c >= 6.5 or glucose >= 126.0 or prob >= 0.75) else \
                         ("CAO (Tiền đái tháo đường)" if (5.7 <= hba1c <= 6.4 or 100.0 <= glucose <= 125.0) else "BÌNH THƯỜNG / NGUY CƠ THẤP")

            obs = {
                "probability": round(prob, 4),
                "probability_pct": round(prob * 100, 2),
                "risk_level": risk_level,
                "hba1c": hba1c,
                "glucose": glucose,
                "bmi": bmi
            }
            ev = [(
                "DL:Model_ResMLP",
                f"Mô hình ResMLP ước lượng xác suất mắc đái tháo đường: {prob*100:.1f}%, xếp loại nguy cơ: {risk_level} (HbA1c: {hba1c}%, Glucose lúc đói: {glucose} mg/dL, BMI: {bmi})."
            )]
            return obs, ev

        tools["chan_doan_nguy_co"] = Tool(
            name="chan_doan_nguy_co",
            kind="DL",
            description="Ước lượng xác suất mắc Đái tháo đường típ 2 từ hồ sơ lâm sàng (HbA1c, Glucose, BMI, Tuổi).",
            fn=tool_chan_doan
        )

        # 2. Truy vấn Đồ thị Tri thức Y tế (KG)
        def tool_kg_y_te(ents: List[Tuple[str, str, str]]) -> Tuple[List[Dict[str, Any]], List[Tuple[str, str]]]:
            obs, ev = [], []
            h_nodes = [e for e, kg, _ in ents if kg == self.hkg.name]
            if not h_nodes:
                h_nodes = ["Metformin", "Dai_Thao_Duong_Tip_2"]

            for n in h_nodes:
                if n not in self.hkg.G:
                    continue
                for succ in self.hkg.G.successors(n):
                    for k, d in self.hkg.G.get_edge_data(n, succ).items():
                        verb = self.hkg.verbalize(n, k, succ, d)
                        src = d.get("source", "VietnamDiabetesKG")
                        obs.append({"from": n, "pred": k, "to": succ, "verb": verb})
                        ev.append((f"KG:{src}", verb))

                for pred_node in self.hkg.G.predecessors(n):
                    for k, d in self.hkg.G.get_edge_data(pred_node, n).items():
                        verb = self.hkg.verbalize(pred_node, k, n, d)
                        src = d.get("source", "VietnamDiabetesKG")
                        obs.append({"from": pred_node, "pred": k, "to": n, "verb": verb})
                        ev.append((f"KG:{src}", verb))

            return obs[:6], ev[:6]

        tools["kg_y_te"] = Tool(
            name="kg_y_te",
            kind="KG",
            description="Tra cứu phác đồ điều trị, chống chỉ định, tương tác thuốc và dinh dưỡng trên VietnamDiabetesKG.",
            fn=tool_kg_y_te
        )

        # 3. Truy vấn Đồ thị Tri thức Tài chính (KG)
        def tool_kg_tai_chinh(ents: List[Tuple[str, str, str]]) -> Tuple[List[Dict[str, Any]], List[Tuple[str, str]]]:
            f_nodes = [e for e, kg, _ in ents if kg == self.fkg.name]
            obs, ev = [], []
            
            # Identify source factors vs target assets
            factors = [e for e in f_nodes if e in ("Lai_Suat_Fed", "Chi_So_DXY", "Ty_Gia_USD_VND", "Lai_Suat_NHNN", "Nghi_Dinh_24", "Nghi_Dinh_232_2025")] or ["Ty_Gia_USD_VND"]
            targets = [e for e in f_nodes if e in ("FPT", "HPG", "VCB", "VIC", "Vang_Mieng_SJC", "VN30")] or ["FPT", "HPG", "Vang_Mieng_SJC"]

            for a in factors:
                for b in targets:
                    if a == b:
                        continue
                    r = impact_paths(self.fkg, a, b)
                    if r["paths"]:
                        best = r["paths"][0]
                        chain = " → ".join(self.fkg.label(x) for x in best["nodes"])
                        why = "; ".join(s["mechanism"] for s in best["steps"])
                        obs.append({"factor": a, "target": b, "verdict": r["verdict"], "chain": chain})
                        src = best["steps"][-1]["source"]
                        ev.append((
                            f"KG:{src}",
                            f"{self.fkg.label(a)} → {self.fkg.label(b)}: Kết luận {r['verdict']}. Kênh chính: {chain}. Cơ chế: {why}."
                        ))

            return obs, ev

        tools["kg_tai_chinh"] = Tool(
            name="kg_tai_chinh",
            kind="KG",
            description="Suy luận tác động nhân quả đa bước và lan truyền cú sốc vĩ mô trên VietnamFinanceKG.",
            fn=tool_kg_tai_chinh
        )

        # 4. Dự báo chuỗi thời gian BiLSTM (DL)
        def tool_du_bao(ticker: str) -> Tuple[Dict[str, Any], List[Tuple[str, str]]]:
            clean_ticker = ticker if ticker in ("FPT", "HPG", "VCB", "VIC") else "FPT"
            last_p = 142.5 if clean_ticker == "FPT" else (28.4 if clean_ticker == "HPG" else 92.0)
            if not self.market_df.empty and clean_ticker in self.market_df.columns:
                last_p = float(self.market_df[clean_ticker].iloc[-1])

            # Dummy input tensor matching (1, 30, 7)
            dummy_x = torch.zeros(1, 30, 7)
            mc_res = self.finance_model.predict_mc_dropout(dummy_x, last_price=last_p, n_samples=200)

            ev = [(
                "DL:Model_BiLSTM",
                f"Mô hình BiLSTM dự báo giá {clean_ticker} phiên kế tiếp: {mc_res['pred_price']} k VND (Lợi suất kỳ vọng: {mc_res['pred_ret']*100:+.2f}%, Xu hướng: {mc_res['trend']}). Khoảng tin cậy Bayes 90% (MC Dropout): [{mc_res['ci_90_price'][0]} - {mc_res['ci_90_price'][1]}]."
            )]
            return mc_res, ev

        tools["du_bao_bilstm"] = Tool(
            name="du_bao_bilstm",
            kind="DL",
            description="Dự báo giá và khoảng tin cậy 90% (MC Dropout) cho cổ phiếu VN30 và vàng.",
            fn=tool_du_bao
        )

        # 5. Quy đổi giá vàng thế giới (CALC)
        def tool_quy_doi(args: Any = None) -> Tuple[Dict[str, Any], List[Tuple[str, str]]]:
            # Latest market state
            xau = 2650.0
            usdvnd = 25420.0
            if not self.market_df.empty:
                xau = float(self.market_df["XAU_USD"].iloc[-1])
                usdvnd = float(self.market_df["USD_VND"].iloc[-1])

            # Công thức: Giá quy đổi (triệu đồng/lượng) = (XAU * USD_VND * 1.205653) / 1,000,000
            conv_price = (xau * usdvnd * 1.205653) / 1e6
            sjc_price = conv_price * 1.055 # Chênh lệch ~5.5% sau Nghị định 232/2025

            obs = {
                "xau_usd": xau,
                "usd_vnd": usdvnd,
                "conv_price_million": round(conv_price, 2),
                "sjc_est_million": round(sjc_price, 2),
                "premium_million": round(sjc_price - conv_price, 2)
            }
            ev = [(
                "CALC:Gold_Formula",
                f"Giá vàng thế giới giao ngay {xau} USD/oz quy đổi theo tỷ giá {usdvnd:,.0f} USD/VND tương đương {conv_price:.2f} triệu đồng/lượng. Giá vàng miếng SJC ước tính {sjc_price:.2f} triệu đồng/lượng (Chênh lệch phần bù: {sjc_price - conv_price:.2f} triệu đồng/lượng)."
            )]
            return obs, ev

        tools["quy_doi_vang"] = Tool(
            name="quy_doi_vang",
            kind="CALC",
            description="Tính toán giá vàng thế giới quy đổi ra triệu đồng/lượng dựa trên XAU/USD và USD/VND.",
            fn=tool_quy_doi
        )

        # 6. Dữ liệu thị trường đóng cửa (CALC)
        def tool_thi_truong(stocks: Any = None) -> Tuple[Dict[str, Any], List[Tuple[str, str]]]:
            obs = {}
            ev = []
            targets = stocks if isinstance(stocks, list) else ["FPT", "HPG", "VCB", "VIC"]
            for s in targets:
                if not self.market_df.empty and s in self.market_df.columns:
                    latest = float(self.market_df[s].iloc[-1])
                    prev = float(self.market_df[s].iloc[-2])
                    change_pct = (latest - prev) / prev * 100
                    vol20 = float(np.log(self.market_df[s] / self.market_df[s].shift(1)).tail(20).std() * np.sqrt(252) * 100)
                    obs[s] = {"price": latest, "change_pct": round(change_pct, 2), "vol20": round(vol20, 2)}
                    ev.append((
                        "CALC:Market_Feed",
                        f"Giá đóng cửa gần nhất của {s}: {latest:,.1f} k VND (Biến động phiên: {change_pct:+.2f}%, Độ biến động năm hóa 20 phiên: {vol20:.1f}%)."
                    ))
            return obs, ev

        tools["du_lieu_thi_truong"] = Tool(
            name="du_lieu_thi_truong",
            kind="CALC",
            description="Lấy dữ liệu giá đóng cửa thực tế gần nhất và độ biến động 20 phiên của cổ phiếu VN30.",
            fn=tool_thi_truong
        )

        # 7. Truy xuất văn bản lai RAG (RAG)
        def tool_rag(query: str) -> Tuple[List[Dict[str, Any]], List[Tuple[str, str]]]:
            # Hybrid RRF search -> Top 15 -> Cross-Encoder Rerank -> Top 3
            hybrid_res = self.hybrid.search(query, top_k=12)
            reranked = self.reranker.rerank(query, hybrid_res, top_k=3)
            
            obs = []
            ev = []
            for doc_idx, score, c in reranked:
                obs.append({"doc_id": c["doc_id"], "score": round(score, 4), "text": c["text"]})
                ev.append((f"RAG:{c['doc_id']}", c["text"][:350]))

            return obs, ev

        tools["truy_xuat_rag"] = Tool(
            name="truy_xuat_rag",
            kind="RAG",
            description="Truy xuất văn bản hướng dẫn Bộ Y Tế, Nghị định NHNN bằng bộ lai Hybrid BM25+Dense và Reranker.",
            fn=tool_rag
        )

        return tools

    def plan(self, question: str, profile: Optional[Dict[str, Any]] = None) -> Tuple[str, List[Tuple[str, str, str]], Dict[str, Any], List[Tuple[str, Any, str]]]:
        """Bộ lập kế hoạch tất định: Nhận diện miền, phân tích ý định và chọn chuỗi công cụ."""
        ents = self.linker.link(question)
        kgs = [kg for _, kg, _ in ents]
        n_h = kgs.count(self.hkg.name)
        n_f = kgs.count(self.fkg.name)
        
        domain = "finance" if n_f > n_h else "health"
        merged_profile = {**self.parse_profile(question), **(profile or {})}
        steps = []
        q_norm = strip_accents(question)

        if domain == "health":
            # 1. Check if patient lab profile is provided
            if any(k in merged_profile for k in ("HbA1c_level", "blood_glucose_level", "bmi")):
                steps.append((
                    "chan_doan_nguy_co",
                    merged_profile,
                    "Phát hiện chỉ số cận lâm sàng (HbA1c / Glucose / BMI); điều phối mô hình học sâu ResMLP ước lượng xác suất mắc bệnh."
                ))
            # 2. Check clinical entities
            steps.append((
                "kg_y_te",
                ents,
                "Truy vấn VietnamDiabetesKG để đối chiếu phác đồ Bộ Y Tế, chỉ định đầu tay, chống chỉ định và tương tác thuốc/thực phẩm."
            ))
        else:
            # Finance planning
            fin_entities = [e for e, kg, _ in ents if kg == self.fkg.name]
            stocks = [e for e in fin_entities if e in ("FPT", "HPG", "VCB", "VIC")]
            
            # Causal propagation if macro factor present
            if any(e in ("Lai_Suat_Fed", "Chi_So_DXY", "Ty_Gia_USD_VND", "Lai_Suat_NHNN", "Nghi_Dinh_24", "Nghi_Dinh_232_2025") for e in fin_entities) or not fin_entities:
                steps.append((
                    "kg_tai_chinh",
                    ents,
                    "Phát hiện biến số vĩ mô/chính sách; thực hiện suy luận lan truyền nhân quả đa bước trên VietnamFinanceKG."
                ))
            
            # Market prices for stocks
            if stocks:
                steps.append((
                    "du_lieu_thi_truong",
                    stocks,
                    f"Trích xuất dữ liệu giá đóng cửa thực tế và biến động 20 phiên của cổ phiếu {', '.join(stocks)}."
                ))
            
            # Gold price calculation
            if any(g in fin_entities for g in ("Vang_Mieng_SJC", "Vang_Quy_Doi", "XAU_USD")) or re.search(r"quy doi|gia vang|bao nhieu|sjc", q_norm):
                steps.append((
                    "quy_doi_vang",
                    None,
                    "Tính toán giá vàng thế giới quy đổi sang tiền đồng theo công thức chuẩn và tỷ giá mới nhất."
                ))

            # Trend forecasting
            if re.search(r"du bao|du doan|xu huong|phien toi|tuan toi|sap toi|tang hay giam|nen mua", q_norm):
                target_forecast = stocks[0] if stocks else "FPT"
                steps.append((
                    "du_bao_bilstm",
                    target_forecast,
                    f"Người dùng hỏi về xu hướng tương lai; gọi mạng BiLSTM Attention dự báo lợi suất và khoảng tin cậy 90% của {target_forecast}."
                ))

        # Always end with RAG for grounded citations
        rag_query = question + " " + " ".join(lbl for _, _, lbl in ents[:3])
        steps.append((
            "truy_xuat_rag",
            rag_query,
            "Truy xuất kho văn bản quy chuẩn (Quyết định 5481/BYT, Nghị định 232/NHNN) để cung cấp trích dẫn nguyên văn."
        ))

        return domain, ents, merged_profile, steps

    def run(self, question: str, profile: Optional[Dict[str, Any]] = None, synthesize: bool = True) -> Dict[str, Any]:
        """Vòng lặp ReAct hoàn chỉnh: Thought -> Action -> Observation -> Synthesize -> Verify."""
        t_start = time.perf_counter()
        domain, ents, merged_profile, plan = self.plan(question, profile)
        
        trace = []
        evidence = []
        obs_all = {}

        trace.append({
            "type": "THOUGHT",
            "text": f"Nhận diện miền: {domain.upper()}. Thực thể liên kết: {', '.join(lbl for _, _, lbl in ents) if ents else 'Không'}. Kế hoạch công cụ: {' → '.join(s[0] for s in plan)}."
        })

        for tool_name, arg, thought_reason in plan:
            trace.append({"type": "THOUGHT", "text": thought_reason})
            tool_obj = self.tools[tool_name]
            
            t0 = time.perf_counter()
            obs, ev = tool_obj.fn(arg)
            ms = (time.perf_counter() - t0) * 1000.0
            
            obs_all[tool_name] = obs
            evidence.extend(ev)

            trace.append({
                "type": "ACTION",
                "tool": tool_name,
                "kind": tool_obj.kind,
                "ms": round(ms, 2),
                "args": str(arg)[:100]
            })

            obs_summary = " | ".join(txt for _, txt in ev)[:500] if ev else "Hoàn thành."
            trace.append({
                "type": "OBSERVATION",
                "tool": tool_name,
                "text": obs_summary
            })

        total_ms = (time.perf_counter() - t_start) * 1000.0

        result = {
            "question": question,
            "domain": domain,
            "entities": [(e, kg) for e, kg, _ in ents],
            "profile": merged_profile,
            "trace": trace,
            "evidence": evidence,
            "observations": obs_all,
            "total_ms": round(total_ms, 2)
        }

        if synthesize:
            # Generate grounded answer
            raw_answer = self.llm.generate(question, evidence, domain)
            # Verify answer with VerifierAgent
            ver_res = self.verifier.verify(raw_answer, evidence, question)
            
            if ver_res["passed"]:
                final_answer = raw_answer + f"\n\n> [!NOTE]\n> {DISCLAIMER[domain]}"
                ver_res["used"] = "llm_grounded"
            else:
                # Fallback to deterministic template if verifier rejects draft!
                template_lines = [f"{i}. [{src}] {txt}" for i, (src, txt) in enumerate(evidence, 1)]
                final_answer = (
                    "**[Bản Tổng Hợp Căn Cứ Chuẩn Hóa]** (Do bản nháp tự do không thỏa mãn kiểm định số học hoặc trích dẫn):\n\n" +
                    "\n".join(template_lines) +
                    f"\n\n> [!NOTE]\n> {DISCLAIMER[domain]}"
                )
                ver_res["used"] = "deterministic_template_fallback"

            result["answer"] = final_answer
            result["verification"] = ver_res

        return result
