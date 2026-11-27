"""
Neo4j Knowledge Graph Query Module — Diabetes Diagnosis System
==============================================================
Được import bởi web/app.py để lấy lời khuyên từ Knowledge Graph.

Nếu Neo4j không khả dụng, app.py sẽ tự động dùng static advice.
"""

import os
from neo4j import GraphDatabase

# ─── Configuration ─────────────────────────────────────────────────────────
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Singleton driver
_driver = None


def _get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def _close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None


# ─── Query Functions ────────────────────────────────────────────────────────
def get_advice(prediction: int, probability: float, input_data: dict) -> dict:
    """
    Query Neo4j Knowledge Graph for personalized medical advice.

    Args:
        prediction:  0 = non-diabetic, 1 = diabetic
        probability: float 0.0–1.0 (probability of being diabetic)
        input_data:  dict of feature values

    Returns:
        dict with structured advice
    """
    # Determine risk level
    if prediction == 0:
        risk_level = "low"
    elif probability >= 0.7:
        risk_level = "high"
    else:
        risk_level = "medium"

    driver = _get_driver()

    with driver.session() as session:
        # ── Risk info ──────────────────────────────────────────────────────
        risk_result = session.run(
            """
            MATCH (r:DiabetesRisk {level: $level})
            RETURN r.label_vi AS label_vi, r.icon AS icon
            """,
            level=risk_level
        ).single()

        label_vi = risk_result["label_vi"] if risk_result else risk_level
        icon     = risk_result["icon"]     if risk_result else "❓"

        # ── Lifestyle advice ───────────────────────────────────────────────
        lifestyle = _query_list(session, risk_level, "LifestyleAdvice", "ls")

        # ── Diet advice ────────────────────────────────────────────────────
        diet = _query_list(session, risk_level, "DietAdvice", "diet")

        # ── Exercise advice ────────────────────────────────────────────────
        exercise = _query_list(session, risk_level, "ExerciseAdvice", "ex")

        # ── Medical tests ──────────────────────────────────────────────────
        tests_result = session.run(
            """
            MATCH (r:DiabetesRisk {level: $level})-[:REQUIRES]->(t:MedicalTest)
            RETURN t.description_vi AS text, t.frequency AS freq
            ORDER BY t.id
            """,
            level=risk_level
        )
        medical_tests = [
            f"{row['text']} — {row['freq']}"
            for row in tests_result
        ]

        # ── Warnings ───────────────────────────────────────────────────────
        warnings_result = session.run(
            """
            MATCH (r:DiabetesRisk {level: $level})-[:HAS_WARNING]->(w:Warning)
            RETURN w.text_vi AS text
            ORDER BY w.urgency DESC
            """,
            level=risk_level
        )
        warnings = [row["text"] for row in warnings_result]

        # ── Specific findings based on input ───────────────────────────────
        specific_findings = _get_specific_findings(session, input_data)

    return {
        "risk_level":       risk_level,
        "risk_label":       f"{icon} {label_vi}",
        "lifestyle":        lifestyle,
        "diet":             diet,
        "exercise":         exercise,
        "medical_tests":    medical_tests,
        "warnings":         warnings,
        "specific_findings": specific_findings
    }


def _query_list(session, risk_level: str, node_label: str, id_prefix: str) -> list:
    """Query advice nodes connected to a risk level."""
    result = session.run(
        f"""
        MATCH (r:DiabetesRisk {{level: $level}})-[:RECOMMENDS]->(a:{node_label})
        RETURN a.text_vi AS text
        ORDER BY a.id
        """,
        level=risk_level
    )
    return [row["text"] for row in result]


def _get_specific_findings(session, input_data: dict) -> list:
    """
    Find symptoms matching the patient's input data, then
    query their Vietnamese descriptions.
    """
    # Determine which symptoms apply
    triggered_symptoms = []

    glucose = input_data.get("Glucose", 0)
    bmi     = input_data.get("BMI", 0)
    bp      = input_data.get("BloodPressure", 0)
    age     = input_data.get("Age", 0)
    insulin = input_data.get("Insulin", 0)
    dpf     = input_data.get("DiabetesPedigreeFunction", 0)
    preg    = input_data.get("Pregnancies", 0)

    if glucose   > 140:  triggered_symptoms.append("high_glucose")
    if bmi       > 30:   triggered_symptoms.append("high_bmi")
    if bp        > 90:   triggered_symptoms.append("high_bp")
    if age       > 45:   triggered_symptoms.append("old_age")
    if insulin   > 200:  triggered_symptoms.append("high_insulin")
    if dpf       > 0.8:  triggered_symptoms.append("family_history")
    if preg      > 5:    triggered_symptoms.append("high_pregnancy")

    if not triggered_symptoms:
        return []

    result = session.run(
        """
        MATCH (s:Symptom)
        WHERE s.name IN $names
        RETURN s.description_vi AS text
        ORDER BY s.name
        """,
        names=triggered_symptoms
    )

    return [row["text"] for row in result]


# ─── Health Check ───────────────────────────────────────────────────────────
def is_connected() -> bool:
    """Returns True if Neo4j is reachable."""
    try:
        driver = _get_driver()
        with driver.session() as session:
            session.run("RETURN 1")
        return True
    except Exception:
        return False


# ─── Demo / Test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing Neo4j query...")

    sample_input = {
        "Pregnancies": 6,
        "Glucose": 148,
        "BloodPressure": 72,
        "SkinThickness": 35,
        "Insulin": 0,
        "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627,
        "Age": 50
    }

    try:
        result = get_advice(prediction=1, probability=0.75, input_data=sample_input)
        print(f"\nRisk: {result['risk_label']}")
        print(f"Lifestyle: {result['lifestyle'][:2]}")
        print(f"Specific: {result['specific_findings']}")
        print("\n✅ Neo4j query successful!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Neo4j may not be running. The web app uses static advice as fallback.")
    finally:
        _close_driver()
