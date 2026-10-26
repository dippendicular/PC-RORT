# Reproducible experiments

## Requirements

Python 3.11+, NumPy, SciPy, CVXPY with an SDP-capable solver (CLARABEL), pytest. The matrix experiment is CPU-oriented; no imaging dataset or GPU is required.

```bash
python -m pip install numpy scipy cvxpy pytest
python -m pytest tests/test_pcrort_matrix.py tests/test_pcrort_robust.py -q
```

## Main comparison

```bash
python -m experiments.run_pcrort_matrix \
  --samples 50 100 \
  --candidates 2 3 \
  --dimensions 1 4 \
  --mismatches 0 0.3 \
  --shared 0.5 \
  --reps 25 --bootstrap 100 --seed 20261026 \
  --out results/pcrort_matrix.csv
```

Parameters: `N` is pilot size, `J0` number of local-plus-source candidates, `p` operator dimension, `mismatch` source-to-local coefficient difference, `shared` common factor strength, `n_final` future final-fit size, `rho` external weight cap, `alpha` uncertainty nominal level.

Methods: `frobenius` (PSD Frobenius ball), `box_psd` (PSD simultaneous entrywise band), `affine_psd` (PSD affine directions), `plug_in` (no region). These bootstrap constructions require empirical assessment, especially when the mismatch is near zero and the first derivative of a quadratic bias term vanishes.

Output `covered` measures *oracle Q membership*, not clinical prediction coverage. `nonlocal` measures selection frequency; `true_contrast` is quadratic risk at oracle Q; `harmful` counts positive oracle contrasts. `status` and `gap` expose numerical non-convergence. Do not discard failed scenarios silently in aggregate calculations. Report conditional performance by N, J0, p and mismatch, empirical coverage next to inclusion power, and solver failure counts.

The simulator currently models shared-encoder dependence through correlated Gaussian score vectors; it is not a full learned neural encoder or proof of conditional coverage. The paper's nominal coverage theorem requires additional assumptions and a different full-universe joint confidence construction. All figures and claims should distinguish matrix experiments from full PC-RORT federated tests.

## CI

The `.github/workflows/pcrort-matrix.yml` workflow runs the numerical tests and a small experiment. Review GitHub Actions logs before treating outputs as verified.
