# M-Motors - Studi Bloc 3

Application web de gestion M-Motors avec ajout du parcours **Location Longue Duree (LLD)**.

Le projet est compose de :
- un frontend `Next.js` (React, TypeScript),
- un backend `FastAPI` (Python),
- une stack Kubernetes `k8s` (base + overlays),
- une CI/CD GitHub Actions (tests, build, scan securite, deploiement).

## Sommaire

- [Architecture](#architecture)
- [Arborescence utile](#arborescence-utile)
- [Prerequis](#prerequis)
- [Demarrage local](#demarrage-local)
- [Variables d'environnement](#variables-denvironnement)
- [Tests et qualite](#tests-et-qualite)
- [CI/CD GitHub Actions](#cicd-github-actions)
- [Kubernetes](#kubernetes)
- [Securite](#securite)
- [Depannage rapide](#depannage-rapide)

## Architecture

### Frontend
- Framework: `Next.js 15`
- Langage: `TypeScript`
- UI: `React`, `Tailwind`
- Rôle: interface utilisateur, appels API, pages publiques/privées

### Backend
- Framework: `FastAPI`
- ORM/migrations: `SQLAlchemy`, `Alembic`
- Serveur: `Uvicorn/Gunicorn`
- Rôle: API REST, logique metier, acces PostgreSQL

### Infrastructure
- Orchestration: `Kubernetes` (manifests Kustomize)
- Ingress: `Traefik`
- Certificats: `cert-manager` (selon env)
- Registry images: `GHCR`

## Arborescence utile

```text
.
├── frontend/                 # Application Next.js
├── backend/                  # API FastAPI + migrations Alembic
├── k8s/
│   ├── base/                 # Ressources communes
│   ├── overlays/             # dev, staging, production
│   └── infra/                # infra cluster (traefik, quotas, rbac...)
├── .github/workflows/        # CI/CD GitHub Actions
└── README.md
```

## Prerequis

- `Node.js` >= 20 (24 utilise en CI)
- `npm`
- `Python` 3.12
- `pip`
- `Docker` (pour builds images)
- `kubectl` + acces cluster (pour deploiement)
- `kustomize` (ou `kubectl kustomize`)

## Demarrage local

## 1) Frontend

```bash
cd frontend
npm ci
npm run dev
```

Frontend disponible en general sur `http://localhost:3000`.

## 2) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Lancer les migrations:

```bash
python manage.py migrate --noinput
```

Lancer l'API:

```bash
uvicorn app.main:application --host 0.0.0.0 --port 8000 --reload
```

API disponible en general sur `http://localhost:8000`.

## Variables d'environnement

## Backend (principales)

Variables importantes:
- `SECRET_KEY` (obligatoire)
- `DATABASE_URL` **ou** `POSTGRES_DB` + `POSTGRES_USER` + `POSTGRES_PASSWORD`
- `POSTGRES_HOST` (defaut: `postgresql`)
- `POSTGRES_PORT` (defaut: `5432`)
- `ALLOWED_ORIGINS` (JSON array ou CSV)

Le backend lit aussi un fichier `.env` en local si present.

## Frontend (principales)

Selon contexte:
- `API_INTERNAL_URL`
- `BACKEND_URL`

Le routing `/api/*` est re-ecrit vers le backend (voir `frontend/next.config.js`).

## Tests et qualite

## Frontend

```bash
cd frontend
npm run lint
npm run type-check
npm run test -- --ci
```

## Backend

```bash
cd backend
pytest -q
ruff check .
mypy . --ignore-missing-imports
```

## CI/CD GitHub Actions

Workflows principaux:
- `ci.yaml`: tests, build/push images GHCR, scans Trivy, publication SARIF
- `deploy-dev.yaml`: deploiement auto sur `develop`
- `deploy-staging.yaml`: deploiement auto sur `main`
- `deploy-production.yaml`: deploiement sur tag `vX.Y.Z` + validation manuelle
- `security-scan.yaml`: scan securite planifie

## Kubernetes

Organisation:
- `k8s/base`: manifests communs
- `k8s/overlays/dev|staging|production`: specificites par environnement
- `k8s/infra`: objets d'infra (rbac, quotas, traefik, etc.)

Exemple de rendu production:

```bash
kustomize build k8s/overlays/production
```

Application:

```bash
kustomize build k8s/overlays/production | kubectl apply -f -
```

## Securite

- Scans images via Trivy dans la CI
- Upload SARIF vers GitHub Security
- SBOM genere en production
- Override frontend pour `picomatch` fixe en `4.0.4`
- Ignore temporaire Trivy (`.trivyignore`) pour `CVE-2026-33671` (faux positif connu sur manifestes)

## Depannage rapide

- Erreur Traefik Middleware non reconnu:
  - verifier les CRDs installes (`kubectl get crd | rg traefik.io`)
  - verifier les `apiVersion` Traefik en `traefik.io/v1alpha1`
- ImagePullBackOff:
  - verifier credentials GHCR (`ghcr-secret`)
  - verifier tag/digest pousse par la CI
- Scan Trivy incoherent:
  - verifier que le scan cible un digest (`@sha256:...`) et non un tag mutable

---

Projet maintenu dans le cadre de l'examen Studi Bloc 3.
