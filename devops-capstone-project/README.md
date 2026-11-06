# Customer Accounts — DevOps Capstone

A containerized Flask REST API for managing customer accounts, with automated quality checks and Kubernetes deployment assets.

![CI](https://github.com/Atharv-Jambhule/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)

## Features

- Create, list, read, update, and delete customer accounts.
- SQLite persistence (local file or mounted volume).
- Security headers with Flask-Talisman.
- Configurable CORS policy with Flask-CORS.
- Unit tests with `nosetests`, coverage, Flake8, and Pylint.
- Docker image and Kubernetes Deployment/Service manifests.
- GitHub Actions CI workflow and Tekton pipeline example.

## Project structure

```text
service/                 Flask application and API routes
tests/                   API, CORS, and security-header tests
.github/workflows/       GitHub Actions CI workflow
k8s/                     Kubernetes deployment and service
tekton/                  Tekton Tasks and Pipeline
docs/                    Backlog and sprint planning references
Dockerfile               Container image definition
setup.cfg                Nose, coverage, Flake8, Pylint configuration
requirements.txt         Runtime and test dependencies
```

## Run locally (Python 3.10+)

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

The API listens on `http://localhost:8080`.

## REST endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/accounts` | Create an account |
| GET | `/accounts` | List all accounts |
| GET | `/accounts/<id>` | Read one account |
| PUT | `/accounts/<id>` | Update an account |
| DELETE | `/accounts/<id>` | Delete an account |
| GET | `/health` | Health check |

### Example account JSON

```json
{
  "name": "Atharv Test Account",
  "email": "atharv.test@example.com",
  "address": "Pune, Maharashtra",
  "phone_number": "9876543210"
}
```

### cURL examples

```bash
curl -i -X POST http://localhost:8080/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Atharv Test Account","email":"atharv.test@example.com","address":"Pune, Maharashtra","phone_number":"9876543210"}'

curl -i http://localhost:8080/accounts
curl -i http://localhost:8080/accounts/1
curl -i -X PUT http://localhost:8080/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Account"}'
curl -i -X DELETE http://localhost:8080/accounts/1
```

## Configuration

- `PORT` — HTTP port (default `8080`)
- `DATABASE_PATH` — SQLite database path (default `./data/accounts.db`)
- `CORS_ORIGINS` — comma-separated allowed origins (default `*` for development)
- `TALISMAN_FORCE_HTTPS` — set `true` behind HTTPS; defaults to `false` for local/container demos.

For production, set explicit trusted CORS origins, enable HTTPS, and use a managed database/secret store.

## Run tests and quality checks

```bash
nosetests
coverage report
flake8 service tests run.py
pylint service tests run.py
```

## Docker

```bash
docker build -t customer-accounts:latest .
docker run --rm -p 8080:8080 -e CORS_ORIGINS="http://localhost:3000" customer-accounts:latest
```

## Kubernetes

```bash
kubectl apply -f k8s/
kubectl get deployments,pods,replicasets,services
kubectl port-forward service/customer-accounts 8080:8080
```

Open `http://localhost:8080/health`.

## GitHub Actions

The workflow at `.github/workflows/ci-build.yaml` checks out the repository, installs dependencies, runs Flake8, executes Nose tests, and generates a coverage report.

## Tekton

Apply the example resources in `tekton/` after configuring a Git clone secret and image registry credentials for your cluster. Replace the sample image registry in `tekton/pipeline.yaml` with your own registry.

## License

Educational project starter. Review dependencies and deployment settings before production use.
