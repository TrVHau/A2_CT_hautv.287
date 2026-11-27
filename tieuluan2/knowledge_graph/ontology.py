"""
ontology.py
Động cơ Bản thể học (Ontology Engine) hình thức hỗ trợ phân cấp lớp đa tầng,
vị từ kèm miền (domain), miền giá trị (range), quan hệ nghịch đảo (inverse),
tính bắc cầu (transitive), đối xứng (symmetric) và kiểm tra ràng buộc logic.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

@dataclass
class Predicate:
    name: str
    domain: str
    range: str
    label_vi: str
    is_transitive: bool = False
    is_symmetric: bool = False
    inverse_of: Optional[str] = None
    description: str = ""

class Ontology:
    def __init__(self, name: str):
        self.name = name
        self.classes: Set[str] = {"Thing"}
        self.superclasses: Dict[str, Set[str]] = {"Thing": set()}
        self.predicates: Dict[str, Predicate] = {}
        self.sub_predicates: Dict[str, str] = {}

    def add_class(self, cls: str, parent: str = "Thing"):
        self.classes.add(cls)
        self.classes.add(parent)
        if cls not in self.superclasses:
            self.superclasses[cls] = set()
        self.superclasses[cls].add(parent)
        if parent not in self.superclasses:
            self.superclasses[parent] = set()

    def add_predicate(self, pred: Predicate):
        self.predicates[pred.name] = pred
        if pred.inverse_of:
            inv_name = pred.inverse_of
            if inv_name not in self.predicates:
                self.predicates[inv_name] = Predicate(
                    name=inv_name,
                    domain=pred.range,
                    range=pred.domain,
                    label_vi=f"nghịch đảo của {pred.label_vi}",
                    inverse_of=pred.name
                )

    def is_a(self, child: str, parent: str) -> bool:
        """Kiểm tra quan hệ phân cấp lớp kế thừa (kể cả đa tầng)."""
        if child == parent:
            return True
        if child not in self.superclasses:
            return False
        visited = set()
        queue = list(self.superclasses.get(child, []))
        while queue:
            curr = queue.pop(0)
            if curr == parent:
                return True
            if curr not in visited:
                visited.add(curr)
                queue.extend(self.superclasses.get(curr, []))
        return False

    def validate_triple(self, s_type: str, pred_name: str, o_type: str) -> Tuple[bool, str]:
        """Kiểm tra ràng buộc miền (domain) và miền giá trị (range) của bộ ba."""
        pred = self.predicates.get(pred_name)
        if not pred:
            return False, f"Vị từ '{pred_name}' chưa được khai báo trong bản thể học {self.name}."
        
        if not self.is_a(s_type, pred.domain):
            return False, f"Vi phạm miền: Chủ thể loại '{s_type}' không phải lớp con của '{pred.domain}' trong vị từ {pred_name}."
        
        if not self.is_a(o_type, pred.range):
            return False, f"Vi phạm miền giá trị: Đối tượng loại '{o_type}' không phải lớp con của '{pred.range}' trong vị từ {pred_name}."
            
        return True, "Hợp lệ"
