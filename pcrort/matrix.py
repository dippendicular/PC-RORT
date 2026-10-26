"""Matrix-layer PC-RORT reference implementation.

This module deliberately implements only the *known-center* conditional second
moment and an exact two-candidate PSD Frobenius-ball benchmark. It does not
estimate pilot-conditional moments or claim confidence coverage.

Candidate order is [local, source_1, ...]. Conditional covariance axes are
(candidate, parameter, candidate, parameter).
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize_scalar


def _symmetric_psd(a: np.ndarray, name: str, tolerance: float = 1e-9) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.isfinite(a).all():
        raise ValueError(f"{name} must be a finite square matrix")
    if not np.allclose(a, a.T, rtol=0, atol=tolerance):
        raise ValueError(f"{name} must be symmetric")
    a = (a + a.T) / 2
    if np.linalg.eigvalsh(a).min() < -tolerance:
        raise ValueError(f"{name} must be positive semidefinite")
    return a


def conditional_risk_matrix(
    conditional_bias: np.ndarray, curvature: np.ndarray, conditional_covariance: np.ndarray
) -> np.ndarray:
    """Return Q=B+V, retaining all off-diagonal source-error covariance.

    conditional_bias: p by J, including the local candidate in column zero.
    curvature: p by p PSD recipient Hessian.
    conditional_covariance: J by p by J by p joint covariance of final-fit errors,
      conditional on the frozen pilot sigma-field.
    """
    bias = np.asarray(conditional_bias, dtype=float)
    if bias.ndim != 2 or not np.isfinite(bias).all():
        raise ValueError("conditional_bias must be finite p x J")
    p, j = bias.shape
    h = _symmetric_psd(curvature, "curvature")
    cov = np.asarray(conditional_covariance, dtype=float)
    if h.shape != (p, p) or cov.shape != (j, p, j, p):
        raise ValueError("incompatible curvature or joint covariance dimensions")
    _symmetric_psd(cov.reshape(j * p, j * p), "joint covariance")
    b = bias.T @ h @ bias
    v = np.array([
        [np.trace(h @ cov[ell, :, k, :]) for ell in range(j)]
        for k in range(j)
    ])
    return _symmetric_psd(b + v, "conditional risk matrix")


def relative_contrast(weights: np.ndarray, risk_matrix: np.ndarray) -> float:
    """v^T Q v - e_local^T Q e_local; local-only is exactly zero."""
    q = _symmetric_psd(risk_matrix, "risk matrix")
    v = np.asarray(weights, dtype=float)
    if v.shape != (len(q),) or np.any(v < -1e-10) or not np.isclose(v.sum(), 1):
        raise ValueError("weights must belong to the candidate simplex")
    return float(v @ q @ v - q[0, 0])


@dataclass(frozen=True)
class TwoCandidateResult:
    external_weight: float
    robust_contrast: float
    local_only: bool
    radius: float
    method: str


def two_candidate_robust_selection(
    center: np.ndarray, radius: float, rho: float, *, tolerance: float = 1e-10
) -> TwoCandidateResult:
    """Optimize Eq. (26) for one source when the entire Frobenius ball is PSD.

    If radius <= lambda_min(center), the PSD constraint is redundant and the
    exact separation support is <center,G> + radius*||G||_F. Outside this
    domain, an SDP oracle is necessary; fail rather than silently solve a
    potentially different nonconvex/unrestricted-box problem.

    Numerical scalar minimization is for controlled experiments, not a
    verified numerical certificate or a high-confidence risk statement.
    """
    q = _symmetric_psd(center, "center")
    if q.shape != (2, 2) or not np.isfinite(radius) or not np.isfinite(rho):
        raise ValueError("expected finite 2x2 center, radius and mass cap")
    if radius < 0 or not (0 <= rho <= 1):
        raise ValueError("radius must be nonnegative and rho between zero and one")
    if radius > np.linalg.eigvalsh(q).min() + tolerance:
        raise NotImplementedError("PSD constraint may be active: use an SDP separation oracle")

    def objective(alpha: float) -> float:
        a = float(alpha)
        v = np.array([1.0 - a, a])
        g = np.outer(v, v) - np.array([[1.0, 0.0], [0.0, 0.0]])
        return float(np.sum(q * g) + radius * np.linalg.norm(g, "fro"))

    if rho == 0:
        return TwoCandidateResult(0., 0., True, radius, "exact-PSD-ball-support")
    fit = minimize_scalar(objective, bounds=(0, rho), method="bounded",
                          options={"xatol": 1e-13})
    if not fit.success:
        raise RuntimeError("Scalar robust minimization failed")
    candidates = [(0., 0.), (rho, objective(rho)), (float(fit.x), objective(fit.x))]
    best_a, best_y = min(candidates, key=lambda z: (z[1], z[0]))
    # Under the convex oracle objective, a nonnegative optimum is local-only.
    if best_y >= -tolerance:
        best_a, best_y = 0., 0.
    return TwoCandidateResult(best_a, best_y, best_a <= tolerance, radius,
                              "exact-PSD-ball-support")
