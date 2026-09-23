# Run Scaffold (Local / Docker / CI/CD) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the app runnable quickly via native dev, Docker Compose, and a GitHub Actions CI pipeline, fixing the two real gaps (broken native-dev API connectivity, Python-only Docker backend) and adding root-level convenience scripts.

**Architecture:** Root `package.json` exposes `dev`, `docker:up`, and `test` shortcuts. A Vite dev-server proxy forwards `/api` to the FastAPI backend and injects the `X-Internal-Request` header so native dev works end-to-end. The backend Docker image gains Rust/Node/Java/GCC/Go toolchains (~2GB, deliberate). A single `.github/workflows/ci.yml` validates backend tests, frontend build+tests, and Docker image builds on every push/PR.

**Tech Stack:** npm (root scripts + `concurrently`), Vite dev proxy, FastAPI/uvicorn, Docker Compose, GitHub Actions, pytest, vitest.

---
## File Structure

| File | Responsibility | Action |
|------|----------------|--------|
| `package.json` (root) | Convenience scripts: `dev`, `docker:up`, `test`, etc. | Create |
| `.gitignore` | Stop ignoring `package-lock.json` so root lockfile is committed | Modify |
| `web/vite.config.js` | Add `/api` dev proxy injecting internal header | Modify |
| `backend/Dockerfile` | Full polyglot toolchains for all 6 runtimes | Modify |
| `.github/workflows/ci.yml` | Validate backend, web, Docker on push/PR | Create |
| `README.md` | "Run It Quickly" cheat sheet | Modify |
| `docs/superpowers/specs/2026-09-23-run-scaffold-design.md` | Approved design (source of truth) | Reference only |

Verification commands below assume win32 PowerShell. POSIX equivalents: replace `curl.exe` with `curl`, `taskkill /PID <pid> /T /F` with `kill <pid>`.

---

### Task 1: Root tooling (`package.json` + `.gitignore`)

**Files:**
- Create: `package.json` (repo root)
- Modify: `.gitignore:2` (remove `package-lock.json` line so root lockfile gets committed; `web/package-lock.json` is already tracked and stays)

- [ ] **Step 1: Remove the `package-lock.json` ignore entry**

Edit `.gitignore`: delete the line `package-lock.json`. Result (top of file):

```gitignore
# Dependencies
node_modules/
```

(Do NOT touch the rest of the file.)

- [ ] **Step 2: Create root `package.json`**

```json
{
  "name": "algo-playground",
  "version": "3.0.0",
  "private": true,
  "scripts": {
    "install:all": "npm --prefix web install && pip install -r backend/requirements.txt",
    "dev": "concurrently -k -n backend,web -c blue,green \"cd backend && python main.py\" \"npm --prefix web run dev\"",
    "dev:web": "npm --prefix web run dev",
    "dev:backend": "cd backend && python main.py",
    "docker:up": "docker compose up -d --build",
    "docker:down": "docker compose down",
    "docker:logs": "docker compose logs -f",
    "test": "npm --prefix web run test && cd backend && python -m pytest",
    "build": "npm --prefix web run build"
  },
  "devDependencies": {
    "concurrently": "^9.0.0"
  }
}
```

- [ ] **Step 3: Install root dependencies**

Run: `npm install`

Expected: creates root `node_modules/concurrently` and root `package-lock.json`. No errors.

- [ ] **Step 4: Verify scripts are registered**

Run: `npm run`

Expected: lists all 9 scripts (`install:all`, `dev`, `dev:web`, `dev:backend`, `docker:up`, `docker:down`, `docker:logs`, `test`, `build`).

- [ ] **Step 5: Commit**

```bash
git add .gitignore package.json package-lock.json
git commit -m "chore: add root npm scripts for dev, Docker, and tests"
```

---

### Task 2: Fix native dev API connectivity (Vite proxy)

**Files:**
- Modify: `web/vite.config.js`

Background: `web/src/hooks/useCodeRunner.js:3` (and `ChallengeLibrary.jsx`, `ProblemCard.jsx`, `ChallengeEmbed.jsx`) fetch `${API_BASE}/api/*` with `API_BASE` defaulting to `''`, i.e. against the Vite origin (port 5173). Vite has no proxy, and `backend/main.py:14-19` returns 403 unless `X-Internal-Request: true` is present. The proxy below fixes both.

- [ ] **Step 1: Add the dev proxy**

Edit `web/vite.config.js`. Replace the `server: { ... }` block with:

```js
  server: {
    port: 5173,
    open: true,
    hot: true,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        headers: {
          'X-Internal-Request': 'true',
        },
      },
    },
  },
```

Keep `plugins`, `build`, and `test` blocks unchanged. Final file must be exactly:

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import mdx from '@mdx-js/rollup';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    mdx(),
  ],
  server: {
    port: 5173,
    open: true,
    hot: true,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        headers: {
          'X-Internal-Request': 'true',
        },
      },
    },
  },
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.js'],
    css: { modules: { classNameStrategy: 'non-scoped' } },
  },
});
```

- [ ] **Step 2: Start backend + frontend in the background**

PowerShell (win32):

```powershell
$b = Start-Process python -ArgumentList 'main.py' -WorkingDirectory 'C:\Users\puppets\Documents\ds_and_algo\backend' -PassThru
$w = Start-Process npm -ArgumentList 'run','dev' -WorkingDirectory 'C:\Users\puppets\Documents\ds_and_algo\web' -PassThru
Start-Sleep -Seconds 15
```

(Vite `open: true` will pop a browser tab — expected. Note: `main.py` binds `127.0.0.1:8001`, Vite binds on 5173.)

- [ ] **Step 3: Verify direct backend access is still blocked**

Run: `curl.exe -s http://localhost:8001/api/languages`

Expected: HTTP 403 body `{"detail":"Direct API access denied. Requests must go through the nginx proxy."}`

- [ ] **Step 4: Verify proxied access through Vite works**

Run: `curl.exe -s http://localhost:5173/api/languages`

Expected: HTTP 200 with a JSON array of `{lang, available, version}` entries (one per runner: python, rust, javascript, java, c, go).

- [ ] **Step 5: Stop the background servers**

```powershell
taskkill /PID $w.Id /T /F
Stop-Process -Id $b.Id -Force
```

If the port is still held, `Stop-Process -Id (Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue).OwningProcess -Force` for 5173 and 8001.

- [ ] **Step 6: Commit**

```bash
git add web/vite.config.js
git commit -m "fix: proxy /api to backend in Vite dev server"
```

---

### Task 3: Polyglot backend Docker image

**Files:**
- Modify: `backend/Dockerfile`

- [ ] **Step 1: Rewrite `backend/Dockerfile`**

Final content:

```dockerfile
FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        default-jdk \
        golang-go \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && ln -s /root/.cargo/bin/* /usr/local/bin/

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

Note: `curl` is required for rustup (slim image doesn't ship it). Keep `curl .dockerignore` untouched (already ignores `__pycache__`, `*.pyc`, `.git`).

- [ ] **Step 2: Build the backend image**

Run: `docker compose build backend`

Expected: image builds successfully. First build takes several minutes (apt + rustup). Do NOT rebuild yet if cached from a prior attempt — a fresh build is expected here.

- [ ] **Step 3: Start the backend container**

Run: `docker compose up -d backend`

Expected: container starts; `docker compose ps` shows `backend` as `Up`.

- [ ] **Step 4: Verify all six toolchains are detected**

Run:

```powershell
docker compose exec backend python -c "from runners import RUNNERS; print({k: v().detect() for k, v in RUNNERS.items()})"
```

Expected: `{'python': True, 'rust': True, 'javascript': True, 'java': True, 'c': True, 'go': True}`

- [ ] **Step 5: Smoke-test a non-Python execution end-to-end through the API**

Run:

```powershell
docker compose exec backend curl -s -X POST -H "Content-Type: application/json" -H "X-Internal-Request: true" -d '{"lang":"javascript","code":"console.log(42)"}' http://localhost:8001/api/run
```

Expected: JSON with `"stdout": "42"` and `"exit_code": 0`.

Also smoke-test Java and Go (they compile, so they exercise javac/gcc/go):

```powershell
docker compose exec backend curl -s -X POST -H "Content-Type: application/json" -H "X-Internal-Request: true" -d '{"lang":"java","code":"public class Main { public static void main(String[] a) { System.out.println(42); } }"}' http://localhost:8001/api/run
docker compose exec backend curl -s -X POST -H "Content-Type: application/json" -H "X-Internal-Request: true" -d '{"lang":"go","code":"package main\nimport \"fmt\"\nfunc main(){ fmt.Println(42) }"}' http://localhost:8001/api/run
```

Expected: each returns `"stdout": "42"` and `"exit_code": 0` (Java/Go may take a few seconds to compile).

- [ ] **Step 6: Verify full Docker Compose stack serves the web app**

Run: `docker compose up -d --build web` (depends_on pulls `backend` up too)

Run: `curl.exe -s http://localhost:8080/api/languages`

Expected: HTTP 200 JSON array (nginx proxies `/api` to backend through the internal network with the header).

- [ ] **Step 7: Tear down**

Run: `docker compose down`

Expected: containers removed.

- [ ] **Step 8: Commit**

```bash
git add backend/Dockerfile
git commit -m "feat: polyglot toolchains in backend Docker image"
```

---

### Task 4: CI/CD pipeline (GitHub Actions)

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create the workflow file**

Create directory `.github/workflows/` and write `ci.yml`:

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  backend:
    name: Backend tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run pytest
        working-directory: backend
        run: python -m pytest

  web:
    name: Frontend build + tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm
          cache-dependency-path: web/package-lock.json
      - name: Install dependencies
        working-directory: web
        run: npm ci
      - name: Build
        working-directory: web
        run: npm run build
      - name: Run vitest
        working-directory: web
        run: npm run test

  docker:
    name: Docker build validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build images
        run: docker compose build
```

- [ ] **Step 2: Sanity-check YAML parsing**

Run:

```powershell
python -c "import yaml" 2>$null; if ($?) { python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('YAML OK')" } else { echo "PyYAML not installed; syntax validated by GitHub on push" }
```

Expected: `YAML OK` (if PyYAML present; otherwise the echo message — acceptable).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions pipeline (validate only)"
```

- [ ] **Step 4: Verify live on GitHub**

Run: `git push origin main`

Expected: GitHub Actions runs all three jobs. Confirm in repo → Actions tab that `backend`, `web`, and `docker` jobs are green. A YAML syntax error fails fast at job creation; a build error appears in the respective job. (If the executor cannot push, note this as a follow-up for the user.)

---

### Task 5: README quick-start docs

**Files:**
- Modify: `README.md:5-28` (the "Quick Start" section, up to but not including the "Production Build" subsection)

- [ ] **Step 1: Replace the Quick Start section**

Replace everything from `## Quick Start` (line 5) up to but not including `## Architecture` (line 30) in `README.md` with the text below. The old `### Backend`, `### Frontend`, and `### Production Build` subsections are folded into the new `### Manual setup (component by component)` at the end.

```markdown
## Run It Quickly

### Native dev (npm scripts)

Prerequisites: Python 3.10+, Node 20+.

```bash
npm install              # installs the root `concurrently` helper
npm run dev              # starts backend (8001) + frontend (5173) together
```

Open http://localhost:5173

Individual servers:

```bash
npm run dev:backend      # FastAPI code runner on http://127.0.0.1:8001
npm run dev:web          # Vite dev server on http://localhost:5173
```

First-time dependency install for a fresh clone: `npm run install:all`.

### Docker (full stack)

Prerequisite: Docker + Docker Compose.

```bash
npm run docker:up        # build & start backend + nginx-served web on :8080
```

Open http://localhost:8080 — stop with `npm run docker:down`, tail logs with `npm run docker:logs`.

### Tests

```bash
npm test                 # frontend vitest suite + backend pytest suite
```

### CI/CD

`.github/workflows/ci.yml` runs on every push and pull request: backend pytest,
frontend build + vitest, and `docker compose build` to validate both images.

### Manual setup (component by component)

For manual control, start each part yourself:

Backend:

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Runs on `http://127.0.0.1:8001` — serves `/api/run` and `/api/languages`.

Frontend:

```bash
cd web
npm install
npm run dev
```

Opens at `http://localhost:5173` — full SPA with hot reload.

Production Build:

```bash
cd web
npm run build
npm run preview
```
```

- [ ] **Step 2: Verify the README renders correctly**

Run: `git diff README.md`

Expected: `## Quick Start` is gone; `## Run It Quickly` has the Native dev / Docker / Tests / CI/CD / Manual setup subsections; the "Architecture" heading still follows it. All fenced code blocks are balanced (each opens and closes with ```).

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add Run It Quickly cheat sheet"
```

---

## Self-Review

**Spec coverage:**

| Spec section | Task |
|---|---|
| Section 1 — Root tooling (`package.json`) | Task 1 |
| Section 1 — `.gitignore` root node_modules / lockfile | Task 1 (Step 1; `node_modules/` already ignored) |
| Section 2 — Vite dev proxy with internal header | Task 2 |
| Section 3 — Polyglot backend Dockerfile (+ `curl` for rustup) | Task 3 |
| Section 4 — `ci.yml` (backend, web, docker jobs) | Task 4 |
| Section 5 — README cheat sheet | Task 5 |

**Consistency:** Root script names in Task 1 (`dev`, `docker:up`, `docker:down`, `docker:logs`, `test`, `build`, `install:all`, `dev:web`, `dev:backend`) are the exact names used in README (Task 5). RunRequest fields are `lang`/`code` (models.py:3-5); the smoke-test payloads use those exact keys. Runner map keys (`python/rust/javascript/java/c/go`) come from `backend/runners/__init__.py:6-12` and match the `/api/languages` expectation in Task 2 Step 4.

**Placeholders:** None — every step has exact file content, commands, or expected output.

**Known tradeoff noted in spec:** the `docker` CI job and Task 3 build are slow (~2GB image). Not addressed by this plan per spec decisions.