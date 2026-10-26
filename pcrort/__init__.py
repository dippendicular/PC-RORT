"""PC-RORT mathematical transport primitives (separate from legacy VOIR)."""
from .matrix import conditional_risk_matrix, relative_contrast, two_candidate_robust_selection

__all__ = ["conditional_risk_matrix", "relative_contrast", "two_candidate_robust_selection"]
