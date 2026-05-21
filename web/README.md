# DSA Study Plan — Web App

A modern React SPA for browsing and interacting with 30 days of Data Structures & Algorithms content. Features MDX lesson pages, a live code playground, and progress tracking — all local-first.

## Quick Start

```bash
npm install
npm run dev      # Dev server at http://localhost:5173
npm run build    # Production build to dist/
npm run preview  # Preview production build
```

The backend (code execution API) runs separately — see `backend/README.md` in the project root.

## Architecture

```
src/
├── components/
│   ├── Layout/          # Shell: Sidebar + TopBar + Outlet
│   ├── Sidebar/         # Fixed sidebar with week-grouped day links
│   ├── TopBar/          # Theme toggle + mobile hamburger
│   ├── HomePage/        # Dashboard with stats row + calendar grid
│   ├── DayPage/         # MDX content renderer + prev/next + mark complete
│   ├── CodePlayground/  # CodeMirror 6 editor with run/reset/output
│   ├── ProblemCard/     # Practice problem card (title, difficulty, pattern)
│   ├── ExportPage/      # Progress report export (markdown + JSON)
│   └── shared/          # Badge, Button, DataTable, InsightBox
├── content/             # 30 MDX lesson files (day-01.mdx through day-30.mdx)
├── context/             # ThemeContext (dark/light), ProgressContext (localStorage)
├── hooks/               # useProgress, useCodeRunner (API fetch)
├── data/navigation.js   # 30-day study plan metadata
└── styles/              # tokens.css (design tokens) + global.css (reset)
```

## Key Decisions

- **Code splitting**: Each MDX day is `React.lazy()` loaded — day chunks only download when visited
- **Progress**: Stored in `localStorage` under key `dsa-progress`; current day derived from `window.location.pathname`
- **Theme**: Dark/light toggle persisted to `localStorage` under key `dsa-theme`
- **Code execution**: Delegated to FastAPI backend at `http://127.0.0.1:8001` — not in-browser WASM

## MDX Content

Each MDX file automatically imports these components (no need to re-import):
- `CodePlayground` — live editor with pre-filled code
- `ProblemCard` — practice problem (title, difficulty easy/medium/hard, pattern)
- `InsightBox` — gradient callout for key takeaways
- `DataTable` — styled comparison tables
- `Badge` — small pill labels

## Development

```bash
npm run dev      # Vite dev server with HMR
npm run build    # Production build
npm run preview  # Serve production build
```
