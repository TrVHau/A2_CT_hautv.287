import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "knowledge_graph")
CYPHER_FILE = os.path.join(KG_DIR, "DB_diabet.cypher")

# Import the dictionary from update_cypher_links.py
from update_cypher_links import CYPHER_HEADER, NODE_URLS

with open(CYPHER_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_header = True

for line in lines:
    if line.strip().startswith("// 1. Clear existing database"):
        in_header = False
        new_lines.append(CYPHER_HEADER.strip() + "\n\n")
        new_lines.append(line)
        continue
    
    if in_header:
        continue
    
    if line.strip().startswith("CREATE (:") and "id: '" in line:
        m = re.search(r"id:\s*'([^']+)'", line)
        if m:
            nid = m.group(1)
            url = NODE_URLS.get(nid, "https://diabetesjournals.org/care/issue/47/Supplement_1")
            # Insert url property after source: '...'
            if "url:" not in line:
                line = re.sub(
                    r"(source:\s*'[^']+')",
                    rf"\1, url: '{url}'",
                    line
                )
    new_lines.append(line)

new_cypher_content = "".join(new_lines)

# Write to all 3 cypher files
target_cyphers = [
    os.path.join(KG_DIR, "DB_diabet.cypher"),
    os.path.join(BASE_DIR, "DB_diabet.cypher"),
    os.path.join(KG_DIR, "diabetes_kg_neo4j.cypher"),
]

for p in target_cyphers:
    with open(p, "w", encoding="utf-8") as f:
        f.write(new_cypher_content)
    print(f"Updated {p} ({len(new_cypher_content)} bytes)")

# Update diabetes_knowledge_graph_expanded.json
json_path = os.path.join(KG_DIR, "diabetes_knowledge_graph_expanded.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        kg_json = json.load(f)
    
    updated_nodes = 0
    if "nodes" in kg_json:
        for node in kg_json["nodes"]:
            nid = node.get("id")
            if nid in NODE_URLS:
                node["url"] = NODE_URLS[nid]
                updated_nodes += 1
            elif "url" not in node:
                node["url"] = "https://diabetesjournals.org/care/issue/47/Supplement_1"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(kg_json, f, ensure_ascii=False, indent=2)
    print(f"Updated {json_path} with URLs on {updated_nodes} nodes.")
