# Coding Challenge Library Integration

## Status
Approved design. Ready for implementation planning.

## Motivation
The `sharadm20/coding-challenge` repository contains ~50 algorithm practice problems across Java, Python, JavaScript, Rust, and SQL. Currently these live in a separate repo with no connection to the 30-day DSA study plan. Integrating them brings contextual practice problems into each lesson day, adds a searchable challenge library for free-form practice, and makes existing solutions runnable through the CodePlayground backend.

## Architecture

```
Browser (React SPA)                  Backend (FastAPI)
┌─────────────────────────────┐      ┌──────────────────────────────┐
│ Existing Routes             │      │ Existing Endpoints           │
│  ├─ / → Dashboard           │      │  POST /api/run              │
│  ├─ /day/:id → DayPage      │      │  GET  /api/languages        │
│  └─ /export → ExportPage    │      │                              │
│                             │      │ New Endpoint                │
│ New Routes                  │      │  GET /api/challenges/{id}/  │
│  ├─ /challenges → Library   │◄────►│    solution → { lang, code }│
│  └─ /challenges/:id → Detail│      └──────────────────────────────┘
│                             │
│ New Components              │      Static Data
│  ├─ ChallengeLibrary        │      ┌──────────────────────────────┐
│  ├─ ChallengeFilters        │      │ challenges/index.json        │
│  └─ ChallengeEmbed (MDX)    │      │  → ~50 problem metadata     │
│                             │      │  → loaded at runtime        │
│ Extended Components         │      └──────────────────────────────┘
│  └─ ProblemCard (+solution) │
└─────────────────────────────┘
```

## Key Decisions

### Source Management: Copy & Organize
- Challenge source files copied into `challenges/{language}/` at repo root
- No git submodule, no subtree — flat copy with human-readable organization
- `.idea/`, `.iml`, IDE config from source repo excluded

### Challenge Metadata: Static JSON Index
- Single `challenges/index.json` as the source of truth for all challenge metadata
- LeetCode-style topic names (Array, String, Tree, Graph, Dynamic Programming)
- Solution code loaded lazily via `/api/challenges/{id}/solution` endpoint
- Auto-classified difficulty by topic (arrays/strings → Easy, trees/graphs → Medium, DP/backtracking → Hard)

### ProblemCard Extension
- Existing ProblemCard gets optional `solutionCode` prop and "Show Solution" toggle
- No breaking changes — problems without solution code render as before
- Solution fetched from backend on first click, cached client-side

### Challenge Library: Client-Side Filtering
- ~50 items is trivially filterable in JavaScript — no backend pagination needed
- Search by title, filter by topic/language/difficulty
- Grid layout with existing ProblemCard components

### MDX Integration: ChallengeEmbed Component
- New `<ChallengeEmbed id="two-sum" />` component for MDX files
- Looks up metadata from index, renders extended ProblemCard
- Single import replaces manual ProblemCard setup in MDX

## Component Tree (Additions)

```
App
├── Layout
│   └── MainContent  <React Router outlet>
│       ├── ChallengeLibrary        ← NEW
│       │   ├── ChallengeFilters    ← NEW
│       │   └── ProblemCard[]       (extended with solution toggle)
│       ├── DayPage
│       │   └── MDXContent
│       │       └── ChallengeEmbed  ← NEW
│       └── ... (existing pages)
```

## Data Flow

### Challenge Loading
1. User navigates to `/challenges`
2. `ChallengeLibrary` fetches `challenges/index.json`
3. Filters applied client-side
4. Each challenge renders as extended ProblemCard

### Solution Reveal
1. User clicks "Show Solution" on a ProblemCard
2. Frontend fetches `GET /api/challenges/{id}/solution`
3. Backend reads the source file from `challenges/` directory
4. Code rendered in read-only CodeMirror block with language-aware highlighting
5. Subsequent clicks toggle visibility (code cached in component state)

### MDX Embedding
1. `ChallengeEmbed` receives challenge ID as prop
2. Looks up metadata from already-loaded index (or fetches if not loaded)
3. Renders ProblemCard with full metadata + solution toggle

## File Structure (Additions)

```
ds_and_algo/
├── challenges/                          ← NEW — copied source files
│   ├── index.json                       ← NEW — master metadata index
│   ├── java/
│   │   ├── TwoSum.java
│   │   ├── ThreeSum.java
│   │   ├── BinarySearch.java
│   │   ├── BinaryTree.java
│   │   ├── ListNode.java
│   │   ├── TreeNode.java
│   │   ├── arrays/
│   │   ├── matrices/
│   │   ├── strings/
│   │   ├── sorts/
│   │   ├── singletons/
│   │   └── excercise/
│   ├── python/
│   ├── javascript/
│   ├── rust/
│   │   └── src/
│   └── sql/
├── backend/
│   └── main.py                          ← UPDATED — add challenges endpoint
├── web/
│   └── src/
│       ├── router.jsx                   ← UPDATED — add /challenges routes
│       ├── components/
│       │   ├── ProblemCard/
│       │   │   └── ProblemCard.jsx      ← UPDATED — add solution toggle
│       │   ├── ChallengeLibrary/
│       │   │   ├── ChallengeLibrary.jsx ← NEW
│       │   │   ├── ChallengeLibrary.module.css
│       │   │   └── ChallengeLibrary.test.jsx
│       │   ├── ChallengeFilters/
│       │   │   ├── ChallengeFilters.jsx ← NEW
│       │   │   ├── ChallengeFilters.module.css
│       │   │   └── ChallengeFilters.test.jsx
│       │   └── shared/
│       │       ├── ChallengeEmbed.jsx   ← NEW
│       │       └── ChallengeEmbed.test.jsx
```

## Day-to-Challenge Mapping

| Day | Topic | Challenges |
|-----|-------|-----------|
| 1 | Arrays & Hashing | TwoSum, ThreeSum, Occurence |
| 2 | Advanced Arrays | PlusOne, MaxContainer, TrappingWater, MaxDistance, MergeTwoArray |
| 3 | String Manipulation | StringPalindrome, ReverseString, Substring, AddAlternate, LongestCommonPrefix, RomanToInt, UniqueSub |
| 4 | Stack & Queue | (ScoreRanges) |
| 5 | Linked List | LinkedListReversal, IntersectingLinkedList |
| 6 | Trees | BinaryTree (diameter, traversal, symmetric, BST), SortedArrayToBST |
| 7 | Review | SummaryRange, SecondLargest |
| 8 | Graphs | Graph, GraphProblems |
| 11 | DP Fundamentals | Fibonacci, Factorial, DeathNoteDecoder |
| 15 | Heaps & Tries | KthMax, RunningMedian |
| 16 | Binary Search | BinarySearch, SortRotatedArray |
| 18 | Segment Trees | MergeSortExample |
| 20 | Bit Manipulation | MinimumFlips |
| 22 | Backtracking | NextNumberInDigit |
| 23 | Divide & Conquer | Quicksort, MergeSortExample |
| 26 | Spanning Tree | MinDistance |
| General | All | SpiralTraverse, RotateByNinety, ValidSudoku, MergeInterval, SellStock, WildcardMatching, FindClosest, MaxDifference, MinMoves, MaxNumberHard, HighestSalary, LambdaExample |

Challenges without day mapping appear only in the Challenge Library.

## Backend Changes

### New Endpoint
```
GET /api/challenges/{challenge_id}/solution
→ 200 { "language": "java", "code": "..." }
→ 404 { "detail": "Challenge not found" }
```

Implementation: validate `challenge_id` against known list, read file from `challenges/{language}/{path}`, return with language tag. Path traversal check required.

### Languages Update
```
GET /api/languages
→ { "available": [...], "missing": [...], "challengeLanguages": ["java", "python", "javascript", "rust"] }
```

## Testing Strategy

### Frontend (Vitest + Testing Library)
| Test File | Coverage |
|-----------|----------|
| `ProblemCard.test.jsx` | Solution toggle renders/hides, fetches on click, handles API error |
| `ChallengeLibrary.test.jsx` | Renders grid, filters by topic/language/difficulty, search filters |
| `ChallengeFilters.test.jsx` | Dropdown selection updates state, search input debounces |
| `ChallengeEmbed.test.jsx` | Renders for valid ID, handles missing ID gracefully |

### Backend (pytest)
| Test | Coverage |
|------|----------|
| `test_solution_endpoint` | Returns correct code, 404 for unknown, blocks path traversal |
| `test_java_dependency` | Compiles ListNode.java + dependent challenge together |

### Data Validation
| Test | Coverage |
|------|----------|
| `challenges/index.json` schema check | All IDs unique, all source paths exist, valid topics/difficulties |

## Non-Goals
- Test case verification (user's code against hidden tests) — future enhancement
- User-submitted solutions or community features
- Automated solution grading or scoring
- Syncing with the upstream coding-challenge repo

## Open Questions Resolved
- Integration style → Both embedded (in MDX) + library page
- Source management → Copy & organize
- Solution loading → Lazy from file (not inlined)
- Topic naming → LeetCode-style (Array, String, Tree, etc.)
- Difficulty → Auto-classified by topic
- Testing → TDD: tests before implementation
