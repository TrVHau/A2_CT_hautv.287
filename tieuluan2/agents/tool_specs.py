"""
tool_specs.py
Đặc tả hình thức 7 công cụ của tác tử ReAct:
Tên, loại công cụ (DL, KG, RAG, CALC), mô tả và hàm thực thi chuẩn hóa.
"""
from dataclasses import dataclass
from typing import Callable, Any, Tuple, List, Dict

@dataclass
class Tool:
    name: str
    kind: str # DL | KG | RAG | CALC
    description: str
    fn: Callable[[Any], Tuple[Any, List[Tuple[str, str]]]]
    # fn returns: (observation_object, list_of_evidence_tuples: [(source_tag, text)])
