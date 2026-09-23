# Run Scaffold Design (Local / Docker / CI/CD)

Date: 2026-09-23

## Goal

Make the app runnable quickly in three contexts — native local dev, Docker,
and a CI/CD pipeline — with a single scaffold that addresses current gaps.

## Current State

Already present in the repo:

- `backend/Dockerfile` (Python 3.11 only)
- `web/Dockerfile` (Node 20 build -> nginx)
- `docker-compose.yml` (web on 8080, backend on internal 8001)
- `web/nginx.conf` (reverse-proxies `/api` to `backend:8001`, sets `X-Internal-Request: true`)
- `backend/tests/test_challenges.py` (pytest)
- Frontend tests (vitest, via `npm test` in `web/`)

Gaps addressed by this design:

1. No single local quick-start command (native dev API connectivity is broken).
2. Backend Docker image only executes Python (other 5 languages report unavailable).
3. No CI/CD pipeline (`.github/workflows/` does not exist).
4. README quick-start is manual step-by-step, not a cheat sheet.

## Decisions

- **Scaffold scope**: root tooling + Docker fix + CI/CD (validate only) + README docs.
- **CI/CD depth**: validate only — no image publishing, no deployment.
- **Local run modes**: both native dev servers and Docker Compose, exposed as root scripts.
- **Backend Docker image**: full polyglot (all 6 language toolchains), accepting a ~2GB image.

## Section 1 — Root Tooling

New file at repo root: `package.json`.

- No runtime dependencies. One devDependency: `concurrently`.
- Scripts:

| Script | Command |
|--------|---------|
| `install:all` | `npm --prefix web install && pip install -r backend/requirements.txt` |
| `dev` | `concurrently -k "cd backend && python main.py" "npm --prefix web run dev"` |
| `dev:web` | `npm --prefix web run dev` |
| `dev:backend` | `cd backend && python main.py` |
| `docker:up` | `docker compose up -d --build` |
| `docker:down` | `docker compose down` |
| `docker:logs` | `docker compose logs -f` |
| `test` | `npm --prefix web run test && cd backend && python -m pytest` |
| `build` | `npm --prefix web run build` |

- Root `node_modules` (`concurrently` only) is added to `.gitignore`.

## Section 2 — Native Dev API Connectivity Fix

Blocker: `web/src/hooks/useCodeRunner.js` and three other files fetch `/api/*`
relative to the Vite origin. Vite has no `/api` proxy, and
`backend/main.py` returns 403 for any request missing `X-Internal-Request: true`
(the `restrict_direct_access` middleware).

Fix: add a dev-server proxy to `web/vite.config.js` `server.proxy` block:

```js
proxy: {
  '/api': {
    target: 'http://localhost:8001',
    changeOrigin: true,
    headers: {
      'X-Internal-Request': 'true',
    },
  },
},
```

No frontend source changes. `VITE_API_BASE` stays unset (empty string), so all
`/api/*` calls route through the Vite dev proxy to the backend.

## Section 3 — Docker Full Polyglot Backend Image

Update `backend/Dockerfile` base install step to add:

- `curl` (required to bootstrap the rustup installer; `python:3.11-slim` does not ship it)
- `build-essential` (gcc for C runner)
- `default-jdk` (javac for Java runner)
- `golang-go` (go for Go runner)
- `nodejs` + `npm` (node for JS runner)
- Rust toolchain via rustup pinned to `stable`; symlink `$HOME/.cargo/bin/*` into `/usr/local/bin`

The `python:3.11-slim` base and the uvicorn `CMD` are unchanged. Expected image
size ~2GB.

Success check: after `docker compose build`, hit the container's
`/api/languages` endpoint and confirm all six runners report `available: true`.

## Section 4 — CI/CD Pipeline

New file: `.github/workflows/ci.yml`.

Runs `on: push` and `on: pull_request`. Three jobs:

1. **backend** — ubuntu-latest; setup-python 3.11; `pip install -r backend/requirements.txt`; `python -m pytest` in `backend/`.
2. **web** — ubuntu-latest; setup-node 20 with npm cache keyed on `web/package-lock.json`; `npm ci`; `npm run build`; `npm run test` in `web/`.
3. **docker** — ubuntu-latest; `docker compose build` (validates both Dockerfiles; slowest job due to ~2GB polyglot image).

## Section 5 — README Quick-Start Docs

Restructure the current "Quick Start" section into a "Run It Quickly" cheat sheet:

- **Native dev**: `npm install`, then `npm run dev` -> http://localhost:5173. Individual servers via `npm run dev:backend` / `npm run dev:web`.
- **Docker**: `npm run docker:up` -> http://localhost:8080. Stop with `npm run docker:down`.
- **Tests**: `npm test` runs both suites.
- **CI/CD**: point at `.github/workflows/ci.yml` and what it validates.
- Keep the existing per-component manual commands in a "Manual setup" subsection.

Also: add root `node_modules/` and root `package-lock.json` handling to `.gitignore` (root lockfile is committed).

## Files Changed

| File | Action |
|------|--------|
| `package.json` | Create (root tooling) |
| `web/vite.config.js` | Edit (add dev proxy) |
| `backend/Dockerfile` | Edit (polyglot toolchains) |
| `.github/workflows/ci.yml` | Create |
| `README.md` | Edit (quick-start cheat sheet) |
| `.gitignore` | Edit (root node_modules / lockfile) |

## Out of Scope

- Publishing Docker images to a registry.
- Deployment to any hosting target.
- Adding linters or new test frameworks (CI validates with existing suites).
- Multi-stage / slimmer polyglot backend variants.