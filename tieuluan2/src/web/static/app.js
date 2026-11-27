/* JavaScript Application Logic for Tieuluan 2 Interactive Platform */

let cy = null;

function switchTab(tabId) {
  // Update nav buttons
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  // Update panes
  document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
  const targetPane = document.getElementById('tab-' + tabId);
  if (targetPane) {
    targetPane.classList.add('active');
  }

  if (tabId === 'kg_explorer') {
    setTimeout(initCytoscape, 100);
  } else if (tabId === 'rag_matrix') {
    loadBenchmarkMatrix();
  }
}

// 1. Healthcare Diabetes Prediction
async function handleDiabetesPredict(e) {
  e.preventDefault();
  const record = {
    age: parseFloat(document.getElementById('diab-age').value),
    gender: document.getElementById('diab-gender').value,
    bmi: parseFloat(document.getElementById('diab-bmi').value),
    HbA1c_level: parseFloat(document.getElementById('diab-hba1c').value),
    blood_glucose_level: parseFloat(document.getElementById('diab-glucose').value),
    hypertension: document.getElementById('diab-hyp').checked ? 1 : 0,
    heart_disease: document.getElementById('diab-heart').checked ? 1 : 0,
    smoking_history: document.getElementById('diab-smoking').value
  };

  const resDiv = document.getElementById('diabetes-result');
  resDiv.classList.remove('hidden');
  resDiv.innerHTML = 'Đang suy luận mạng nơ-ron DiabetesMLP trên GPU...';

  try {
    const resp = await fetch('/api/predict/diabetes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(record)
    });
    const data = await resp.json();

    const isHigh = data.risk_status.includes('NGUY CƠ CAO');
    resDiv.innerHTML = `
      <div class="result-title" style="color: ${isHigh ? '#ef4444' : '#10b981'}">
        KẾT QUẢ ĐÁNH GIÁ: ${data.risk_status}
      </div>
      <div class="metric-grid">
        <div class="metric-card">
          <div class="metric-val">${data.risk_percentage}</div>
          <div class="metric-lbl">Xác suất Nguy cơ (P)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">${data.threshold}</div>
          <div class="metric-lbl">Ngưỡng Quyết định (&tau;)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">10.497</div>
          <div class="metric-lbl">Tham số MLP (PyTorch)</div>
        </div>
      </div>
      <p style="margin-top: 0.8rem; font-size: 0.85rem; color: #d1d5db;">
        <strong>Khuyến nghị lâm sàng:</strong> ${data.clinical_advice}
      </p>
    `;
  } catch (err) {
    resDiv.innerHTML = `<span style="color: #ef4444">Lỗi: ${err.message}</span>`;
  }
}

// 2. Finance Forecast
async function handleFinanceForecast(e) {
  e.preventDefault();
  const asset = document.getElementById('fin-asset').value;
  const last_price = parseFloat(document.getElementById('fin-price').value);

  const resDiv = document.getElementById('finance-result');
  resDiv.classList.remove('hidden');
  resDiv.innerHTML = 'Đang lấy cửa sổ 30 phiên và chạy 200 lượt MC Dropout trên BiLSTM...';

  try {
    const resp = await fetch('/api/forecast/finance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asset, last_price })
    });
    const data = await resp.json();

    const isUp = data.predicted_log_return > 0;
    resDiv.innerHTML = `
      <div class="result-title" style="color: ${isUp ? '#10b981' : '#f59e0b'}">
        DỰ BÁO BI-LSTM: ${data.recommendation}
      </div>
      <div class="metric-grid">
        <div class="metric-card">
          <div class="metric-val">${data.predicted_next_price.toLocaleString('vi-VN')} đ</div>
          <div class="metric-lbl">Giá Dự báo Phiên tới</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">${data.return_pct_str}</div>
          <div class="metric-lbl">Lợi suất Kỳ vọng</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">${data.prob_increase_str}</div>
          <div class="metric-lbl">Xác suất Tăng giá</div>
        </div>
      </div>
      <p style="margin-top: 0.8rem; font-size: 0.82rem; color: #d1d5db;">
        <strong>Khoảng tin cậy 90% (MC Dropout):</strong> ${data.ci_90_price_str} VND<br>
        <strong>Độ bất định kết hợp (&sigma;):</strong> &plusmn;${(data.mc_uncertainty_std * 100).toFixed(2)}%
      </p>
    `;
  } catch (err) {
    resDiv.innerHTML = `<span style="color: #ef4444">Lỗi: ${err.message}</span>`;
  }
}

// 3. Cytoscape Knowledge Graph Viewer
async function initCytoscape() {
  if (cy) {
    cy.resize();
    return;
  }
  try {
    const resp = await fetch('/api/kg/graph');
    const graphData = await resp.json();

    cy = cytoscape({
      container: document.getElementById('cy'),
      elements: [...graphData.nodes, ...graphData.edges],
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'background-color': 'data(color)',
            'color': '#fff',
            'font-size': '11px',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-outline-color': '#111827',
            'text-outline-width': 2,
            'width': 35,
            'height': 35
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '9px',
            'color': '#94a3b8',
            'text-rotation': 'autorotate',
            'text-background-opacity': 0.8,
            'text-background-color': '#0f172a',
            'text-background-padding': 2
          }
        }
      ],
      layout: {
        name: 'cose',
        idealEdgeLength: 80,
        nodeOverlap: 20,
        refresh: 20,
        fit: true,
        padding: 30,
        randomize: false,
        componentSpacing: 100,
        nodeRepulsion: 400000,
        edgeElasticity: 100,
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0
      }
    });
  } catch (err) {
    console.error('Lỗi khởi tạo Cytoscape:', err);
  }
}

// 4. Load RAG Benchmark Matrix
async function loadBenchmarkMatrix() {
  const tbody = document.getElementById('benchmark-tbody');
  if (tbody.children.length > 0) return;

  try {
    const resp = await fetch('/api/rag/benchmark');
    const data = await resp.json();
    tbody.innerHTML = '';

    data.benchmark_matrix.forEach(row => {
      const tr = document.createElement('tr');
      const isTop = row.retriever.includes('Cross-Encoder') && row.strategy.includes('Ngữ nghĩa');
      if (isTop) {
        tr.style.background = 'rgba(16, 185, 129, 0.12)';
        tr.style.fontWeight = '600';
      }
      tr.innerHTML = `
        <td>${row.strategy}</td>
        <td><strong>${row.retriever}</strong></td>
        <td>${(row.hit1 * 100).toFixed(0)}%</td>
        <td>${(row.hit5 * 100).toFixed(0)}%</td>
        <td>${row.mrr.toFixed(2)}</td>
        <td>${row.ndcg.toFixed(2)}</td>
        <td>${row.latency_ms} ms</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Lỗi tải bảng benchmark:', err);
  }
}

// 5. Unified Chat and Grounded ReAct
async function handleUnifiedQuery(customQuery = null) {
  const q = customQuery || document.getElementById('unified-query').value.trim();
  if (!q) return;

  const loading = document.getElementById('chat-loading');
  const resArea = document.getElementById('chat-result-area');
  loading.classList.remove('hidden');
  resArea.classList.add('hidden');

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q })
    });
    const data = await resp.json();
    loading.classList.add('hidden');
    resArea.classList.remove('hidden');

    // Render Trace
    const traceBox = document.getElementById('trace-steps');
    traceBox.innerHTML = '';
    data.reasoning_trace.forEach(step => {
      const sDiv = document.createElement('div');
      sDiv.className = `trace-step step-${step.type.toLowerCase()}`;
      if (step.type === 'Thought') {
        sDiv.innerHTML = `<strong>[Bước ${step.step} - THOUGHT]:</strong> ${step.content}`;
      } else if (step.type === 'Action') {
        sDiv.innerHTML = `<strong>[Bước ${step.step} - ACTION]:</strong> Gọi công cụ <code>${step.tool}</code> | Đối số: ${JSON.stringify(step.args)}`;
      } else if (step.type === 'Observation') {
        sDiv.innerHTML = `<strong>[Bước ${step.step} - OBSERVATION (${step.latency_ms})]:</strong> ${step.content}`;
      }
      traceBox.appendChild(sDiv);
    });

    // Render Evidence
    const evBox = document.getElementById('evidence-list');
    evBox.innerHTML = '';
    data.evidence_list.forEach(ev => {
      const eDiv = document.createElement('div');
      eDiv.className = 'evidence-item';
      eDiv.innerHTML = `<strong>${ev.id} ${ev.source}:</strong> ${ev.snippet}`;
      evBox.appendChild(eDiv);
    });

    // Render Final Answer
    const ansDiv = document.getElementById('final-answer-content');
    ansDiv.innerHTML = data.final_answer.replace(/\n/g, '<br>');

    // Render Audit Badge
    const auditDiv = document.getElementById('verifier-badge');
    const audit = data.audit_verification;
    if (audit.passed) {
      auditDiv.style.background = 'rgba(16, 185, 129, 0.2)';
      auditDiv.style.color = '#34d399';
      auditDiv.style.border = '1px solid rgba(16, 185, 129, 0.4)';
      auditDiv.innerHTML = `✓ ${audit.audit_verdict} — Trích dẫn hợp lệ: ${audit.unique_citations} nguồn | Độ trung thực số học: ${audit.faithfulness_percentage}`;
    } else {
      auditDiv.style.background = 'rgba(239, 68, 68, 0.2)';
      auditDiv.style.color = '#f87171';
      auditDiv.style.border = '1px solid rgba(239, 68, 68, 0.4)';
      auditDiv.innerHTML = `✗ ${audit.audit_verdict} — Số liệu không có căn cứ: ${audit.unsupported_numbers.join(', ')}`;
    }
  } catch (err) {
    loading.classList.add('hidden');
    alert('Lỗi truy vấn: ' + err.message);
  }
}

function runHealthcareQuery(q) {
  switchTab('unified_chat');
  document.getElementById('unified-query').value = q;
  handleUnifiedQuery(q);
}

function runFinanceQuery(q) {
  switchTab('unified_chat');
  document.getElementById('unified-query').value = q;
  handleUnifiedQuery(q);
}
