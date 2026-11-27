"""
Agent 3: Clinical & Tabular Modality Consultant
Analyzes inductive bias on tabular data, Conv1D limitations, and imbalanced clinical metrics.
"""


class TabularModalityAgent:
    def __init__(self):
        self.name = "Clinical Modality Consultant Agent"
        self.role = "Tabular Inductive Bias & Clinical Epidemiology Auditor"

    def evaluate(self, modality: str, model_name: str, metrics: dict, patient_risk_profile: dict = None):
        clinical_notes = []
        acc = metrics.get("accuracy", 0.0)
        f1 = metrics.get("macro_f1", 0.0)

        if modality == "diabetes":
            clinical_notes.append("Clinical data exhibits 86.1% vs 13.9% class imbalance. Standard accuracy is deceptive.")
            if acc > 0.85 and f1 < 0.65:
                clinical_notes.append(f"Model demonstrates 'Accuracy Paradox': High Accuracy ({acc*100:.1f}%) masked by low Macro-F1 ({f1:.4f}).")
            clinical_notes.append("Pedagogical Reality: Conv1D operates under an implicit sequence assumption. If clinical features (e.g. BMI, Glucose, Age) are randomly permuted, Conv1D filters learn spurious adjacent correlations.")
            clinical_notes.append("Recommendation: Tree-based ensembles (Random Forest, XGBoost) are inherently superior for heterogeneous tabular features, but Conv1D provides an instructive baseline for multi-modal architectures.")
        else:
            clinical_notes.append("Modality is visual grid data. Spatial inductive bias (locality and translation equivariance) is strictly valid.")

        return {
            "agent": self.name,
            "role": self.role,
            "accuracy_paradox_flag": bool(acc > 0.85 and f1 < 0.65 and modality == "diabetes"),
            "macro_f1_score": round(f1, 4),
            "clinical_notes": clinical_notes,
            "epidemiological_verdict": "Inductive Bias Matched" if modality != "diabetes" else "Inductive Bias Pedagogically Constrained"
        }
