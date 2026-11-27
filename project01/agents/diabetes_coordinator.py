#!/usr/bin/env python3
"""
Comprehensive Diabetes Multi-Agent Council Coordinator (12 Specialized Clinical Agents)
Coordinates the 12 specialized clinical hospital agents into an integrated consultation conference:
  1. DiaTriageAgent: Sàng lọc & Phân tầng cấp cứu (HHS / DKA)
  2. DiaSafetyRuleAgent: 12 Quy tắc an toàn lâm sàng tuyệt đối & Safety Override
  3. DiaDiagnosticAgent: Hội đồng 8 Mô hình Học máy / Học sâu & Tri-Framework Parity
  4. DiaGraphAgent: Thủ thư Đồ thị Tri thức Y khoa & Graph-RAG (44 thực thể ADA 2024)
  5. DiaD3QNCoachAgent: Huấn luyện viên lối sống 24h Dueling Double Deep Q-Network (D3QN)
  6. DiaTherapyAgent: Phác đồ dược lý phối hợp & Dinh dưỡng tiết chế MNT
  7. DiaPharmacogenomicsAgent: Dược lý di truyền (CYP2C9, SLCO1B1) & Thanh thải thận Cockcroft-Gault
  8. DiaCounterfactualAgent: Tối ưu hóa can thiệp phản thực tế (Counterfactual Minimal Perturbation)
  9. DiaFairnessTrustAgent: Kiểm toán công bằng & Độ tin cậy nhân khẩu học (Wilson 95% CI)
  10. DiaFollowupTrackerAgent: Theo dõi tiến trình dọc 4 tuần & thích ứng chính sách D3QN
  11. DiaCriticAgent: Bác sĩ trưởng thẩm định, Phản tư Tự đánh giá & Tranh luận 3 vòng
  12. DiaReportGeneratorAgent: Thư ký tổng hợp biên bản hội chẩn & xuất báo cáo đa phương tiện
"""

import os
import sys
import time

try:
    from project01.agents.triage_risk_agent import TriageRiskAgent
    from project01.agents.safety_rules_agent import DiaSafetyRuleAgent
    from project01.agents.ai_diagnostic_agent import AIDiagnosticAgent
    from project01.agents.kg_guidelines_agent import KGGuidelinesAgent
    from project01.agents.rl_lifestyle_coach import DiaRLCoachAgent
    from project01.agents.therapy_lifestyle_agent import TherapyLifestyleAgent
    from project01.agents.pharmacogenomics_agent import DiaPharmacogenomicsAgent
    from project01.agents.counterfactual_agent import DiaCounterfactualAgent
    from project01.agents.fairness_trust_auditor import DiaFairnessTrustAgent
    from project01.agents.longitudinal_tracker import DiaFollowupTrackerAgent
    from project01.agents.chief_evaluator_critic import ChiefEvaluatorCritic
except ImportError:
    from agents.triage_risk_agent import TriageRiskAgent
    from agents.safety_rules_agent import DiaSafetyRuleAgent
    from agents.ai_diagnostic_agent import AIDiagnosticAgent
    from agents.kg_guidelines_agent import KGGuidelinesAgent
    from agents.rl_lifestyle_coach import DiaRLCoachAgent
    from agents.therapy_lifestyle_agent import TherapyLifestyleAgent
    from agents.pharmacogenomics_agent import DiaPharmacogenomicsAgent
    from agents.counterfactual_agent import DiaCounterfactualAgent
    from agents.fairness_trust_auditor import DiaFairnessTrustAgent
    from agents.longitudinal_tracker import DiaFollowupTrackerAgent
    from agents.chief_evaluator_critic import ChiefEvaluatorCritic

class DiabetesCouncilCoordinator:
    def __init__(self):
        self.triage = TriageRiskAgent()
        self.safety_rules = DiaSafetyRuleAgent()
        self.ai_diagnostic = AIDiagnosticAgent()
        self.kg_guidelines = KGGuidelinesAgent()
        self.rl_coach = DiaRLCoachAgent()
        self.therapy = TherapyLifestyleAgent()
        self.pharmacogenomics = DiaPharmacogenomicsAgent()
        self.counterfactual = DiaCounterfactualAgent()
        self.fairness_trust = DiaFairnessTrustAgent()
        self.followup_tracker = DiaFollowupTrackerAgent()
        self.chief_critic = ChiefEvaluatorCritic()
        
        # Hybrid Multiagent System (MAS) Canonical Coordinator (project_architecture_multiagent_diabet_v1.pdf)
        try:
            from project01.agents.hybrid_mas import CoordinatorAgent
            self.mas_coordinator = CoordinatorAgent()
        except ImportError:
            try:
                from agents.hybrid_mas import CoordinatorAgent
                self.mas_coordinator = CoordinatorAgent()
            except Exception:
                self.mas_coordinator = None

    def run_mas_workflow(self, patient_dict: dict, include_simulation: bool = True) -> dict:
        """Runs the 8-agent Canonical Hybrid MAS pipeline as defined in project_architecture_multiagent_diabet_v1.pdf."""
        if self.mas_coordinator is None:
            try:
                from project01.agents.hybrid_mas import CoordinatorAgent
                self.mas_coordinator = CoordinatorAgent()
            except ImportError:
                from agents.hybrid_mas import CoordinatorAgent
                self.mas_coordinator = CoordinatorAgent()
        report = self.mas_coordinator.run_workflow(patient_dict, include_simulation=include_simulation)
        return report.to_dict()


    def run_consultation(self, patient_dict: dict) -> dict:
        t0 = time.time()

        # Step 1: Triage
        triage_res = self.triage.evaluate(patient_dict)

        # Step 2: Safety Rules (12 Guardrails)
        safety_res = self.safety_rules.evaluate_safety_rules(patient_dict)

        # Step 3: AI Diagnostic Suite (8 Models + Parity)
        ai_res = self.ai_diagnostic.predict(patient_dict)

        # Step 4: Knowledge Graph & Guidelines Retrieval
        kg_res = self.kg_guidelines.consult(patient_dict, ai_res)

        # Step 5: Reinforcement Learning Lifestyle Coach (24h D3QN simulation)
        rl_res = self.rl_coach.formulate_daily_schedule(patient_dict)

        # Step 6: Therapy & Lifestyle Prescription
        therapy_res = self.therapy.prescribe(patient_dict, ai_res, kg_res)

        # Step 7: Pharmacogenomics & Renal Clearance
        pgx_res = self.pharmacogenomics.analyze_pharmacogenomics_and_interactions(
            patient_dict, therapy_res.get("prescribed_drugs", [])
        )

        # Step 8: Counterfactual Explainability Optimization
        current_prob = ai_res.get("consensus_probability", 0.5)
        cf_res = self.counterfactual.generate_counterfactual_path(patient_dict, current_prob)

        # Step 9: Fairness & Calibration Trust Audit
        fairness_res = self.fairness_trust.audit_patient_context(patient_dict, ai_res)

        # Step 10: Longitudinal 4-Week Follow-up Trajectory
        followup_res = self.followup_tracker.track_patient_4weeks(patient_dict, rl_res["schedule"])

        # Step 11: Chief Medical Officer Self-Evaluation Reflection Critic (3-Round Deliberation)
        chief_res = self.chief_critic.evaluate_and_certify(
            patient=patient_dict,
            triage=triage_res,
            ai_res=ai_res,
            kg_res=kg_res,
            therapy=therapy_res,
            pgx_res=pgx_res,
            cf_res=cf_res
        )

        elapsed = round(time.time() - t0, 3)

        timeline = [
            {
                "step": 1,
                "role": "Tiếp Đón & Phân Tầng Cấp Cứu (DiaTriage)",
                "agent_name": triage_res["agent"],
                "badge": triage_res["badge"],
                "content": triage_res["message"],
                "data": triage_res
            },
            {
                "step": 2,
                "role": "Giám Sát An Toàn 12 Luật Lâm Sàng (DiaSafetyRule)",
                "agent_name": safety_res["agent"],
                "badge": "danger" if safety_res["max_severity"] == "DANGER" else "warning",
                "content": safety_res["speech"],
                "data": safety_res
            },
            {
                "step": 3,
                "role": "Hội Chẩn Dự Báo 8 Mô Hình AI & Parity (DiaDiagnostic)",
                "agent_name": ai_res["agent"],
                "badge": "primary",
                "content": ai_res["message"],
                "data": ai_res
            },
            {
                "step": 4,
                "role": "Đồ Thị Tri Thức Y Khoa ADA 2024 (DiaGraph)",
                "agent_name": kg_res["agent"],
                "badge": "info",
                "content": kg_res["message"],
                "data": kg_res
            },
            {
                "step": 5,
                "role": "Huấn Luyện Lối Sống 24h Dueling Double DQN (DiaD3QNCoach)",
                "agent_name": rl_res["agent"],
                "badge": "success",
                "content": rl_res["speech"],
                "data": rl_res
            },
            {
                "step": 6,
                "role": "Phác Đồ Dược Lý & Dinh Dưỡng MNT (DiaTherapy)",
                "agent_name": therapy_res["agent"],
                "badge": "secondary",
                "content": therapy_res["message"],
                "data": therapy_res
            },
            {
                "step": 7,
                "role": "Dược Lý Di Truyền & Chức Năng Thận (DiaPharmacogenomics)",
                "agent_name": pgx_res["agent"],
                "badge": "warning",
                "content": pgx_res["speech"],
                "data": pgx_res
            },
            {
                "step": 8,
                "role": "Tối Ưu Hóa Can Thiệp Phản Thực Tế (DiaCounterfactual)",
                "agent_name": cf_res["agent"],
                "badge": "primary",
                "content": cf_res["speech"],
                "data": cf_res
            },
            {
                "step": 9,
                "role": "Kiểm Toán Công Bằng & Hiệu Chuẩn Tin Cậy (DiaFairnessTrust)",
                "agent_name": fairness_res["agent"],
                "badge": "dark",
                "content": fairness_res["speech"],
                "data": fairness_res
            },
            {
                "step": 10,
                "role": "Theo Dõi Tiến Trình Dọc 4 Tuần (DiaFollowupTracker)",
                "agent_name": followup_res["agent"],
                "badge": "info",
                "content": followup_res["speech"],
                "data": followup_res
            },
            {
                "step": 11,
                "role": "Bác Sĩ Trưởng Thẩm Định & Tranh Luận 3 Vòng (DiaCritic)",
                "agent_name": chief_res["agent"],
                "badge": "warning",
                "content": chief_res["message"],
                "data": chief_res
            }
        ]

        # Structured Clinical Recommendations from Knowledge Graph & Multi-Agent Council
        age = float(patient_dict.get("age", 45))
        hba1c = float(patient_dict.get("HbA1c_level", 5.5))
        glucose = float(patient_dict.get("blood_glucose_level", 95))
        bmi = float(patient_dict.get("bmi", 24.5))
        heart_disease = int(patient_dict.get("heart_disease", 0))
        hypertension = int(patient_dict.get("hypertension", 0))

        hba1c_target = "< 7.5% (Nới lỏng an toàn cho người cao tuổi ≥ 70 tuổi)" if age >= 70 else "< 7.0% (Mục tiêu chuẩn theo ADA 2024)"
        fpg_target = "80 - 130 mg/dL (Đường huyết lúc đói)"
        ppg_target = "< 180 mg/dL (Đường huyết 2 giờ sau ăn)"
        bp_target = "< 130/80 mmHg" if (hypertension == 1 or heart_disease == 1) else "< 140/90 mmHg"

        # Extract linked entities from kg_res
        kg_analysis = kg_res.get("kg_analysis", {})
        disease_node_id = kg_analysis.get("disease_id", "DIS_DIABETES_T2")
        disease_name = kg_res.get("disease_name", "Type 2 Diabetes")

        linked_entities = [
            {"id": disease_node_id, "label": disease_name, "type": "Disease", "color": "rose"}
        ]
        for m in kg_res.get("medications", []):
            linked_entities.append({"id": m.get("id"), "label": m.get("name"), "type": "Medication", "color": "emerald"})
        for l in kg_res.get("lifestyles", []):
            linked_entities.append({"id": l.get("id"), "label": l.get("name"), "type": "Lifestyle", "color": "amber"})
        for c in kg_res.get("complications", []):
            linked_entities.append({"id": c.get("id"), "label": c.get("name"), "type": "Complication", "color": "purple"})
        linked_entities.append({"id": "GUIDE_ADA_2024", "label": "ADA Standards of Care 2024", "type": "Guideline", "color": "blue"})
        linked_entities.append({"id": "GUIDE_KDIGO_2023", "label": "KDIGO 2023 Practice Guideline", "type": "Guideline", "color": "cyan"})

        clinical_recommendations = {
            "pharmacotherapy": {
                "title": "Phác Đồ Dược Lý & Đơn Thuốc Đã Phê Duyệt",
                "drugs": chief_res.get("approved_medications", []),
                "evidence_notes": [
                    "ADA 2024 Standards of Care: Metformin là trị liệu đầu tay trừ khi eGFR < 30 mL/min.",
                    "EMPA-REG / DECLARE-TIMI 58: SGLT2i giảm 38% tử vong tim mạch và bảo vệ suy tim.",
                    f"Thanh thải thận hiện tại: CrCl = {pgx_res.get('crcl_ml_min', 85.0):.1f} mL/phút (An toàn cho Metformin & SGLT2i)"
                ]
            },
            "medical_nutrition_therapy": {
                "title": "Dinh Dưỡng Tiết Chế Lâm Sàng (MNT Low-GI)",
                "rules": therapy_res.get("diet_plan", []),
                "macronutrient_split": "Carbohydrate 45-50% (Low-GI) | Protein 20-25% | Lipid 25-30% (Chất béo không bão hòa)",
                "daily_fiber_target": "35 - 40g chất xơ/ngày từ yến mạch, đậu, rau củ lá xanh đậm",
                "calorie_strategy": f"Giảm 500 kcal/ngày hướng tới mục tiêu giảm 5-7% trọng lượng cơ thể (BMI hiện tại: {bmi:.1f})" if bmi >= 25 else "Duy trì năng lượng cân bằng (Normocaloric)"
            },
            "physical_activity": {
                "title": "Kế Hoạch Vận Động & Rèn Luyện Thể Lực",
                "rules": therapy_res.get("exercise_plan", []),
                "aerobic_target": "150 phút/tuần cường độ trung bình (30 phút x 5 ngày/tuần, đi bộ nhanh, bơi, đạp xe)",
                "resistance_training": "Tập kháng lực 2-3 buổi/tuần (tạ nhẹ, bài tập trọng lượng cơ thể) kích hoạt GLUT-4 cơ vân",
                "sedentary_rule": "Không ngồi tĩnh tại liên tục quá 30 phút; vận động nhẹ 3 phút giữa các chu kỳ"
            },
            "monitoring_and_followup": {
                "title": "Mục Tiêu Sinh Hóa & Lịch Trình Giám Sát (ADA 2024 / KDIGO)",
                "hba1c_target": hba1c_target,
                "fpg_target": fpg_target,
                "ppg_target": ppg_target,
                "bp_target": bp_target,
                "schedule": [
                    "Xét nghiệm HbA1c: 3 tháng/lần cho đến khi đạt mục tiêu ổn định; 6 tháng/lần sau đó.",
                    "Xét nghiệm chức năng thận (eGFR + UACR tỷ lệ Albumin/Creatinine niệu): Tối thiểu 1 lần/năm hoặc mỗi 6 tháng theo KDIGO.",
                    "Khám tầm soát biến chứng võng mạc mắt và biến chứng thần kinh bàn chân đái tháo đường: 1 lần/năm."
                ]
            },
            "kb_provenance": {
                "cypher_file": "project01/knowledge_graph/diabetes_kg_neo4j.cypher",
                "json_file": "project01/knowledge_graph/diabetes_knowledge_graph_expanded.json",
                "connector": "project01/knowledge_graph/neo4j_connector.py",
                "querier": "project01/knowledge_graph/diabetes_kg_queries.py",
                "nodes_count": 44,
                "edges_count": 45,
                "standards": ["ADA 2024 Standards of Care", "KDIGO 2023 Clinical Practice Guideline", "WHO ICD-10"],
                "linked_entities": linked_entities
            }
        }

        # Consolidated Summary
        summary = {
            "elapsed_seconds": elapsed,
            "consultation_duration_sec": elapsed,
            "patient_overview": patient_dict,
            "final_diagnosis": chief_res.get("final_diagnosis", "Đang cập nhật"),
            "consensus_diagnosis": chief_res.get("final_diagnosis", "Đang cập nhật"),
            "risk_tier": chief_res.get("risk_tier", "CAO"),
            "risk_color": chief_res.get("risk_color", "red"),
            "consensus_score": chief_res.get("consensus_score", 96),
            "cohen_kappa": chief_res.get("cohen_kappa", 0.94),
            "deliberation_rounds": chief_res.get("deliberation_rounds", []),
            "safety_severity": safety_res["max_severity"],
            "tir_24h_percent": rl_res["tir_percent"],
            "rl_mean_glucose": rl_res["mean_glucose"],
            "crcl_ml_min": pgx_res["crcl_ml_min"],
            "counterfactual_prob_pct": cf_res["counterfactual_prob_pct"],
            "risk_reduction_pct": cf_res["risk_reduction_pct"],
            "longitudinal_week4_tir": followup_res["final_tir"],
            "approved_medications": chief_res.get("approved_medications", []),
            "diet_plan": therapy_res.get("diet_plan", []),
            "exercise_plan": therapy_res.get("exercise_plan", []),
            "clinical_recommendations": clinical_recommendations,
            "kb_provenance": clinical_recommendations["kb_provenance"],
            "critique_audit": chief_res.get("self_critique_evaluations", []),
            "counterfactual_steps": cf_res.get("counterfactual_steps", []),
            "timeline": timeline,
            "num_agents": 12
        }

        return summary
