import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

html_path = os.path.join("assignment2", "web_mobile_app", "templates", "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace topbar
target_topbar = """<div class="topbar">
  <div>
    <div class="topbar-brand">🏠 Dự đoán giá nhà Việt Nam</div>
    <div class="topbar-sub">Vietnam Housing Dataset 2024 · {{ metrics.name }}</div>
  </div>
  <a href="/mobile" class="topbar-switch">📱 Giao diện Mobile</a>
</div>"""

replacement_topbar = """<div class="topbar">
  <div>
    <div class="topbar-brand">🏠 Hệ Thống Định Giá Nhà Đất Việt Nam Nâng Cao</div>
    <div class="topbar-sub">Học phần Hệ thống Thông minh · Trịnh Vũ Hậu (B21DCCN287) · {{ metrics.name }} (R² = {{ metrics.r2 }})</div>
  </div>
  <div style="display:flex;gap:10px;align-items:center;">
    <button onclick="openGallery()" style="background:#10b981;color:white;border:none;padding:7px 14px;border-radius:8px;font-weight:600;font-size:12px;cursor:pointer;display:flex;align-items:center;gap:6px;">
      <span>📊</span> Thư Viện 14 Biểu Đồ (300 DPI)
    </button>
    <a href="/mobile" class="topbar-switch">📱 Giao diện Mobile</a>
  </div>
</div>"""

if target_topbar in c:
    c = c.replace(target_topbar, replacement_topbar)
    print("Replaced topbar successfully.")
else:
    # Try normalizing line endings
    c_norm = c.replace("\r\n", "\n")
    target_norm = target_topbar.replace("\r\n", "\n")
    if target_norm in c_norm:
        c = c_norm.replace(target_norm, replacement_topbar)
        print("Replaced topbar (normalized LF) successfully.")
    else:
        print("Warning: target_topbar not found directly.")

modal_html = """
<!-- Modal Thư Viện 14 Biểu Đồ -->
<div id="galleryModal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.85);z-index:9999;backdrop-filter:blur(4px);overflow-y:auto;padding:24px;">
  <div style="max-width:1100px;margin:0 auto;background:#ffffff;border-radius:16px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#ffffff;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;">
      <div>
        <h2 style="font-size:18px;font-weight:700;margin:0;">📊 THƯ VIỆN 14 BIỂU ĐỒ NGHIÊN CỨU & KIỂM ĐỊNH CHUYÊN SÂU (300 DPI)</h2>
        <p style="font-size:12px;opacity:0.85;margin:4px 0 0 0;">Hệ thống Định giá Nhà đất Việt Nam · Trịnh Vũ Hậu (B21DCCN287) · PTIT 2026</p>
      </div>
      <button onclick="closeGallery()" style="background:rgba(255,255,255,0.2);color:#ffffff;border:none;width:36px;height:36px;border-radius:50%;font-size:18px;cursor:pointer;">✕</button>
    </div>
    <div style="padding:24px;display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;">
      {% for fig in figures %}
      <div style="border:1px solid #e2e8f0;border-radius:12px;padding:12px;background:#f8fafc;display:flex;flex-direction:column;justify-content:space-between;">
        <div>
          <a href="/figures/{{ fig.file }}" target="_blank">
            <img src="/figures/{{ fig.file }}" alt="{{ fig.title }}" style="width:100%;height:190px;object-fit:cover;border-radius:8px;border:1px solid #cbd5e1;cursor:pointer;" />
          </a>
          <h4 style="font-size:13px;font-weight:700;color:#1e293b;margin:10px 0 4px 0;">{{ fig.id }}. {{ fig.title }}</h4>
          <p style="font-size:11.5px;color:#64748b;line-height:1.4;">{{ fig.desc }}</p>
        </div>
        <div style="margin-top:10px;">
          <a href="/figures/{{ fig.file }}" target="_blank" style="display:inline-block;background:#3b82f6;color:#ffffff;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:11px;font-weight:600;">🔍 Phóng to 300 DPI</a>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>

<script>
function openGallery() {
  document.getElementById('galleryModal').style.display = 'block';
}
function closeGallery() {
  document.getElementById('galleryModal').style.display = 'none';
}
</script>
"""

if "id=\"galleryModal\"" not in c:
    c = c.replace("</body>", modal_html + "\n</body>")
    print("Injected modal HTML successfully.")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated index.html completely!")
