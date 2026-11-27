"""
Neo4j Knowledge Graph Visualization & Documentation
====================================================
This module describes the Diabetes Knowledge Graph structure
and provides visualization utilities.
"""

# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE GRAPH SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

GRAPH_SCHEMA = """
╔══════════════════════════════════════════════════════════════════════╗
║           DIABETES KNOWLEDGE GRAPH — NODE & RELATIONSHIP SCHEMA      ║
╚══════════════════════════════════════════════════════════════════════╝

NODE TYPES
──────────

(:DiabetesRisk)
  Properties: level, label_vi, probability_threshold, prediction, icon
  Values:     low | medium | high

(:Symptom)
  Properties: name, description_vi
  Examples:   high_glucose, high_bmi, high_bp, old_age, family_history

(:LifestyleAdvice)
  Properties: id, text_vi
  Examples:   Monitor blood glucose, adequate hydration, sleep hygiene

(:DietAdvice)
  Properties: id, text_vi
  Examples:   Limit refined carbs, whole grains, reduce sugar

(:ExerciseAdvice)
  Properties: id, text_vi
  Examples:   30min daily walk, swimming, avoid overexertion

(:MedicalTest)
  Properties: id, name, frequency, description_vi
  Examples:   HbA1c (3mo), Eye exam (annual), Kidney function

(:Warning)
  Properties: id, text_vi, urgency (critical|high|medium|low)


RELATIONSHIPS
─────────────

(:Symptom)     -[:INDICATES]->    (:DiabetesRisk)
(:DiabetesRisk)-[:RECOMMENDS]->   (:LifestyleAdvice)
(:DiabetesRisk)-[:RECOMMENDS]->   (:DietAdvice)
(:DiabetesRisk)-[:RECOMMENDS]->   (:ExerciseAdvice)
(:DiabetesRisk)-[:REQUIRES]->     (:MedicalTest)
(:DiabetesRisk)-[:HAS_WARNING]->  (:Warning)


QUERY FLOW
──────────

Patient Input → ML Model → Prediction + Probability
                                    ↓
                        Determine Risk Level
                    (low / medium / high)
                                    ↓
                    Query DiabetesRisk node
                                    ↓
               Traverse RECOMMENDS & REQUIRES edges
                                    ↓
              Collect Advice, Tests, Warnings
                                    ↓
           Match Symptoms to Specific Patient Findings
                                    ↓
                Return Personalized Advice Bundle


SAMPLE CYPHER QUERIES
─────────────────────

# Get all advice for high-risk patient:
MATCH (r:DiabetesRisk {level: 'high'})-[:RECOMMENDS]->(a)
RETURN labels(a)[0] AS type, a.text_vi AS advice

# Get required tests with frequency:
MATCH (r:DiabetesRisk {level: 'high'})-[:REQUIRES]->(t:MedicalTest)
RETURN t.name, t.frequency, t.description_vi

# Find which symptoms indicate high risk:
MATCH (s:Symptom)-[:INDICATES]->(r:DiabetesRisk {level: 'high'})
RETURN s.description_vi

# Full patient advice query:
MATCH (r:DiabetesRisk {level: $level})
OPTIONAL MATCH (r)-[:RECOMMENDS]->(advice)
OPTIONAL MATCH (r)-[:REQUIRES]->(test:MedicalTest)
OPTIONAL MATCH (r)-[:HAS_WARNING]->(warn:Warning)
RETURN r, collect(DISTINCT advice) AS advices,
       collect(DISTINCT test) AS tests,
       collect(DISTINCT warn) AS warnings
"""


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH STATISTICS (after setup)
# ══════════════════════════════════════════════════════════════════════════════

EXPECTED_STATS = {
    "DiabetesRisk":    3,   # low, medium, high
    "Symptom":         7,
    "LifestyleAdvice": 7,
    "DietAdvice":      8,
    "ExerciseAdvice":  6,
    "MedicalTest":     7,
    "Warning":         5,
    "Relationships":  "~60+"
}


def print_schema():
    """Print the Knowledge Graph schema."""
    print(GRAPH_SCHEMA)
    print("\nExpected Node Counts After Setup:")
    for node, count in EXPECTED_STATS.items():
        print(f"  {node:<20} {count}")


def visualize_risk_levels():
    """ASCII visualization of risk levels and their connections."""
    viz = """
    ┌─────────────────────────────────────────────────────────────┐
    │              DIABETES RISK KNOWLEDGE GRAPH                  │
    └─────────────────────────────────────────────────────────────┘

    Patient
    Measurements ──→  ML Model ──→ Prediction + Probability
                                            │
                           ┌────────────────┼────────────────┐
                           ▼                ▼                ▼
                        [LOW]           [MEDIUM]          [HIGH]
                       Prob<40%        40%≤Prob<70%     Prob≥70%
                           │                │                │
              ┌────────────┤   ┌────────────┤   ┌────────────┤
              ▼            │   ▼            │   ▼            │
        Lifestyle(4)       │  Lifestyle(5)  │  Lifestyle(5)  │
        Diet(3)            │  Diet(4)       │  Diet(6)       │
        Exercise(2)        │  Exercise(3)   │  Exercise(4)   │
        Tests(3)           │  Tests(4)      │  Tests(5)      │
        Warnings(0)        │  Warnings(2)   │  Warnings(3)   │
                           │                │                │
              └────────────┘   └────────────┘   └────────────┘
                                       │
                              ┌────────┴────────┐
                              ▼                 ▼
                        Specific         Symptom
                        Findings    ←  Matching
                        (per patient)
    """
    print(viz)


if __name__ == "__main__":
    print_schema()
    print("\n")
    visualize_risk_levels()
