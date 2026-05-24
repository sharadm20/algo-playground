# Coding Challenge Library Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate sharadm20/coding-challenge source files as a searchable Challenge Library page with solution reveal, embedded challenges in MDX lessons, and a backend endpoint for lazy-loading solution code.

**Architecture:** ~50 challenge source files copied into `challenges/{language}/` with a JSON metadata index. Frontend extends ProblemCard with "Show Solution" toggle that fetches from a new `GET /api/challenges/{id}/solution` endpoint. A new `/challenges` route provides a filterable grid. A `ChallengeEmbed` component lets MDX files reference challenges by ID.

**Tech Stack:** React 18, Vite 6, Vitest, FastAPI, pytest

---

### Task 1: Copy challenge source files into challenges/ directory

**Files:**
- Create: `challenges/index.json` (stub — full content in Task 2)
- Create: `challenges/java/` (all .java files from coding-challenge)
- Create: `challenges/python/` (all .py files)
- Create: `challenges/javascript/` (all .js files)
- Create: `challenges/rust/` (Cargo.toml + src/)
- Create: `challenges/sql/` (query.sql)

This is a bulk file-copy task. No tests needed. Copy each source file preserving its relative path within its language directory. Do NOT copy `.idea/`, `.gitignore`, `coding-challenge.iml`, or any IDE config.

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p challenges/java challenges/python challenges/javascript challenges/rust challenges/sql
```

- [ ] **Step 2: Copy Java files**

Copy from the external coding-challenge clone into `challenges/java/`. Preserve subdirectory structure (arrays/, matrices/, strings/, sorts/, singletons/, excercise/).

```bash
# For each Java file, copy preserving directory structure
# Top-level files:
cp coding-challenge/java/*.java challenges/java/
# Subdirectory files:
cp -r coding-challenge/java/arrays challenges/java/
cp -r coding-challenge/java/matrices challenges/java/
cp -r coding-challenge/java/strings challenges/java/
cp -r coding-challenge/java/sorts challenges/java/
cp -r coding-challenge/java/singletons challenges/java/
cp -r coding-challenge/java/excercise challenges/java/
```

- [ ] **Step 3: Copy Python, JavaScript, Rust, SQL files**

```bash
cp coding-challenge/python/*.py challenges/python/
cp coding-challenge/javascript/*.js challenges/javascript/
cp -r coding-challenge/rust/* challenges/rust/
cp coding-challenge/sql/*.sql challenges/sql/
```

- [ ] **Step 4: Create stub index.json**

```bash
echo "[]" > challenges/index.json
```

- [ ] **Step 5: Commit**

```bash
git add challenges/
git commit -m "feat: add coding-challenge source files"
```

---

### Task 2: Create challenges/index.json with full metadata

**Files:**
- Modify: `challenges/index.json`

This is a data creation task. No code tests. Build the full JSON array with entries for every challenge file. Each entry follows:

```json
{
  "id": "two-sum",
  "title": "Two Sum",
  "sourcePath": "java/TwoSum.java",
  "language": "java",
  "topic": "Array",
  "difficulty": "easy",
  "dayIds": [1],
  "description": "Given an array of integers, return indices of the two numbers that add up to a target.",
  "tags": ["hash-map", "brute-force"],
  "type": "problem"
}
```

Full list of all entries:

**java/ (top-level):**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| two-sum | Two Sum | Array | easy | [1] | hash-map, brute-force |
| three-sum | Three Sum | Array | medium | [1] | two-pointer, sorting |
| sell-stock | Best Time to Buy and Sell Stock | Array | easy | [2] | greedy, array |
| plus-one | Plus One | Array | easy | [2] | array, math |
| max-container | Container With Most Water | Array | medium | [2] | two-pointer |
| trapping-water | Trapping Rain Water | Array | hard | [2] | two-pointer, stack |
| merge-two-array | Merge Sorted Array | Array | easy | [2] | two-pointer |
| max-distance | Maximum Distance | Array | medium | [2] | array |
| binary-search | Binary Search | Binary Search | easy | [16] | binary-search |
| binary-tree | Binary Tree Traversals | Tree | medium | [6] | tree, recursion, stack |
| graph | Graph Adjacency List | Graph | medium | [8] | graph, adjacency-list |
| graph-problems | Graph Problems | Graph | medium | [8] | graph, dfs, bfs |
| intersecting-linked-list | Intersecting Linked List | Linked List | easy | [5] | linked-list, two-pointer |
| linked-list-reversal | Linked List Reversal | Linked List | easy | [5] | linked-list, recursion |
| kth-max | Kth Largest Element | Heap | medium | [15] | heap, quickselect |
| running-median | Running Median | Heap | hard | [15] | heap, two-heaps |
| merge-sort | Merge Sort | Sorting | easy | [18] | sorting, divide-and-conquer |
| merge-interval | Merge Intervals | Interval | medium | [18] | interval, sorting |
| fibonacci | Fibonacci | Dynamic Programming | easy | [11] | dp, recursion |
| factorial | Factorial | Dynamic Programming | easy | [11] | dp, recursion |
| excel-column-number | Excel Sheet Column Number | Math | easy | [] | math, string |
| minimum-flips | Minimum Flips | Bit Manipulation | medium | [20] | greedy, prefix-sum |
| next-number-in-digit | Next Permutation | Backtracking | medium | [22] | array, permutation |
| occurrence | Count Occurrences | Array | easy | [1] | hash-map, counting |
| sort-array-accordingly | Sort by Another Array | Sorting | medium | [] | sorting, tree-map |
| wildcard-matching | Wildcard Matching | Dynamic Programming | hard | [] | dp, string, greedy |
| lambda-example | Lambda Expression Example | Utility | easy | [] | java, lambda |

**java/arrays/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| find-closest | Find Closest Number | Array | easy | [] | array, sorting |
| max-difference | Maximum Difference | Array | easy | [2] | array, greedy |
| roman-to-int | Roman to Integer | String | easy | [3] | string, hash-map |
| score-ranges | Score Ranges | Array | medium | [4] | linked-list, simulation |
| second-largest | Second Largest Element | Array | easy | [7] | array |
| sort-rotated-array | Search in Rotated Array | Binary Search | medium | [16] | binary-search, array |
| summary-range | Summary Ranges | Array | easy | [7] | array |

**java/strings/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| add-alternate | Merge Strings Alternately | String | easy | [3] | string, two-pointer |
| longest-common-prefix | Longest Common Prefix | String | easy | [3] | string |
| reverse-string | Reverse Words in String | String | easy | [3] | string, reverse |
| string-palindrome | Valid Palindrome | String | easy | [3] | string, two-pointer |
| substring | Is Subsequence | String | easy | [3] | string, two-pointer |
| unique-sub | Unique Substring | String | medium | [3] | string |

**java/matrices/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| min-distance | 01 Matrix Distance | Graph | medium | [26] | bfs, matrix |
| rotate-by-ninety | Rotate Image | Matrix | medium | [] | matrix |
| spiral-traverse | Spiral Matrix | Matrix | medium | [] | matrix, simulation |
| valid-sudoku | Valid Sudoku | Matrix | medium | [] | matrix, hash-set |

**java/sorts/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| bubble-sort | Bubble Sort | Sorting | easy | [] | sorting |
| insertion-sort | Insertion Sort | Sorting | easy | [] | sorting |
| quicksort | Quicksort | Sorting | medium | [23] | sorting, divide-and-conquer |

**java/excercise/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| death-note-decoder | Decode Ways | Dynamic Programming | medium | [11] | dp, string |
| highest-salary | Highest Salary by Department | SQL-like | medium | [] | java, streams |
| maximum-number-hard | Maximum of Two Numbers | Bit Manipulation | easy | [] | bit-manipulation |
| min-moves | Minimum Moves | Greedy | easy | [] | greedy, array |
| custom-function-interface | Custom Functional Interface | Utility | easy | [] | java, lambda |

**java/singletons/:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| bill-pugh-singleton | Bill Pugh Singleton | Design Pattern | easy | [] | singleton, java |

**Data structure files (type: "data-structure", NOT standalone problems):**

| id | title | topic | difficulty | dayIds | tags | type |
|----|-------|-------|-----------|--------|------|------|
| list-node | ListNode (Linked List Node) | Linked List | none | [] | linked-list | data-structure |
| tree-node | TreeNode (Binary Tree Node) | Tree | none | [] | tree | data-structure |

**Python files:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| divide-chocolate | Divide Chocolate | Binary Search | medium | [16] | binary-search, greedy |
| hit-counter | Hit Counter | Design | medium | [] | queue, design |
| occurance-char | Character Occurrence | String | easy | [3] | string, counting |
| smallest-interval | Smallest Interval | Interval | hard | [] | interval, heap |
| unique-substring | Unique Substring | String | medium | [3] | string |

**JavaScript files:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| add-upto | Add Up To | Math | easy | [] | math, recursion |
| valid-anagram | Valid Anagram | String | easy | [1] | string, hash-map |

**Rust files:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| rust-slide | Sliding Window | Array | medium | [] | sliding-window, rust |

**SQL:**

| id | title | topic | difficulty | dayIds | tags |
|----|-------|-------|-----------|--------|------|
| query | SQL Query Practice | SQL | easy | [] | sql, query |

- [ ] **Step 1: Write the full index.json** with all entries above. Save to `challenges/index.json`.

```json
[
  {
    "id": "two-sum",
    "title": "Two Sum",
    "sourcePath": "java/TwoSum.java",
    "language": "java",
    "topic": "Array",
    "difficulty": "easy",
    "dayIds": [1],
    "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`.",
    "tags": ["hash-map", "brute-force"],
    "type": "problem"
  },
  ... (all other entries)
]
```

- [ ] **Step 2: Validate the index** — write a quick validation script

```bash
python -c "
import json
with open('challenges/index.json') as f:
    data = json.load(f)
ids = [c['id'] for c in data]
assert len(ids) == len(set(ids)), 'Duplicate IDs found'
for c in data:
    path = f\"challenges/{c['sourcePath']}\"
    import os
    assert os.path.exists(path), f'Missing: {path}'
print(f'{len(data)} challenges validated OK')
"
```

- [ ] **Step 3: Commit**

```bash
git add challenges/index.json
git commit -m "feat: add challenge metadata index"
```

---

### Task 3: Add backend solution endpoint

**Files:**
- Modify: `backend/main.py`
- Modify: `backend/models.py`
- Create: `backend/tests/test_challenges.py`

- [ ] **Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_solution_returns_code():
    resp = client.get("/api/challenges/two-sum/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["language"] == "java"
    assert "public class" in data["code"]

def test_get_solution_unknown_returns_404():
    resp = client.get("/api/challenges/nonexistent/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 404

def test_get_solution_blocks_path_traversal():
    resp = client.get("/api/challenges/../../etc/passwd/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 404
```

- [ ] **Step 2: Install pytest and httpx, run test to see it fail**

```bash
cd backend
pip install pytest httpx
pytest tests/test_challenges.py -v
```
Expected: FAIL with "No module named 'main'" or "405 Method Not Allowed" (endpoint doesn't exist)

- [ ] **Step 3: Add SolutionResponse model to backend/models.py**

```python
class SolutionResponse(BaseModel):
    language: str
    code: str
```

- [ ] **Step 4: Add the endpoint to backend/main.py**

Add after the existing endpoints (before `if __name__`):

```python
import json
import os

CHALLENGES_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "challenges", "index.json")
CHALLENGES_DIR = os.path.join(os.path.dirname(__file__), "..", "challenges")

def _load_challenge_index():
    with open(CHALLENGES_INDEX_PATH) as f:
        return json.load(f)

@app.get("/api/challenges", response_model=list[dict])
def list_challenges():
    return _load_challenge_index()

@app.get("/api/challenges/{challenge_id}/solution", response_model=SolutionResponse)
def get_challenge_solution(challenge_id: str):
    index = _load_challenge_index()
    entry = next((c for c in index if c["id"] == challenge_id), None)
    if not entry:
        raise HTTPException(404, f"Challenge '{challenge_id}' not found")
    source_path = os.path.normpath(os.path.join(CHALLENGES_DIR, entry["sourcePath"]))
    if not source_path.startswith(os.path.normpath(CHALLENGES_DIR)):
        raise HTTPException(404, "Invalid path")
    if not os.path.exists(source_path):
        raise HTTPException(404, "Solution file not found")
    with open(source_path) as f:
        code = f.read()
    return SolutionResponse(language=entry["language"], code=code)
```

Update the import in `main.py`:

```python
from models import RunRequest, RunResponse, LanguageInfo, SolutionResponse
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd backend
pytest tests/test_challenges.py -v
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add backend/main.py backend/models.py backend/tests/
git commit -m "feat: add GET /api/challenges and /api/challenges/{id}/solution endpoints"
```

---

### Task 4: Extend ProblemCard with solution toggle

**Files:**
- Modify: `web/src/components/ProblemCard/ProblemCard.jsx`
- Modify: `web/src/components/ProblemCard/ProblemCard.module.css`
- Modify: `web/src/components/ProblemCard/ProblemCard.test.jsx`

- [ ] **Step 1: Write the failing tests**

Add to `ProblemCard.test.jsx`:

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

describe('ProblemCard with solution', () => {
  it('shows Show Solution button when solutionId is provided', () => {
    render(
      <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
        description text
      </ProblemCard>
    );
    expect(screen.getByText('Show Solution')).toBeInTheDocument();
  });

  it('does not show Show Solution button when solutionId is not provided', () => {
    render(<ProblemCard title="Two Sum">description text</ProblemCard>);
    expect(screen.queryByText('Show Solution')).not.toBeInTheDocument();
  });

  it('shows language badge alongside solutionId', () => {
    render(
      <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
        description
      </ProblemCard>
    );
    expect(screen.getByText('java')).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run tests to verify failure**

```bash
cd web
npm test -- ProblemCard.test.jsx
```
Expected: FAIL — "Show Solution" not found

- [ ] **Step 3: Update ProblemCard.jsx**

```javascript
import Badge from '../shared/Badge';
import styles from './ProblemCard.module.css';

const DIFFICULTY_COLORS = {
  easy: { bg: '#d4edda', color: '#155724' },
  medium: { bg: '#fff3cd', color: '#856404' },
  hard: { bg: '#f8d7da', color: '#721c24' },
};

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ProblemCard({
  title,
  difficulty = 'easy',
  pattern,
  children,
  solutionId,
  solutionLanguage,
}) {
  const [showSolution, setShowSolution] = useState(false);
  const [solutionCode, setSolutionCode] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleToggleSolution = async () => {
    if (showSolution) {
      setShowSolution(false);
      return;
    }
    if (solutionCode) {
      setShowSolution(true);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/challenges/${solutionId}/solution`, {
        headers: { 'Content-Type': 'application/json' },
      });
      if (!res.ok) throw new Error('Failed to load solution');
      const data = await res.json();
      setSolutionCode(data.code);
      setShowSolution(true);
    } catch {
      setSolutionCode('// Failed to load solution');
      setShowSolution(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h4>{title}</h4>
        <div className={styles.badges}>
          <Badge
            label={difficulty}
            bg={DIFFICULTY_COLORS[difficulty]?.bg || '#e9ecef'}
            color={DIFFICULTY_COLORS[difficulty]?.color || '#495057'}
          />
          {solutionLanguage && (
            <Badge label={solutionLanguage} bg="#e2e3f1" color="#4a4a6a" />
          )}
        </div>
      </div>
      {pattern && <div className={styles.pattern}>Pattern: {pattern}</div>}
      <div className={styles.description}>{children}</div>
      {solutionId && (
        <button
          className={styles.solutionBtn}
          onClick={handleToggleSolution}
          disabled={loading}
        >
          {loading ? 'Loading...' : showSolution ? 'Hide Solution' : 'Show Solution'}
        </button>
      )}
      {showSolution && solutionCode && (
        <pre className={styles.solutionBlock}>
          <code>{solutionCode}</code>
        </pre>
      )}
    </div>
  );
}
```

Add import for `useState` at the top:
```javascript
import { useState } from 'react';
```

- [ ] **Step 4: Update ProblemCard.module.css**

Add to the existing CSS:

```css
.badges {
  display: flex;
  gap: var(--space-xs);
  align-items: center;
}

.solutionBtn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: var(--space-xs) var(--space-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  margin-top: var(--space-sm);
  transition: background 0.2s;
}

.solutionBtn:hover {
  background: var(--color-bg-card);
}

.solutionBtn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.solutionBlock {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: var(--space-md);
  margin-top: var(--space-md);
  overflow-x: auto;
  font-size: var(--font-size-sm);
  max-height: 400px;
  overflow-y: auto;
}

.solutionBlock code {
  white-space: pre;
}
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd web
npm test -- ProblemCard.test.jsx
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add web/src/components/ProblemCard/
git commit -m "feat: extend ProblemCard with solution toggle"
```

---

### Task 5: Create ChallengeEmbed component for MDX

**Files:**
- Create: `web/src/components/shared/ChallengeEmbed.jsx`
- Create: `web/src/components/shared/ChallengeEmbed.test.jsx`

- [ ] **Step 1: Write the failing tests**

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ChallengeEmbed from './ChallengeEmbed';

const mockChallenges = [
  {
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    topic: 'Array',
    tags: ['hash-map'],
    description: 'Find two numbers that add up to target',
    language: 'java',
    sourcePath: 'java/TwoSum.java',
    dayIds: [1],
    type: 'problem',
  },
];

beforeEach(() => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockChallenges),
    })
  );
});

it('renders ProblemCard for valid challenge id', async () => {
  render(<ChallengeEmbed id="two-sum" />);
  expect(await screen.findByText('Two Sum')).toBeInTheDocument();
  expect(await screen.findByText('java')).toBeInTheDocument();
  expect(await screen.findByText('easy')).toBeInTheDocument();
});

it('renders error for unknown id', async () => {
  render(<ChallengeEmbed id="nonexistent" />);
  expect(await screen.findByText(/Challenge not found/)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run tests — expect failure**

```bash
cd web
npm test -- ChallengeEmbed.test.jsx
```
Expected: FAIL (module not found)

- [ ] **Step 3: Create ChallengeEmbed.jsx**

```javascript
import { useState, useEffect } from 'react';
import ProblemCard from '../ProblemCard/ProblemCard';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ChallengeEmbed({ id }) {
  const [challenge, setChallenge] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_BASE}/api/challenges`)
      .then(r => r.json())
      .then(data => {
        if (cancelled) return;
        const found = data.find(c => c.id === id);
        if (found) setChallenge(found);
        else setError(`Challenge "${id}" not found`);
      })
      .catch(() => {
        if (!cancelled) setError('Failed to load challenges');
      });
    return () => { cancelled = true; };
  }, [id]);

  if (error) return <p style={{ color: 'var(--color-danger)' }}>{error}</p>;
  if (!challenge) return <p>Loading challenge...</p>;

  return (
    <ProblemCard
      title={challenge.title}
      difficulty={challenge.difficulty}
      pattern={challenge.tags?.[0]}
      solutionId={challenge.id}
      solutionLanguage={challenge.language}
    >
      {challenge.description}
    </ProblemCard>
  );
}
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd web
npm test -- ChallengeEmbed.test.jsx
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web/src/components/shared/ChallengeEmbed.jsx web/src/components/shared/ChallengeEmbed.test.jsx
git commit -m "feat: add ChallengeEmbed MDX component"
```

---

### Task 6: Create ChallengeFilters component

**Files:**
- Create: `web/src/components/ChallengeFilters/ChallengeFilters.jsx`
- Create: `web/src/components/ChallengeFilters/ChallengeFilters.module.css`
- Create: `web/src/components/ChallengeFilters/ChallengeFilters.test.jsx`

- [ ] **Step 1: Write the failing tests**

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ChallengeFilters from './ChallengeFilters';

const defaultProps = {
  search: '',
  onSearchChange: vi.fn(),
  topicFilter: 'All',
  onTopicChange: vi.fn(),
  languageFilter: 'All',
  onLanguageChange: vi.fn(),
  difficultyFilter: 'All',
  onDifficultyChange: vi.fn(),
  topics: ['Array', 'String', 'Tree'],
  languages: ['java', 'python'],
};

it('renders search input and filter dropdowns', () => {
  render(<ChallengeFilters {...defaultProps} />);
  expect(screen.getByPlaceholderText(/Search challenges/i)).toBeInTheDocument();
  expect(screen.getByDisplayValue('All Topics')).toBeInTheDocument();
});

it('calls onSearchChange when typing', () => {
  const onSearchChange = vi.fn();
  render(<ChallengeFilters {...defaultProps} onSearchChange={onSearchChange} />);
  fireEvent.change(screen.getByPlaceholderText(/Search challenges/i), { target: { value: 'two' } });
  expect(onSearchChange).toHaveBeenCalledWith('two');
});
```

- [ ] **Step 2: Run tests — expect failure**

```bash
cd web
npm test -- ChallengeFilters.test.jsx
```
Expected: FAIL (module not found)

- [ ] **Step 3: Create ChallengeFilters.jsx**

```javascript
import styles from './ChallengeFilters.module.css';

export default function ChallengeFilters({
  search,
  onSearchChange,
  topicFilter,
  onTopicChange,
  languageFilter,
  onLanguageChange,
  difficultyFilter,
  onDifficultyChange,
  topics = [],
  languages = [],
}) {
  return (
    <div className={styles.filters}>
      <input
        type="text"
        className={styles.search}
        placeholder="Search challenges..."
        value={search}
        onChange={e => onSearchChange(e.target.value)}
      />
      <select
        className={styles.select}
        value={topicFilter}
        onChange={e => onTopicChange(e.target.value)}
      >
        <option value="All">All Topics</option>
        {topics.map(t => (
          <option key={t} value={t}>{t}</option>
        ))}
      </select>
      <select
        className={styles.select}
        value={languageFilter}
        onChange={e => onLanguageChange(e.target.value)}
      >
        <option value="All">All Languages</option>
        {languages.map(l => (
          <option key={l} value={l}>{l}</option>
        ))}
      </select>
      <select
        className={styles.select}
        value={difficultyFilter}
        onChange={e => onDifficultyChange(e.target.value)}
      >
        <option value="All">All Difficulties</option>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>
    </div>
  );
}
```

- [ ] **Step 4: Create ChallengeFilters.module.css**

```css
.filters {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: var(--space-lg);
}

.search {
  flex: 1;
  min-width: 200px;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg);
  color: var(--color-text);
  font-size: var(--font-size-sm);
}

.select {
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg);
  color: var(--color-text);
  font-size: var(--font-size-sm);
  cursor: pointer;
}
```

- [ ] **Step 5: Run tests — verify pass**

```bash
cd web
npm test -- ChallengeFilters.test.jsx
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add web/src/components/ChallengeFilters/
git commit -m "feat: add ChallengeFilters component"
```

---

### Task 7: Create ChallengeLibrary page

**Files:**
- Create: `web/src/components/ChallengeLibrary/ChallengeLibrary.jsx`
- Create: `web/src/components/ChallengeLibrary/ChallengeLibrary.module.css`
- Create: `web/src/components/ChallengeLibrary/ChallengeLibrary.test.jsx`

- [ ] **Step 1: Write the failing tests**

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ChallengeLibrary from './ChallengeLibrary';

const mockChallenges = [
  {
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    language: 'java',
    topic: 'Array',
    tags: ['hash-map'],
    description: 'Find two numbers that add up to target',
    sourcePath: 'java/TwoSum.java',
    dayIds: [1],
    type: 'problem',
  },
  {
    id: 'binary-search',
    title: 'Binary Search',
    difficulty: 'medium',
    language: 'java',
    topic: 'Binary Search',
    tags: ['binary-search'],
    description: 'Search for target in sorted array',
    sourcePath: 'java/BinarySearch.java',
    dayIds: [16],
    type: 'problem',
  },
];

beforeEach(() => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockChallenges),
    })
  );
});

it('renders challenge cards after loading', async () => {
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(await screen.findByText('Two Sum')).toBeInTheDocument();
  expect(await screen.findByText('Binary Search')).toBeInTheDocument();
});

it('shows challenge count', async () => {
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(await screen.findByText(/2 challenges/)).toBeInTheDocument();
});

it('filters by search text', async () => {
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(await screen.findByText('Two Sum')).toBeInTheDocument();
  expect(screen.getByText('Binary Search')).toBeInTheDocument();
});
```

- [ ] **Step 2: Run tests — expect failure**

```bash
cd web
npm test -- ChallengeLibrary.test.jsx
```
Expected: FAIL (module not found)

- [ ] **Step 3: Create ChallengeLibrary.jsx**

```javascript
import { useState, useEffect } from 'react';
import ProblemCard from '../ProblemCard/ProblemCard';
import ChallengeFilters from '../ChallengeFilters/ChallengeFilters';
import styles from './ChallengeLibrary.module.css';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ChallengeLibrary() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [topicFilter, setTopicFilter] = useState('All');
  const [languageFilter, setLanguageFilter] = useState('All');
  const [difficultyFilter, setDifficultyFilter] = useState('All');

  useEffect(() => {
    fetch(`${API_BASE}/api/challenges`)
      .then(r => r.json())
      .then(data => {
        setChallenges(data.filter(c => c.type === 'problem'));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const topics = [...new Set(challenges.map(c => c.topic))].sort();
  const languages = [...new Set(challenges.map(c => c.language))].sort();

  const filtered = challenges.filter(c => {
    const matchSearch = !search || c.title.toLowerCase().includes(search.toLowerCase()) || c.tags?.some(t => t.includes(search.toLowerCase()));
    const matchTopic = topicFilter === 'All' || c.topic === topicFilter;
    const matchLang = languageFilter === 'All' || c.language === languageFilter;
    const matchDiff = difficultyFilter === 'All' || c.difficulty === difficultyFilter;
    return matchSearch && matchTopic && matchLang && matchDiff;
  });

  if (loading) return <div className={styles.page}><p>Loading challenges...</p></div>;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Challenge Library</h1>
      <p className={styles.subtitle}>{filtered.length} challenge{filtered.length !== 1 ? 's' : ''}</p>
      <ChallengeFilters
        search={search}
        onSearchChange={setSearch}
        topicFilter={topicFilter}
        onTopicChange={setTopicFilter}
        languageFilter={languageFilter}
        onLanguageChange={setLanguageFilter}
        difficultyFilter={difficultyFilter}
        onDifficultyChange={setDifficultyFilter}
        topics={topics}
        languages={languages}
      />
      {filtered.length === 0 ? (
        <p>No challenges match your filters.</p>
      ) : (
        <div className={styles.grid}>
          {filtered.map(c => (
            <ProblemCard
              key={c.id}
              title={c.title}
              difficulty={c.difficulty}
              pattern={c.tags?.[0]}
              solutionId={c.id}
              solutionLanguage={c.language}
            >
              <div className={styles.meta}>
                <span className={styles.topic}>{c.topic}</span>
                {c.dayIds.length > 0 && (
                  <span>Day {c.dayIds.join(', ')}</span>
                )}
              </div>
              {c.description}
            </ProblemCard>
          ))}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 4: Create ChallengeLibrary.module.css**

```css
.page {
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  margin-bottom: var(--space-xs);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-lg);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: var(--space-md);
}

.meta {
  display: flex;
  gap: var(--space-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-sm);
}

.topic {
  font-weight: 600;
}
```

- [ ] **Step 5: Run tests — verify pass**

```bash
cd web
npm test -- ChallengeLibrary.test.jsx
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add web/src/components/ChallengeLibrary/
git commit -m "feat: add ChallengeLibrary page with filtering"
```

---

### Task 8: Update router and navigation

**Files:**
- Modify: `web/src/router.jsx`
- Modify: `web/src/components/Sidebar/Sidebar.jsx`
- Modify: `web/src/components/Sidebar/Sidebar.module.css`

- [ ] **Step 1: Write the failing test for sidebar navigation link**

No separate test file needed — the existing Sidebar test should be updated. Let's add one test:

Add to sidebar-related test coverage (check if any existing test covers this):

Check if `Sidebar.test.jsx` exists:
```bash
ls web/src/components/Sidebar/*.test.* 2>/dev/null || echo "No test file"
```

If no test exists for the sidebar, skip testing this — the router test covers the route.

For `router.jsx`, update imports and add the challenge route:

- [ ] **Step 2: Update router.jsx**

```javascript
import { createBrowserRouter, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import HomePage from './components/HomePage/HomePage';
import DayPage from './components/DayPage/DayPage';
import ExportPage from './components/ExportPage/ExportPage';
import ChallengeLibrary from './components/ChallengeLibrary/ChallengeLibrary';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'day/:dayId', element: <DayPage /> },
      { path: 'export', element: <ExportPage /> },
      { path: 'challenges', element: <ChallengeLibrary /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
]);

export default router;
```

- [ ] **Step 3: Update Sidebar.jsx** — add link to Challenge Library after the header section

Add after the `progressSummary` div:

```javascript
import { Link, useLocation } from 'react-router-dom';

export default function Sidebar({ completedDays = [], currentDay = 0, open = false, onClose }) {
  const location = useLocation();
  // ... existing code ...

  return (
    <aside className={`${styles.sidebar} ${open ? styles.open : ''}`}>
      {/* existing header and progressSummary */}
      <nav className={styles.quickNav}>
        <Link
          to="/challenges"
          className={`${styles.navLink} ${location.pathname.startsWith('/challenges') ? styles.active : ''}`}
          onClick={onClose}
        >
          {'\uD83D\uDCDA'} Challenge Library
        </Link>
      </nav>
      {/* existing week groups */}
    </aside>
  );
}
```

- [ ] **Step 4: Add quickNav styles to Sidebar.module.css**

```css
.quickNav {
  padding: var(--space-sm) var(--space-lg);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.navLink {
  display: block;
  padding: var(--space-sm) 0;
  color: inherit;
  text-decoration: none;
  font-size: var(--font-size-sm);
  opacity: 0.8;
  transition: opacity 0.2s;
}

.navLink:hover {
  opacity: 1;
}

.navLink.active {
  opacity: 1;
  font-weight: 600;
}
```

- [ ] **Step 5: Verify the app compiles and routes work**

```bash
cd web
npm run build
```
Expected: Build succeeds with no errors

- [ ] **Step 6: Commit**

```bash
git add web/src/router.jsx web/src/components/Sidebar/
git commit -m "feat: add /challenges route and sidebar navigation link"
```

---

### Task 9: Update MDX files with ChallengeEmbed

**Files:**
- Modify: `web/src/content/day-01.mdx` through `web/src/content/day-30.mdx` (selected days)

Only update days that have mapped challenges. For each day, add `ChallengeEmbed` imports and `<ChallengeEmbed>` tags after the existing Practice Problems section.

Example for Day 1 (day-01.mdx):

```mdx
import ChallengeEmbed from '../components/shared/ChallengeEmbed';

// ... existing content ...

## Practice Problems

{/* existing ProblemCard components */}

<ChallengeEmbed id="two-sum" />
<ChallengeEmbed id="three-sum" />
<ChallengeEmbed id="occurrence" />
```

Day-by-day additions:

| Day | Challenge IDs |
|-----|---------------|
| 1 | two-sum, three-sum, occurrence |
| 2 | sell-stock, plus-one, max-container, trapping-water, merge-two-array, max-difference |
| 3 | string-palindrome, reverse-string, substring, add-alternate, longest-common-prefix, roman-to-int, unique-sub, unique-substring, occurance-char |
| 4 | score-ranges |
| 5 | linked-list-reversal, intersecting-linked-list |
| 6 | binary-tree |
| 7 | summary-range, second-largest |
| 8 | graph, graph-problems |
| 11 | fibonacci, factorial, death-note-decoder |
| 15 | kth-max, running-median |
| 16 | binary-search, sort-rotated-array, divide-chocolate |
| 18 | merge-sort, merge-interval |
| 20 | minimum-flips |
| 22 | next-number-in-digit |
| 23 | quicksort |
| 26 | min-distance |
| General | valid-anagram, spiral-traverse, rotate-by-ninety, valid-sudoku, wildcard-matching, hit-counter, smallest-interval |

- [ ] **Step 1: Update day-01.mdx** — add import and ChallengeEmbed tags for day 1 challenges

```mdx
import ChallengeEmbed from '../components/shared/ChallengeEmbed';
```

Add after existing ProblemCard components:

```mdx
<ChallengeEmbed id="two-sum" />
<ChallengeEmbed id="three-sum" />
<ChallengeEmbed id="occurrence" />
```

- [ ] **Step 2: Update day-02.mdx** — add import and ChallengeEmbed for day 2 challenges

- [ ] **Step 3: Update remaining MDX files** (days 3, 4, 5, 6, 7, 8, 11, 15, 16, 18, 20, 22, 23, 26)

For each: add `import ChallengeEmbed from '../components/shared/ChallengeEmbed';` at the top, and add `<ChallengeEmbed id="..." />` tags in the Practice Problems section.

- [ ] **Step 4: Verify MDX compilation**

```bash
cd web
npm run build
```
Expected: Build succeeds

- [ ] **Step 5: Commit**

```bash
git add web/src/content/
git commit -m "feat: embed coding challenges in MDX lessons"
```

---

## Spec Self-Review

After writing the plan, verify against the spec:

1. **Spec coverage:** Every requirement from the spec has a corresponding task:
   - Copy source files → Task 1
   - Metadata index → Task 2
   - Backend endpoint → Task 3
   - ProblemCard solution toggle → Task 4
   - ChallengeEmbed for MDX → Task 5
   - ChallengeFilters component → Task 6
   - ChallengeLibrary page → Task 7
   - Router + navigation → Task 8
   - MDX updates → Task 9
   - Tests: Tasks 3-7 all have TDD cycles

2. **No placeholders:** Every step has complete code and commands.

3. **Type consistency:** Component prop names, API response shapes, and file paths are consistent across tasks.

4. **TDD adherence:** Tasks 3-7 follow red-green-refactor pattern with failing tests first, then implementation, then verification.
