# PC-RORT matrix-layer migration (first increment)

The existing VOIR multimodal loaders, encoder models, federated representation
training, and provenance evidence gate remain intact. The new `pcrort` package
holds the paper-specific conditional risk matrix and local-relative selection
primitives independently of legacy VOIR deliberation/selection.

## Included now

- Conditional Q=B+V with the *full joint* pilot-conditional final-fit covariance,
  including local/source and cross-source covariance blocks.
- Exact local-relative contrast against the local-only vertex.
- Controlled two-candidate robust Frobenius-ball benchmark when the **entire
  ball is PSD** (`radius <= lambda_min(center)`).
- Regression tests reproducing the full-versus-diagonal shared-encoder
  include/exclude decision flip.

Run from repository root: `python -m unittest discover -s tests -v`.

## Not yet implemented

The simultaneous pilot confidence construction, certified radius (24),
general J-candidate PSD/SOCP separation oracle, constraint-generation master,
pilot/final-fit partitions and locking, recipient adaptation, independent paired
calibration, typed-stratum operator estimation, and actual end-to-end PC-RORT
federated experiments remain separate work. This benchmark **does not**
establish confidence coverage, clinical-risk improvement, or a numerical
solver certificate.

## Migration boundary

Do not replace `voir/selective.py` with the new selector or claim that
`voir/deliberation.py` estimates the manuscript's typed relation operator.
Reuse provenance checks as the input eligibility boundary and introduce an
explicit typed (P,Q,D) schema with annotation-availability, patient, lesion,
time, target, and lineage validation before connecting the matrix-layer
algorithm to the clinical predictor.
