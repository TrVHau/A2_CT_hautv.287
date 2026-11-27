import sys
import re

with open('c:/code/A2_CT_hautv.287/project01/web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

fetches = re.findall(r'fetch\([\'"`](/[^\'"`]+)[\'"`]', text)
print("Unique fetch endpoints:")
for ep in sorted(set(fetches)):
    print(" -", ep)
