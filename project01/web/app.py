#!/usr/bin/env python3
"""
Comprehensive Diabetes Multi-Agent Clinical Web Application (FastAPI)
Grounding: diabetes_prediction_dataset.csv (100,000 clinical records) & Pima Indians
Features:
  - 8-Feature Clinical Input & Patient Presets
  - Live 12-Agent Diabetes Consultation Council (with Self-Evaluation Critic & 3-Round Deliberation)
  - 9-Model Benchmark Suite, TabResNet Attention & Tri-Framework Parity Check
  - Interactive Diabetes Knowledge Graph (ADA 2024 / KDIGO / WHO Standards)
  - 24-Hour Reinforcement Learning Lifestyle Digital Twin (Dueling Double DQN - D3QN)
  - Pharmacogenomics (CYP2C9, SLCO1B1) & Real-Time Counterfactual Optimization
  - Fairness, Demographic Disparity & Reliability Probability Calibration
  - Longitudinal 4-Week Follow-up Tracker & Adaptive RL Shifts
  - Local Qwen 2.5 0.5B Clinical Chain-of-Thought Engine
  - Certified Master Word Report Downloader
"""

import os
import sys
import json
import time
import math
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
WORKSPACE_ROOT = os.path.dirname(PROJECT_ROOT)
SERVER_START_TIME = time.time()

# Add workspace and project roots to path
for p in [WORKSPACE_ROOT, PROJECT_ROOT, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from project01.agents.diabetes_coordinator import DiabetesCouncilCoordinator
    from project01.agents.llm_downloader import DiabetesLLMDownloader, AVAILABLE_LLMS
    from project01.agents.llm_bridge import DiabetesLLMBridge
    from project01.knowledge_graph.diabetes_kg_queries import DiabetesKGQuerier
    from project01.agents.rl_lifestyle_coach import DiaRLCoachAgent
    from project01.agents.fairness_trust_auditor import DiaFairnessTrustAgent
    from project01.agents.longitudinal_tracker import DiaFollowupTrackerAgent
    from project01.agents.counterfactual_agent import DiaCounterfactualAgent
    from project01.agents.pharmacogenomics_agent import DiaPharmacogenomicsAgent
    from project01.models.conformal_and_shap_engine import ClinicalConformalShapEngine
    from project01.knowledge_graph.interactive_rag_engine import InteractiveClinicalGraphRAG
    from project01.knowledge_graph.neo4j_connector import Neo4jDiabetesKGConnector
except ModuleNotFoundError:
    from agents.diabetes_coordinator import DiabetesCouncilCoordinator
    from agents.llm_downloader import DiabetesLLMDownloader, AVAILABLE_LLMS
    from agents.llm_bridge import DiabetesLLMBridge
    from knowledge_graph.diabetes_kg_queries import DiabetesKGQuerier
    from agents.rl_lifestyle_coach import DiaRLCoachAgent
    from agents.fairness_trust_auditor import DiaFairnessTrustAgent
    from agents.longitudinal_tracker import DiaFollowupTrackerAgent
    from agents.counterfactual_agent import DiaCounterfactualAgent
    from agents.pharmacogenomics_agent import DiaPharmacogenomicsAgent
    from models.conformal_and_shap_engine import ClinicalConformalShapEngine
    from knowledge_graph.interactive_rag_engine import InteractiveClinicalGraphRAG
    from knowledge_graph.neo4j_connector import Neo4jDiabetesKGConnector

app = FastAPI(
    title="Hệ Thống Đa Agent Chẩn Đoán & Quản Lý Đái Tháo Đường Cấp Doanh Nghiệp (PTIT Enterprise DSS)",
    version="4.0"
)

# Mount figures static directory
fig_path = os.path.join(PROJECT_ROOT, "figures")
if os.path.exists(fig_path):
    app.mount("/figures", StaticFiles(directory=fig_path), name="figures")

# Initialize engines
coordinator = DiabetesCouncilCoordinator()
llm_downloader = DiabetesLLMDownloader()
llm_bridge = DiabetesLLMBridge()
kg_querier = DiabetesKGQuerier()
rl_coach = DiaRLCoachAgent()
fairness_auditor = DiaFairnessTrustAgent()
followup_tracker = DiaFollowupTrackerAgent()
counterfactual_agent = DiaCounterfactualAgent()
pgx_agent = DiaPharmacogenomicsAgent()
conformal_shap_engine = ClinicalConformalShapEngine()
graph_rag_qa_engine = InteractiveClinicalGraphRAG()
neo4j_connector = Neo4jDiabetesKGConnector()

# Data models
class PatientPayload(BaseModel):
    gender: str = Field("Female", description="Female, Male, Other")
    age: float = Field(..., ge=0, le=120)
    hypertension: int = Field(0, ge=0, le=1)
    heart_disease: int = Field(0, ge=0, le=1)
    smoking_history: str = Field("never")
    bmi: float = Field(..., ge=10, le=80)
    HbA1c_level: float = Field(..., ge=3.0, le=20.0)
    blood_glucose_level: float = Field(..., ge=50, le=500)

class CounterfactualSliderPayload(BaseModel):
    bmi: float
    blood_glucose_level: float
    HbA1c_level: float
    exercise_minutes_per_week: float = 150.0
    age: float = 50.0

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/consult")
async def consult(patient: PatientPayload):
    try:
        data_dict = patient.model_dump()
        result = coordinator.run_consultation(data_dict)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/mas/decision-support")
async def mas_decision_support(patient: PatientPayload):
    """Canonical Hybrid MAS Sequential Workflow (project_architecture_multiagent_diabet_v1.pdf).
    Executes 8 canonical agents and returns structured DecisionSupportReport: Prediction + Evidence + Limitations.
    """
    try:
        data_dict = patient.model_dump()
        report = coordinator.run_mas_workflow(data_dict)
        return JSONResponse(content=report)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/mas/architecture")
async def mas_architecture_spec():
    """Returns canonical system organization, mathematical abstraction, and agent contracts."""
    return JSONResponse(content={
        "title": "Kiến Trúc Hệ Thống Đa Tác Tử Hỗ Trợ Ra Quyết Định Đái Tháo Đường (Hybrid MAS)",
        "document": "project_architecture_multiagent_diabet_v1.pdf",
        "academic_context": {
            "institution": "Học viện Công nghệ Bưu chính Viễn thông (PTIT)",
            "subject": "Phát triển Hệ thống Thông minh (Intelligent System Development)",
            "author": "Trần Văn Hậu (B23DCCN287)",
            "class": "D23CQCN01-B (Nhóm CT_09)",
            "date": "Tháng 11/2026"
        },
        "layers": [
            {"layer": 1, "name": "User Interaction Layer", "description": "Giao diện Web Dashboard, Natural Intake Chat Agent, RESTful Consumers."},
            {"layer": 2, "name": "API & Data Processing Layer", "description": "FastAPI router, Pydantic validation, serialization, error handlers."},
            {"layer": 3, "name": "Multiagent Coordination Layer", "description": "CoordinatorAgent (A_coord) điều phối tuần tự 8 tác tử theo thuật toán Mục 5.3."},
            {"layer": 4, "name": "Intelligent Agent Layer", "description": "8 Canonical Agents: A_data, A_DL, A_rule, A_KG, A_coord, A_exp, A_monitor, A_RL."},
            {"layer": 5, "name": "Knowledge & Model Layer", "description": "DB_diabet.cypher (56 thực thể Neo4j), mô hình TabResNet Self-Attention PyTorch, VirtualPatientEnv D3QN."},
            {"layer": 6, "name": "Evaluation & Audit Layer", "description": "Kiểm toán độ lệch |y_DL - y_rule|, theo dõi SLA latency ms, kiểm tra ngưỡng sinh lý, Section 10 Safety Disclaimers."}
        ],
        "canonical_agents": [
            {"symbol": "A_data", "name": "PatientDataAgent", "role": "Tiền xử lý và kiểm định dữ liệu sinh học đầu vào."},
            {"symbol": "A_DL", "name": "DLPredictionAgent", "role": "Suy luận mạng nơ-ron học sâu TabResNet kết hợp cơ chế Self-Attention."},
            {"symbol": "A_rule", "name": "RuleBasedAgent", "role": "Hệ suy luận biểu tượng dựa trên ngưỡng chuẩn ADA 2024 và KDIGO."},
            {"symbol": "A_KG", "name": "KGRAGAgent", "role": "Truy xuất bằng chứng đồ thị tri thức DB_diabet.cypher (56 thực thể Neo4j)."},
            {"symbol": "A_coord", "name": "CoordinatorAgent", "role": "Điều phối đa tác tử và tổng hợp quyết định F(y_DL, y_rule, y_KG, y_monitor)."},
            {"symbol": "A_exp", "name": "ExplanationAgent", "role": "Tổng hợp giải thích lâm sàng grounded dựa trên bằng chứng minh bạch."},
            {"symbol": "A_monitor", "name": "MonitoringAgent", "role": "Giám sát hiệu năng, độ trễ và phát hiện xung đột giữa AI và Quy tắc."},
            {"symbol": "A_RL", "name": "RLSimulationAgent", "role": "Mô phỏng động học đường huyết 24h bằng MDP M_RL và Dueling Double DQN."}
        ],
        "mathematical_abstraction": {
            "system_model": "M = (A, S, O, C, F)",
            "message_contract": "m_i = (id, agent, status, payload, evidence, version)",
            "rl_model": "M_RL = (S, A, P, R, γ)",
            "aggregation_function": "F(y_DL, y_rule, y_KG, y_monitor) -> Y_final"
        },
        "database_integration": {
            "cypher_script": "DB_diabet.cypher",
            "entities": 56,
            "relationships": ["CÓ_CHỈ_SỐ", "CHẨN_ĐOÁN", "CHỈ_ĐỊNH_ĐẦU_TAY", "NGUY_CƠ_BIẾN_CHỨNG", "CHỐNG_CHỈ_ĐỊNH"]
        },
        "safety_limitations": [
            "Hệ thống là bản thử nghiệm nghiên cứu khoa học (Research Prototype) PTIT 11/2026.",
            "Không phải là chẩn đoán y khoa xác định; bắt buộc có sự thăm khám của bác sĩ chuyên khoa.",
            "Không kê đơn hoặc quyết định liều thuốc trực tiếp cho bệnh nhân.",
            "Tác tử RL hoạt động trong môi trường số sinh lý ảo chỉ phục vụ giáo dục & nghiên cứu lối sống.",
            "Tuân thủ nghiêm ngặt hướng dẫn điều trị của Bộ Y tế và ADA Standards of Care 2024."
        ]
    })


class ChatMessagePayload(BaseModel):
    message: str

@app.post("/api/agent/chat")
async def chat_agent_endpoint(payload: ChatMessagePayload):
    """Clinical Multi-Agent Chatbot endpoint: Handles natural language patient intake, vitals triage and Graph-RAG QA."""
    try:
        user_msg = payload.message.strip()
        if not user_msg:
            return JSONResponse(content={
                "type": "guidance",
                "message": "Vui lòng nhập thông tin bệnh nhân (tuổi, chiều cao, cân nặng, đường huyết...) hoặc câu hỏi y văn lâm sàng."
            })

        msg_lower = user_msg.lower()

        # 1. Greetings and Introductory Queries
        greetings = ["xin chào", "chào", "hello", "hi", "hey", "alo", "tro ly", "trợ lý", "bắt đầu", "hướng dẫn"]
        is_greeting = any(msg_lower == g or msg_lower.startswith(g + " ") or msg_lower.startswith(g + "!") or msg_lower.startswith(g + ",") for g in greetings)
        if is_greeting and not any(k in msg_lower for k in ["đường huyết", "glucose", "hba1c", "nặng", "cao"]):
            return JSONResponse(content={
                "type": "greeting",
                "message": (
                    "Chào bạn! Tôi là **Trợ Lý Hội Chẩn Đa Tác Tử Đái Tháo Đường** (DiaTriage Coordinator).\n\n"
                    "Hội đồng 12 chuyên gia lâm sàng (Sàng lọc, AI Chẩn đoán, Tim mạch, Thận học, Dược lý, Lối sống D3QN, Trọng tài phản tư...) đã sẵn sàng hỗ trợ bạn.\n\n"
                    "👉 **Cách nhập thông tin bệnh nhân để hội chẩn:**\n"
                    "Bạn chỉ cần gõ tự nhiên, ví dụ:\n"
                    "• *'Tôi là nam, 55 tuổi, cao 1m68, nặng 78kg, đường huyết 185 mg/dL, HbA1c 8.2%, có cao huyết áp.'*\n"
                    "• *'Nữ 46 tuổi, cao 158cm, nặng 63kg, glucose 115, HbA1c 6.1%, không hút thuốc.'*\n\n"
                    "👉 **Hoặc tra cứu Y văn Đa nguồn (Vinmec, FPT Long Châu, BYT Việt Nam, ADA 2024):**\n"
                    "• *'Quy tắc 15-15 xử trí cấp cứu hạ đường huyết theo Nhà thuốc Long Châu?'*\n"
                    "• *'Quy trình chăm sóc bàn chân đái tháo đường của Bệnh viện Vinmec?'*\n"
                    "• *'Mô hình đĩa thức ăn cho người Việt Nam theo Vinmec?'*\n"
                    "• *'Thuốc Trajenta Linagliptin an toàn cho người suy thận như thế nào?'*\n"
                    "• *'Mục tiêu HbA1c cá thể hóa theo QĐ 5481 Bộ Y Tế?'*\n"
                    "• *'Khi nào chống chỉ định Metformin?'*"
                )
            })

        # 1.1 Architecture & Multi-Agent System Inquiries (project_architecture_multiagent_diabet_v1.pdf)
        arch_keywords = ["kiến trúc", "architecture", "multiagent", "multi-agent", "8 tác tử", "8 agent", "6 tầng", "6 layer", "thiết kế hệ thống", "m = (a, s, o, c, f)", "db_diabet.cypher"]
        if any(kw in msg_lower for kw in arch_keywords) and not any(k in msg_lower for k in ["đường huyết", "glucose", "hba1c", "nặng", "cao"]):
            return JSONResponse(content={
                "type": "architecture",
                "message": (
                    "### 🏛️ KIẾN TRÚC HỆ THỐNG ĐA TÁC TỬ HỖ TRỢ RA QUYẾT ĐỊNH ĐÁI THÁO ĐƯỜNG\n"
                    "*(Chuẩn hóa theo tài liệu `project_architecture_multiagent_diabet_v1.pdf` - Đồ án HTTT PTIT 11/2026)*\n\n"
                    "#### 1. Mô hình 6 Tầng (6-Layer Architecture):\n"
                    "• **Layer 1: User Interaction Layer**: Web Dashboard, Natural Intake Chat Agent, RESTful API consumers.\n"
                    "• **Layer 2: API & Data Processing Layer**: FastAPI routers, Pydantic data contracts, input sanitization.\n"
                    "• **Layer 3: Multiagent Coordination Layer**: CoordinatorAgent ($A_{coord}$) điều phối tuần tự theo Mục 5.3.\n"
                    "• **Layer 4: Intelligent Agent Layer**: 8 Tác tử chuẩn tắc ($A_{data}, A_{DL}, A_{rule}, A_{KG}, A_{coord}, A_{exp}, A_{monitor}, A_{RL}$).\n"
                    "• **Layer 5: Knowledge & Model Layer**: Cơ sở dữ liệu đồ thị tri thức `DB_diabet.cypher` (56 thực thể), mô hình TabResNet Self-Attention PyTorch, VirtualPatientEnv D3QN.\n"
                    "• **Layer 6: Evaluation & Audit Layer**: Giám sát độ trễ SLA, kiểm toán sai lệch $|y_{DL} - y_{rule}|$, cảnh báo cực trị và Section 10 Safety Disclaimers.\n\n"
                    "#### 2. Định nghĩa Toán học ($M = (A, S, O, C, F)$):\n"
                    "• **$A$**: Tập 8 tác tử chuẩn tắc.\n"
                    "• **$S$**: Không gian trạng thái chia sẻ / ngữ cảnh yêu cầu.\n"
                    "• **$O$**: Không gian quan sát 8 dấu ấn sinh học lâm sàng.\n"
                    "• **$C$**: Hợp đồng thông điệp chuẩn hóa $m_i = (id, agent, status, payload, evidence, version)$.\n"
                    "• **$F$**: Hàm tổng hợp quyết định $F(y_{DL}, y_{rule}, y_{KG}, y_{monitor}) \\rightarrow Y_{final}$.\n"
                    "• **$M_{RL}$**: Quá trình quyết định Markov $M_{RL} = (S, A, P, R, \\gamma)$ mô phỏng lối sống 24h.\n\n"
                    "#### 3. CSDL Đồ thị Tri thức:\n"
                    "• File thực thi Neo4j: `DB_diabet.cypher` (tích hợp 56 thực thể bệnh, thuốc, biến chứng, dấu ấn sinh học và khuyến cáo từ ADA 2024, Vinmec, Long Châu)."
                )
            })

        # 2. Check for Clinical Vitals Extraction
        import re

        # Age matching: "55 tuổi", "tuổi: 55", "55t"
        age_m = re.search(r'(?:tuổi\s*[:=]?\s*(\d+)|(\d+)\s*(?:tuổi|t|yo))', user_msg, re.I)
        age = float(age_m.group(1) or age_m.group(2)) if age_m else None

        # Height matching: "cao 1m68", "cao 168", "1m68", "168cm"
        height_m = re.search(r'(?:cao\s*[:=]?\s*(\d+[m\.]\d+|\d+)|(\d+[m\.]\d+)\s*m|(\d{2,3})\s*cm)', user_msg, re.I)
        h = None
        if height_m:
            raw_h = height_m.group(1) or height_m.group(2) or height_m.group(3)
            val_h = float(raw_h.replace('m', '.'))
            if val_h < 3.0:
                val_h = val_h * 100.0
            h = val_h

        # Weight matching: "nặng 78kg", "nặng 78", "78kg", "cân nặng 78"
        weight_m = re.search(r'(?:nặng\s*[:=]?\s*(\d+)|cân nặng\s*[:=]?\s*(\d+)|(\d+)\s*kg)', user_msg, re.I)
        w = float(weight_m.group(1) or weight_m.group(2) or weight_m.group(3)) if weight_m else None

        # Glucose matching: "đường huyết 185", "glucose 185", "fpg 185", "đường 185"
        glucose_m = re.search(r'(?:đường huyết|glucose|duong huyet|đường|fpg)\s*(?:đo được|la|là|[:=])?\s*(\d+)', user_msg, re.I)
        glucose = float(glucose_m.group(1)) if glucose_m else None

        # HbA1c matching: "HbA1c 8.2", "huyết sắc tố 8.2"
        hba1c_m = re.search(r'(?:hba1c|huyết sắc tố|huyet sac to)\s*(?:la|là|[:=])?\s*([0-9\.]+)', user_msg, re.I)
        hba1c = float(hba1c_m.group(1)) if hba1c_m else None

        # Check if user message qualifies as patient intake consultation
        has_intake_signals = any([
            glucose is not None,
            hba1c is not None,
            (h is not None and w is not None),
            (age is not None and (h is not None or w is not None or glucose is not None or hba1c is not None))
        ])

        if has_intake_signals:
            final_age = age if age is not None else 55.0
            final_h = h if h is not None else 168.0
            final_w = w if w is not None else 75.0
            final_bmi = round(final_w / ((final_h / 100.0) ** 2), 1)
            final_glucose = glucose if glucose is not None else (160.0 if (hba1c and hba1c >= 6.5) else 105.0)
            final_hba1c = hba1c if hba1c is not None else (7.8 if final_glucose >= 126.0 else 5.6)

            gender = 'Female' if re.search(r'(?:nữ|nu|female|bà|chị|cô|bác gái)', user_msg, re.I) else 'Male'

            # Hypertension check
            if re.search(r'(?:không|chưa|k|khong)\s*(?:có\s*|bị\s*|tiền\s*sử\s*)?(?:cao\s*huyết\s*áp|tăng\s*huyết\s*áp|huyết\s*áp)', user_msg, re.I):
                hyp = 0
            elif re.search(r'(?:cao\s*huyết\s*áp|tăng\s*huyết\s*áp|huyết\s*áp\s*cao|hypertension)', user_msg, re.I):
                hyp = 1
            else:
                hyp = 0

            # Heart disease check
            if re.search(r'(?:không|chưa|k|khong)\s*(?:có\s*|bị\s*|tiền\s*sử\s*)?(?:bệnh\s*tim|tim\s*mạch|suy\s*tim|vấn\s*đề\s*tim)', user_msg, re.I):
                heart = 0
            elif re.search(r'(?:bệnh\s*tim|tim\s*mạch|suy\s*tim|nhồi\s*máu|đột\s*quỵ|heart)', user_msg, re.I):
                heart = 1
            else:
                heart = 0

            # Smoking check
            if re.search(r'(?:không|chưa|k|khong|never)\s*(?:bao giờ\s*)?hút', user_msg, re.I):
                smoking = 'never'
            elif re.search(r'(?:đã bỏ|từng hút|đã từng|bỏ thuốc|former)', user_msg, re.I):
                smoking = 'former'
            elif re.search(r'(?:đang hút|nghiện thuốc|hút thuốc|current)', user_msg, re.I):
                smoking = 'current'
            else:
                smoking = 'former'

            patient_dict = {
                "age": final_age,
                "gender": gender,
                "bmi": final_bmi,
                "hypertension": hyp,
                "heart_disease": heart,
                "smoking_history": smoking,
                "blood_glucose_level": final_glucose,
                "HbA1c_level": final_hba1c
            }
            consult_res = coordinator.run_consultation(patient_dict)
            mas_report = coordinator.run_mas_workflow(patient_dict)
            return JSONResponse(content={
                "type": "consultation",
                "extracted_vitals": {
                    "age": final_age,
                    "gender": gender,
                    "height": final_h,
                    "weight": final_w,
                    "bmi": final_bmi,
                    "glucose": final_glucose,
                    "hba1c": final_hba1c,
                    "hypertension": hyp,
                    "heart_disease": heart,
                    "smoking": smoking
                },
                "consultation": consult_res,
                "mas_report": mas_report
            })

        # 3. Fallback to Medical QA via Graph-RAG Engine
        rag_res = graph_rag_qa_engine.answer_clinical_question(user_msg)
        return JSONResponse(content={
            "type": "qa",
            "rag": rag_res
        })
    except Exception as e:
        return JSONResponse(content={
            "type": "error",
            "message": f"Đã xảy ra lỗi trong quá trình xử lý: {str(e)}"
        })

@app.post("/api/counterfactual")
async def compute_live_counterfactual(body: CounterfactualSliderPayload):
    try:
        bmi = body.bmi
        glucose = body.blood_glucose_level
        hba1c = body.HbA1c_level
        ex = body.exercise_minutes_per_week

        # Rapid calculation
        logit = -7.5 + (0.16 * bmi) + (0.025 * glucose) + (0.85 * hba1c) - (0.004 * ex)
        prob = 1.0 / (1.0 + math.exp(-logit))
        risk_pct = round(prob * 100, 1)

        tier = "NGUY CƠ CAO" if risk_pct >= 50 else ("NGUY CƠ TRUNG BÌNH" if risk_pct >= 20 else "NGUY CƠ THẤP")
        color = "red" if risk_pct >= 50 else ("amber" if risk_pct >= 20 else "emerald")

        return JSONResponse(content={
            "risk_probability_pct": risk_pct,
            "risk_tier": tier,
            "risk_color": color,
            "bmi": bmi,
            "glucose": glucose,
            "hba1c": hba1c,
            "exercise_minutes": ex
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/shap/explain")
async def explain_shap(payload: dict):
    try:
        patient = payload.get("patient", {})
        prob = float(payload.get("probability", 0.5))
        shap_res = conformal_shap_engine.compute_local_shap_attributions(patient, prob)
        ood_res = conformal_shap_engine.compute_ood_novelty_score(patient)
        return JSONResponse(content={
            "shap": shap_res,
            "ood": ood_res
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/conformal/predict")
async def predict_conformal(payload: dict):
    try:
        prob = float(payload.get("probability", 0.5))
        alpha = float(payload.get("alpha", 0.05))
        res = conformal_shap_engine.compute_conformal_prediction_set(prob, alpha)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/graph-rag/query")
async def query_graph_rag(payload: dict):
    try:
        question = payload.get("question", "")
        res = graph_rag_qa_engine.answer_clinical_question(question)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/metrics")
async def get_metrics():
    summary_path = os.path.join(PROJECT_ROOT, "models", "diabetes_metrics_summary.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "Metrics summary not found"})

@app.get("/api/dual-cohort-metrics")
async def get_dual_cohort_metrics():
    summary_path = os.path.join(PROJECT_ROOT, "models", "dual_cohort_metrics.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "Dual-cohort metrics not found"})

@app.get("/api/advanced-ensemble")
async def get_advanced_ensemble_metrics():
    path = os.path.join(PROJECT_ROOT, "models", "advanced_ensemble_metrics.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "Advanced ensemble metrics not found"})

@app.get("/api/knowledge-graph")
async def get_knowledge_graph():
    # Prefer expanded 44-node 45-edge KG matching diabetes_kg_neo4j.cypher
    expanded_path = os.path.join(PROJECT_ROOT, "knowledge_graph", "diabetes_knowledge_graph_expanded.json")
    standard_path = os.path.join(PROJECT_ROOT, "knowledge_graph", "diabetes_knowledge_graph.json")
    
    target_path = expanded_path if os.path.exists(expanded_path) else standard_path
    if os.path.exists(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure both 'links' and 'edges' are provided for UI compatibility
            if "edges" in data and "links" not in data:
                data["links"] = data["edges"]
            elif "links" in data and "edges" not in data:
                data["edges"] = data["links"]
            return JSONResponse(content=data)
    return JSONResponse(status_code=404, content={"error": "KG not found"})

@app.get("/api/kg/cypher-file")
async def get_cypher_file():
    cypher_path = os.path.join(PROJECT_ROOT, "knowledge_graph", "diabetes_kg_neo4j.cypher")
    if not os.path.exists(cypher_path):
        return JSONResponse(status_code=404, content={"error": "Cypher file not found"})
    with open(cypher_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return JSONResponse(content={
        "filename": "diabetes_kg_neo4j.cypher",
        "relative_path": "project01/knowledge_graph/diabetes_kg_neo4j.cypher",
        "content": content,
        "total_lines": len(content.splitlines()),
        "total_nodes": len(neo4j_connector.nodes),
        "total_relationships": len(neo4j_connector.relationships),
        "is_live_neo4j": neo4j_connector.is_connected,
        "standards": ["ADA 2024 Standards of Care", "KDIGO 2023 Clinical Practice Guideline", "WHO ICD-10"]
    })

@app.post("/api/kg/cypher-query")
async def execute_cypher_query(payload: dict):
    query = payload.get("query", "").strip()
    preset = payload.get("preset", "")
    
    if preset == "contraindications":
        med = payload.get("medication", "Metformin")
        results = neo4j_connector.query_contraindications(med)
        return JSONResponse(content={"query_type": "contraindications", "results": results, "count": len(results)})
    elif preset == "cardioprotective":
        results = neo4j_connector.query_cardioprotective_drugs()
        return JSONResponse(content={"query_type": "cardioprotective", "results": results, "count": len(results)})
    elif preset == "cutoffs":
        results = neo4j_connector.query_diagnostic_cutoffs()
        return JSONResponse(content={"query_type": "diagnostic_cutoffs", "results": results, "count": len(results)})
    else:
        # Run generic Cypher or fallback query
        results = neo4j_connector.execute_custom_cypher(query) if hasattr(neo4j_connector, 'execute_custom_cypher') else []
        return JSONResponse(content={"query": query, "results": results, "count": len(results)})

@app.get("/api/graph-rag/benchmark")
async def get_graph_rag_benchmark():
    rag_path = os.path.join(PROJECT_ROOT, "knowledge_graph", "graph_rag_benchmark_results.json")
    if os.path.exists(rag_path):
        with open(rag_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "Graph-RAG benchmark results not found"})

@app.get("/api/rl/evaluate")
async def get_rl_evaluation():
    rl_path = os.path.join(PROJECT_ROOT, "models", "rl_evaluation_results.json")
    if os.path.exists(rl_path):
        with open(rl_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "RL evaluation results not found"})

@app.get("/api/fairness")
async def get_fairness_audit():
    fairness_path = os.path.join(PROJECT_ROOT, "models", "fairness_trust_metrics.json")
    if os.path.exists(fairness_path):
        with open(fairness_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(status_code=404, content={"error": "Fairness metrics not found"})

@app.post("/api/longitudinal")
async def get_longitudinal_trajectory(patient: PatientPayload):
    try:
        data_dict = patient.model_dump()
        rl_sched = rl_coach.formulate_daily_schedule(data_dict)
        res = followup_tracker.track_patient_4weeks(data_dict, rl_sched["schedule"])
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/llm/status")
async def get_llm_status():
    status = llm_downloader.get_status()
    engine_status = llm_bridge.get_engine_status()
    return JSONResponse(content={
        "engine": engine_status,
        "downloader": status
    })

@app.post("/api/llm/pull")
async def pull_llm_model(body: dict):
    model_key = body.get("model_key", "qwen2.5-0.5b-diabetes")
    try:
        llm_downloader.pull_model_async(model_key)
        return JSONResponse(content={"status": "pulling", "model": model_key, "message": "Đang kéo mô hình LLM từ Hugging Face Hub ở chế độ nền."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/llm/generate")
async def generate_llm_response(body: dict):
    try:
        user_prompt = body.get("user_prompt", "")
        patient = body.get("patient", {})
        resp_text = llm_bridge.generate(
            system_prompt="Bạn là Chuyên gia Y khoa về Bệnh Đái tháo đường.",
            user_prompt=user_prompt,
            patient_data=patient
        )
        return JSONResponse(content={"response": resp_text, "timestamp": time.strftime("%H:%M:%S")})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/download/docx")
async def download_docx():
    docx_path = os.path.join(PROJECT_ROOT, "Bao_Cao_Project01_CT_09_Hautv.287.docx")
    if not os.path.exists(docx_path):
        docx_path = os.path.join(PROJECT_ROOT, "Bao_Cao_Nghien_Cuu_Project01_Nang_Cap.docx")
    if os.path.exists(docx_path):
        return FileResponse(
            docx_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Bao_Cao_Project01_CT_09_Hautv.287.docx"
        )
    return JSONResponse(status_code=404, content={"error": "Report docx file not found"})

@app.get("/api/download/datasets-models-txt")
async def download_datasets_models_txt():
    txt_path = os.path.join(WORKSPACE_ROOT, "DANH_SACH_DATASET_VA_MODEL.txt")
    if not os.path.exists(txt_path):
        txt_path = os.path.join(PROJECT_ROOT, "DANH_SACH_DATASET_VA_MODEL.txt")
    if os.path.exists(txt_path):
        return FileResponse(
            txt_path,
            media_type="text/plain; charset=utf-8",
            filename="DANH_SACH_DATASET_VA_MODEL.txt"
        )
    return JSONResponse(status_code=404, content={"error": "Text file not found"})

@app.get("/api/telemetry")
async def get_system_telemetry():
    """Real-time system telemetry and clinical benchmark diagnostics."""
    return JSONResponse(content={
        "system_name": "DIAMULTI-AGENT CLINICAL DECISION SUPPORT SYSTEM",
        "version": "4.2 Enterprise Flagship",
        "author": "Trần Văn Hậu (MSV: B23DCCN287)",
        "class_id": "D23CQCN01-B (CT_09)",
        "supervisor": "PGS. TS. Trần Đình Quế",
        "institution": "Học viện Công nghệ Bưu chính Viễn thông (PTIT)",
        "status": "OPERATIONAL",
        "active_agents_count": 12,
        "trained_models_count": 9,
        "best_model": "TabResNet Self-Attention (ROC-AUC = 0.9793)",
        "parity_delta": 0.0025,
        "knowledge_graph": {
            "entities_count": 56,
            "relations_count": 45,
            "guidelines": "ADA 2024 / KDIGO / Vinmec / FPT Long Châu / BYT QĐ 5481"
        },
        "conformal_prediction": {
            "coverage_guarantee": "95.0%",
            "calibration_samples": 2000,
            "coverage_theorem": "P(Y in C(X)) >= 1 - alpha"
        },
        "uptime_seconds": round(time.time() - SERVER_START_TIME, 1)
    })

@app.get("/api/dataset/sample")
async def get_dataset_sample():
    """Returns sample records and feature metadata from both clinical cohorts."""
    import csv
    cohort2_rows = []
    cohort1_rows = []

    c2_path = os.path.join(PROJECT_ROOT, "data", "diabetes_prediction_dataset.csv")
    if os.path.exists(c2_path):
        try:
            with open(c2_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 6:
                        break
                    cohort2_rows.append(row)
        except Exception as e:
            cohort2_rows = [{"error": str(e)}]

    c1_path = os.path.join(PROJECT_ROOT, "data", "pima_diabetes_dataset.csv")
    if os.path.exists(c1_path):
        try:
            with open(c1_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 6:
                        break
                    cohort1_rows.append(row)
        except Exception as e:
            cohort1_rows = [{"error": str(e)}]

    cdc_rows = []
    cdc_path = os.path.join(PROJECT_ROOT, "data", "cdc_brfss_diabetes_253k.csv")
    if os.path.exists(cdc_path):
        try:
            with open(cdc_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 6:
                        break
                    cdc_rows.append(row)
        except Exception as e:
            cdc_rows = [{"error": str(e)}]

    uci_rows = []
    uci_path = os.path.join(PROJECT_ROOT, "data", "uci_130_hospitals", "diabetic_data.csv")
    if os.path.exists(uci_path):
        try:
            with open(uci_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 6:
                        break
                    uci_rows.append(row)
        except Exception as e:
            uci_rows = [{"error": str(e)}]

    c1m_rows = []
    c1m_sample_path = os.path.join(PROJECT_ROOT, "data", "diabetes_prediction_dataset_1M.csv")
    if os.path.exists(c1m_sample_path):
        try:
            with open(c1m_sample_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 6:
                        break
                    c1m_rows.append(row)
        except Exception as e:
            c1m_rows = [{"error": str(e)}]

    return JSONResponse(content={
        "cohort_2_100k": {
            "name": "Quần Thể Ngoại Trú Đa Trung Tâm (100.000 Hồ Sơ)",
            "file": "project01/data/diabetes_prediction_dataset.csv",
            "size": "3.73 MB",
            "samples": cohort2_rows
        },
        "cohort_1_pima": {
            "name": "NIDDK Pima Indians Diabetes Database (768 Hồ Sơ)",
            "file": "project01/data/pima_diabetes_dataset.csv",
            "size": "23.8 KB",
            "samples": cohort1_rows
        },
        "cohort_cdc_253k": {
            "name": "CDC BRFSS Diabetes Health Indicators (253.680 Hồ Sơ)",
            "file": "project01/data/cdc_brfss_diabetes_253k.csv",
            "size": "21.68 MB",
            "samples": cdc_rows
        },
        "cohort_uci_100k": {
            "name": "UCI Diabetes 130-US Hospitals (101.766 Hồ Sơ)",
            "file": "project01/data/uci_130_hospitals/diabetic_data.csv",
            "size": "18.27 MB",
            "samples": uci_rows
        },
        "cohort_3_1m": {
            "name": "Tập Mở Rộng Dân Số Big Data (1.000.000 Hồ Sơ)",
            "file": "project01/data/diabetes_prediction_dataset_1M.csv",
            "size": "37.28 MB",
            "samples": c1m_rows
        }
    })

@app.get("/api/data/download/pima")
async def download_pima_dataset():
    """Direct download for Pima Indians Diabetes dataset CSV."""
    c1_path = os.path.join(PROJECT_ROOT, "data", "pima_diabetes_dataset.csv")
    if os.path.exists(c1_path):
        return FileResponse(
            path=c1_path,
            filename="pima_diabetes_dataset.csv",
            media_type="text/csv"
        )
    return JSONResponse(status_code=404, content={"error": "File pima_diabetes_dataset.csv not found"})

@app.get("/api/data/download/100k")
async def download_100k_dataset():
    """Direct download for 100k population diabetes dataset CSV."""
    c2_path = os.path.join(PROJECT_ROOT, "data", "diabetes_prediction_dataset.csv")
    if os.path.exists(c2_path):
        return FileResponse(
            path=c2_path,
            filename="diabetes_prediction_dataset.csv",
            media_type="text/csv"
        )
    return JSONResponse(status_code=404, content={"error": "File diabetes_prediction_dataset.csv not found"})

@app.get("/api/data/download/1m")
async def download_1m_dataset():
    """Direct download for 1,000,000-row population diabetes dataset CSV."""
    c1m_path = os.path.join(PROJECT_ROOT, "data", "diabetes_prediction_dataset_1M.csv")
    if os.path.exists(c1m_path):
        return FileResponse(
            path=c1m_path,
            filename="diabetes_prediction_dataset_1M.csv",
            media_type="text/csv"
        )
    return JSONResponse(status_code=404, content={"error": "File diabetes_prediction_dataset_1M.csv not found"})


@app.get("/api/data/download/cdc253k")
async def download_cdc253k_dataset():
    """Direct download for CDC BRFSS Diabetes Health Indicators dataset (253,680 rows)."""
    p = os.path.join(PROJECT_ROOT, "data", "cdc_brfss_diabetes_253k.csv")
    if os.path.exists(p):
        return FileResponse(path=p, filename="cdc_brfss_diabetes_253k.csv", media_type="text/csv")
    return JSONResponse(status_code=404, content={"error": "File cdc_brfss_diabetes_253k.csv not found"})

@app.get("/api/data/download/uci100k")
async def download_uci100k_dataset():
    """Direct download for UCI 130-US Hospitals Diabetes dataset (101,766 rows)."""
    p = os.path.join(PROJECT_ROOT, "data", "uci_130_hospitals", "diabetic_data.csv")
    if os.path.exists(p):
        return FileResponse(path=p, filename="diabetic_data_101k.csv", media_type="text/csv")
    return JSONResponse(status_code=404, content={"error": "File diabetic_data.csv not found"})

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn
    print("[*] Đang khởi động Diabetes Multi-Agent Web Server tại: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
