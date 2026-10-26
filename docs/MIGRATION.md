# PC-RORT codebase map

All evidence, deliberation, selective, covariance and robust transport components
are under `pcrort/`. The prior nested namespace has been removed.

| Component | Current location |
| --- | --- |
| Evidence admissibility | `pcrort/evidence.py` |
| Multimodal deliberation | `pcrort/deliberation.py` |
| Selective prediction | `pcrort/selective.py` |
| Conditional operator risk matrix | `pcrort/matrix.py` |
| General PSD robust optimization | `pcrort/robust.py` |
| Direct-Q uncertainty-set comparison | `pcrort/uncertainty.py` |
| Power and coverage experiments | `experiments/run_pcrort_matrix.py` |
| Interactive analysis | `notebooks/run_pipeline.ipynb` |
| Authenticated web workspace | `webapp/` |

The training scripts use repository-root packages, and the multimodal model
reads its optional deliberation configuration from `pcrort:` in
`configs/multimodal.yaml`.

The paper's full typed-stratum recipient adaptation and paired-calibration
pipeline needs its own explicit implementation path; the existing selective
prediction component is a different operational policy.
