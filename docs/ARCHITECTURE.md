# PC-RORT architecture

## Layer boundaries

1. **Evidence eligibility:** Independent observed record pairs are admitted through identity, target, index time, pair availability, derivation lineage and typed-annotation checks. The retained `pcrort.legacy.evidence` checks are starting infrastructure, not a full typed (polarity, qualification, derivation dependence) implementation.
2. **Shared encoder:** Only designated representation parameters participate in federation. Existing `models/` and `federated/` code provides infrastructure; it does not automatically have the fixed-dimensional influence expansion assumed by the paper.
3. **Pilot inference:** The statistical selector requires a shared encoder that is frozen, recipient/site-specific pilot operator estimates, recipient curvature, linked-cluster influence summaries, and a *joint* covariance of future final-fit errors. Pilot-conditional error means and covariance include residual common-encoder dependence.
4. **Risk matrix:** `pcrort.matrix.conditional_risk_matrix` computes `Q=B+V` in the common basis. It expects `bias[p,J]`, `H[p,p]`, and `Omega[J,p,J,p]`; local candidate is index zero. A PSD check rejects inconsistent joint covariance.
5. **Uncertainty and selection:** `pcrort.robust` implements convex quadratic cutting planes with a PSD-constrained CVXPY separation oracle. Supported experimental sets are Frobenius, PSD entrywise box, and PSD affine ellipsoid. The numerical termination gap is not a mathematically verified upper confidence bound.
6. **Weight locking:** The paper requires source eligibility, uncertainty and all weights to be fixed using pilot information *before* fresh final-fit operators are released. The full locked-weight pipeline remains future integration work.
7. **Recipient adaptation and paired calibration:** Must use matched local-only fitting, disjoint calibration clusters, and a bounded paired-loss upper confidence bound. The retained `pcrort.legacy.selective` policy performs a different task and must not be substituted for this gate.

## Source layout

- `data/`: clinical-data adapters, pair matching, modality-specific datasets.
- `models/`: radiology, pathology, genomic and multimodal encoders.
- `training/`: network training utilities.
- `federated/`: shared-parameter aggregation and site/coordinator wrappers.
- `pcrort/`: research algorithm, uncertainty, selection and legacy boundaries.
- `experiments/`: CLI entrypoints for training and matrix experiments.
- `evaluation/`: metrics and plotting.
- `webapp/`: separate optional research portal.

## Distinguishing retained functionality

Legacy deliberation uses signed attention and class scores; it does *not* estimate the paper's context-indexed typed operator or solve Eq. (26). Legacy selective prediction uses temperature/conformal heuristics; it is *not* the independent paired empirical-Bernstein transfer gate. Both modules remain accessible from `pcrort.legacy`, and must be treated as optional baselines.

## Package invocation

Launch commands from the repository root, for example `python -m experiments.train_multimodal` and `python -m experiments.run_pcrort_matrix`. Root modules are imported as `models`, `data`, `evaluation`, `training`, `utils` and `federated`, while research algorithm primitives use the `pcrort` namespace.
