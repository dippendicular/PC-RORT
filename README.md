# PC-RORT

**Provenance-Constrained Recipient-Optimal Relation Transport for Federated Multimodal Learning**

PC-RORT is a Python research and engineering platform combining multimodal representation learning, provenance-aware evidence processing, federated training infrastructure, and robust recipient-specific relation transport.

## Quick start

Python 3.11 or newer:

```bash
git clone https://github.com/dippendicular/PC-RORT.git
cd PC-RORT
python -m pip install -e .
pcrort demo
```

The lightweight install includes the numerical optimizer, covariance matrix utilities, and uncertainty-set comparison tools.

For notebooks, model training and the web portal together:

```bash
python -m pip install -e ".[dev,models,web]"
```

## Interactive notebook

Open `notebooks/run_pipeline.ipynb` in JupyterLab or Google Colab and select **Run All**. It includes the covariance decision flip, general PSD optimization, uncertainty-set comparison, Monte Carlo power experiment and plots. Start Jupyter locally with:

```bash
jupyter lab notebooks/run_pipeline.ipynb
```

## CLI experiments

```bash
python -m experiments.run_pcrort_matrix --reps 25 --bootstrap 100
```

The runner compares Frobenius, simultaneous PSD entrywise and affine PSD uncertainty models with a plug-in baseline. Results and configuration metadata are written to `results/`.

## Multimodal training

Configure the dataset paths in `configs/` and execute a training entry point:

```bash
python -m experiments.train_multimodal --config configs/multimodal.yaml
```

Available modes: `train_radiology`, `train_pathology`, `train_genomics`, and `train_multimodal`. Training requires the corresponding dataset manifest and modality files.

## Web app

The FastAPI workspace includes account access, dataset uploads, queued training jobs, a model inventory, and a radiology inference interface. Copy `.env.example` to `.env`, configure PostgreSQL/Redis/S3-compatible services and secrets, then:

```bash
pcrort web
```

Open `http://127.0.0.1:8000`. API reference: `/api/docs`. Deployment and worker setup are described in [Web App Guide](docs/WEBAPP.md).

## Project layout

| Location | Purpose |
| --- | --- |
| `pcrort/` | Matrix construction, robust optimizer, uncertainty methods, evidence and deliberation |
| `experiments/` | Statistical experiments and model-training CLI |
| `models/` | Radiology, pathology, genomics, and multimodal models |
| `federated/` | Federated client/server and aggregation |
| `data/` | Datasets, provenance-related patient matching and preprocessing |
| `evaluation/` | Metrics and plotting |
| `webapp/` | FastAPI service, database, workers and dashboard |
| `notebooks/` | Interactive research workflow |
| `tests/` | Numerical regression and invariant tests |

Documentation: [Architecture](docs/ARCHITECTURE.md) · [Experiments](docs/EXPERIMENTS.md) · [Web App](docs/WEBAPP.md) · [Contributing](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
