"""
Annotated Code Listings for Master Treatise
All source code listings correspond to runnable modules in tieuluan2/src/
"""

CODE_LISTINGS = {
    "listing_2_1": {
        "caption": "Listing 2.1. Thuật toán Suy diễn Tiến RDFS (Forward Chaining) đến Điểm Bất động trong reasoning.py",
        "code": """def forward_chain_rdfs(graph: rdflib.Graph) -> int:
    \"\"\"
    Applies RDFS entailment rules (rdfs2, rdfs3, rdfs7, rdfs9)
    iteratively until fixed-point closure (no new triples derived).
    \"\"\"
    inferred_total = 0
    iteration = 0
    while True:
        iteration += 1
        new_triples = set()
        
        # Rule rdfs9: (C1 subClassOf C2) & (x type C1) => (x type C2)
        for s, _, c1 in graph.triples((None, RDF.type, None)):
            for _, _, c2 in graph.triples((c1, RDFS.subClassOf, None)):
                if (s, RDF.type, c2) not in graph:
                    new_triples.add((s, RDF.type, c2))
                    
        # Rule rdfs7: (p1 subPropertyOf p2) & (x p1 y) => (x p2 y)
        for p1, _, p2 in graph.triples((None, RDFS.subPropertyOf, None)):
            for s, _, o in graph.triples((None, p1, None)):
                if (s, p2, o) not in graph:
                    new_triples.add((s, p2, o))
                    
        # Rule rdfs2: (p domain C) & (x p y) => (x type C)
        for p, _, c in graph.triples((None, RDFS.domain, None)):
            for s, _, _ in graph.triples((None, p, None)):
                if (s, RDF.type, c) not in graph:
                    new_triples.add((s, RDF.type, c))
                    
        # Rule rdfs3: (p range C) & (x p y) => (y type C)
        for p, _, c in graph.triples((None, RDFS.range, None)):
            for _, _, o in graph.triples((None, p, None)):
                if isinstance(o, rdflib.URIRef) and (o, RDF.type, c) not in graph:
                    new_triples.add((o, RDF.type, c))
                    
        if not new_triples:
            break  # Fixed-point reached!
            
        for triple in new_triples:
            graph.add(triple)
        inferred_total += len(new_triples)
        
    return inferred_total"""
    },
    "listing_2_2": {
        "caption": "Listing 2.2. Triển khai 5 Truy vấn SPARQL Chuyên sâu Q1 - Q5 trong sparql_engine.py",
        "code": """SPARQL_QUERIES = {
    "Q1_LethalDrugInteraction": \"\"\"
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drugA ?drugB ?risk ?severity ?warning
        WHERE {
            ?drugA med:interactsWith ?drugB ;
                   med:hasLethalRisk ?risk ;
                   med:interactionSeverity ?severity ;
                   med:clinicalWarning ?warning .
            FILTER (?drugA = med:Metformin && ?drugB = med:Ethanol)
        }
    \"\"\",
    "Q2_DualTherapyHbA1c": \"\"\"
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drug ?class ?renalBenefit
        WHERE {
            ?drug med:prescribedInStep "Step 2 - Dual Therapy" ;
                  med:belongsToClass ?class ;
                  med:hasCardioRenalBenefit ?renalBenefit .
        }
    \"\"\",
    "Q3_RenalContraindications": \"\"\"
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drug ?minEGFR ?action
        WHERE {
            ?drug med:requiresRenalAdjustment true ;
                  med:contraindicatedWhenEGFRBelow ?minEGFR ;
                  med:recommendedAction ?action .
        }
        ORDER BY DESC(?minEGFR)
    \"\"\",
    "Q4_FedRateToGoldSpread": \"\"\"
        PREFIX fin: <http://ptit.edu.vn/fin/>
        SELECT ?intermediate ?target ?relation
        WHERE {
            fin:FedFundsRate ?p1 ?intermediate .
            ?intermediate ?p2 ?target .
        }
    \"\"\",
    "Q5_ExchangeRateImpact": \"\"\"
        PREFIX fin: <http://ptit.edu.vn/fin/>
        SELECT ?stock ?exposureType ?impactDirection ?mitigation
        WHERE {
            ?stock fin:sensitiveTo fin:USD_VND_Rate ;
                   fin:exposureType ?exposureType ;
                   fin:earningsImpact ?impactDirection ;
                   fin:hedgingMechanism ?mitigation .
        }
    \"\"\"
}"""
    },
    "listing_3_1": {
        "caption": "Listing 3.1. Thuật toán Truy xuất Thưa BM25 Okapi cho Tiếng Việt trong sparse_retrieval.py",
        "code": """class BM25Retriever:
    \"\"\"Okapi BM25 implementation optimized for Vietnamese medical/financial corpus.\"\"\"
    def __init__(self, corpus: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(tokenize_vietnamese(d['text'])) for d in corpus]
        self.avgdl = sum(self.doc_len) / max(len(self.doc_len), 1)
        self.doc_freqs = Counter()
        self.doc_token_counts = []
        for d in corpus:
            tokens = tokenize_vietnamese(d['text'])
            counts = Counter(tokens)
            self.doc_token_counts.append(counts)
            for token in counts.keys():
                self.doc_freqs[token] += 1
        self.N = len(corpus)
        self.idf = {t: math.log((self.N - freq + 0.5) / (freq + 0.5) + 1.0)
                    for t, freq in self.doc_freqs.items()}

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = tokenize_vietnamese(query)
        scores = []
        for idx, counts in enumerate(self.doc_token_counts):
            score = 0.0
            dl = self.doc_len[idx]
            denom_const = self.k1 * (1.0 - self.b + self.b * (dl / self.avgdl))
            for q in q_tokens:
                if q in counts:
                    tf = counts[q]
                    idf = self.idf.get(q, 0.0)
                    score += idf * (tf * (self.k1 + 1.0)) / (tf + denom_const)
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)"""
    },
    "listing_3_2": {
        "caption": "Listing 3.2. Thuật toán Dung hợp Thứ hạng Nghịch đảo (Hybrid RRF k=60) trong hybrid_retrieval.py",
        "code": """def reciprocal_rank_fusion(
    ranked_lists: List[List[Tuple[str, float]]],
    k: int = 60
) -> List[Tuple[str, float]]:
    \"\"\"
    Combines multiple rankings (e.g., BM25 and Dense Cosine)
    using Cormack et al.'s Reciprocal Rank Fusion formula:
    RRF(d) = sum_{m} 1.0 / (k + rank_m(d))
    \"\"\"
    rrf_scores = defaultdict(float)
    for rank_list in ranked_lists:
        for rank, (doc_id, _) in enumerate(rank_list, start=1):
            rrf_scores[doc_id] += 1.0 / (k + rank)
            
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs"""
    },
    "listing_4_1": {
        "caption": "Listing 4.1. Kiến trúc Mạng Nơ-ron PyTorch DiabetesMLP trong diabetes_mlp.py",
        "code": """class DiabetesMLP(nn.Module):
    \"\"\"
    13 -> 128 -> 64 -> 1 with BatchNorm, ReLU, and Dropout.
    Exact parameter count: 10,497 trainable parameters.
    \"\"\"
    def __init__(self, d_in: int = 13, hidden: tuple = (128, 64), dropout: float = 0.2):
        super().__init__()
        layers = []
        curr_d = d_in
        for h in hidden:
            layers.extend([
                nn.Linear(curr_d, h),
                nn.BatchNorm1d(h),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            curr_d = h
        layers.append(nn.Linear(curr_d, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Squeeze output to shape (batch_size,)
        return self.net(x).squeeze(-1)"""
    },
    "listing_4_2": {
        "caption": "Listing 4.2. Vòng lặp Huấn luyện Weighted BCE và Hiệu chuẩn Ngưỡng Youden J trong diabetes_mlp.py",
        "code": """def train_diabetes_mlp(
    X_train: np.ndarray, y_train: np.ndarray,
    X_val: np.ndarray, y_val: np.ndarray,
    epochs: int = 60, lr: float = 1e-3, pos_weight: float = 10.3
) -> Tuple[DiabetesMLP, float]:
    model = DiabetesMLP(d_in=13)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    # Weight positive errors 10.3x heavily to combat severe class imbalance
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight]))
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        logits = model(torch.tensor(X_train, dtype=torch.float32))
        loss = criterion(logits, torch.tensor(y_train, dtype=torch.float32))
        loss.backward()
        optimizer.step()
        
    # Calibrate decision threshold tau on validation set maximizing Youden's J
    model.eval()
    with torch.no_grad():
        val_probs = torch.sigmoid(model(torch.tensor(X_val, dtype=torch.float32))).numpy()
    
    thresholds = np.linspace(0.1, 0.99, 100)
    best_tau, best_j = 0.5, -1.0
    for tau in thresholds:
        preds = (val_probs >= tau).astype(int)
        sensitivity = recall_score(y_val, preds, zero_division=0)
        specificity = np.sum((y_val == 0) & (preds == 0)) / np.sum(y_val == 0)
        j_stat = sensitivity + specificity - 1.0
        if j_stat > best_j:
            best_j = j_stat
            best_tau = tau
            
    return model, best_tau  # Calibrated tau = 0.9016"""
    },
    "listing_5_1": {
        "caption": "Listing 5.1. Kiến trúc Mạng Nơ-ron PyTorch BiLSTM SeqForecaster trong finance_bilstm.py",
        "code": """class SeqForecaster(nn.Module):
    \"\"\"
    Bidirectional LSTM with FC head predicting next-session log return.
    Total parameter count: exactly 140,865 trainable parameters.
    \"\"\"
    def __init__(self, d_in: int = 7, hidden: int = 64, layers: int = 2, dropout: float = 0.2):
        super().__init__()
        self.rnn = nn.LSTM(
            input_size=d_in,
            hidden_size=hidden,
            num_layers=layers,
            batch_first=True,
            dropout=dropout if layers > 1 else 0.0,
            bidirectional=True
        )
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(2 * hidden, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.rnn(x)
        last_step = out[:, -1, :]  # shape: (batch_size, 128)
        return self.head(last_step).squeeze(-1)"""
    },
    "listing_5_2": {
        "caption": "Listing 5.2. Thuật toán Monte Carlo Dropout 200 Lượt Tạo Dải Quạt Tin Cậy 90% trong finance_bilstm.py",
        "code": """def monte_carlo_forecast(
    model: SeqForecaster,
    x_input: torch.Tensor,
    last_price: float,
    passes: int = 200
) -> Dict[str, Any]:
    \"\"\"
    Runs 200 stochastic forward passes with active dropout (p=0.2)
    to estimate epistemic uncertainty distribution.
    \"\"\"
    model.train()  # Keep dropout active during inference!
    returns = []
    with torch.no_grad():
        for _ in range(passes):
            pred_return = model(x_input).item()
            returns.append(pred_return)
            
    returns = np.array(returns)
    mu_return = float(np.mean(returns))
    sigma_return = float(np.std(returns))
    
    # 90% Gaussian confidence interval: [mu - 1.645*sigma, mu + 1.645*sigma]
    pred_price = last_price * np.exp(mu_return)
    ci90_lower = last_price * np.exp(mu_return - 1.645 * sigma_return)
    ci90_upper = last_price * np.exp(mu_return + 1.645 * sigma_return)
    
    return {
        "expected_price": round(pred_price, 2),
        "ci90_lower": round(ci90_lower, 2),
        "ci90_upper": round(ci90_upper, 2),
        "volatility_sigma": round(sigma_return, 4)
    }"""
    },
    "listing_6_1": {
        "caption": "Listing 6.1. Thuật toán Vòng Lặp ReAct Engine (Thought -> Action -> Observation) trong react_engine.py",
        "code": """class ReActEngine:
    \"\"\"Executes structured ReAct loop grounded in deterministic tool execution.\"\"\"
    def __init__(self, planner: DeterministicPlanner, verifier: GroundedVerifier):
        self.planner = planner
        self.verifier = verifier

    def run(self, query: str) -> Dict[str, Any]:
        trace = []
        # Step 1: Deterministic Plan
        plan = self.planner.create_plan(query)
        collected_context = []
        
        # Step 2: Sequential Tool Execution Loop
        for step in plan:
            thought = f"Cần thực thi công cụ {step['tool']} với đối số {step['args']}"
            action = step['tool']
            observation = dispatch_tool(step['tool'], step['args'])
            collected_context.append(str(observation))
            trace.append({
                "thought": thought,
                "action": action,
                "observation": observation
            })
            
        # Step 3: Synthesis with Grounded Verification
        draft_response = synthesize_grounded_answer(query, trace)
        verification = self.verifier.verify(draft_response, collected_context)
        
        if not verification["passed"]:
            # Auto-regeneration with strict constraint
            draft_response = regenerate_strict(query, trace, verification["violations"])
            
        return {
            "query": query,
            "response": draft_response,
            "trace": trace,
            "verification": verification
        }"""
    },
    "listing_6_2": {
        "caption": "Listing 6.2. Thuật toán Kiểm Chứng Độ Trung Thực Số Liệu Grounded Verifier trong grounded_verifier.py",
        "code": """class GroundedVerifier:
    \"\"\"Audits citation presence [Dxx] and enforces numeric faithfulness >= 0.85.\"\"\"
    def verify(self, response: str, contexts: List[str]) -> Dict[str, Any]:
        # 1. Audit citations [D01] - [D17]
        citations = re.findall(r'\\[D(\\d{2})\\]', response)
        has_citations = len(citations) > 0
        
        # 2. Extract numeric tokens from response and tool contexts
        resp_nums = set(re.findall(r'\\b\\d+(?:[.,]\\d+)?%?\\b', response))
        ctx_text = " ".join(contexts)
        ctx_nums = set(re.findall(r'\\b\\d+(?:[.,]\\d+)?%?\\b', ctx_text))
        
        if not resp_nums:
            faithfulness = 1.0
            unmatched = []
        else:
            matched = resp_nums.intersection(ctx_nums)
            unmatched = list(resp_nums.difference(ctx_nums))
            faithfulness = len(matched) / len(resp_nums)
            
        passed = has_citations and (faithfulness >= 0.85)
        return {
            "passed": passed,
            "faithfulness": round(faithfulness, 4),
            "citations_found": citations,
            "unmatched_numbers": unmatched
        }"""
    }
}
