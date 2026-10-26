# Matrix-level power and uncertainty comparison

Install the project's dependencies and CVXPY; use a solver such as CLARABEL.
Run from repo root:

```bash
python -m unittest discover -s tests -v
python -m experiments.run_pcrort_matrix --samples 50 100 --candidates 2 3 --dimensions 1 4 --mismatches 0 0.3 --reps 25 --bootstrap 100 --out results/pcrort_matrix.csv
```

This comparison implements three pilot bootstrap uncertainty proposals:
1. PSD Frobenius ball with a percentile radius;
2. PSD-constrained simultaneous studentized entrywise box;
3. PSD affine ellipsoid from the covariance of Q-bootstrap symmetric entries.

The robust selector uses a convex quadratic master and PSD-constrained
separation-oracle SDP with CVXPY. The solver's numerical gap is not a
mathematically verified interval/dual certificate. **Empirical coverage must
be measured**; neither the direct-Q bootstrap (especially at vanishing
mismatch) nor the affine ellipsoid is asserted to satisfy Theorem 1.

Output columns include empirical oracle-matrix containment (coverage),
nonlocal selection, true quadratic contrast and harm, objective, optimization
gap, solver status, and runtime. Compare matched scenarios, not selection
rates alone. `plug_in` is a risk-minimization baseline without uncertainty.

The simulation uses a **fixed known linear score encoder** represented by
joint Gaussian pilot score vectors and the analytical covariance of the
future final-fit operator mean. It does not implement full multimodal
federation, typed operator training, confidence region (39), clinical-risk
adaptation, or the separate calibration step. It is a focused experiment
for selecting an uncertainty engine before end-to-end integration.

The shared-encoder factor is represented by correlated site scores. Change
`--shared` to vary common-encoder dependence. Simulation `true_contrast`
is a quadratic operator-error target, not patient-level diagnostic risk.
