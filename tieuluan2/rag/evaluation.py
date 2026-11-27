"""
evaluation.py
Đánh giá định lượng chất lượng truy xuất:
- Hit@1, Hit@3, Hit@5
- MRR (Mean Reciprocal Rank)
- nDCG@10
- Đo độ trễ thời gian thực thi (Latency in ms)
"""
import math
import time
from typing import List, Dict, Any, Tuple

def compute_retrieval_metrics(retrieved_ids: List[str], ground_truth_ids: List[str], k_list: List[int] = [1, 3, 5, 10]) -> Dict[str, float]:
    """Tính các độ đo chuẩn Hit@k, MRR và nDCG@10 cho một truy vấn."""
    gt_set = set(ground_truth_ids)
    metrics = {}
    
    # 1. Hit@k
    for k in k_list:
        hits = any(r in gt_set for r in retrieved_ids[:k])
        metrics[f"hit@{k}"] = 1.0 if hits else 0.0

    # 2. MRR (Mean Reciprocal Rank)
    mrr = 0.0
    for rank, r in enumerate(retrieved_ids, 1):
        if r in gt_set:
            mrr = 1.0 / rank
            break
    metrics["mrr"] = mrr

    # 3. nDCG@10
    dcg = 0.0
    for rank, r in enumerate(retrieved_ids[:10], 1):
        rel = 1.0 if r in gt_set else 0.0
        dcg += rel / math.log2(rank + 1)
        
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(gt_set), 10) + 1))
    metrics["ndcg@10"] = dcg / idcg if idcg > 0 else 0.0

    return metrics

def benchmark_all_retrievers(queries_with_gt: List[Dict[str, Any]], retrievers: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """Chạy đối chuẩn đồng thời các bộ truy xuất trên tập câu hỏi kiểm định."""
    results = {}
    for r_name, retriever in retrievers.items():
        total_metrics = {"hit@1": 0.0, "hit@3": 0.0, "hit@5": 0.0, "mrr": 0.0, "ndcg@10": 0.0}
        total_time_ms = 0.0
        n_queries = len(queries_with_gt)

        for item in queries_with_gt:
            q = item["query"]
            gt = item["ground_truth_docs"]
            
            t0 = time.perf_counter()
            ret_res = retriever.search(q, top_k=10)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            total_time_ms += latency_ms

            # Extract doc_ids from retrieved chunks
            ret_ids = [c["doc_id"] for _, _, c in ret_res]
            m = compute_retrieval_metrics(ret_ids, gt)
            for k in total_metrics:
                total_metrics[k] += m[k]

        avg_metrics = {k: round(v / max(1, n_queries), 4) for k, v in total_metrics.items()}
        avg_metrics["avg_latency_ms"] = round(total_time_ms / max(1, n_queries), 2)
        results[r_name] = avg_metrics

    return results
