# SOUL — DSA Study Plan SPA

This project has been fully redesigned from a static HTML site into a **modern React SPA** with a FastAPI backend for polyglot code execution. All 30 days of DSA content are written as MDX files with interactive code playgrounds.

## Architecture

```
ds_and_algo/
├── backend/          # FastAPI + code runners (Python/Rust/JS/Java/C/Go)
├── web/              # React SPA (Vite + MDX + CodeMirror 6)
├── python_projects/  # Legacy Python implementations
├── rust_projects/    # Legacy Rust implementations
└── docs/             # Design docs + implementation plans
```

## Key Decisions

- **React 18 + Vite 6** — modern build tooling with fast HMR
- **MDX** — each day is an `.mdx` file rendering as a lazy-loaded React component
- **CodeMirror 6** — in-browser code editor with syntax highlighting for 6 languages
- **FastAPI backend** — sandboxed code execution (not WASM), runs on port 8001
- **localStorage** — progress and theme persistence, no auth/server
- **Progress sharing** — markdown/JSON export (no multi-user)

## Component Map

- `Layout.jsx` — shell with Sidebar + TopBar + Outlet
- `HomePage.jsx` — dashboard with StatsRow + CalendarGrid
- `DayPage.jsx` — renders MDX + day nav + mark-complete/redo
- `CodePlayground.jsx` — CodeMirror 6 editor + run button + output panel
- `ExportPage.jsx` — markdown/JSON download + clipboard
- `Sidebar.jsx` — week-grouped day links with progress summary

## Content

30 MDX files in `web/src/content/day-XX.mdx`, each importing:
- `CodePlayground` — live code editor
- `ProblemCard` — practice problem (title, difficulty, pattern)
- `InsightBox` — key takeaways
- `DataTable` — comparison tables
- `Badge` — difficulty labels

## Running

```bash
# Backend (port 8001)
cd backend && pip install -r requirements.txt && python main.py

# Frontend (port 5173)
cd web && npm install && npm run dev
```

The frontend builds to `web/dist/` for production preview.

## Extending

To add a new day: create `web/src/content/day-XX.mdx`, add it to the import map in `DayPage.jsx`, and add its metadata to `navigation.js`.

To add a new language runner: create `backend/runners/<lang>_runner.py` extending `BaseRunner`.
