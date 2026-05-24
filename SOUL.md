# SOUL — DSA Study Plan SPA

A modern interactive study plan for mastering Data Structures & Algorithms. Combines 30 days of MDX lessons with an integrated Challenge Library of 61 practice problems, plus an SQL ↔ Java Stream API translation library.

## Architecture

```
ds_and_algo/
├── backend/          # FastAPI + code runners (Python/Rust/JS/Java/C/Go)
├── challenges/       # 61 coding challenge solutions across 6 languages
├── web/              # React SPA (Vite + MDX + CodeMirror 6)
├── references/       # Legacy reference materials (study guides, old projects)
│   ├── study-guides/ # DOCX study guides for Days 1-19
│   ├── legacy-site/  # Gen 1 static HTML site (config, pages, scripts)
│   ├── python-projects/ # Legacy Python implementations
│   └── rust-projects/   # Legacy Rust implementations
├── docs/             # Design specs + implementation plans
└── .obsidian/        # Obsidian vault configuration
```

## Key Decisions

- **React 18 + Vite 6** — modern build tooling with fast HMR
- **MDX** — each day is an `.mdx` file rendering as a lazy-loaded React component
- **CodeMirror 6** — in-browser code editor with syntax highlighting for 6 languages
- **FastAPI backend** — sandboxed code execution (not WASM), runs on port 8001
- **localStorage** — progress and theme persistence, no auth/server
- **Progress sharing** — markdown/JSON export (no multi-user)
- **Challenge Library** — 61 problems integrated from sharadm20/coding-challenge, mapped to lesson days
- **Solution reveal** — reference solutions loaded lazily from backend, toggle per-problem
- **SQL Streams** — 18 SQL→Java Stream API translation examples in a dedicated browseable library
- **No backend dependency for SQL Streams** — query data embedded in frontend for instant filtering

## Component Map

- `Layout.jsx` — shell with Sidebar + TopBar + Outlet
- `HomePage.jsx` — dashboard with StatsRow + CalendarGrid
- `DayPage.jsx` — renders MDX + day nav + mark-complete/redo
- `CodePlayground.jsx` — CodeMirror 6 editor + run button + output panel
- `ExportPage.jsx` — markdown/JSON download + clipboard
- `Sidebar.jsx` — week-grouped day links with progress summary, Challenge Library link, SQL Streams link
- `ProblemCard.jsx` — practice problem (title, difficulty, pattern, solution toggle)
- `ChallengeLibrary.jsx` — full grid page with search/filter for all 61 challenges
- `ChallengeFilters.jsx` — search input + topic/language/difficulty dropdowns
- `ChallengeEmbed.jsx` — MDX-friendly wrapper: `<ChallengeEmbed id="two-sum" />`
- `SqlStreamCard.jsx` — expandable SQL/Java side-by-side card with schema & model viewer
- `SqlStreamFilters.jsx` — search + category/domain/difficulty dropdowns
- `SqlStreamsPage.jsx` — full page composing filters + query card grid

## Content

30 MDX files in `web/src/content/day-XX.mdx`, each importing:
- `CodePlayground` — live code editor
- `ProblemCard` / `ChallengeEmbed` — practice problems
- `InsightBox` — key takeaways
- `DataTable` — comparison tables
- `Badge` — difficulty labels

## Challenge Library

61 problems copied from [sharadm20/coding-challenge](https://github.com/sharadm20/coding-challenge), stored in `challenges/`:

| Language | Count |
|----------|-------|
| Java | 45 |
| Python | 5 |
| JavaScript | 2 |
| Rust | 2 |
| SQL | 1 |

Challenges are indexed in `challenges/index.json` with metadata: topic, difficulty, day mapping, tags. Solutions are lazy-loaded via `GET /api/challenges/{id}/solution`. Problems are embedded in relevant MDX lessons via `ChallengeEmbed` and browsable at `/challenges`.

## SQL Streams Library

18 SQL→Java Stream API translation examples from [sql-java-stream-learning](https://github.com/sharadm20/sql-java-stream-learning), stored in `web/src/data/sqlStreamQueries.js`:

| Category | Count |
|----------|-------|
| Filtering & Conditionals | 2 |
| Nth Most/Least Queries | 3 |
| Grouping & Aggregation | 4 |
| Window Functions | 3 |
| Joins & Relationships | 3 |
| Subqueries & EXISTS | 1 |
| Pivot & Conditional Logic | 1 |
| CTEs & Hierarchical Queries | 1 |

Each query includes SQL code, Java Stream equivalent, explanation, expected output, and a collapsible schema & models panel (DDL, sample data, Java entity classes). Data is embedded in frontend — no backend needed. Browsable at `/sql-streams`.

## Running

```bash
# Backend (port 8001)
cd backend && pip install -r requirements.txt && python main.py

# Frontend (port 5173)
cd web && npm install && npm run dev
```

The frontend builds to `web/dist/` for production preview.

## Testing

```bash
# Frontend tests (Vitest) — 116 tests across 22 files
cd web && npm test

# Backend tests (pytest)
cd backend && python -m pytest
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/languages | Available language runtimes |
| POST | /api/run | Execute code in specified language |
| GET | /api/challenges | List all challenges with metadata |
| GET | /api/challenges/{id}/solution | Get solution code for a challenge |

## Extending

To add a new day: create `web/src/content/day-XX.mdx`, add it to the import map in `DayPage.jsx`, and add its metadata to `navigation.js`.

To add a new language runner: create `backend/runners/<lang>_runner.py` extending `BaseRunner`.

To add a new challenge: place the source file in `challenges/<language>/`, add an entry to `challenges/index.json`, and embed in MDX via `<ChallengeEmbed id="your-id" />`.

To add a new SQL Stream example: add an entry to the `queries` array in `web/src/data/sqlStreamQueries.js` and optionally update the domain schema bundle.
