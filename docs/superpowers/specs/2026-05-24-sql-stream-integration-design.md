# SQL → Java Stream Integration Design

## Overview

Integrate the 18 SQL→Java Stream API translation examples from `sql-java-stream-learning` into the existing DSA Study Plan SPA as a dedicated `/sql-streams` browseable library page. This follows the same pattern as the Challenge Library (`/challenges`) but is purpose-built for SQL/Java side-by-side comparison.

## Data Model

### Query Example

```typescript
interface SqlStreamQuery {
  id: string;                    // kebab-case unique id, e.g. "filter-basic"
  category: string;              // e.g. "Filtering & Conditionals"
  difficulty: "beginner" | "intermediate" | "advanced";
  title: string;                 // e.g. "Find Customers with High Purchase Amounts"
  description: string;           // one-line summary
  domain: string;                // maps to a schema bundle key: "ecommerce" | "hr" | "social-media" | "student"
  sqlQuery: string;              // the SQL query (multi-line string)
  javaStreamCode: string;        // the Java Stream equivalent (multi-line string)
  explanation: string;           // markdown explanation of the translation
  output: string;                // expected query result (ASCII table)
}
```

### Domain Schema Bundle

```typescript
interface DomainSchema {
  domain: string;                // matches query domain key
  ddl: string;                   // CREATE TABLE statements for the domain
  sampleData: string;            // INSERT statements for sample data
  javaModels: string;            // Java entity/DTO class definitions
}
```

### File: `web/src/data/sqlStreamQueries.js`

Exports:
- `queries: SqlStreamQuery[]` — all 18 query examples
- `domainSchemas: Record<string, DomainSchema>` — schema bundles keyed by domain
- `categories: string[]` — unique category names for filter dropdowns
- `domains: string[]` — unique domain keys for filter dropdowns
- `difficulties: string[]` — ["beginner", "intermediate", "advanced"]
- `domainLabels: Record<string, string>` — human-readable labels with emoji

Source: Copy and restructure from `sql-java-stream-learning` (`lib/queries.ts`, `sql-schema/schema.sql`, `java-models/AllModels.java`). Adapted from TypeScript to JS.

## File Organization

```
web/src/
├── data/
│   └── sqlStreamQueries.js      # All 18 queries + domain schema bundles
├── components/
│   └── sql-streams/
│       ├── SqlStreamCard.jsx     # Expandable card: SQL/Java side-by-side
│       ├── SqlStreamCard.test.jsx
│       ├── SqlStreamFilters.jsx  # Search + category/domain/difficulty
│       ├── SqlStreamFilters.test.jsx
│       └── SqlStreamSchema.jsx   # Collapsible schema & model viewer
├── pages/
│   ├── SqlStreamsPage.jsx        # Filters + card grid layout
│   └── SqlStreamsPage.test.jsx
├── router.jsx                   # Add /sql-streams route
└── sidebar.jsx                  # Add nav link
```

## Components

### SqlStreamCard

**Collapsed view:**
- Title + description
- Difficulty badge (color-coded: green/yellow/red) — reuse existing badge style
- Domain badge with emoji label
- Category label
- Expand chevron

**Expanded view:**
- Two-column grid: SQL on left (green-tinted `<pre>`), Java on right (blue-tinted `<pre>`)
- Each code block has a copy button with "Copied!" feedback (via `navigator.clipboard.writeText`)
- Syntax highlighting via existing `<pre>` styling (not CodeMirror — avoids loading editors for display-only code)
- Explanation section (blue background, book icon)
- Expected output section (terminal icon, `<pre>` block)
- "Show schema" toggle at bottom — reveals SqlStreamSchema component for the card's domain

### SqlStreamFilters

- Search input (filters by title, description, SQL, Java code)
- Category dropdown (derived from unique categories in data)
- Domain dropdown (4 domains with emoji labels)
- Difficulty dropdown (beginner / intermediate / advanced)
- Active filter badges with dismiss (X) buttons
- "Clear all filters" button when any filter active
- Results count text: "X of 18 queries"

All filtering is client-side via `useMemo` — no backend calls.

### SqlStreamSchema

- Collapsible panel shown/hidden by "Show schema" toggle on the card
- Three sub-sections with accordion/collapse:
  - **Database Schema** — DDL (CREATE TABLE)
  - **Sample Data** — INSERT statements
  - **Java Models** — Entity/DTO classes
- Each sub-section has its own copy button
- Code displayed in `<pre>` blocks matching card styling

### SqlStreamsPage

- **State:** `selectedCategory`, `selectedDomain`, `selectedDifficulty`, `searchQuery`, `expandedCards` (Set of IDs), `schemaVisibleCards` (Set of IDs)
- **Layout:** Title "SQL ↔ Java Streams" → filter panel → results count → vertically stacked card grid → empty state
- Empty state: centered icon + "No queries match your filters" message
- Footer: "Showing X of 18 SQL → Java Stream translations"

## Routing & Navigation

- Route: `/sql-streams` — renders `SqlStreamsPage`
- Sidebar: new "SQL Streams" link after "Challenge Library", with database icon

## Testing

12 tests total, following existing patterns (vitest + jsdom + @testing-library/react):

| Component | Tests |
|---|---|
| SqlStreamFilters | 4: renders all dropdowns, search filters by text, category filter works, multiple filters combine |
| SqlStreamCard | 4: renders collapsed, expands on click, shows SQL code, shows Java code |
| SqlStreamsPage | 4: renders with all cards, filters reduce results, empty state, clear filters restores all |

No backend tests needed — no new backend code.

## Implementation Order

1. Create `web/src/data/sqlStreamQueries.js` with all 18 queries and domain schema bundles
2. Create `SqlStreamCard` component + tests
3. Create `SqlStreamFilters` component + tests
4. Create `SqlStreamSchema` component
5. Create `SqlStreamsPage` + tests
6. Add `/sql-streams` route and sidebar link
7. Verify: `npm run build`, `npm run test`

## Out of Scope

- MDX inline embeds (confirmed: library page only)
- Backend API changes (data embedded in frontend)
- Java models as downloadable files (shown inline in schema toggle)
- Authentication or user progress tracking
- Adding new query examples beyond the existing 18
