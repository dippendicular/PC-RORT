# PC-RORT web portal

The portal provides authenticated dataset management, asynchronous training jobs,
model inventory and radiology inference. It uses FastAPI, SQLAlchemy, Celery,
Redis, PostgreSQL and S3-compatible object storage.

## Local stack (quick start)

From the repository root, with Docker installed:

```bash
python -m pip install -e ".[models,web]"
docker compose up -d
cp .env.example .env
pcrort web
```

Open `http://127.0.0.1:8000` for the browser console. In a separate
terminal, start the background training worker:

```bash
celery -A webapp.tasks.celery worker --loglevel=info
```

The Compose stack provides loopback-only PostgreSQL, Redis, MinIO and a
development bucket. Its credentials are placeholders for **local development
only**; replace them and deploy managed services with HTTPS and migrations for
real deployment.

## Install

```bash
python -m pip install -e ".[web,models]"
cp .env.example .env
pcrort web
```

Configure PostgreSQL, Redis, S3-compatible storage and **strong distinct secrets**
in `.env` first. Run the Celery worker separately:

```bash
celery -A webapp.tasks.celery worker --loglevel=info
```

The API health probe is `GET /api/health`, the authenticated optimization route is `POST /api/transport/optimize`, and API documentation is at
`/api/docs`. The browser dashboard is served at `/`.
The `pcrort web` command binds to localhost only. Production deployments
require HTTPS, secure cookies, trusted reverse-proxy settings, migrations,
audit logging, isolated workers, private object storage, monitoring, and
infrastructure hardening.

### Security

Authentication is cookie-backed and mutations use CSRF checks. Dataset upload
has configured limits and path validation; image uploads have a 20 MB cap.
Model loading is restricted to tensor-only PyTorch checkpoint decoding.
Do not expose the sample credentials in `.env.example` to a public endpoint.

### Project boundary

The portal's existing radiology inference route is a separate model workflow,
not the full relation-transport pathway. The PC-RORT statistical transport
components currently have separate numerical experiment entrypoints.

## Browser-based robust optimization

The workspace provides a risk-matrix editor and an authenticated POST route at
`/api/transport/optimize`. Supply a symmetric PSD center matrix for two to
eight candidates, a nonnegative Frobenius radius and an external-mass cap
`rho`. Candidate zero is the local estimator. The API returns the selected
weights, robust contrast, numerical gap and convergence status. The endpoint
has a 6-request/minute per-client rate limit and limits solver iterations.

The optimizer is a numerical research tool and is not connected to the web
portal's clinical-image prediction endpoint. Online clinical deployment
requires separate evaluation, governance and security review.
