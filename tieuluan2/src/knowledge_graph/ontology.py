"""
Ontology Definition and Rule Specifications for Tieuluan 2:
- Predicate class with domain, range, and logic properties (transitive, symmetric, inverse_of)
- Ontology class maintaining the class hierarchy and is_a relationships
- Constraint Validator checking domain and range compliance
"""

from typing import Dict, List, Optional, Set, Tuple


class Predicate:
    """Predicate descriptor with domain, range, and logical axioms."""
    def __init__(
        self,
        name: str,
        domain: Optional[str] = None,
        range_: Optional[str] = None,
        transitive: bool = False,
        symmetric: bool = False,
        inverse_of: Optional[str] = None,
        description: str = "",
        polarity: Optional[int] = None  # +1 for positive causal, -1 for negative causal
    ):
        self.name = name
        self.domain = domain
        self.range_ = range_
        self.transitive = transitive
        self.symmetric = symmetric
        self.inverse_of = inverse_of
        self.description = description
        self.polarity = polarity

    def __repr__(self):
        return f"<Predicate {self.name}: {self.domain} -> {self.range_}>"


class Ontology:
    """Ontology hierarchy managing subclass relationships and subsumption testing."""
    def __init__(self, name: str):
        self.name = name
        self.classes: Set[str] = set()
        self.subclass_of: Dict[str, Set[str]] = {}
        self.predicates: Dict[str, Predicate] = {}

    def add_class(self, cls: str, parent: Optional[str] = None):
        """Add a class and optional direct superclass."""
        self.classes.add(cls)
        if cls not in self.subclass_of:
            self.subclass_of[cls] = set()
        if parent:
            self.classes.add(parent)
            if parent not in self.subclass_of:
                self.subclass_of[parent] = set()
            self.subclass_of[cls].add(parent)

    def add_predicate(self, pred: Predicate):
        """Register a predicate."""
        self.predicates[pred.name] = pred

    def is_subclass_of(self, child: str, parent: str) -> bool:
        """Transitive closure check: child is_a parent."""
        if child == parent:
            return True
        visited = set()
        queue = [child]
        while queue:
            curr = queue.pop(0)
            if curr == parent:
                return True
            visited.add(curr)
            for p in self.subclass_of.get(curr, set()):
                if p not in visited:
                    queue.append(p)
        return False

    def validate_triple(self, subj_type: str, pred_name: str, obj_type: str) -> Tuple[bool, str]:
        """Validate whether (subj_type, pred_name, obj_type) conforms to domain/range constraints."""
        if pred_name not in self.predicates:
            return False, f"Predicate '{pred_name}' is not registered in ontology {self.name}"
        
        pred = self.predicates[pred_name]
        
        # Check domain constraint
        if pred.domain and not self.is_subclass_of(subj_type, pred.domain):
            return False, f"Domain violation: subject type '{subj_type}' is not a subclass of expected domain '{pred.domain}' for predicate '{pred_name}'"
            
        # Check range constraint
        if pred.range_ and not self.is_subclass_of(obj_type, pred.range_):
            return False, f"Range violation: object type '{obj_type}' is not a subclass of expected range '{pred.range_}' for predicate '{pred_name}'"

        return True, "Valid triple assertion"
