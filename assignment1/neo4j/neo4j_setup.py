"""
Neo4j Knowledge Graph Setup — Diabetes Diagnosis System
========================================================
Script này tạo và populate Knowledge Graph trong Neo4j.

Chạy: python neo4j_setup.py

Yêu cầu:
  pip install neo4j
  Neo4j server đang chạy (mặc định: bolt://localhost:7687)
"""

from neo4j import GraphDatabase
import os

# ─── Configuration ─────────────────────────────────────────────────────────
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


# ─── Schema ────────────────────────────────────────────────────────────────
"""
Node Types:
  (:DiabetesRisk {level, label_vi, probability_threshold})
  (:Symptom      {name, description_vi})
  (:LifestyleAdvice {category, text_vi})
  (:DietAdvice       {text_vi})
  (:ExerciseAdvice   {text_vi})
  (:MedicalTest      {name, frequency, description_vi})
  (:Warning          {text_vi, urgency})

Relationships:
  (:DiabetesRisk)-[:HAS_SYMPTOM]->(:Symptom)
  (:DiabetesRisk)-[:RECOMMENDS_LIFESTYLE]->(:LifestyleAdvice)
  (:DiabetesRisk)-[:RECOMMENDS_DIET]->(:DietAdvice)
  (:DiabetesRisk)-[:RECOMMENDS_EXERCISE]->(:ExerciseAdvice)
  (:DiabetesRisk)-[:REQUIRES_TEST]->(:MedicalTest)
  (:DiabetesRisk)-[:HAS_WARNING]->(:Warning)
  (:Symptom)-[:TRIGGERS_RISK]->(:DiabetesRisk)
"""


CYPHER_SETUP = """
// ─── Clear existing data ───────────────────────────────────────────────────
MATCH (n) DETACH DELETE n;

// ─── Create DiabetesRisk nodes ─────────────────────────────────────────────
CREATE (:DiabetesRisk {
  level: 'low',
  label_vi: 'Nguy Cơ Thấp',
  probability_threshold: 0.4,
  prediction: 0,
  icon: '🟢'
});

CREATE (:DiabetesRisk {
  level: 'medium',
  label_vi: 'Nguy Cơ Trung Bình',
  probability_threshold: 0.7,
  prediction: 1,
  icon: '🟡'
});

CREATE (:DiabetesRisk {
  level: 'high',
  label_vi: 'Nguy Cơ Cao',
  probability_threshold: 1.0,
  prediction: 1,
  icon: '🔴'
});

// ─── Create Symptom nodes ──────────────────────────────────────────────────
CREATE (:Symptom {name: 'high_glucose',    description_vi: 'Đường huyết cao (> 140 mg/dL)'});
CREATE (:Symptom {name: 'high_bmi',        description_vi: 'Thừa cân / béo phì (BMI > 30)'});
CREATE (:Symptom {name: 'high_bp',         description_vi: 'Huyết áp cao (> 90 mm Hg)'});
CREATE (:Symptom {name: 'old_age',         description_vi: 'Tuổi cao (> 45)'});
CREATE (:Symptom {name: 'high_insulin',    description_vi: 'Kháng insulin'});
CREATE (:Symptom {name: 'family_history',  description_vi: 'Tiền sử gia đình mắc tiểu đường'});
CREATE (:Symptom {name: 'high_pregnancy',  description_vi: 'Nhiều lần mang thai'});

// ─── Create Lifestyle Advice nodes ─────────────────────────────────────────
CREATE (:LifestyleAdvice {id: 'ls_monitor',   text_vi: 'Theo dõi đường huyết hàng ngày'});
CREATE (:LifestyleAdvice {id: 'ls_water',     text_vi: 'Uống đủ nước (2-3 lít/ngày)'});
CREATE (:LifestyleAdvice {id: 'ls_sleep',     text_vi: 'Ngủ đủ giấc 7-8 tiếng mỗi đêm'});
CREATE (:LifestyleAdvice {id: 'ls_stress',    text_vi: 'Giảm stress bằng thiền hoặc yoga'});
CREATE (:LifestyleAdvice {id: 'ls_smoke',     text_vi: 'Không hút thuốc lá'});
CREATE (:LifestyleAdvice {id: 'ls_weight',    text_vi: 'Duy trì cân nặng lý tưởng'});
CREATE (:LifestyleAdvice {id: 'ls_checkup',   text_vi: 'Kiểm tra sức khỏe định kỳ 6-12 tháng/lần'});

// ─── Create Diet Advice nodes ──────────────────────────────────────────────
CREATE (:DietAdvice {id: 'diet_carb',    text_vi: 'Hạn chế carbohydrate tinh chế (bánh mì trắng, gạo trắng)'});
CREATE (:DietAdvice {id: 'diet_grain',   text_vi: 'Ưu tiên ngũ cốc nguyên hạt'});
CREATE (:DietAdvice {id: 'diet_veg',     text_vi: 'Tăng cường rau xanh và trái cây ít đường'});
CREATE (:DietAdvice {id: 'diet_sugar',   text_vi: 'Hạn chế đường và đồ ngọt'});
CREATE (:DietAdvice {id: 'diet_meals',   text_vi: 'Ăn ít nhưng nhiều bữa (5-6 bữa/ngày)'});
CREATE (:DietAdvice {id: 'diet_alcohol', text_vi: 'Hạn chế rượu bia'});
CREATE (:DietAdvice {id: 'diet_balance', text_vi: 'Duy trì chế độ ăn cân bằng dinh dưỡng'});
CREATE (:DietAdvice {id: 'diet_process', text_vi: 'Hạn chế thực phẩm chế biến sẵn'});

// ─── Create Exercise Advice nodes ──────────────────────────────────────────
CREATE (:ExerciseAdvice {id: 'ex_walk',  text_vi: 'Đi bộ nhanh 30 phút/ngày, 5 ngày/tuần'});
CREATE (:ExerciseAdvice {id: 'ex_swim',  text_vi: 'Bơi lội hoặc đạp xe nhẹ nhàng'});
CREATE (:ExerciseAdvice {id: 'ex_yoga',  text_vi: 'Tập thở và căng cơ buổi sáng'});
CREATE (:ExerciseAdvice {id: 'ex_safe',  text_vi: 'Tránh vận động quá mạnh khi đường huyết không ổn định'});
CREATE (:ExerciseAdvice {id: 'ex_min',   text_vi: 'Tập thể dục ít nhất 150 phút/tuần'});
CREATE (:ExerciseAdvice {id: 'ex_sit',   text_vi: 'Hạn chế ngồi một chỗ quá lâu'});

// ─── Create Medical Test nodes ─────────────────────────────────────────────
CREATE (:MedicalTest {id: 'test_hba1c',   name: 'HbA1c',          frequency: '3 tháng/lần',   description_vi: 'Xét nghiệm HbA1c kiểm tra đường huyết trung bình 3 tháng'});
CREATE (:MedicalTest {id: 'test_eye',     name: 'Khám mắt',       frequency: '1 năm/lần',     description_vi: 'Kiểm tra mắt phát hiện bệnh võng mạc tiểu đường'});
CREATE (:MedicalTest {id: 'test_kidney',  name: 'Chức năng thận', frequency: '6 tháng/lần',   description_vi: 'Xét nghiệm creatinine và microalbumin niệu'});
CREATE (:MedicalTest {id: 'test_bp',      name: 'Huyết áp',       frequency: 'Mỗi lần khám',  description_vi: 'Đo huyết áp kiểm soát nguy cơ tim mạch'});
CREATE (:MedicalTest {id: 'test_foot',    name: 'Bàn chân',       frequency: '6 tháng/lần',   description_vi: 'Kiểm tra bàn chân phát hiện biến chứng thần kinh ngoại vi'});
CREATE (:MedicalTest {id: 'test_glucose', name: 'Đường huyết',    frequency: '1 năm/lần',     description_vi: 'Xét nghiệm đường huyết lúc đói'});
CREATE (:MedicalTest {id: 'test_lipid',   name: 'Mỡ máu',         frequency: '1 năm/lần',     description_vi: 'Xét nghiệm cholesterol và triglyceride'});

// ─── Create Warning nodes ──────────────────────────────────────────────────
CREATE (:Warning {id: 'warn_doctor',   text_vi: 'Khám bác sĩ chuyên khoa Nội tiết ngay lập tức', urgency: 'critical'});
CREATE (:Warning {id: 'warn_meds',     text_vi: 'Xem xét điều trị bằng thuốc theo chỉ định bác sĩ', urgency: 'high'});
CREATE (:Warning {id: 'warn_diet',     text_vi: 'Không tự ý thay đổi chế độ ăn đột ngột', urgency: 'medium'});
CREATE (:Warning {id: 'warn_consult',  text_vi: 'Nên tư vấn bác sĩ về chế độ phòng ngừa', urgency: 'medium'});
CREATE (:Warning {id: 'warn_monitor',  text_vi: 'Theo dõi chặt chẽ các yếu tố rủi ro', urgency: 'low'});
"""

CYPHER_RELATIONS = """
// ─── Link Symptoms to Risk Levels ─────────────────────────────────────────
MATCH (s:Symptom {name: 'high_glucose'}),   (r:DiabetesRisk {level: 'high'})
CREATE (s)-[:INDICATES]->(r);
MATCH (s:Symptom {name: 'high_glucose'}),   (r:DiabetesRisk {level: 'medium'})
CREATE (s)-[:INDICATES]->(r);

MATCH (s:Symptom {name: 'high_bmi'}),       (r:DiabetesRisk {level: 'high'})
CREATE (s)-[:INDICATES]->(r);
MATCH (s:Symptom {name: 'high_bmi'}),       (r:DiabetesRisk {level: 'medium'})
CREATE (s)-[:INDICATES]->(r);

MATCH (s:Symptom {name: 'high_bp'}),        (r:DiabetesRisk {level: 'medium'})
CREATE (s)-[:INDICATES]->(r);

MATCH (s:Symptom {name: 'old_age'}),        (r:DiabetesRisk {level: 'medium'})
CREATE (s)-[:INDICATES]->(r);
MATCH (s:Symptom {name: 'family_history'}), (r:DiabetesRisk {level: 'medium'})
CREATE (s)-[:INDICATES]->(r);

// ─── Link Risk to Lifestyle Advice ─────────────────────────────────────────
MATCH (r:DiabetesRisk {level: 'high'}), (a:LifestyleAdvice {id: 'ls_monitor'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:LifestyleAdvice {id: 'ls_water'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:LifestyleAdvice {id: 'ls_sleep'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:LifestyleAdvice {id: 'ls_stress'})  CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:LifestyleAdvice {id: 'ls_smoke'})   CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'medium'}), (a:LifestyleAdvice {id: 'ls_water'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:LifestyleAdvice {id: 'ls_sleep'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:LifestyleAdvice {id: 'ls_stress'})  CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:LifestyleAdvice {id: 'ls_weight'})  CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'low'}), (a:LifestyleAdvice {id: 'ls_weight'})  CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:LifestyleAdvice {id: 'ls_checkup'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:LifestyleAdvice {id: 'ls_stress'})  CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:LifestyleAdvice {id: 'ls_sleep'})   CREATE (r)-[:RECOMMENDS]->(a);

// ─── Link Risk to Diet Advice ───────────────────────────────────────────────
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_carb'})    CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_grain'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_veg'})     CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_sugar'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_meals'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:DietAdvice {id: 'diet_alcohol'}) CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'medium'}), (a:DietAdvice {id: 'diet_carb'})    CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:DietAdvice {id: 'diet_veg'})     CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:DietAdvice {id: 'diet_sugar'})   CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:DietAdvice {id: 'diet_balance'}) CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'low'}), (a:DietAdvice {id: 'diet_balance'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:DietAdvice {id: 'diet_process'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:DietAdvice {id: 'diet_veg'})     CREATE (r)-[:RECOMMENDS]->(a);

// ─── Link Risk to Exercise Advice ──────────────────────────────────────────
MATCH (r:DiabetesRisk {level: 'high'}), (a:ExerciseAdvice {id: 'ex_walk'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:ExerciseAdvice {id: 'ex_swim'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:ExerciseAdvice {id: 'ex_yoga'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'high'}), (a:ExerciseAdvice {id: 'ex_safe'}) CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'medium'}), (a:ExerciseAdvice {id: 'ex_walk'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:ExerciseAdvice {id: 'ex_swim'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'medium'}), (a:ExerciseAdvice {id: 'ex_min'})  CREATE (r)-[:RECOMMENDS]->(a);

MATCH (r:DiabetesRisk {level: 'low'}), (a:ExerciseAdvice {id: 'ex_min'}) CREATE (r)-[:RECOMMENDS]->(a);
MATCH (r:DiabetesRisk {level: 'low'}), (a:ExerciseAdvice {id: 'ex_sit'}) CREATE (r)-[:RECOMMENDS]->(a);

// ─── Link Risk to Medical Tests ─────────────────────────────────────────────
MATCH (r:DiabetesRisk {level: 'high'}), (t:MedicalTest {id: 'test_hba1c'})  CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'high'}), (t:MedicalTest {id: 'test_eye'})    CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'high'}), (t:MedicalTest {id: 'test_kidney'}) CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'high'}), (t:MedicalTest {id: 'test_bp'})     CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'high'}), (t:MedicalTest {id: 'test_foot'})   CREATE (r)-[:REQUIRES]->(t);

MATCH (r:DiabetesRisk {level: 'medium'}), (t:MedicalTest {id: 'test_glucose'}) CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'medium'}), (t:MedicalTest {id: 'test_bp'})      CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'medium'}), (t:MedicalTest {id: 'test_lipid'})   CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'medium'}), (t:MedicalTest {id: 'test_hba1c'})   CREATE (r)-[:REQUIRES]->(t);

MATCH (r:DiabetesRisk {level: 'low'}), (t:MedicalTest {id: 'test_glucose'}) CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'low'}), (t:MedicalTest {id: 'test_bp'})      CREATE (r)-[:REQUIRES]->(t);
MATCH (r:DiabetesRisk {level: 'low'}), (t:MedicalTest {id: 'test_lipid'})   CREATE (r)-[:REQUIRES]->(t);

// ─── Link Risk to Warnings ──────────────────────────────────────────────────
MATCH (r:DiabetesRisk {level: 'high'}), (w:Warning {id: 'warn_doctor'})  CREATE (r)-[:HAS_WARNING]->(w);
MATCH (r:DiabetesRisk {level: 'high'}), (w:Warning {id: 'warn_meds'})    CREATE (r)-[:HAS_WARNING]->(w);
MATCH (r:DiabetesRisk {level: 'high'}), (w:Warning {id: 'warn_diet'})    CREATE (r)-[:HAS_WARNING]->(w);

MATCH (r:DiabetesRisk {level: 'medium'}), (w:Warning {id: 'warn_consult'}) CREATE (r)-[:HAS_WARNING]->(w);
MATCH (r:DiabetesRisk {level: 'medium'}), (w:Warning {id: 'warn_monitor'}) CREATE (r)-[:HAS_WARNING]->(w);
"""


# ─── Setup Class ───────────────────────────────────────────────────────────
class DiabetesKnowledgeGraph:

    def __init__(self, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"✓ Connected to Neo4j at {uri}")

    def close(self):
        self.driver.close()

    def run(self, cypher: str):
        with self.driver.session() as session:
            # Split by semicolon for multi-statement execution
            statements = [s.strip() for s in cypher.split(';') if s.strip()]
            for stmt in statements:
                session.run(stmt)

    def setup(self):
        print("Creating nodes...")
        self.run(CYPHER_SETUP)
        print("Creating relationships...")
        self.run(CYPHER_RELATIONS)
        print("✓ Knowledge Graph created successfully!")

    def verify(self):
        with self.driver.session() as session:
            counts = {}
            for label in ["DiabetesRisk", "Symptom", "LifestyleAdvice",
                          "DietAdvice", "ExerciseAdvice", "MedicalTest", "Warning"]:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as cnt")
                counts[label] = result.single()["cnt"]

            rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as cnt")
            counts["Relationships"] = rel_result.single()["cnt"]

        print("\n── Graph Statistics ──────────────────────────")
        for label, count in counts.items():
            print(f"  {label:<25} {count:>4}")
        return counts


# ─── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    print("="*50)
    print("  Diabetes Knowledge Graph Setup")
    print("="*50)
    print(f"\nConnecting to: {NEO4J_URI}")
    print(f"Username:      {NEO4J_USER}")
    print(f"Password:      {'*' * len(NEO4J_PASSWORD)}\n")

    try:
        kg = DiabetesKnowledgeGraph()
        kg.setup()
        kg.verify()
        kg.close()

        print("\n✅ Knowledge Graph setup complete!")
        print("\nNode types created:")
        print("  • DiabetesRisk  (low / medium / high)")
        print("  • Symptom       (7 symptoms)")
        print("  • LifestyleAdvice, DietAdvice, ExerciseAdvice")
        print("  • MedicalTest   (7 tests)")
        print("  • Warning       (5 warnings)")
        print("\nYou can now query the graph using neo4j_query.py")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure Neo4j is running: systemctl start neo4j")
        print("  2. Check credentials in NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD")
        print("  3. Install driver: pip install neo4j")
        print("\nThe web app will still work using static advice (no Neo4j needed).")
        sys.exit(1)
