# Contributing to PC-RORT

Contributions should target reproducible statistical inference and documented numerical behavior. Please open changes as pull requests with focused tests and a concise explanation of which theorem, equation, or experimental contract they affect.

## Development setup

```bash
python -m pip install numpy scipy cvxpy pytest
python -m pytest tests/test_pcrort_matrix.py tests/test_pcrort_robust.py -q
```

For multimodal or web app changes, install `requirements.txt` and include the relevant data-free smoke checks. Do not submit patient data, access tokens, credentials, pretrained weights without distribution rights, or private provenance graphs.

Maintain strict separation between pilot selection, fresh final-fit estimation, local adaptation and independent calibration. Changes to uncertainty regions must report empirical oracle coverage, selection power, false nonlocal selection, and solver status together. Distinguish numerical solver gaps from proven dual/interval bounds.

Code contributions are submitted under the repository's MIT license; ensure you have the right to contribute the code and check third-party licenses before adding dependencies or artifacts.
