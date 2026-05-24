# 30-Day DSA Study Plan

A modern interactive study plan for mastering Data Structures & Algorithms. Features a **React SPA** with MDX content, an in-browser **CodeMirror 6 code editor**, a **FastAPI backend** for polyglot code execution (Python, Rust, JavaScript, Java, C, Go), and an integrated **Challenge Library** with 59 practice problems from LeetCode & interview prep.

## Quick Start

### Backend (code execution API)
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Runs on `http://127.0.0.1:8001` — serves `/api/run` and `/api/languages`.

### Frontend (web app)
```bash
cd web
npm install
npm run dev
```
Opens at `http://localhost:5173` — full SPA with hot reload.

### Production Build
```bash
cd web
npm run build
npm run preview
```

## Architecture

```
ds_and_algo/
├── backend/                    # FastAPI code execution API
│   ├── main.py                 # App entry: CORS, /api/run, /api/languages, /api/challenges
│   ├── models.py               # Pydantic request/response models
│   ├── sandbox.py              # Secure subprocess sandbox with timeout
│   ├── start.bat               # One-click Windows launcher
│   └── runners/                # Polyglot execution engines
│       ├── base.py             # BaseRunner ABC
│       ├── python_runner.py    # Python (3.10+)
│       ├── rust_runner.py      # Rust (cargo script)
│       ├── js_runner.py        # JavaScript (Node.js)
│       └── other_runners.py    # Java, C, Go
├── challenges/                 # Coding challenge solutions (59 problems)
│   ├── index.json              # Metadata index (topics, difficulty, day mappings)
│   ├── java/                   # Java solutions (BST, Trees, Graphs, DP, etc.)
│   ├── python/                 # Python solutions
│   ├── javascript/             # JavaScript solutions
│   ├── rust/                   # Rust solutions (Cargo project)
│   └── sql/                    # SQL queries
├── web/                        # React SPA
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/         # App shell (Sidebar + TopBar + Outlet)
│   │   │   ├── Sidebar/        # Week-grouped day navigation + challenge link
│   │   │   ├── TopBar/         # Theme toggle + mobile hamburger
│   │   │   ├── HomePage/       # Dashboard with stats + calendar grid
│   │   │   ├── DayPage/        # MDX rendering + day nav + progress buttons
│   │   │   ├── CodePlayground/ # CodeMirror 6 editor + output panel
│   │   │   ├── ProblemCard/    # Reusable problem card with solution toggle
│   │   │   ├── ChallengeLibrary/ # Searchable/filterable challenge grid
│   │   │   ├── ChallengeFilters/ # Search + topic/language/difficulty filters
│   │   │   ├── ExportPage/     # Progress report export (markdown/JSON)
│   │   │   └── shared/         # Badge, Button, DataTable, InsightBox, ChallengeEmbed
│   │   ├── content/            # 30 MDX lesson files (with embedded challenges)
│   │   ├── context/            # ThemeContext + ProgressContext
│   │   ├── hooks/              # useProgress, useCodeRunner
│   │   ├── data/navigation.js  # 30-day metadata
│   │   └── styles/             # Design tokens + global CSS
│   └── vite.config.js
├── python_projects/            # Legacy Python implementations
├── rust_projects/              # Legacy Rust implementations
├── docs/                       # Design specs + implementation plans
│   └── superpowers/
│       ├── specs/              # Design documents
│       └── plans/              # Implementation plans
└── .obsidian/                  # Obsidian vault configuration
```

## Features

- **30 Days of Content** — MDX lessons with interactive code examples
- **Challenge Library** — 59 practice problems across 7 languages, searchable by topic/language/difficulty
- **Inline Challenge Embedding** — challenges appear in relevant lessons via `<ChallengeEmbed>`
- **Solution Reveal** — hidden by default, toggle to see reference solutions from LeetCode/interview prep
- **Polyglot Code Playground** — edit and run Python, Rust, JS, Java, C, Go in-browser
- **Progress Tracking** — localStorage persistence, mark-complete/redo per day
- **Progress Export** — markdown report + JSON data with download and clipboard copy
- **Dark/Light Theme** — persistent theme toggle
- **Mobile Responsive** — collapsible sidebar with overlay on small screens
- **Lazy-Loaded MDX** — each day is a separate code-split chunk for fast initial load

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 6, React Router v7 |
| Content | MDX (via @mdx-js/rollup) |
| Editor | CodeMirror 6 (Python, Rust, JS, Java, C++) |
| Backend | FastAPI (Python 3.10+) |
| Execution | Sandboxed subprocess with timeout |

## How to Use

1. **Open the app** at `http://localhost:5173`
2. **Navigate** using the sidebar or calendar grid on the homepage
3. **Read the lesson** for each day — explanations, key concepts, code examples
4. **Practice** — each day has embedded coding challenges with solution reveal
5. **Browse the Challenge Library** — click "Challenge Library" in the sidebar to search all 59 problems by topic, language, or difficulty
6. **Edit and run code** directly in the CodePlayground — change the code, click Run
7. **Mark days complete** as you finish them — track your progress
8. **Export your progress** from the Export page as markdown or JSON

## Adding a New Day

1. Create `web/src/content/day-XX.mdx` with lesson content
2. Add it to the import map in `web/src/components/DayPage/DayPage.jsx`
3. Add its metadata to `web/src/data/navigation.js` (day, title, week, weekTitle)
4. Done — the sidebar and calendar will pick it up automatically

## Adding a New Language

1. Create `backend/runners/<lang>_runner.py` extending `BaseRunner`
2. Implement `execute(code, timeout, test_data) -> RunResult`
3. Add the runner to the LANGUAGE_MAP in `backend/main.py`
4. Add the language option to `CodePlayground.jsx`'s `LANG_OPTIONS` array

## License

MIT — free to use for educational purposes.
