# DSA Study Plan — React SPA + Interactive Code Playground Redesign

## Status
Approved design. Ready for implementation planning.

## Motivation
The existing 30-day DSA study plan uses static HTML pages per day with hardcoded content and no interactive features. The goal is a modern single-page application with live code editing/execution, a flexible polyglot backend, and a refreshed design system — while keeping the project self-contained and local-first.

## Architecture

```
Browser (React SPA)                  Backend (FastAPI)
┌─────────────────────────────┐      ┌──────────────────────────────┐
│ React Router                │      │ POST /api/run                │
│  ├─ / → Dashboard           │◄────►│   { code, lang } → { output }│
│  ├─ /day/:id → DayPage      │      │                              │
│  └─ /export → ExportPage    │      │ POST /api/languages          │
│                             │      │   → { available, missing }   │
│ MDX Content Files           │      │                              │
│  └─ content/day*.mdx        │      │ Code Executors:              │
│                             │      │  python → python3 -c "..."   │
│ React Components            │      │  rust   → rustc + run        │
│  ├─ CodePlayground          │      │  js     → node               │
│  ├─ ProblemCard             │      │  java   → javac + run        │
│  ├─ ProgressBar             │      │  c      → gcc + run          │
│  └─ ...                     │      │  go     → go run             │
└─────────────────────────────┘      └──────────────────────────────┘
```

## Key Decisions

### Framework: React + Vite
- React 18+ with React Router v7 for SPA routing
- Vite as build tool (already in use, proven)
- CSS Modules for scoped styling + a global design tokens file
- ESBuild for MDX compilation via `@mdx-js/rollup`

### Content: MDX
- Each day is an `.mdx` file in `web/content/`
- Frontmatter (YAML) for metadata: day number, title, week, status, topics
- Body is markdown with embedded React components
- All 30 days will be written as fresh MDX content (Days 1-19 rewritten)

### Code Playground: CodeMirror 6
- Language modes: Python, Rust, JavaScript/TypeScript, Java, C, Go
- Theme-aware (dark/light), syntax highlighting, bracket matching, line numbers
- Each code block in MDX renders as editable playground
- "Run" button sends to backend; "Reset" restores initial code
- Output panel shows stdout, stderr, test results, timing

### Backend: FastAPI (Python)
- Lightweight REST API, runs alongside Vite dev server
- Language dispatcher pattern — each language is a handler function
- Sandboxed execution: temp files, 30s timeout, 1MB output limit, auto-cleanup
- `GET /api/languages` probes available toolchains
- No authentication (local-only)
- CORS enabled for `localhost:5173` (Vite) and `localhost:8080`

### Progress: localStorage + Export
- Single-user progress stored in localStorage (no migration needed from current system)
- Reset: per-day reset or full-plan restart
- Export: JSON report, Markdown summary, progress badge HTML

### Design System
- Design tokens: CSS custom properties for colors, spacing, typography
- Dark/light theme toggle
- Responsive: mobile sidebar as overlay, desktop as fixed panel
- Consistent component library (buttons, cards, tables, badges)

## Component Tree

```
App
├── ThemeProvider (dark/light context)
├── Layout
│   ├── Sidebar
│   │   ├── Logo + Title
│   │   ├── ProgressSummary (count, percent, streak)
│   │   ├── WeekGroup (×4)
│   │   │   └── DayLink (number, title, status icon)
│   │   └── ExportLink
│   ├── TopBar
│   │   ├── Search (filter days by topic)
│   │   ├── ThemeToggle
│   │   └── ExportButton
│   └── MainContent  <React Router outlet>
│       ├── HomePage
│       │   ├── StatsRow (completed, remaining, percent, problems)
│       │   ├── CalendarGrid (30-day clickable calendar)
│       │   ├── RecentActivity
│       │   └── QuickStart
│       ├── DayPage
│       │   ├── PageHeader (title, week, status badge, date)
│       │   ├── MDXContent
│       │   │   ├── Section (h2)
│       │   │   ├── SubSection (h3)
│       │   │   ├── ProblemCard (title, difficulty, pattern, description, solution toggle)
│       │   │   ├── CodePlayground (editor, run button, reset, output)
│       │   │   ├── DataTable
│       │   │   ├── InsightBox
│       │   │   └── ContentList
│       │   ├── DayNavigation (prev/next/home buttons)
│       │   └── ResetDayButton
│       └── ExportPage
│           ├── ProgressReport
│           ├── ShareBadge
│           └── DownloadButtons (JSON, Markdown)
```

## Data Flow

### Content Loading
1. Vite compiles MDX files to React components at build time
2. React Router uses dynamic imports: `/day/1` → `import('./content/day1.mdx')`
3. DayPage wrapper provides layout, navigation, and header
4. CodePlayground components within MDX receive their code as props

### Code Execution
1. User edits code in CodeMirror and clicks "Run"
2. CodePlayground sends POST to `/api/run` with `{ code, lang }`
3. Backend dispatches to language handler
4. Handler writes temp file, executes with timeout, captures output
5. Response: `{ stdout, stderr, tests, timing_ms, exit_code }`
6. Frontend renders output in the output panel below the editor

## File Structure

```
ds_and_algo/
├── backend/
│   ├── main.py              # FastAPI app, CORS, routes
│   ├── runners/
│   │   ├── __init__.py
│   │   ├── base.py          # Base runner class
│   │   ├── python_runner.py
│   │   ├── rust_runner.py
│   │   ├── js_runner.py
│   │   ├── java_runner.py
│   │   ├── c_runner.py
│   │   └── go_runner.py
│   ├── sandbox.py            # Temp dir, timeout, output capture
│   ├── requirements.txt
│   └── start.sh / start.bat
├── web/                       # New React SPA
│   ├── content/
│   │   ├── day1.mdx
│   │   ├── day2.mdx
│   │   ├── ...
│   │   └── day30.mdx
│   ├── content/
│   │   └── day*.mdx
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── router.jsx
│   │   ├── styles/
│   │   │   ├── tokens.css      # Design tokens
│   │   │   ├── global.css
│   │   │   └── components/     # Per-component CSS modules
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   ├── Sidebar/
│   │   │   ├── DayPage/
│   │   │   ├── HomePage/
│   │   │   ├── ExportPage/
│   │   │   ├── CodePlayground/
│   │   │   ├── ProblemCard/
│   │   │   └── shared/         # Button, Badge, Table, etc.
│   │   ├── context/
│   │   │   ├── ThemeContext.jsx
│   │   │   └── ProgressContext.jsx
│   │   └── hooks/
│   │       ├── useProgress.js
│   │       └── useCodeRunner.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── python_projects/            # Keep existing (reference)
├── rust_projects/              # Keep existing (reference)
├── Day*.docx                   # Keep existing (reference)
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-05-21-dsa-study-plan-spa-redesign.md
```

## Remaining Days Content (20-30)

These will be generated as MDX files as part of this project, following the same pattern as the existing days. The study plan already defines topics for all 30 days.

## Non-Goals (Out of Scope)
- User authentication or accounts
- Real-time collaboration
- Deployment to cloud hosting
- Package manager for code execution (Docker)
- Production security hardening (local tool)

## Open Questions Resolved
- Multi-user → Progress sharing/export only, no auth
- Modern → Full SPA + design system overhaul
- Framework → React
- Content format → MDX
- Code execution → Backend (FastAPI), polyglot dispatcher
- Language support → Python, Rust, JS, Java, C, Go (extensible)
