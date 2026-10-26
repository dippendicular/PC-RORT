# Migration status

The repository and public interfaces are branded **PC-RORT**. Legacy experimental infrastructure is retained under `pcrort/legacy/`. The old top-level namespace has been removed from the development branch.

| Component | Status |
| --- | --- |
| Radiology/pathology/genomics data loaders | Existing / retained |
| Shared encoders, fusion and federated learning | Existing / retained |
| Existing evidence contract | Migrated to `pcrort.legacy`, requires typed-provenance extension |
| Existing signed deliberation | Migrated to `pcrort.legacy`, baseline only |
| Existing threshold/conformal selection | Migrated to `pcrort.legacy`, baseline only |
| Conditional Q=B+V | Added to `pcrort.matrix` |
| General PSD separation and robust weights | Added to `pcrort.robust` |
| Direct-Q bootstrap uncertainty proposals | Added to `pcrort.uncertainty` |
| Matrix-layer power/coverage simulation | Added to `experiments.run_pcrort_matrix` |
| Full pilot/final-fit locking and post-screen projection | Not integrated end-to-end |
| Typed operator estimation, adaptation, paired-loss calibration | Not integrated end-to-end |

## Compatibility changes

- Module imports formerly containing a repository-specific external package prefix now use this repository's root modules (`data`, `models`, `evaluation`, `training`, etc.).
- Optional historical deliberation flag is `pcrort_legacy` in `configs/multimodal.yaml`; historical model outputs use the same label to distinguish them from full PC-RORT.
- `PCRORTLegacyDeliberation` is a baseline class; PC-RORT's robust transport remains in `pcrort.robust`.
- Launch commands from repository root; a standalone pip-installable package is not claimed yet.
- Older notebook cells/configuration examples have been aligned to current root imports. Research run configs and saved checkpoints may require explicit migration if they refer to retired keys/classes.

## Next integration steps

Complete provenance typed-schema validation, fixed-dimensional regular encoder/influence summarization, patient-cluster-separated pilot/final-fit samples, full-universe valid confidence-region construction, locked transport, matched local adaptation, and paired independent calibration. Integrate with site clients only after numerical tests and matrix-layer coverage/power analysis establish a useful uncertainty engine.
