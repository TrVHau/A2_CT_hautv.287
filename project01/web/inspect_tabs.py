with open('c:/code/A2_CT_hautv.287/project01/web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']tab-([^"\']+)["\']', text)
print("Tabs found:", matches)

# Find major headers
headers = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', text)
print(f"Total headers: {len(headers)}")
for h in headers[:20]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print(" -", clean[:80])
