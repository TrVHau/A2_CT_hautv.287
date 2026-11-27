/* ═══════════════════════════════════════════════════════════════════════════
   DiabetesAI — Main JavaScript
   Handles: form submission, prediction display, tabs, advice rendering
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── DOM Elements ────────────────────────────────────────────────────────
  const form         = document.getElementById('diagnosis-form');
  const predictBtn   = document.getElementById('predict-btn');
  const resetBtn     = document.getElementById('reset-btn');

  const placeholder  = document.getElementById('result-placeholder');
  const loading      = document.getElementById('result-loading');
  const content      = document.getElementById('result-content');

  const banner       = document.getElementById('diagnosis-banner');
  const bannerIcon   = document.getElementById('banner-icon');
  const diagTitle    = document.getElementById('diagnosis-title');
  const diagSub      = document.getElementById('diagnosis-subtitle');

  const gaugeFill    = document.getElementById('gauge-fill');
  const probValue    = document.getElementById('prob-value');
  const riskBadge    = document.getElementById('risk-badge');

  const specificBox  = document.getElementById('specific-findings');
  const findingsList = document.getElementById('findings-list');

  const warningsBox  = document.getElementById('warnings-box');
  const warningsList = document.getElementById('warnings-list');

  const summaryGrid  = document.getElementById('summary-grid');

  const tabBtns      = document.querySelectorAll('.tab-btn');
  const tabContents  = document.querySelectorAll('.tab-content');

  // ── Tab Switching ───────────────────────────────────────────────────────
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + target).classList.add('active');
    });
  });

  // ── Reset Form ──────────────────────────────────────────────────────────
  resetBtn.addEventListener('click', () => {
    form.reset();
    showPlaceholder();
  });

  // ── Form Submit ─────────────────────────────────────────────────────────
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await runPrediction();
  });

  // ── Run Prediction ──────────────────────────────────────────────────────
  async function runPrediction() {
    // Collect form data
    const formData = new FormData(form);
    const payload  = {};
    for (const [key, val] of formData.entries()) {
      payload[key] = parseFloat(val);
    }

    showLoading();

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        showError(data.error || 'Đã xảy ra lỗi không xác định.');
        return;
      }

      showResult(data);

    } catch (err) {
      showError('Không thể kết nối đến server. Hãy đảm bảo Flask app đang chạy.');
    }
  }

  // ── Show States ─────────────────────────────────────────────────────────
  function showPlaceholder() {
    placeholder.classList.remove('hidden');
    loading.classList.add('hidden');
    content.classList.add('hidden');
  }

  function showLoading() {
    placeholder.classList.add('hidden');
    loading.classList.remove('hidden');
    content.classList.add('hidden');
  }

  function showError(msg) {
    loading.classList.add('hidden');
    placeholder.classList.remove('hidden');
    placeholder.innerHTML = `
      <div class="placeholder-icon">⚠️</div>
      <h3>Đã xảy ra lỗi</h3>
      <p>${escHtml(msg)}</p>
    `;
  }

  // ── Render Result ───────────────────────────────────────────────────────
  function showResult(data) {
    loading.classList.add('hidden');
    placeholder.classList.add('hidden');

    const isDiabetic = data.prediction === 1;
    const prob       = data.probability;           // 0–100
    const riskLevel  = data.risk_level;            // 'low' | 'medium' | 'high'
    const advice     = data.advice;

    // ── Banner ─────────────────────────────────────────────────────────
    banner.className = 'diagnosis-banner ' + (isDiabetic ? 'diabetic' : 'healthy');
    bannerIcon.textContent = isDiabetic ? '⚠️' : '✅';
    diagTitle.textContent  = data.prediction_label;
    diagSub.textContent    = `Xác suất mắc bệnh: ${prob}%`;

    // ── Gauge ──────────────────────────────────────────────────────────
    probValue.textContent = prob + '%';
    gaugeFill.style.left  = prob + '%';

    // Color prob value by risk
    const probColors = { low: '#43A047', medium: '#FB8C00', high: '#E53935' };
    probValue.style.color = probColors[riskLevel] || '#212121';

    // ── Risk Badge ─────────────────────────────────────────────────────
    const riskIcons = { low: '🟢', medium: '🟡', high: '🔴' };
    riskBadge.className = `risk-badge ${riskLevel}`;
    riskBadge.textContent = `${riskIcons[riskLevel]} ${data.risk_label}`;

    // ── Specific Findings ──────────────────────────────────────────────
    const findings = advice.specific_findings || [];
    if (findings.length > 0) {
      specificBox.classList.remove('hidden');
      findingsList.innerHTML = findings
        .map(f => `<li>${escHtml(f)}</li>`)
        .join('');
    } else {
      specificBox.classList.add('hidden');
    }

    // ── Advice Lists ───────────────────────────────────────────────────
    renderList('lifestyle-list', advice.lifestyle || []);
    renderList('diet-list',      advice.diet       || []);
    renderList('exercise-list',  advice.exercise   || []);
    renderList('medical-list',   advice.medical_tests || []);

    // Reset tabs to first
    tabBtns.forEach((b, i) => b.classList.toggle('active', i === 0));
    tabContents.forEach((c, i) => c.classList.toggle('active', i === 0));

    // ── Warnings ───────────────────────────────────────────────────────
    const warnings = advice.warnings || [];
    if (warnings.length > 0) {
      warningsBox.classList.remove('hidden');
      warningsList.innerHTML = warnings
        .map(w => `<li>${escHtml(w)}</li>`)
        .join('');
    } else {
      warningsBox.classList.add('hidden');
    }

    // ── Input Summary ──────────────────────────────────────────────────
    const summary = data.input_summary || {};
    summaryGrid.innerHTML = Object.entries(summary)
      .map(([label, val]) => `
        <div class="summary-item">
          <span class="s-label">${escHtml(label)}</span>
          <span class="s-value">${typeof val === 'number' ? val.toFixed(val % 1 === 0 ? 0 : 2) : val}</span>
        </div>
      `)
      .join('');

    // ── Show ───────────────────────────────────────────────────────────
    content.classList.remove('hidden');

    // Smooth scroll to result on mobile
    if (window.innerWidth < 1024) {
      document.getElementById('result-card').scrollIntoView({
        behavior: 'smooth', block: 'start'
      });
    }
  }

  // ── Helpers ─────────────────────────────────────────────────────────────
  function renderList(listId, items) {
    const el = document.getElementById(listId);
    if (!el) return;
    el.innerHTML = items.length
      ? items.map(item => `<li>${escHtml(item)}</li>`).join('')
      : '<li>Không có thông tin.</li>';
  }

  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ── Keyboard Shortcut: Enter to predict ────────────────────────────────
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      predictBtn.click();
    }
  });

  // ── Tooltip: Ctrl+Enter hint ────────────────────────────────────────────
  predictBtn.title = 'Phím tắt: Ctrl + Enter';

}());
