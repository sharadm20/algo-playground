# DSA Study Plan — React SPA + Interactive Code Playground

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the existing static HTML DSA study plan into a modern React SPA with interactive code playgrounds, a FastAPI backend for polyglot code execution, MDX content for all 30 days, and shareable progress reports.

**Architecture:** React 18 SPA (Vite + React Router + MDX) serves day content with embedded interactive code editors. FastAPI backend dispatches code to language-specific runners (Python, Rust, JS, Java, C, Go) in sandboxed subprocesses. Progress lives in localStorage; export generates downloadable reports.

**Tech Stack:** React 18, Vite, React Router v7, CodeMirror 6, MDX (`@mdx-js/rollup`), FastAPI, CSS Modules, Pyodide (optional fallback)

---

## File Structure

```
ds_and_algo/
├── backend/
│   ├── main.py                  # FastAPI app entry
│   ├── sandbox.py               # Temp dir, timeout, output capture
│   ├── models.py                # Pydantic request/response models
│   ├── runners/
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base runner
│   │   ├── python_runner.py
│   │   ├── rust_runner.py
│   │   ├── js_runner.py
│   │   └── other_runners.py     # Java, C, Go
│   ├── requirements.txt
│   └── start.bat
├── web/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── router.jsx
│   │   ├── styles/
│   │   │   ├── tokens.css
│   │   │   └── global.css
│   │   ├── context/
│   │   │   ├── ThemeContext.jsx
│   │   │   └── ProgressContext.jsx
│   │   ├── hooks/
│   │   │   ├── useProgress.js
│   │   │   └── useCodeRunner.js
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Layout.jsx
│   │   │   │   └── Layout.module.css
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── WeekGroup.jsx
│   │   │   │   ├── DayLink.jsx
│   │   │   │   └── Sidebar.module.css
│   │   │   ├── TopBar/
│   │   │   │   ├── TopBar.jsx
│   │   │   │   └── TopBar.module.css
│   │   │   ├── HomePage/
│   │   │   │   ├── HomePage.jsx
│   │   │   │   ├── StatsRow.jsx
│   │   │   │   ├── CalendarGrid.jsx
│   │   │   │   └── HomePage.module.css
│   │   │   ├── DayPage/
│   │   │   │   ├── DayPage.jsx
│   │   │   │   ├── DayPage.module.css
│   │   │   │   └── DayNavigation.jsx
│   │   │   ├── CodePlayground/
│   │   │   │   ├── CodePlayground.jsx
│   │   │   │   ├── OutputPanel.jsx
│   │   │   │   └── CodePlayground.module.css
│   │   │   ├── ProblemCard/
│   │   │   │   ├── ProblemCard.jsx
│   │   │   │   └── ProblemCard.module.css
│   │   │   ├── ExportPage/
│   │   │   │   ├── ExportPage.jsx
│   │   │   │   └── ExportPage.module.css
│   │   │   └── shared/
│   │   │       ├── Button.jsx
│   │   │       ├── Badge.jsx
│   │   │       ├── DataTable.jsx
│   │   │       ├── InsightBox.jsx
│   │   │       └── shared.module.css
│   │   └── data/
│   │       └── navigation.js    # Day metadata (week, title, etc.)
│   └── content/
│       ├── day1.mdx  …  day30.mdx
│       └── index.js             # Re-exports all MDX pages for lazy loading
├── docs/
│   └── superpowers/
│       ├── specs/
│       └── plans/
```

---

### Phase 1: Backend (FastAPI)

#### Task 1: Backend project scaffold + models

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/models.py`
- Create: `backend/sandbox.py`

**Step 1: Create `backend/requirements.txt`**

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic==2.9.0
```

**Step 2: Create `backend/models.py`**

```python
from pydantic import BaseModel

class RunRequest(BaseModel):
    code: str
    lang: str

class TestResult(BaseModel):
    name: str
    passed: bool
    expected: str
    actual: str

class RunResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    timing_ms: int
    tests: list[TestResult] | None = None

class LanguageInfo(BaseModel):
    lang: str
    available: bool
    version: str | None = None
```

**Step 3: Create `backend/sandbox.py`**

```python
import os
import tempfile
import subprocess
import shutil
import time
import signal

class Sandbox:
    def __init__(self, timeout=30, max_output=1048576):
        self.timeout = timeout
        self.max_output = max_output

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="dsa_")
        return self.temp_dir

    def __exit__(self, *args):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run(self, cmd, cwd, input_data=None):
        start = time.time()
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
        )
        try:
            stdout, stderr = proc.communicate(input=input_data, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            return {
                "stdout": stdout[:self.max_output],
                "stderr": stderr[:self.max_output] + "\n[TIMEOUT: Process killed after 30s]",
                "exit_code": -1,
                "timing_ms": int((time.time() - start) * 1000),
            }
        elapsed = int((time.time() - start) * 1000)
        return {
            "stdout": stdout[:self.max_output],
            "stderr": stderr[:self.max_output],
            "exit_code": proc.returncode,
            "timing_ms": elapsed,
        }
```

**Step 4: Verify files exist**

Run: `python -c "import fastapi; print('OK')"`
Expected: `OK`

**Step 5: Commit**

```bash
git add backend/requirements.txt backend/models.py backend/sandbox.py
git commit -m "feat(backend): add project scaffold, models, and sandbox"
```

---

#### Task 2: Base runner + Python runner

**Files:**
- Create: `backend/runners/__init__.py`
- Create: `backend/runners/base.py`
- Create: `backend/runners/python_runner.py`

**Step 1: Create `backend/runners/__init__.py`**

```python
from .python_runner import PythonRunner
from .rust_runner import RustRunner
from .js_runner import JsRunner
from .other_runners import JavaRunner, CRunner, GoRunner

RUNNERS = {
    "python": PythonRunner,
    "rust": RustRunner,
    "javascript": JsRunner,
    "java": JavaRunner,
    "c": CRunner,
    "go": GoRunner,
}
```

**Step 2: Create `backend/runners/base.py`**

```python
from abc import ABC, abstractmethod
from ..sandbox import Sandbox
from ..models import RunResponse, TestResult

class BaseRunner(ABC):
    def __init__(self):
        self.sandbox = Sandbox()

    @abstractmethod
    def execute(self, code: str) -> RunResponse:
        ...

    def detect(self) -> bool:
        return False

    @staticmethod
    def parse_tests(output: str) -> list[TestResult]:
        return []

    def _make_response(self, result: dict, tests: list[TestResult] | None = None) -> RunResponse:
        return RunResponse(
            stdout=result["stdout"],
            stderr=result["stderr"],
            exit_code=result["exit_code"],
            timing_ms=result["timing_ms"],
            tests=tests or [],
        )
```

**Step 3: Create `backend/runners/python_runner.py`**

```python
import shutil
import re
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import TestResult

class PythonRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/script.py"
            with open(filepath, "w") as f:
                f.write(code)
            result = self.sandbox.run(["python", filepath], tmpdir)
            tests = self.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("python") is not None

    @staticmethod
    def parse_tests(output: str) -> list[TestResult]:
        tests = []
        for line in output.split("\n"):
            m = re.match(r"(✅|❌|PASS|FAIL)\s*(.*)", line)
            if m:
                status = m.group(1) in ("✅", "PASS")
                tests.append(TestResult(
                    name=m.group(2).strip(),
                    passed=status,
                    expected="",
                    actual="",
                ))
        return tests
```

**Step 4: Create `backend/runners/rust_runner.py`**

```python
import shutil
import os
import re
from .base import BaseRunner
from ..sandbox import Sandbox
from ..models import TestResult

class RustRunner(BaseRunner):
    TEMPLATE = """fn main() {{
    {}
}}"""

    def execute(self, code: str) -> RunResponse:
        wrapped = self.TEMPLATE.format(code) if "fn main" not in code else code
        with Sandbox() as tmpdir:
            src_dir = f"{tmpdir}/src"
            os.makedirs(src_dir, exist_ok=True)
            with open(f"{src_dir}/main.rs", "w") as f:
                f.write(wrapped)
            with open(f"{tmpdir}/Cargo.toml", "w") as f:
                f.write('[package]\nname = "temp"\nversion = "0.1.0"\nedition = "2021"\n')
            result = self.sandbox.run(["cargo", "run", "-q"], tmpdir)
            tests = self.parse_tests(result["stdout"])
            return self._make_response(result, tests)

    def detect(self) -> bool:
        return shutil.which("rustc") is not None

    @staticmethod
    def parse_tests(output: str) -> list[TestResult]:
        tests = []
        for line in output.split("\n"):
            m = re.match(r"(✅|❌|PASS|FAIL)\s*(.*)", line)
            if m:
                status = m.group(1) in ("✅", "PASS")
                tests.append(TestResult(
                    name=m.group(2).strip(),
                    passed=status,
                    expected="",
                    actual="",
                ))
        return tests
```

**Step 5: Verify both runners work**

Run: `python -c "from backend.runners.python_runner import PythonRunner; r=PythonRunner(); print(r.detect())"`
Expected: `True`

**Step 6: Commit**

```bash
git add backend/runners/
git commit -m "feat(backend): add base runner, python runner, and rust runner"
```

---

#### Task 3: JS, Java, C, Go runners

**Files:**
- Create: `backend/runners/js_runner.py`
- Create: `backend/runners/other_runners.py`

**Step 1: Create `backend/runners/js_runner.py`**

```python
import shutil
from .base import BaseRunner
from ..sandbox import Sandbox

class JsRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/script.js"
            with open(filepath, "w") as f:
                f.write(code)
            result = self.sandbox.run(["node", filepath], tmpdir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("node") is not None
```

**Step 2: Create `backend/runners/other_runners.py`**

```python
import shutil
import os
from .base import BaseRunner
from ..sandbox import Sandbox

class JavaRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        class_name = "Main"
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/{class_name}.java"
            with open(filepath, "w") as f:
                f.write(code)
            build = self.sandbox.run(["javac", filepath], tmpdir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = self.sandbox.run(["java", "-cp", tmpdir, class_name], tmpdir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("javac") is not None


class CRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/program.c"
            binary = f"{tmpdir}/program"
            with open(filepath, "w") as f:
                f.write(code)
            build = self.sandbox.run(["gcc", filepath, "-o", binary], tmpdir)
            if build["exit_code"] != 0:
                return self._make_response(build)
            result = self.sandbox.run([binary], tmpdir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("gcc") is not None


class GoRunner(BaseRunner):
    def execute(self, code: str) -> RunResponse:
        with Sandbox() as tmpdir:
            filepath = f"{tmpdir}/main.go"
            with open(filepath, "w") as f:
                f.write(code)
            result = self.sandbox.run(["go", "run", filepath], tmpdir)
            return self._make_response(result)

    def detect(self) -> bool:
        return shutil.which("go") is not None
```

**Step 3: Check imports compile**

Run: `python -c "from backend.runners import RUNNERS; print(list(RUNNERS.keys()))"`
Expected: `['python', 'rust', 'javascript', 'java', 'c', 'go']`

**Step 4: Commit**

```bash
git add backend/runners/js_runner.py backend/runners/other_runners.py
git commit -m "feat(backend): add JS, Java, C, and Go runners"
```

---

#### Task 4: FastAPI main app + language detection

**Files:**
- Create: `backend/main.py`
- Create: `backend/start.bat`

**Step 1: Create `backend/main.py`**

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .runners import RUNNERS
from .models import RunRequest, RunResponse, LanguageInfo

app = FastAPI(title="DSA Code Runner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:5173", "http://127.0.0.1:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/languages")
def get_languages() -> list[LanguageInfo]:
    result = []
    for lang, runner_cls in RUNNERS.items():
        runner = runner_cls()
        result.append(LanguageInfo(
            lang=lang,
            available=runner.detect(),
            version=None,
        ))
    return result

@app.post("/api/run", response_model=RunResponse)
def run_code(req: RunRequest):
    lang = req.lang.lower()
    if lang not in RUNNERS:
        raise HTTPException(400, f"Unsupported language: {lang}. Supported: {list(RUNNERS.keys())}")
    runner = RUNNERS[lang]()
    if not runner.detect():
        raise HTTPException(400, f"Runtime not found for {lang}. Install the toolchain and try again.")
    try:
        return runner.execute(req.code)
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
```

**Step 2: Create `backend/start.bat`**

```batch
@echo off
echo Starting DSA Code Runner backend...
cd /d "%~dp0"
uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
```

**Step 3: Test backend starts**

Run: `cd backend && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 &`
Expected: Server starts on port 8001. Kill the process after confirming.

**Step 4: Commit**

```bash
git add backend/main.py backend/start.bat
git commit -m "feat(backend): add FastAPI main app with CORS and language detection"
```

---

### Phase 2: Frontend Foundation (React SPA)

#### Task 5: React scaffold + Vite config + dependencies

**Files:**
- Modify: `web/package.json`
- Modify: `web/vite.config.js`
- Create: `web/index.html` (overwrite existing)
- Create: `web/src/main.jsx`
- Create: `web/src/App.jsx`
- Create: `web/src/router.jsx`
- Create: `web/src/data/navigation.js`

**Step 1: Update `web/package.json`**

```json
{
  "name": "dsa-study-plan-spa",
  "version": "3.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --port 8080",
    "start": "concurrently \"cd ../backend && uvicorn backend.main:app --host 127.0.0.1 --port 8001\" \"vite --port 5173 --open\""
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^7.0.0",
    "@codemirror/lang-python": "^6.1.0",
    "@codemirror/lang-javascript": "^6.2.0",
    "@codemirror/lang-rust": "^6.0.0",
    "@codemirror/lang-java": "^6.0.0",
    "@codemirror/lang-cpp": "^6.0.0",
    "@codemirror/lang-json": "^6.0.0",
    "codemirror": "^6.0.0",
    "@codemirror/view": "^6.0.0",
    "@codemirror/state": "^6.0.0",
    "@codemirror/basic-setup": "^0.20.0",
    "@codemirror/theme-one-dark": "^6.1.0",
    "@codemirror/language": "^6.0.0",
    "@codemirror/commands": "^6.0.0",
    "@mdx-js/rollup": "^3.0.0",
    "react-markdown": "^9.0.0",
    "remark-gfm": "^4.0.0"
  },
  "devDependencies": {
    "vite": "^6.4.1",
    "@vitejs/plugin-react": "^4.3.0",
    "concurrently": "^9.0.0"
  }
}
```

**Step 2: Update `web/vite.config.js`**

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import mdx from '@mdx-js/rollup';
import { resolve } from 'path';

export default defineConfig({
  root: 'web',
  plugins: [
    react(),
    mdx(),
  ],
  server: {
    port: 5173,
    open: true,
    hot: true,
    host: true,
  },
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'web/src'),
    },
  },
});
```

**Step 3: Create `web/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>30-Day DSA Study Plan</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

**Step 4: Create `web/src/main.jsx`**

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Step 5: Create `web/src/router.jsx`**

```jsx
import { createBrowserRouter, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import HomePage from './components/HomePage/HomePage';
import DayPage from './components/DayPage/DayPage';
import ExportPage from './components/ExportPage/ExportPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'day/:dayId', element: <DayPage /> },
      { path: 'export', element: <ExportPage /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
]);

export default router;
```

**Step 6: Create `web/src/App.jsx`**

```jsx
import { RouterProvider } from 'react-router-dom';
import router from './router';

export default function App() {
  return <RouterProvider router={router} />;
}
```

**Step 7: Create `web/src/data/navigation.js`**

```javascript
export const studyDays = [
  { day: 1, title: 'Arrays & Hashing', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 2, title: 'Advanced Arrays', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 3, title: 'String Manipulation', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 4, title: 'Stack & Queue', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 5, title: 'Linked List', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 6, title: 'Trees', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 7, title: 'Review & Practice', week: 1, weekTitle: 'Week 1 — Foundations' },
  { day: 8, title: 'Graphs', week: 2, weekTitle: 'Week 2 — Advanced Structures' },
  { day: 9, title: 'Advanced Graphs', week: 2, weekTitle: 'Week 2 — Advanced Structures' },
  { day: 10, title: 'Review & Practice', week: 2, weekTitle: 'Week 2 — Advanced Structures' },
  { day: 11, title: 'DP Fundamentals', week: 3, weekTitle: 'Week 3 — Dynamic Programming' },
  { day: 12, title: 'Advanced DP', week: 3, weekTitle: 'Week 3 — Dynamic Programming' },
  { day: 13, title: 'More Advanced DP', week: 3, weekTitle: 'Week 3 — Dynamic Programming' },
  { day: 14, title: 'DP Review', week: 3, weekTitle: 'Week 3 — Dynamic Programming' },
  { day: 15, title: 'Heaps & Tries', week: 4, weekTitle: 'Week 4 — Advanced Topics' },
  { day: 16, title: 'Binary Search', week: 4, weekTitle: 'Week 4 — Advanced Topics' },
  { day: 17, title: 'Search Review', week: 4, weekTitle: 'Week 4 — Advanced Topics' },
  { day: 18, title: 'Segment Trees', week: 4, weekTitle: 'Week 4 — Advanced Topics' },
  { day: 19, title: 'Advanced Data Structures', week: 4, weekTitle: 'Week 4 — Advanced Topics' },
  { day: 20, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 21, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 22, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 23, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 24, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 25, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 26, title: 'TBD', week: 5, weekTitle: 'Week 5 — Advanced Algorithms' },
  { day: 27, title: 'TBD', week: 6, weekTitle: 'Week 6 — Wrap Up' },
  { day: 28, title: 'TBD', week: 6, weekTitle: 'Week 6 — Wrap Up' },
  { day: 29, title: 'TBD', week: 6, weekTitle: 'Week 6 — Wrap Up' },
  { day: 30, title: 'Final Review', week: 6, weekTitle: 'Week 6 — Wrap Up' },
];
```

**Step 8: Install dependencies**

Run: `cd web && npm install`
Expected: All packages install without errors

**Step 9: Commit**

```bash
git add web/package.json web/vite.config.js web/index.html web/src/main.jsx web/src/App.jsx web/src/router.jsx web/src/data/navigation.js
git commit -m "feat(frontend): add React scaffold with Vite, Router, and navigation data"
```

---

#### Task 6: Design tokens + global styles

**Files:**
- Create: `web/src/styles/tokens.css`
- Create: `web/src/styles/global.css`

**Step 1: Create `web/src/styles/tokens.css`**

```css
:root {
  /* Colors */
  --color-primary: #2c3e50;
  --color-primary-light: #34495e;
  --color-accent: #3498db;
  --color-accent-hover: #2980b9;
  --color-success: #27ae60;
  --color-warning: #f39c12;
  --color-danger: #e74c3c;
  --color-text: #2c3e50;
  --color-text-secondary: #7f8c8d;
  --color-bg: #f8f9fa;
  --color-bg-card: #ffffff;
  --color-border: #dee2e6;
  --color-sidebar-bg: #1a252f;
  --color-sidebar-text: #ecf0f1;
  --color-code-bg: #1e1e1e;
  --color-code-text: #d4d4d4;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Typography */
  --font-sans: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --font-size-3xl: 2.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);

  /* Radii */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}

[data-theme="dark"] {
  --color-bg: #1a1a2e;
  --color-bg-card: #16213e;
  --color-text: #e0e0e0;
  --color-text-secondary: #a0a0a0;
  --color-border: #2a2a4a;
  --color-sidebar-bg: #0f0f23;
  --color-code-bg: #0d0d1a;
}
```

**Step 2: Create `web/src/styles/global.css`**

```css
@import './tokens.css';

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-sans);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.7;
  min-height: 100vh;
}

a {
  color: var(--color-accent);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}

code, pre {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

h1, h2, h3, h4, h5, h6 {
  line-height: 1.3;
  color: var(--color-primary);
}

h1 { font-size: var(--font-size-3xl); }
h2 { font-size: var(--font-size-2xl); }
h3 { font-size: var(--font-size-xl); }

p { margin-bottom: var(--space-md); }

ul, ol {
  padding-left: var(--space-lg);
  margin-bottom: var(--space-md);
}

li { margin-bottom: var(--space-xs); }
```

**Step 3: Commit**

```bash
git add web/src/styles/
git commit -m "feat(frontend): add design tokens and global styles with dark theme"
```

---

#### Task 7: Layout + Sidebar components

**Files:**
- Create: `web/src/components/Layout/Layout.jsx`
- Create: `web/src/components/Layout/Layout.module.css`
- Create: `web/src/components/Sidebar/Sidebar.jsx`
- Create: `web/src/components/Sidebar/WeekGroup.jsx`
- Create: `web/src/components/Sidebar/DayLink.jsx`
- Create: `web/src/components/Sidebar/Sidebar.module.css`

**Step 1: Create `web/src/components/Layout/Layout.module.css`**

```css
.layout {
  display: flex;
  min-height: 100vh;
}

.main {
  flex: 1;
  margin-left: 280px;
  padding: var(--space-xl) var(--space-2xl);
  max-width: 1100px;
}

@media (max-width: 768px) {
  .main {
    margin-left: 0;
    padding: var(--space-md);
  }
}
```

**Step 2: Create `web/src/components/Layout/Layout.jsx`**

```jsx
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import TopBar from '../TopBar/TopBar';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import styles from './Layout.module.css';

export default function Layout() {
  return (
    <ThemeProvider>
      <ProgressProvider>
        <div className={styles.layout}>
          <Sidebar />
          <div className={styles.main}>
            <TopBar />
            <Outlet />
          </div>
        </div>
      </ProgressProvider>
    </ThemeProvider>
  );
}
```

**Step 3: Create `web/src/components/Sidebar/Sidebar.module.css`**

```css
.sidebar {
  width: 280px;
  background: var(--color-sidebar-bg);
  color: var(--color-sidebar-text);
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.header {
  padding: var(--space-lg);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.header h1 {
  font-size: var(--font-size-lg);
  color: inherit;
  margin-bottom: var(--space-xs);
}

.header p {
  font-size: var(--font-size-sm);
  opacity: 0.7;
  margin: 0;
}

.progressSummary {
  padding: var(--space-md) var(--space-lg);
  font-size: var(--font-size-sm);
  opacity: 0.8;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.nav {
  padding: var(--space-sm) 0;
}

.weekTitle {
  padding: var(--space-md) var(--space-lg) var(--space-xs);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.5;
  font-weight: 600;
}

.dayList {
  list-style: none;
  padding: 0;
  margin: 0;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  .sidebar.open {
    transform: translateX(0);
  }
}
```

**Step 4: Create `web/src/components/Sidebar/DayLink.jsx`**

```jsx
import { NavLink } from 'react-router-dom';

const statusIcon = {
  completed: '✓',
  current: '●',
  upcoming: '→',
};

export default function DayLink({ day, title, isComplete, isCurrent, dayNumber }) {
  const status = isComplete ? 'completed' : isCurrent ? 'current' : 'upcoming';

  return (
    <li style={{ margin: '2px 0' }}>
      <NavLink
        to={`/day/${day}`}
        style={({ isActive }) => ({
          display: 'flex',
          alignItems: 'center',
          padding: '10px 20px',
          color: 'var(--color-sidebar-text)',
          textDecoration: 'none',
          borderLeft: '3px solid transparent',
          background: isActive ? 'rgba(52,152,219,0.2)' : 'transparent',
          borderLeftColor: isActive ? 'var(--color-accent)' : 'transparent',
        })}
      >
        <span style={{
          width: 28, height: 28, borderRadius: '50%',
          background: isComplete ? 'var(--color-success)' : isCurrent ? 'var(--color-accent)' : 'rgba(255,255,255,0.1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '0.75rem', fontWeight: 600, marginRight: 12, flexShrink: 0,
        }}>
          {day}
        </span>
        <span style={{ flex: 1, fontSize: '0.9rem' }}>{title}</span>
        <span style={{ fontSize: '0.9rem', opacity: isComplete ? 1 : 0.5 }}>
          {statusIcon[status]}
        </span>
      </NavLink>
    </li>
  );
}
```

**Step 5: Create `web/src/components/Sidebar/WeekGroup.jsx`**

```jsx
import DayLink from './DayLink';
import styles from './Sidebar.module.css';

export default function WeekGroup({ weekTitle, days, completedDays, currentDay }) {
  return (
    <nav className={styles.nav}>
      <div className={styles.weekTitle}>{weekTitle}</div>
      <ul className={styles.dayList}>
        {days.map(d => (
          <DayLink
            key={d.day}
            day={d.day}
            dayNumber={d.day}
            title={d.title}
            isComplete={completedDays.includes(d.day)}
            isCurrent={d.day === currentDay}
          />
        ))}
      </ul>
    </nav>
  );
}
```

**Step 6: Create `web/src/components/Sidebar/Sidebar.jsx`**

```jsx
import { Link, useParams } from 'react-router-dom';
import { useProgress } from '../../hooks/useProgress';
import { studyDays } from '../../data/navigation';
import WeekGroup from './WeekGroup';
import styles from './Sidebar.module.css';

function groupByWeek(days) {
  const weeks = {};
  days.forEach(d => {
    if (!weeks[d.week]) weeks[d.week] = { title: d.weekTitle, days: [] };
    weeks[d.week].days.push(d);
  });
  return Object.entries(weeks).sort(([a], [b]) => Number(a) - Number(b));
}

export default function Sidebar() {
  const { progress, currentDay } = useProgress();
  const weeks = groupByWeek(studyDays);
  const total = studyDays.length;
  const done = progress.completedDays.length;
  const pct = Math.round((done / total) * 100);

  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
          <h1>DSA Study Plan</h1>
          <p>30 Days to Mastery</p>
        </Link>
      </div>
      <div className={styles.progressSummary}>
        {done}/{total} days completed ({pct}%)
      </div>
      {weeks.map(([week, w]) => (
        <WeekGroup
          key={week}
          weekTitle={w.title}
          days={w.days}
          completedDays={progress.completedDays}
          currentDay={currentDay}
        />
      ))}
    </aside>
  );
}
```

**Step 7: Commit**

```bash
git add web/src/components/Layout/ web/src/components/Sidebar/
git commit -m "feat(frontend): add Layout, Sidebar, WeekGroup, and DayLink components"
```

---

#### Task 8: Context providers (Theme + Progress)

**Files:**
- Create: `web/src/context/ThemeContext.jsx`
- Create: `web/src/context/ProgressContext.jsx`
- Create: `web/src/hooks/useProgress.js`

**Step 1: Create `web/src/context/ThemeContext.jsx`**

```jsx
import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export function useTheme() {
  return useContext(ThemeContext);
}

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('dsaTheme') || 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('dsaTheme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => (t === 'light' ? 'dark' : 'light'));

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

**Step 2: Create `web/src/hooks/useProgress.js`**

```javascript
import { useContext } from 'react';
import { ProgressContext } from '../context/ProgressContext';

export function useProgress() {
  const ctx = useContext(ProgressContext);
  if (!ctx) throw new Error('useProgress must be used within ProgressProvider');
  return ctx;
}
```

**Step 3: Create `web/src/context/ProgressContext.jsx`**

```jsx
import { createContext, useState, useCallback, useEffect } from 'react';

const STORAGE_KEY = 'dsaProgress';

function loadProgress() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return JSON.parse(stored);
  } catch {}
  return { completedDays: [], startedAt: new Date().toISOString() };
}

function getCurrentDayFromPath() {
  const m = window.location.pathname.match(/\/day\/(\d+)/);
  return m ? Number(m[1]) : 0;
}

export const ProgressContext = createContext(null);

export function ProgressProvider({ children }) {
  const [progress, setProgress] = useState(loadProgress);
  const [currentDay, setCurrentDay] = useState(getCurrentDayFromPath);

  useEffect(() => {
    const handleLocationChange = () => setCurrentDay(getCurrentDayFromPath());
    window.addEventListener('popstate', handleLocationChange);
    return () => window.removeEventListener('popstate', handleLocationChange);
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const markComplete = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.includes(day) ? p.completedDays : [...p.completedDays, day].sort((a, b) => a - b),
    }));
  }, []);

  const markIncomplete = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.filter(d => d !== day),
    }));
  }, []);

  const resetDay = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.filter(d => d !== day),
    }));
  }, []);

  const resetAll = useCallback(() => {
    setProgress({ completedDays: [], startedAt: new Date().toISOString() });
  }, []);

  const exportProgress = useCallback(() => {
    return {
      ...progress,
      exportDate: new Date().toISOString(),
      totalDays: 30,
    };
  }, [progress]);

  return (
    <ProgressContext.Provider value={{
      progress, currentDay,
      markComplete, markIncomplete, resetDay, resetAll, exportProgress,
    }}>
      {children}
    </ProgressContext.Provider>
  );
}
```

**Step 4: Commit**

```bash
git add web/src/context/ web/src/hooks/
git commit -m "feat(frontend): add ThemeContext, ProgressContext, and useProgress hook"
```

---

#### Task 9: HomePage (dashboard)

**Files:**
- Create: `web/src/components/HomePage/HomePage.jsx`
- Create: `web/src/components/HomePage/StatsRow.jsx`
- Create: `web/src/components/HomePage/CalendarGrid.jsx`
- Create: `web/src/components/HomePage/HomePage.module.css`

**Step 1: Create `web/src/components/HomePage/HomePage.module.css`**

```css
.page {
  padding-top: var(--space-md);
}

.title {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--space-sm);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
  margin-bottom: var(--space-lg);
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.statCard {
  background: var(--color-bg-card);
  padding: var(--space-lg);
  border-radius: var(--radius-md);
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.statNumber {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-accent);
}

.statLabel {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: var(--space-xs);
}

.calendar {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--space-sm);
  margin-bottom: var(--space-xl);
}

.day {
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  padding: var(--space-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  text-decoration: none;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.day:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.completed {
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  color: white;
}

.current {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 0 0 3px var(--color-bg-card), 0 0 0 6px var(--color-accent);
}

.upcoming {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.dayNumber {
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.dayTopic {
  font-size: 0.6rem;
  opacity: 0.8;
  margin-top: 2px;
}

.dayStatus {
  font-size: var(--font-size-sm);
  position: absolute;
  top: 2px;
  right: 4px;
}

@media (max-width: 768px) {
  .stats { grid-template-columns: repeat(2, 1fr); }
  .calendar { grid-template-columns: repeat(3, 1fr); }
}
```

**Step 2: Create `web/src/components/HomePage/CalendarGrid.jsx`**

```jsx
import { Link } from 'react-router-dom';
import { studyDays } from '../../data/navigation';
import styles from './HomePage.module.css';

export default function CalendarGrid({ completedDays, currentDay }) {
  return (
    <div className={styles.calendar}>
      {studyDays.map(d => {
        const isComplete = completedDays.includes(d.day);
        const isCurrent = d.day === currentDay;
        const statusClass = isComplete ? styles.completed : isCurrent ? styles.current : styles.upcoming;
        return (
          <Link
            key={d.day}
            to={`/day/${d.day}`}
            className={`${styles.day} ${statusClass}`}
            style={{ position: 'relative' }}
          >
            <span className={styles.dayStatus}>
              {isComplete ? '✓' : isCurrent ? '▶' : ''}
            </span>
            <span className={styles.dayNumber}>{d.day}</span>
            <span className={styles.dayTopic}>{d.title}</span>
          </Link>
        );
      })}
    </div>
  );
}
```

**Step 3: Create `web/src/components/HomePage/StatsRow.jsx`**

```jsx
import styles from './HomePage.module.css';

export default function StatsRow({ completed, total }) {
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  return (
    <div className={styles.stats}>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{completed}</div>
        <div className={styles.statLabel}>Completed</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{total - completed}</div>
        <div className={styles.statLabel}>Remaining</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{pct}%</div>
        <div className={styles.statLabel}>Progress</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>170+</div>
        <div className={styles.statLabel}>Problems</div>
      </div>
    </div>
  );
}
```

**Step 4: Create `web/src/components/HomePage/HomePage.jsx`**

```jsx
import { Link } from 'react-router-dom';
import { useProgress } from '../../hooks/useProgress';
import StatsRow from './StatsRow';
import CalendarGrid from './CalendarGrid';
import styles from './HomePage.module.css';

export default function HomePage() {
  const { progress, currentDay } = useProgress();
  const completed = progress.completedDays.length;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>30-Day DSA Study Plan</h1>
      <p className={styles.subtitle}>Your journey to mastering Data Structures & Algorithms</p>

      <StatsRow completed={completed} total={30} />

      <h2>Calendar</h2>
      <p style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text-secondary)' }}>
        Click any day to start learning.
      </p>

      <CalendarGrid completedDays={progress.completedDays} currentDay={currentDay} />

      <div style={{ marginTop: 'var(--space-xl)', textAlign: 'center' }}>
        <Link
          to="/export"
          style={{
            display: 'inline-block',
            padding: 'var(--space-sm) var(--space-lg)',
            background: 'var(--color-accent)',
            color: 'white',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
          }}
        >
          Export Progress Report
        </Link>
      </div>
    </div>
  );
}
```

**Step 5: Commit**

```bash
git add web/src/components/HomePage/
git commit -m "feat(frontend): add HomePage with stats and calendar grid"
```

---

#### Task 10: TopBar component (search + theme toggle)

**Files:**
- Create: `web/src/components/TopBar/TopBar.jsx`
- Create: `web/src/components/TopBar/TopBar.module.css`

**Step 1: Create `web/src/components/TopBar/TopBar.module.css`**

```css
.bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-md);
  padding: var(--space-sm) 0 var(--space-lg);
  margin-bottom: var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.search {
  flex: 1;
  max-width: 300px;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  background: var(--color-bg-card);
  color: var(--color-text);
}

.search:focus {
  outline: none;
  border-color: var(--color-accent);
}

.themeBtn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  transition: background 0.2s;
}

.themeBtn:hover {
  background: var(--color-bg-card);
}
```

**Step 2: Create `web/src/components/TopBar/TopBar.jsx`**

```jsx
import { useTheme } from '../../context/ThemeContext';
import styles from './TopBar.module.css';

export default function TopBar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={styles.bar}>
      <input
        type="search"
        placeholder="Search days..."
        className={styles.search}
      />
      <button className={styles.themeBtn} onClick={toggleTheme}>
        {theme === 'light' ? '🌙 Dark' : '☀️ Light'}
      </button>
    </div>
  );
}
```

**Step 3: Commit**

```bash
git add web/src/components/TopBar/
git commit -m "feat(frontend): add TopBar with search and theme toggle"
```

---

### Phase 3: Interactive Components

#### Task 11: CodePlayground — the core interactive feature

**Files:**
- Create: `web/src/components/CodePlayground/CodePlayground.jsx`
- Create: `web/src/components/CodePlayground/OutputPanel.jsx`
- Create: `web/src/components/CodePlayground/CodePlayground.module.css`
- Create: `web/src/hooks/useCodeRunner.js`

**Step 1: Create `web/src/hooks/useCodeRunner.js`**

```javascript
import { useState, useCallback } from 'react';

const API_BASE = 'http://127.0.0.1:8001';

export function useCodeRunner() {
  const [state, setState] = useState({ running: false, output: null, error: null });

  const run = useCallback(async (code, lang) => {
    setState({ running: true, output: null, error: null });
    try {
      const res = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, lang }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Execution failed');
      }
      const data = await res.json();
      setState({ running: false, output: data, error: null });
    } catch (e) {
      setState({ running: false, output: null, error: e.message });
    }
  }, []);

  return { ...state, run };
}
```

**Step 2: Create `web/src/components/CodePlayground/CodePlayground.module.css`**

```css
.wrapper {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin: var(--space-lg) 0;
  background: var(--color-bg-card);
}

.toolbar {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--color-code-bg);
  border-bottom: 1px solid var(--color-border);
}

.langSelect {
  background: rgba(255,255,255,0.1);
  color: var(--color-code-text);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-sm);
  padding: 4px 8px;
  font-size: var(--font-size-sm);
  font-family: var(--font-mono);
}

.runBtn {
  background: var(--color-success);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  padding: 4px 16px;
  font-size: var(--font-size-sm);
  font-weight: 600;
  cursor: pointer;
}

.runBtn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.runBtn:hover:not(:disabled) {
  opacity: 0.9;
}

.resetBtn {
  background: rgba(255,255,255,0.1);
  color: var(--color-code-text);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-sm);
  padding: 4px 12px;
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.editor {
  min-height: 200px;
}

.output {
  padding: var(--space-md);
  background: #0d0d1a;
  color: #d4d4d4;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  line-height: 1.5;
  max-height: 300px;
  overflow-y: auto;
  border-top: 1px solid var(--color-border);
  white-space: pre-wrap;
}

.output .success {
  color: var(--color-success);
}

.output .error {
  color: var(--color-danger);
}

.timing {
  font-size: var(--font-size-xs);
  opacity: 0.6;
  margin-top: var(--space-sm);
}

.testResult {
  margin: 2px 0;
}
```

**Step 3: Create `web/src/components/CodePlayground/OutputPanel.jsx`**

```jsx
import styles from './CodePlayground.module.css';

export default function OutputPanel({ output, error, running }) {
  if (running) {
    return <div className={styles.output}>Running...</div>;
  }

  if (error) {
    return <div className={styles.output}><span className={styles.error}>Error: {error}</span></div>;
  }

  if (!output) return null;

  return (
    <div className={styles.output}>
      {output.stdout && <div>{output.stdout}</div>}
      {output.stderr && <div className={styles.error}>{output.stderr}</div>}
      {output.tests && output.tests.map((t, i) => (
        <div key={i} className={`${styles.testResult} ${t.passed ? styles.success : styles.error}`}>
          {t.passed ? '✅' : '❌'} {t.name}
        </div>
      ))}
      <div className={styles.timing}>{output.timing_ms}ms</div>
    </div>
  );
}
```

**Step 4: Create `web/src/components/CodePlayground/CodePlayground.jsx`**

```jsx
import { useState, useEffect, useRef } from 'react';
import { EditorView, basicSetup } from 'codemirror';
import { EditorState } from '@codemirror/state';
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import { rust } from '@codemirror/lang-rust';
import { java } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import { oneDark } from '@codemirror/theme-one-dark';
import { useCodeRunner } from '../../hooks/useCodeRunner';
import { useTheme } from '../../context/ThemeContext';
import OutputPanel from './OutputPanel';
import styles from './CodePlayground.module.css';

const LANG_MODES = {
  python, javascript, js: javascript,
  rust, java, c: cpp, cpp, go: javascript,
};

const LANG_OPTIONS = [
  { value: 'python', label: 'Python' },
  { value: 'rust', label: 'Rust' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
  { value: 'c', label: 'C' },
  { value: 'go', label: 'Go' },
];

export default function CodePlayground({ initialCode = '', language = 'python' }) {
  const editorRef = useRef(null);
  const viewRef = useRef(null);
  const [code, setCode] = useState(initialCode);
  const [lang, setLang] = useState(language);
  const [resetCode] = useState(initialCode);
  const { running, output, error, run } = useCodeRunner();
  const { theme } = useTheme();

  useEffect(() => {
    if (!editorRef.current) return;
    if (viewRef.current) viewRef.current.destroy();

    const langMode = LANG_MODES[lang] || python;
    const extensions = [basicSetup, langMode()];
    if (theme === 'dark') extensions.push(oneDark);

    const state = EditorState.create({
      doc: code,
      extensions,
    });

    viewRef.current = new EditorView({
      state,
      parent: editorRef.current,
      dispatch: (tr) => {
        viewRef.current.update([tr]);
        if (tr.docChanged) setCode(viewRef.current.state.doc.toString());
      },
    });

    return () => viewRef.current?.destroy();
  }, [lang, theme]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.toolbar}>
        <select
          className={styles.langSelect}
          value={lang}
          onChange={e => setLang(e.target.value)}
        >
          {LANG_OPTIONS.map(o => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <button className={styles.runBtn} disabled={running} onClick={() => run(code, lang)}>
          {running ? 'Running...' : '▶ Run'}
        </button>
        <button className={styles.resetBtn} onClick={() => setCode(resetCode)}>
          ↺ Reset
        </button>
      </div>
      <div className={styles.editor} ref={editorRef} />
      <OutputPanel output={output} error={error} running={running} />
    </div>
  );
}
```

**Step 5: Commit**

```bash
git add web/src/hooks/useCodeRunner.js web/src/components/CodePlayground/
git commit -m "feat(frontend): add CodePlayground with CodeMirror 6 and code runner hook"
```

---

#### Task 12: ProblemCard + shared components

**Files:**
- Create: `web/src/components/ProblemCard/ProblemCard.jsx`
- Create: `web/src/components/ProblemCard/ProblemCard.module.css`
- Create: `web/src/components/shared/Button.jsx`
- Create: `web/src/components/shared/Badge.jsx`
- Create: `web/src/components/shared/DataTable.jsx`
- Create: `web/src/components/shared/InsightBox.jsx`
- Create: `web/src/components/shared/shared.module.css`

**Step 1: Create `web/src/components/ProblemCard/ProblemCard.module.css`**

```css
.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin: var(--space-lg) 0;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--color-accent);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-sm);
}

.header h4 {
  margin: 0;
}

.pattern {
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  font-weight: 500;
  margin-bottom: var(--space-sm);
}

.description {
  margin-bottom: var(--space-md);
}

.solution {
  background: var(--color-bg);
  padding: var(--space-md);
  border-radius: var(--radius-sm);
  margin-top: var(--space-md);
}

.solution summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--color-accent);
}

.solutionContent {
  margin-top: var(--space-sm);
}
```

**Step 2: Create `web/src/components/ProblemCard/ProblemCard.jsx`**

```jsx
import { useState } from 'react';
import Badge from '../shared/Badge';
import styles from './ProblemCard.module.css';

const DIFFICULTY_COLORS = {
  easy: { bg: '#d4edda', color: '#155724' },
  medium: { bg: '#fff3cd', color: '#856404' },
  hard: { bg: '#f8d7da', color: '#721c24' },
};

export default function ProblemCard({ title, difficulty = 'easy', pattern, children }) {
  const [showSolution, setShowSolution] = useState(false);

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h4>{title}</h4>
        <Badge
          label={difficulty}
          bg={DIFFICULTY_COLORS[difficulty]?.bg || '#e9ecef'}
          color={DIFFICULTY_COLORS[difficulty]?.color || '#495057'}
        />
      </div>
      {pattern && <div className={styles.pattern}>Pattern: {pattern}</div>}
      <div className={styles.description}>{children}</div>
      <details className={styles.solution} open={showSolution}>
        <summary onClick={e => { e.preventDefault(); setShowSolution(!showSolution); }}>
          {showSolution ? 'Hide Solution' : 'Show Solution'}
        </summary>
        <div className={styles.solutionContent} onClick={() => {}}>
          {/* Solution content rendered from MDX child */}
        </div>
      </details>
    </div>
  );
}
```

**Step 3: Create `web/src/components/shared/Badge.jsx`**

```jsx
export default function Badge({ label, bg = '#e9ecef', color = '#495057' }) {
  return (
    <span style={{
      fontSize: '0.75rem',
      padding: '3px 10px',
      borderRadius: '12px',
      textTransform: 'uppercase',
      fontWeight: 600,
      background: bg,
      color,
    }}>
      {label}
    </span>
  );
}
```

**Step 4: Create `web/src/components/shared/Button.jsx`**

```jsx
export default function Button({ children, variant = 'primary', onClick, disabled, style }) {
  const variants = {
    primary: { background: 'var(--color-accent)', color: 'white', borderColor: 'var(--color-accent)' },
    secondary: { background: 'transparent', color: 'var(--color-accent)', borderColor: 'var(--color-accent)' },
    success: { background: 'var(--color-success)', color: 'white', borderColor: 'var(--color-success)' },
    danger: { background: 'var(--color-danger)', color: 'white', borderColor: 'var(--color-danger)' },
  };

  const v = variants[variant] || variants.primary;

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        padding: '10px 20px',
        border: '2px solid',
        borderRadius: 'var(--radius-md)',
        fontWeight: 600,
        fontSize: '0.95rem',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        transition: 'all 0.2s',
        ...v,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
```

**Step 5: Create `web/src/components/shared/DataTable.jsx`**

```jsx
export default function DataTable({ headers, rows }) {
  return (
    <div style={{
      overflow: 'hidden',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      margin: 'var(--space-lg) 0',
    }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        background: 'var(--color-bg-card)',
      }}>
        <thead>
          <tr style={{ background: 'var(--color-primary)', color: 'white' }}>
            {headers.map((h, i) => (
              <th key={i} style={{
                padding: '12px 16px',
                textAlign: 'left',
                textTransform: 'uppercase',
                fontSize: '0.85rem',
                letterSpacing: '0.5px',
              }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{ borderBottom: i < rows.length - 1 ? '1px solid var(--color-border)' : 'none' }}>
              {row.map((cell, j) => (
                <td key={j} style={{ padding: '12px 16px' }}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Step 6: Create `web/src/components/shared/InsightBox.jsx`**

```jsx
export default function InsightBox({ title = 'Key Insights', children }) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: 'var(--space-lg)',
      borderRadius: 'var(--radius-md)',
      margin: 'var(--space-lg) 0',
    }}>
      {title && <h3 style={{ color: 'white', marginBottom: 'var(--space-md)' }}>{title}</h3>}
      {children}
    </div>
  );
}
```

**Step 7: Commit**

```bash
git add web/src/components/ProblemCard/ web/src/components/shared/
git commit -m "feat(frontend): add ProblemCard, Badge, Button, DataTable, and InsightBox"
```

---

#### Task 13: DayPage — MDX content rendering with navigation

**Files:**
- Create: `web/src/components/DayPage/DayPage.jsx`
- Create: `web/src/components/DayPage/DayPage.module.css`
- Create: `web/src/components/DayPage/DayNavigation.jsx`

**Step 1: Create `web/src/components/DayPage/DayPage.module.css`**

```css
.page {
  padding-top: var(--space-sm);
}

.header {
  margin-bottom: var(--space-xl);
  padding-bottom: var(--space-lg);
  border-bottom: 2px solid var(--color-border);
}

.header h1 {
  margin-bottom: var(--space-xs);
}

.meta {
  display: flex;
  gap: var(--space-md);
  margin-top: var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  align-items: center;
  flex-wrap: wrap;
}

.actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-md);
}

.nav {
  display: flex;
  gap: var(--space-md);
  margin-top: var(--space-xl);
  padding-top: var(--space-lg);
  border-top: 2px solid var(--color-border);
  flex-wrap: wrap;
}
```

**Step 2: Create `web/src/components/DayPage/DayNavigation.jsx`**

```jsx
import { Link } from 'react-router-dom';
import { studyDays } from '../../data/navigation';

export default function DayNavigation({ day }) {
  const prev = studyDays.find(d => d.day === day - 1);
  const next = studyDays.find(d => d.day === day + 1);

  return (
    <div style={{ display: 'flex', gap: 'var(--space-md)', marginTop: 'var(--space-xl)', paddingTop: 'var(--space-lg)', borderTop: '2px solid var(--color-border)', flexWrap: 'wrap' }}>
      {prev && (
        <Link
          to={`/day/${prev.day}`}
          style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '12px 20px', border: '2px solid var(--color-border)',
            borderRadius: 'var(--radius-md)', textDecoration: 'none',
            color: 'var(--color-text)', transition: 'all 0.2s',
          }}
        >
          <span>←</span>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', opacity: 0.7 }}>Previous</span>
            <span>Day {prev.day}: {prev.title}</span>
          </div>
        </Link>
      )}
      <Link
        to="/"
        style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '12px 20px', border: '2px solid var(--color-border)',
          borderRadius: 'var(--radius-md)', textDecoration: 'none',
          color: 'var(--color-text)',
        }}
      >
        🏠 Home
      </Link>
      {next && (
        <Link
          to={`/day/${next.day}`}
          style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '12px 20px', border: '2px solid var(--color-accent)',
            borderRadius: 'var(--radius-md)', textDecoration: 'none',
            color: 'var(--color-accent)', fontWeight: 600,
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', opacity: 0.7 }}>Next</span>
            <span>Day {next.day}: {next.title}</span>
          </div>
          <span>→</span>
        </Link>
      )}
    </div>
  );
}
```

**Step 3: Create `web/src/components/DayPage/DayPage.jsx`**

```jsx
import { useParams, Navigate } from 'react-router-dom';
import { useState, lazy, Suspense } from 'react';
import { studyDays } from '../../data/navigation';
import { useProgress } from '../../hooks/useProgress';
import Badge from '../shared/Badge';
import Button from '../shared/Button';
import DayNavigation from './DayNavigation';
import styles from './DayPage.module.css';

const DAYS = {
  1: lazy(() => import('../../content/day1.mdx')),
  2: lazy(() => import('../../content/day2.mdx')),
  3: lazy(() => import('../../content/day3.mdx')),
  4: lazy(() => import('../../content/day4.mdx')),
  5: lazy(() => import('../../content/day5.mdx')),
  6: lazy(() => import('../../content/day6.mdx')),
  7: lazy(() => import('../../content/day7.mdx')),
  8: lazy(() => import('../../content/day8.mdx')),
  9: lazy(() => import('../../content/day9.mdx')),
  10: lazy(() => import('../../content/day10.mdx')),
  11: lazy(() => import('../../content/day11.mdx')),
  12: lazy(() => import('../../content/day12.mdx')),
  13: lazy(() => import('../../content/day13.mdx')),
  14: lazy(() => import('../../content/day14.mdx')),
  15: lazy(() => import('../../content/day15.mdx')),
  16: lazy(() => import('../../content/day16.mdx')),
  17: lazy(() => import('../../content/day17.mdx')),
  18: lazy(() => import('../../content/day18.mdx')),
  19: lazy(() => import('../../content/day19.mdx')),
  20: lazy(() => import('../../content/day20.mdx')),
  21: lazy(() => import('../../content/day21.mdx')),
  22: lazy(() => import('../../content/day22.mdx')),
  23: lazy(() => import('../../content/day23.mdx')),
  24: lazy(() => import('../../content/day24.mdx')),
  25: lazy(() => import('../../content/day25.mdx')),
  26: lazy(() => import('../../content/day26.mdx')),
  27: lazy(() => import('../../content/day27.mdx')),
  28: lazy(() => import('../../content/day28.mdx')),
  29: lazy(() => import('../../content/day29.mdx')),
  30: lazy(() => import('../../content/day30.mdx')),
};

export default function DayPage() {
  const { dayId } = useParams();
  const day = Number(dayId);
  const { progress, markComplete, markIncomplete, resetDay } = useProgress();
  const [resetting, setResetting] = useState(false);

  if (isNaN(day) || day < 1 || day > 30) {
    return <Navigate to="/" replace />;
  }

  const dayInfo = studyDays.find(d => d.day === day);
  if (!dayInfo) return <Navigate to="/" replace />;

  const isComplete = progress.completedDays.includes(day);
  const MDXComponent = DAYS[day];

  const handleReset = () => {
    resetDay(day);
    setResetting(true);
    setTimeout(() => setResetting(false), 500);
  };

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1>Day {day}: {dayInfo.title}</h1>
        <div className={styles.meta}>
          <Badge
            label={isComplete ? 'Completed' : 'In Progress'}
            bg={isComplete ? '#d4edda' : '#fff3cd'}
            color={isComplete ? '#155724' : '#856404'}
          />
          <span>{dayInfo.weekTitle}</span>
        </div>
        <div className={styles.actions}>
          {isComplete ? (
            <Button variant="danger" onClick={handleReset} disabled={resetting}>
              ↺ Redo Day {day}
            </Button>
          ) : (
            <Button variant="success" onClick={() => markComplete(day)}>
              ✓ Mark Complete
            </Button>
          )}
        </div>
      </div>

      <Suspense fallback={<div style={{ padding: '40px', textAlign: 'center', color: 'var(--color-text-secondary)' }}>Loading day content...</div>}>
        <MDXComponent />
      </Suspense>

      <DayNavigation day={day} />
    </div>
  );
}
```

**Step 4: Commit**

```bash
git add web/src/components/DayPage/
git commit -m "feat(frontend): add DayPage with MDX rendering, progress, reset, and navigation"
```

---

#### Task 14: ExportPage

**Files:**
- Create: `web/src/components/ExportPage/ExportPage.jsx`
- Create: `web/src/components/ExportPage/ExportPage.module.css`

**Step 1: Create `web/src/components/ExportPage/ExportPage.module.css`**

```css
.page {
  padding-top: var(--space-sm);
}

.title {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--space-md);
}

.report {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-lg);
}

.reportLine {
  padding: var(--space-xs) 0;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

.actions {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}
```

**Step 2: Create `web/src/components/ExportPage/ExportPage.jsx`**

```jsx
import { useProgress } from '../../hooks/useProgress';
import { studyDays } from '../../data/navigation';
import Button from '../shared/Button';
import styles from './ExportPage.module.css';

function generateMarkdown(progress, days) {
  const total = days.length;
  const done = progress.completedDays.length;
  const pct = Math.round((done / total) * 100);
  const lines = [
    `# DSA Study Plan — Progress Report`,
    ``,
    `**Progress:** ${done}/${total} days completed (${pct}%)`,
    `**Started:** ${new Date(progress.startedAt).toLocaleDateString()}`,
    `**Exported:** ${new Date().toLocaleDateString()}`,
    ``,
    `## Days`,
    ``,
  ];
  days.forEach(d => {
    const status = progress.completedDays.includes(d.day) ? '✅' : '⬜';
    lines.push(`${status} **Day ${d.day}:** ${d.title} (${d.weekTitle})`);
  });
  lines.push(``, `---`, `Generated by DSA Study Plan`);
  return lines.join('\n');
}

export default function ExportPage() {
  const { progress } = useProgress();

  const total = studyDays.length;
  const done = progress.completedDays.length;
  const pct = Math.round((done / total) * 100);

  const md = generateMarkdown(progress, studyDays);
  const json = JSON.stringify(progress, null, 2);

  const download = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Export Progress</h1>

      <div className={styles.report}>
        <div className={styles.reportLine}>📊 DSA Study Plan Progress Report</div>
        <div className={styles.reportLine}>Progress: {done}/{total} days ({pct}%)</div>
        <div className={styles.reportLine}>Started: {new Date(progress.startedAt).toLocaleDateString()}</div>
        <div className={styles.reportLine}>Exported: {new Date().toLocaleDateString()}</div>
        <div style={{ marginTop: 'var(--space-md)' }}>
          {studyDays.map(d => (
            <div key={d.day} className={styles.reportLine}>
              {progress.completedDays.includes(d.day) ? '✅' : '⬜'} Day {d.day}: {d.title}
            </div>
          ))}
        </div>
      </div>

      <div className={styles.actions}>
        <Button onClick={() => download(md, 'dsa-progress.md', 'text/markdown')}>
          📄 Download Markdown
        </Button>
        <Button variant="secondary" onClick={() => download(json, 'dsa-progress.json', 'application/json')}>
          📋 Download JSON
        </Button>
        <Button variant="secondary" onClick={() => {
          navigator.clipboard.writeText(md);
        }}>
          📋 Copy to Clipboard
        </Button>
      </div>
    </div>
  );
}
```

**Step 3: Commit**

```bash
git add web/src/components/ExportPage/
git commit -m "feat(frontend): add ExportPage with markdown and JSON export"
```

---

### Phase 4: MDX Content for All 30 Days

#### Task 15: Create MDX content index + first 5 days

**Files:**
- Create: `web/content/day1.mdx` through `web/content/day5.mdx`
- Create: `web/content/day6.mdx` through `web/content/day10.mdx`
- Create: `web/content/day11.mdx` through `web/content/day15.mdx`
- Create: `web/content/day16.mdx` through `web/content/day20.mdx`
- Create: `web/content/day21.mdx` through `web/content/day25.mdx`
- Create: `web/content/day26.mdx` through `web/content/day30.mdx`

**Process:** Each MDX file follows the same structure:

```mdx
---
day: N
title: "Topic Title"
week: M
topics: ["Topic1", "Topic2"]
completed: false
---

## Topic Overview

[Explanation of the day's topic with key concepts]

## Essential Problems

<ProblemCard title="Problem Name" difficulty="easy" pattern="Pattern Name">
  Problem description and key insight.
</ProblemCard>

## Interactive Example

<CodePlayground
  language="python"
  initialCode={`# Example code here`}
/>

## Practice Problems

| # | Problem | Difficulty |
|---|---------|------------|
| 1 | Problem Name | Easy |

## Key Insights

<InsightBox>
- Insight 1
- Insight 2
</InsightBox>
```

Each day (1-19) must be rewritten from the existing DOCX + HTML content into MDX format. Days 20-30 use the study plan from `30_day_dsa_study_plan_detailed.txt`.

**Step 1: Create day1.mdx through day5.mdx with content from existing Day1-5 materials**

Use the content from:
- `Day1_Arrays_Hashing.docx` + `web/day1.html` → `web/content/day1.mdx`
- `Day2_Advanced_Arrays.docx` + `web/day2.html` → `web/content/day2.mdx`
- etc.

**Step 2: Create day6.mdx through day10.mdx**

**Step 3: Create day11.mdx through day15.mdx**

**Step 4: Create day16.mdx through day20.mdx**

**Step 5: Create day21.mdx through day25.mdx**

**Step 6: Create day26.mdx through day30.mdx**

**Step 7: Commit**

```bash
git add web/content/
git commit -m "feat(content): add MDX content for all 30 days"
```

---

### Phase 5: Integration & Polish

#### Task 16: Responsive mobile sidebar toggle

**Modify:** `web/src/components/Sidebar/Sidebar.jsx`

Add hamburger menu toggle for mobile:

```jsx
import { useState } from 'react';

export default function Sidebar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: 'none', position: 'fixed', top: 10, left: 10, zIndex: 200,
          background: 'var(--color-sidebar-bg)', color: 'white', border: 'none',
          borderRadius: 'var(--radius-sm)', padding: '8px 12px', fontSize: '1.2rem',
          cursor: 'pointer',
        }}
        className={styles.hamburger}
      >
        {open ? '✕' : '☰'}
      </button>
      <aside className={`${styles.sidebar} ${open ? styles.open : ''}`}>
        {/* existing content */}
      </aside>
      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{ position: 'fixed', inset: 0, zIndex: 99 }}
        />
      )}
    </>
  );
}
```

Add to CSS:
```css
@media (max-width: 768px) {
  .hamburger { display: block !important; }
}
```

**Commit:** `git commit -m "feat(frontend): add responsive mobile sidebar with hamburger toggle"`

---

#### Task 17: Verify build and dev server work

**Step 1:** Run `npm run build` in `web/`

Expected: Vite builds successfully with no errors

**Step 2:** Start backend:
```bash
cd backend && uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

**Step 3:** Start frontend in another terminal:
```bash
cd web && npm run dev
```

**Step 4:** Open http://localhost:5173 and verify:
- HomePage loads with stats and calendar
- Clicking a day navigates to /day/N
- Day content renders from MDX
- CodePlayground editor is interactive
- Theme toggle works
- Export page generates markdown

**Step 5:** Test API:
```bash
curl -X POST http://127.0.0.1:8001/api/run -H "Content-Type: application/json" -d '{"code": "print(2+2)", "lang": "python"}'
```
Expected: `{"stdout": "4\n", "stderr": "", "exit_code": 0, "timing_ms": ...}`

**Commit:** `git commit -m "chore: verify build and integration"`

---

## Spec Coverage Check

| Spec Requirement | Tasks |
|---|---|
| React SPA with client-side routing | 5, 13 |
| MDX content for all days | 15 |
| Code playground (edit/run/debug) | 11 |
| Polyglot execution (Python, Rust, JS, Java, C, Go) | 2, 3, 4 |
| Backend FastAPI code runner | 1, 2, 3, 4 |
| Progress tracking with localStorage | 8 |
| Mark complete / redo day / restart plan | 8, 13, 14 |
| Export / share progress | 14 |
| Design system + dark/light theme | 6, 7, 8 |
| Responsive mobile layout | 7, 16 |
| Search (top bar) | 10 |
