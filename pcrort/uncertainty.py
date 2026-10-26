"""Pilot-bootstrap uncertainty proposals on the J x J risk matrix.

These are *experimentally evaluated constructions*, not a replacement for
the manuscript's proven joint-gamma confidence region. Especially at zero
mismatch, plug-in Q is second-order and standard percentile bootstrap may
not provide nominal simultaneous coverage. Coverage must be measured.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import chi2
from .robust import UncertaintySet


def symmetric_features(q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    ii = np.triu_indices(len(q))
    return q[ii]


def symmetric_matrix(features: np.ndarray, size: int) -> np.ndarray:
    x = np.zeros((size, size), dtype=float)
    ii = np.triu_indices(size)
    x[ii] = features
    x[(ii[1], ii[0])] = features
    return x


def pilot_risk_matrix(pilot: np.ndarray, n_final: int) -> np.ndarray:
    """Plug-in Q for isotropic H=I/p and iid joint site noise.

    Pilot rows represent independent replicate vectors of J site-specific
    p-dimensional estimation-error scores. The first (local) bias column is
    fixed at zero; external bias is estimated relative to local.
    """
    x = np.asarray(pilot, dtype=float)
    if x.ndim != 3 or x.shape[0] < 3 or x.shape[1] < 1 or x.shape[2] < 1:
        raise ValueError("pilot must have shape (N>=3, J, p)")
    if n_final < 1:
        raise ValueError("n_final must be positive")
    n, j, p = x.shape
    average = x.mean(axis=0)
    b = average - average[:1]
    b[0] = 0.
    flat = (x - average).reshape(n, j * p)
    cov = flat.T @ flat / (n - 1)
    # Contract within-source and cross-source covariance through H = I/p.
    v = np.empty((j, j))
    for k in range(j):
        for ell in range(j):
            block = cov[k*p:(k+1)*p, ell*p:(ell+1)*p]
            v[k, ell] = np.trace(block) / (p * n_final)
    q = b @ b.T / p + v
    return (q + q.T) / 2


def bootstrap_matrices(
    pilot: np.ndarray, n_final: int, repetitions: int, rng: np.random.Generator
) -> np.ndarray:
    if repetitions < 10:
        raise ValueError("at least 10 bootstrap draws required")
    n = len(pilot)
    out = []
    for _ in range(repetitions):
        indices = rng.integers(0, n, n)
        out.append(pilot_risk_matrix(pilot[indices], n_final))
    return np.asarray(out)


def proposals(
    center: np.ndarray, bootstrap: np.ndarray, alpha: float = .05
) -> dict[str, UncertaintySet]:
    """Return comparable Frobenius, PSD-box, and affine-ellipsoid proposals.

    Frobenius radius: percentile of bootstrap Frobenius deviations.
    Box: max studentized entrywise deviation bootstrap critical value.
    Affine: eigen-directions of bootstrap covariance in symmetric Q space
    with chi-square radius (diagnostic Gaussian approximation).
    None currently carries a formal simultaneous coverage claim.
    """
    q = np.asarray(center, dtype=float)
    bs = np.asarray(bootstrap, dtype=float)
    j = len(q)
    if bs.ndim != 3 or bs.shape[1:] != q.shape or len(bs) < 10:
        raise ValueError("expected B x J x J bootstrap matrices")
    if not (0 < alpha < 1):
        raise ValueError("alpha must lie in (0,1)")
    dev = bs - q
    radii = np.linalg.norm(dev.reshape(len(bs), -1), axis=1)
    fro_radius = float(np.quantile(radii, 1 - alpha))
    iu = np.triu_indices(j)
    diffs = dev[:, iu[0], iu[1]]
    stdev = np.std(diffs, axis=0, ddof=1)
    stdev = np.maximum(stdev, 1e-12)
    stat = np.max(np.abs(diffs) / stdev[None, :], axis=1)
    cutoff = float(np.quantile(stat, 1 - alpha))
    widths = symmetric_matrix(cutoff * stdev, j)
    # Affine Q-space bootstrap covariance; retain only numerically supported
    # covariance directions. q must be PSD but the affine region is PSD-clipped.
    covariance = np.cov(diffs, rowvar=False)
    covariance = np.atleast_2d(covariance)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    active = eigenvalues > max(float(eigenvalues.max()) * 1e-10, 1e-20)
    directions = np.stack([
        symmetric_matrix(eigenvectors[:, i] * np.sqrt(eigenvalues[i]), j)
        for i in np.where(active)[0]
    ]) if np.any(active) else np.zeros((1, j, j))
    affine_radius = float(np.sqrt(chi2.ppf(1 - alpha, max(1, int(active.sum())))))
    return {
        "frobenius": UncertaintySet(q, "frobenius", fro_radius),
        "box_psd": UncertaintySet(q, "box_psd", widths=widths),
        "affine_psd": UncertaintySet(q, "affine_psd", affine_radius, directions=directions),
    }


def contains(uncertainty: UncertaintySet, matrix: np.ndarray, tol: float = 1e-9) -> bool:
    """Check membership in an experimental region for coverage diagnostics."""
    q = np.asarray(matrix, float)
    if q.shape != uncertainty.center.shape or np.linalg.eigvalsh(q).min() < -tol:
        return False
    delta = q - uncertainty.center
    if uncertainty.kind == "frobenius":
        return bool(np.linalg.norm(delta, "fro") <= uncertainty.radius + tol)
    if uncertainty.kind == "box_psd":
        return bool(np.all(np.abs(delta) <= uncertainty.widths + tol))
    d = uncertainty.directions.reshape(len(uncertainty.directions), -1).T
    coeff, *_ = np.linalg.lstsq(d, delta.ravel(), rcond=None)
    residual = np.linalg.norm(d @ coeff - delta.ravel())
    return bool(residual <= tol * max(1., np.linalg.norm(q, "fro")) and
                np.linalg.norm(coeff) <= uncertainty.radius + tol)
