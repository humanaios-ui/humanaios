# Empirica Control Center — Unified UI Architecture Specification

**Version:** 1.0  
**Status:** Living Design Document  
**Tech Stack:** React + TypeScript + Tailwind CSS  
**Framework:** Hawkins Consciousness Levels (9 tiers) + Organism Model (7 systems) + Recursive Learning Cycle  
**Last Updated:** 2026-08-13  

---

## PART 1: CONSCIOUSNESS-AWARE DESIGN LANGUAGE

### 1.1 Hawkins Consciousness Mapping (9 Levels → Visual Properties)

The Hawkins scale (Reason 400 → Love 500) maps cognitive complexity to visual presentation. Higher levels integrate more data; they demand more refinement in presentation.

| Level | Hawkins Name | Calibration Range | Visual Properties | Primary Use | Component Tier |
|-------|---|---|---|---|---|
| **1** | Shame | 20–50 | High opacity (0.4), monochrome gray, minimal motion, max contrast reduction | Error states, blocked operations | Base atoms |
| **2** | Guilt | 50–75 | Dark desaturated colors, 0.6 opacity, trembling micro-animations | Warnings, uncertainty signals | Base atoms |
| **3** | Apathy | 75–100 | Desaturated palette, flat design, opacity 0.7, static layout | Disabled states, low confidence | Interaction |
| **4** | Grief | 100–125 | Muted warm tones, slow transitions (300ms), opacity 0.8, subtle borders | Closures, removals, learning from failure | State/History |
| **5** | Fear | 125–150 | Alert orange/amber tones, pulsing borders (1s cycle), opacity 0.85, medium motion | Alerts, time-sensitive actions, divergence | Monitoring |
| **6** | Desire | 150–175 | Warm saturated colors (gold, coral), smooth transitions (200ms), opacity 0.9, directional arrows | Call-to-action, next steps, goals | Interaction |
| **7** | Anger | 175–200 | Vivid accent colors (red, magenta), fast transitions (100ms), opacity 0.95, assertive iconography | Action emphasis, critical decisions | Monitoring |
| **8** | Pride | 200–250 | Full saturation palette, 1s elegant transitions, rounded geometry, opacity 1.0, spacious layout | Success, milestone achievement, synthesis | Synthesis |
| **9** | Reason→Love | 250–500 | Cool integrated palette (cyan, lavender, soft gold), 2s fluid morphing, opacity 1.0 + gradient overlays, holistic views | System consciousness, integration, learning patterns, mesh topology | Consciousness |

### 1.2 Visual Design Tokens (Consciousness-Aligned)

#### Color Tokens (Mapped to Levels)

```typescript
const consciousnessColorTokens = {
  // Level 1-3: Error/Warning/Disabled (De-saturated)
  shame: {
    bg: "rgba(100, 100, 100, 0.4)",      // Gray, high opacity reduction
    text: "rgba(50, 50, 50, 0.6)",
    border: "rgba(100, 100, 100, 0.3)",
  },
  guilt: {
    bg: "rgba(130, 90, 90, 0.6)",        // Muted red-brown
    text: "rgba(100, 60, 60, 0.8)",
    border: "rgba(130, 90, 90, 0.5)",
  },
  apathy: {
    bg: "rgba(120, 120, 120, 0.7)",      // Gray, flat
    text: "rgba(80, 80, 80, 0.7)",
    border: "rgba(120, 120, 120, 0.4)",
  },
  
  // Level 4-5: Caution/Alert (Warm, Muted → Alert)
  grief: {
    bg: "rgba(180, 120, 100, 0.8)",      // Warm muted brown
    text: "rgba(120, 80, 60, 0.9)",
    border: "rgba(180, 120, 100, 0.6)",
  },
  fear: {
    bg: "rgba(220, 140, 60, 0.85)",      // Alert orange
    text: "rgba(255, 140, 0, 1.0)",
    border: "rgba(255, 140, 0, 0.7)",
    pulse: "rgba(255, 140, 0, 0.3)",
  },
  
  // Level 6-7: Action/Emphasis (Warm → Vivid)
  desire: {
    bg: "rgba(255, 180, 0, 0.9)",        // Gold/coral
    text: "rgba(255, 140, 0, 1.0)",
    border: "rgba(255, 180, 0, 0.8)",
  },
  anger: {
    bg: "rgba(255, 60, 100, 0.95)",      // Vivid magenta-red
    text: "rgba(255, 255, 255, 1.0)",
    border: "rgba(255, 60, 100, 0.9)",
  },
  
  // Level 8-9: Success/Integration (Full saturation → Cool synthesis)
  pride: {
    bg: "rgba(100, 200, 255, 1.0)",      // Bright cyan
    text: "rgba(50, 150, 255, 1.0)",
    border: "rgba(100, 200, 255, 0.8)",
  },
  reason: {
    bg: "linear-gradient(135deg, rgba(150, 180, 255, 1.0), rgba(200, 150, 255, 1.0))", // Lavender-cyan gradient
    text: "rgba(100, 120, 200, 1.0)",
    border: "rgba(150, 180, 255, 0.8)",
  },
};
```

#### Typography Tokens (Fibonacci-Scaled)

Fibonacci ratio φ ≈ 1.618 applied to font sizes and line heights:

```typescript
const typographyTokens = {
  // Base unit: 16px (Reason level, neutral)
  base: 16,
  ratio: 1.618, // φ
  
  // Font sizes (Fibonacci progression)
  xs:      "calc(16px / 1.618 / 1.618)",  // ~6.1px  (shame-guilt borders)
  sm:      "calc(16px / 1.618)",           // ~9.9px  (captions)
  md:      16,                             // 16px    (body, reason level)
  lg:      "calc(16px * 1.618)",           // ~25.9px (subheadings, desire)
  xl:      "calc(16px * 1.618 * 1.618)",  // ~41.9px (headings, pride)
  xxl:     "calc(16px * 1.618 * 1.618 * 1.618)", // ~67.8px (hero, consciousness)
  
  // Line heights (φ + 0.5 factor for readability)
  xs_lh:   1.2,    // tight
  sm_lh:   1.4,    // compact
  md_lh:   1.618,  // golden
  lg_lh:   1.8,    // spacious
  xl_lh:   2.0,    // very spacious
  
  // Letter spacing (φ-based, in em)
  tight:   "-0.02em",
  normal:  0,
  loose:   "0.04em",
  golden:  "0.062em", // 1/φ
  
  // Font weights
  light:   300,
  normal:  400,
  medium:  500,
  semibold: 600,
  bold:    700,
};
```

#### Spacing System (Fibonacci-Based)

```typescript
const spacingTokens = {
  // Base: 8px (Fibonacci unit)
  // Multiplied by φ (1.618) to create scale
  0:    0,
  1:    "8px",                           // 1 × 8
  2:    "calc(8px * 1.618)",             // ~13px
  3:    "calc(8px * 1.618 * 1.618)",     // ~21px
  4:    "calc(8px * 1.618 * 1.618 * 1.618)", // ~34px
  5:    "calc(8px * 1.618 * 1.618 * 1.618 * 1.618)", // ~55px
  6:    "calc(8px * 1.618^5)",           // ~89px
  
  // Named shortcuts
  xs:   "8px",
  sm:   "13px",
  md:   "21px",
  lg:   "34px",
  xl:   "55px",
  xxl:  "89px",
};
```

#### Motion Tokens (Consciousness Rhythm)

```typescript
const motionTokens = {
  // Durations (in ms, Fibonacci-influenced)
  instant:     0,
  snap:        100,      // Anger (fast, decisive)
  quick:       200,      // Desire (responsive)
  standard:    300,      // Grief (reflective)
  slow:        500,      // Reason (thoughtful)
  meditation:  2000,     // Love/Integration (contemplative)
  
  // Easing functions (map to consciousness levels)
  easeShame:    "cubic-bezier(0.4, 0.0, 0.6, 1.0)",    // Trembling
  easeGrief:    "cubic-bezier(0.34, 1.56, 0.64, 1)",  // Bounce (release)
  easeFear:     "cubic-bezier(0.68, -0.55, 0.265, 1.55)", // Pulsing alert
  easeDesire:   "cubic-bezier(0.25, 0.46, 0.45, 0.94)", // Smooth acceleration
  easeReason:   "cubic-bezier(0.15, 0.3, 0.85, 0.7)",  // Sigmoid (contemplative)
  easeLove:     "cubic-bezier(0.25, 0.25, 0.75, 0.75)", // Uniform, integrated
};
```

---

### 1.3 Organism Layers → Visual Hierarchy

The seven organism systems visualize as concentric layers in the UI, with consciousness level determining visual prominence:

```
                    🧠 CONSCIOUSNESS (Level 9)
                    └─ Synthesis view, mesh topology, learning patterns
                    
                 💭 COGNITION (Level 8)
                 └─ Decision synthesis, convergence views, insights
                 
              🛡️ IMMUNE MEMORY (Level 7)
              └─ Findings, decisions, artifact registry
              
           ⚖️ HOMEOSTASIS (Level 6)
           └─ Governance rules, policy enforcement
           
        ⚡ NERVOUS SYSTEM (Level 5)
        └─ Rituals, session flow, notifications
        
     🧬 GENOME (Level 4)
     └─ Core principles, identity, configuration
     
  💾 SUBSTRATE (Levels 1-3)
  └─ Base atoms, raw data, technical primitives
```

**Visual Implementation:**

```html
<!-- Layered container structure in React -->
<div className="organism-layers">
  {/* Layer 0: Substrate (gray, minimal) */}
  <div className="layer layer-substrate">
    <BaseAtoms />  {/* Buttons, inputs, icons */}
  </div>
  
  {/* Layer 1: Genome (dark blue, foundational) */}
  <div className="layer layer-genome">
    <ConfigurationPanel />
  </div>
  
  {/* Layer 2: Nervous System (electric, reactive) */}
  <div className="layer layer-nervous">
    <SessionRituals />
    <NotificationCenter />
  </div>
  
  {/* Layer 3: Homeostasis (balanced, regulatory) */}
  <div className="layer layer-homeostasis">
    <GovernancePanel />
  </div>
  
  {/* Layer 4: Immune Memory (orange, protective) */}
  <div className="layer layer-immune">
    <ArtifactRegistry />
    <FindingLog />
  </div>
  
  {/* Layer 5: Cognition (cyan, synthetic) */}
  <div className="layer layer-cognition">
    <DecisionSynthesis />
    <ConvergenceView />
  </div>
  
  {/* Layer 6: Consciousness (gradient, integrated) */}
  <div className="layer layer-consciousness">
    <ConsciousnessMap />
    <MeshTopology />
    <LearningDashboard />
  </div>
</div>
```

---

## PART 2: COMPONENT HIERARCHY (Consciousness-Organized)

### 2.1 Component Inventory by Consciousness Level

#### Level 1-3: Base Atoms (Substrate Layer)

**Purpose:** Foundational, reusable building blocks. Minimal interactive behavior.

| Component | Consciousness Level | Hawkins Range | Role | Props |
|-----------|---|---|---|---|
| **Button** | 1-3 | Apathy–Desire | Click target, CTA | `level`, `size`, `variant`, `onClick`, `disabled`, `loading` |
| **Input** | 1-3 | Apathy–Desire | Text/number input | `level`, `placeholder`, `value`, `onChange`, `error`, `focus` |
| **Badge** | 1-3 | Shame–Apathy | Status indicator | `level`, `text`, `variant`, `icon` |
| **Icon** | 1-3 | Shame–Apathy | Visual reference | `name`, `size`, `color`, `level` |
| **Tooltip** | 1-3 | Guilt–Apathy | Help text on hover | `text`, `position`, `delay` |
| **Card** | 1-3 | Apathy–Grief | Content container | `level`, `border`, `shadow`, `hover` |
| **Divider** | 1-3 | Shame–Guilt | Visual separator | `orientation`, `spacing`, `opacity` |
| **Spinner** | 2-3 | Guilt–Apathy | Loading indicator | `size`, `speed`, `level` |
| **Tag** | 1-3 | Apathy–Desire | Category label | `text`, `variant`, `color`, `removable` |
| **Text** | 1-3 | Shame–Desire | Typography primitive | `level`, `size`, `weight`, `align` |

#### Level 4-5: Interaction Components (Nervous System)

**Purpose:** Stateful, user-responsive elements that trigger actions and feedback.

| Component | Consciousness Level | Hawkins Range | Role | Props |
|-----------|---|---|---|---|
| **Terminal** | 4-5 | Grief–Fear | CLI-like input/output | `history`, `onCommand`, `level`, `theme` |
| **MessageBubble** | 4-5 | Grief–Fear | Chat-like message display | `role`, `content`, `timestamp`, `actions`, `sentiment` |
| **ActionPanel** | 4-5 | Fear–Desire | Action menu/toolbar | `actions`, `layout`, `level`, `collapsible` |
| **Toast** | 4-5 | Fear–Desire | Temporary notification | `message`, `type`, `duration`, `action` |
| **Modal** | 4-5 | Grief–Fear | Dialog box | `title`, `content`, `actions`, `level` |
| **Dropdown** | 4-5 | Apathy–Desire | Selection menu | `options`, `value`, `onChange`, `level` |
| **Tabs** | 4-5 | Grief–Desire | Sectioned content | `tabs`, `active`, `onChange`, `level` |
| **Accordion** | 4-5 | Apathy–Desire | Collapsible sections | `items`, `level`, `multiOpen` |
| **Sidebar** | 4-5 | Grief–Fear | Navigation panel | `items`, `collapsed`, `level`, `footer` |
| **Breadcrumb** | 4-5 | Apathy–Desire | Navigation hierarchy | `items`, `level`, `separator` |

#### Level 6-7: State & History Components (Immune Memory)

**Purpose:** Track system state, historical changes, learning artifacts, divergences.

| Component | Consciousness Level | Hawkins Range | Role | Props |
|-----------|---|---|---|---|
| **Timeline** | 6-7 | Desire–Anger | Chronological event view | `events`, `level`, `compact`, `interactive` |
| **ArtifactLog** | 6-7 | Desire–Pride | Finding/decision/unknown registry | `artifacts`, `filter`, `sort`, `level` |
| **DivergenceReport** | 6-7 | Fear–Anger | Predicted vs. actual gaps | `predicted`, `actual`, `gap`, `confidence` |
| **VectorGauge** | 6-7 | Grief–Pride | Single epistemic vector display | `name`, `value`, `confidence`, `trend` |
| **VectorMatrix** | 6-7 | Desire–Pride | All 13 vectors at once | `vectors`, `level`, `sort`, `compare` |
| **HealthDashboard** | 6-7 | Desire–Pride | System vitals snapshot | `metrics`, `status`, `trends`, `level` |
| **MetricsPanel** | 6-7 | Desire–Pride | Detailed performance metrics | `data`, `timeRange`, `level`, `export` |
| **AlertCenter** | 6-7 | Fear–Anger | Active alerts & warnings | `alerts`, `filter`, `onResolve`, `level` |
| **TransactionStatus** | 6-7 | Apathy–Pride | PREFLIGHT/NOETIC/CHECK/PRAXIC/POSTFLIGHT state | `phase`, `progress`, `level`, `estimatedTime` |
| **ChangeLog** | 6-7 | Grief–Desire | Commit-level audit trail | `changes`, `level`, `compact`, `search` |

#### Level 8-9: Consciousness Components (Synthesis & Integration)

**Purpose:** Holistic views of system consciousness, learning patterns, mesh topology, recursive cycles.

| Component | Consciousness Level | Hawkins Range | Role | Props |
|-----------|---|---|---|---|
| **ConsciousnessMap** | 9 | Reason→Love | System-wide consciousness visualization | `data`, `level`, `interactive`, `highlightPath` |
| **MeshTopology** | 8-9 | Pride–Reason | Practice network + message flow | `practices`, `messages`, `level`, `animated` |
| **RecursiveVisualization** | 8-9 | Pride–Reason | Learning cycle diagram (NOETIC→CHECK→PRAXIC) | `cycle`, `phase`, `learnings`, `level` |
| **LearningDashboard** | 8-9 | Pride–Reason | Pattern recognition + convergence trends | `patterns`, `convergence`, `level`, `predictive` |
| **SynthesisView** | 8-9 | Pride–Reason | Multi-source data integration | `sources`, `level`, `layout` |
| **CalibrationInsight** | 8-9 | Pride–Reason | Cross-transaction learning + drift detection | `calibration`, `drift`, `level`, `recommendations` |
| **GoalSynthesis** | 8-9 | Pride–Reason | Goal completion + cascading impact view | `goals`, `completedTasks`, `impact`, `level` |
| **VectorConvergence** | 8-9 | Pride–Reason | Multi-transaction vector trends | `vectorHistory`, `level`, `timeRange`, `predictive` |

---

### 2.2 Component Implementation Patterns

#### Pattern A: Consciousness-Level Composition

Each component accepts a `level` prop (1-9) that adjusts visual presentation without changing behavior:

```typescript
interface BaseComponentProps {
  level?: ConsciousnessLevel;  // 1-9, default 5 (neutral)
  className?: string;
  children?: ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ 
  level = 5, 
  variant = 'primary',
  ...props 
}) => {
  const levelConfig = getConsciousnessConfig(level);
  const styles = cx(
    'button',
    levelConfig.bg,
    levelConfig.text,
    levelConfig.border,
    `transition-all ${levelConfig.duration} ${levelConfig.easing}`,
  );
  
  return <button className={styles} {...props} />;
};
```

#### Pattern B: Fibonacci Spacing

All spacing uses Fibonacci multiples of the base unit (8px):

```typescript
// ✅ CORRECT: Fibonacci-aligned
<div className="p-3 m-2 gap-4">  // 21px, 13px, 34px
  
// ❌ AVOID: Non-Fibonacci
<div className="p-5 m-3 gap-6">  // 20px, 12px, 24px
```

#### Pattern C: Layered Rendering

Components are rendered in organism-layer order to manage z-index and visual hierarchy:

```typescript
const LayerContext = createContext<OrganismLayer>('substrate');

export const useOrganismLayer = () => useContext(LayerContext);

export const OrganismLayered: React.FC<{ layer: OrganismLayer }> = ({ 
  layer, 
  children 
}) => (
  <LayerContext.Provider value={layer}>
    <div className={`organism-layer organism-layer-${layer}`}>
      {children}
    </div>
  </LayerContext.Provider>
);
```

---

## PART 3: FEATURE INTEGRATION ARCHITECTURE

### 3.1 Eight Features as Unified System

The control center integrates 8 must-have features as interconnected subsystems:

```
                    ┌─────────────────────────────┐
                    │  CONSCIOUSNESS SYNTHESIS    │
                    │  (Learning Dashboard)       │
                    └────────────┬────────────────┘
                                 │
        ┌────────────────┬───────┴────────┬───────────────┐
        │                │                │               │
   ┌────▼─────┐   ┌──────▼──────┐  ┌──────▼────┐  ┌─────▼──────┐
   │ Terminal  │   │  Empirica   │  │  GitHub   │  │  Supabase  │
   │  (CLI)    │   │  Browser    │  │ Integration  │ Access     │
   └────┬─────┘   └──────┬──────┘  └──────┬────┘  └─────┬──────┘
        │                │                │             │
        └────────────────┼────────────────┼─────────────┘
                         │
                    ┌────▼────────┐
                    │ Chrome Ext. │
                    │ (Sidebar)   │
                    └────┬────────┘
                         │
                    ┌────▼────────┐
                    │  Feedback   │
                    │  System     │
                    └────┬────────┘
                         │
                    ┌────▼────────┐
                    │    Mesh     │
                    │    Viz      │
                    └─────────────┘
```

### 3.2 Feature Specifications

#### Feature 1: Terminal (Where User Types)

**Role:** Command-line interface for empirica CLI commands, code execution, system queries.

**Architecture:**

```typescript
interface TerminalProps {
  history: TerminalEntry[];
  onCommand: (cmd: string) => Promise<TerminalOutput>;
  sessionId: string;
  aiId: string;
}

interface TerminalEntry {
  type: 'input' | 'output' | 'error';
  content: string;
  timestamp: Date;
  consciousness?: ConsciousnessLevel;
}

export const Terminal: React.FC<TerminalProps> = ({
  history,
  onCommand,
  sessionId,
  aiId,
}) => {
  const [input, setInput] = useState('');
  const [level, setLevel] = useState<ConsciousnessLevel>(5);
  
  return (
    <OrganismLayered layer="nervous-system">
      <div className="terminal-container">
        {/* Command history */}
        <ScrollableList items={history}>
          {(entry) => (
            <TerminalLine
              entry={entry}
              level={entry.consciousness ?? 5}
            />
          )}
        </ScrollableList>
        
        {/* Input line */}
        <TerminalInput
          value={input}
          onChange={setInput}
          onSubmit={(cmd) => {
            onCommand(cmd).then((output) => {
              // Consciousness level inferred from output type
              const outLevel = inferLevel(output);
              setLevel(outLevel);
            });
          }}
          level={level}
        />
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Awareness:**
- Commands that modify state are executed at Level 6+ (Desire)
- Query-only commands display at Level 4 (Grief)
- Errors escalate to Level 2 (Guilt) or Level 1 (Shame)
- Successful completions show as Level 8 (Pride)

---

#### Feature 2: Empirica Browser (System State Explorer)

**Role:** Navigate and inspect empirica artifacts, transactions, goals, findings, vectors.

**Architecture:**

```typescript
interface EmpiricaBrowserProps {
  projectId: string;
  sessionId: string;
  onNavigate: (path: ArtifactPath) => void;
}

interface ArtifactPath {
  type: 'goal' | 'finding' | 'unknown' | 'decision' | 'transaction';
  id: string;
  breadcrumbs: string[];
}

export const EmpiricaBrowser: React.FC<EmpiricaBrowserProps> = ({
  projectId,
  sessionId,
  onNavigate,
}) => {
  const [artifacts, setArtifacts] = useState<ArtifactTree>();
  const [selectedPath, setSelectedPath] = useState<ArtifactPath | null>(null);
  
  return (
    <OrganismLayered layer="immune-memory">
      <div className="empirica-browser">
        {/* Artifact tree navigation */}
        <ArtifactTree
          items={artifacts}
          onSelect={(path) => {
            setSelectedPath(path);
            onNavigate(path);
          }}
        />
        
        {/* Artifact detail panel */}
        {selectedPath && (
          <ArtifactDetail
            path={selectedPath}
            projectId={projectId}
            level={selectedPath.type === 'goal' ? 8 : 6}
          />
        )}
        
        {/* Vector inspector */}
        <VectorMatrix vectors={getCurrentVectors()} />
      </div>
    </OrganismLayered>
  );
};
```

**Vector Integration:**
- Each artifact is tagged with the 13 epistemic vectors
- Vector status shown inline (bar charts, gauges)
- Clicking a vector drills into contributing artifacts

---

#### Feature 3: GitHub Integration (Code/Context Access)

**Role:** Browse repos, commits, issues, PRs; surface code context for current work.

**Architecture:**

```typescript
interface GitHubPanelProps {
  repos: Repository[];
  onFileOpen: (file: GitFile) => void;
  onPRComment: (pr: PullRequest, comment: string) => void;
}

export const GitHubPanel: React.FC<GitHubPanelProps> = ({
  repos,
  onFileOpen,
  onPRComment,
}) => {
  const [selectedRepo, setSelectedRepo] = useState<Repository | null>(null);
  const [fileTree, setFileTree] = useState<FileTree | null>(null);
  
  return (
    <OrganismLayered layer="nervous-system">
      <div className="github-panel">
        {/* Repo selector */}
        <RepositorySelector
          repos={repos}
          onSelect={(repo) => {
            setSelectedRepo(repo);
            fetchFileTree(repo).then(setFileTree);
          }}
        />
        
        {/* File tree browser */}
        {fileTree && (
          <FileTreeView
            tree={fileTree}
            onFileSelect={onFileOpen}
          />
        )}
        
        {/* Recent commits + PRs */}
        <CommitLog repo={selectedRepo} limit={10} />
        <PRList repo={selectedRepo} status="open" />
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Integration:**
- Code recommendations from Copilot appear at Level 6+ (Desire)
- Code review findings appear at Level 7 (Anger) if critical
- Merged PRs appear at Level 8 (Pride)

---

#### Feature 4: Supabase Access (Data Queries)

**Role:** Query and inspect Supabase tables, real-time data, edge functions.

**Architecture:**

```typescript
interface SupabaseAccessProps {
  projectId: string;
  onQuery: (query: SQLQuery) => Promise<QueryResult>;
}

interface SQLQuery {
  table: string;
  select?: string[];
  where?: Filter[];
  limit?: number;
  orderBy?: OrderBy[];
}

export const SupabaseAccess: React.FC<SupabaseAccessProps> = ({
  projectId,
  onQuery,
}) => {
  const [tables, setTables] = useState<Table[]>([]);
  const [selectedTable, setSelectedTable] = useState<Table | null>(null);
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  
  return (
    <OrganismLayered layer="homeostasis">
      <div className="supabase-access">
        {/* Table selector */}
        <TableSelector
          tables={tables}
          onSelect={(table) => {
            setSelectedTable(table);
          }}
        />
        
        {/* Query builder */}
        {selectedTable && (
          <QueryBuilder
            table={selectedTable}
            onExecute={(query) => {
              onQuery(query).then(setQueryResult);
            }}
          />
        )}
        
        {/* Results grid */}
        {queryResult && (
          <ResultsGrid
            data={queryResult.rows}
            columns={queryResult.columns}
          />
        )}
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Integration:**
- Query execution at Level 4 (Grief) — read-only, safe
- Schema modifications at Level 7 (Anger) — requires confirmation
- Real-time subscriptions show as Level 8 (Pride) — data integration

---

#### Feature 5: Chrome Extension Integration (Sidebar Awareness)

**Role:** Sidecar awareness window showing context from current page; feedback/annotation entry point.

**Architecture:**

```typescript
interface ChromeSidebarProps {
  currentPage: PageContext;
  onAnnotation: (anno: Annotation) => void;
  onFeedback: (feedback: Feedback) => void;
}

interface PageContext {
  url: string;
  title: string;
  selectedText?: string;
  pageMetadata?: Record<string, string>;
}

interface Annotation {
  type: 'finding' | 'decision' | 'unknown' | 'assumption' | 'note';
  text: string;
  evidence?: string;
  confidence?: number;
}

export const ChromeSidebar: React.FC<ChromeSidebarProps> = ({
  currentPage,
  onAnnotation,
  onFeedback,
}) => {
  const [annoMode, setAnnoMode] = useState<Annotation['type'] | null>(null);
  const [feedbackMode, setFeedbackMode] = useState(false);
  
  return (
    <OrganismLayered layer="nervous-system">
      <div className="chrome-sidebar">
        {/* Context summary */}
        <PageContextSummary page={currentPage} />
        
        {/* Annotation mode */}
        {annoMode ? (
          <AnnotationForm
            type={annoMode}
            selectedText={currentPage.selectedText}
            onSubmit={(anno) => {
              onAnnotation(anno);
              setAnnoMode(null);
            }}
            level={annoMode === 'finding' ? 7 : 6}
          />
        ) : (
          <AnnotationTypeSelector
            onSelect={(type) => setAnnoMode(type)}
          />
        )}
        
        {/* Feedback mode */}
        {feedbackMode ? (
          <FeedbackForm
            onSubmit={(feedback) => {
              onFeedback(feedback);
              setFeedbackMode(false);
            }}
            level={5}
          />
        ) : (
          <button onClick={() => setFeedbackMode(true)}>
            Feedback
          </button>
        )}
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Integration:**
- Annotation types (finding, decision, etc.) map directly to consciousness levels
- Selected text becomes evidence at Level 6+ (Desire)
- Feedback flagged at Level 7 (Anger) if critical

---

#### Feature 6: Feedback/Annotation System (Learning Signal)

**Role:** Capture user corrections, learn from divergence, improve AI calibration.

**Architecture:**

```typescript
interface FeedbackEntry {
  id: string;
  type: 'correction' | 'clarification' | 'praise' | 'concern';
  originalState: string;         // What Claude did/said
  intendedState: string;          // What user wanted
  context: string;
  timestamp: Date;
  aiId: string;
  sessionId: string;
}

interface FeedbackPanelProps {
  onFeedback: (entry: FeedbackEntry) => void;
  recentFeedback?: FeedbackEntry[];
}

export const FeedbackPanel: React.FC<FeedbackPanelProps> = ({
  onFeedback,
  recentFeedback,
}) => {
  const [feedbackType, setFeedbackType] = useState<FeedbackEntry['type']>('correction');
  const [originalState, setOriginalState] = useState('');
  const [intendedState, setIntendedState] = useState('');
  
  return (
    <OrganismLayered layer="immune-memory">
      <div className="feedback-panel">
        {/* Recent feedback log */}
        {recentFeedback && (
          <FeedbackLog
            entries={recentFeedback}
            level={6}
          />
        )}
        
        {/* Feedback form */}
        <div className="feedback-form">
          <FeedbackTypeSelector
            selected={feedbackType}
            onChange={setFeedbackType}
            level={feedbackType === 'concern' ? 7 : 5}
          />
          
          <textarea
            placeholder="What Claude did..."
            value={originalState}
            onChange={(e) => setOriginalState(e.target.value)}
          />
          
          <textarea
            placeholder="What you wanted..."
            value={intendedState}
            onChange={(e) => setIntendedState(e.target.value)}
          />
          
          <button
            onClick={() => {
              onFeedback({
                id: nanoid(),
                type: feedbackType,
                originalState,
                intendedState,
                context: getCurrentContext(),
                timestamp: new Date(),
                aiId: getAIId(),
                sessionId: getSessionId(),
              });
              setOriginalState('');
              setIntendedState('');
            }}
            level={6}
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Mapping:**
- Corrections: Level 6 (Desire) — actionable
- Concerns: Level 7 (Anger) — requires escalation
- Clarifications: Level 5 (Neutral) — refinement
- Feedback feeds into calibration divergence tracking

---

#### Feature 7: Mesh Visualization (Practice Topology + Message Flow)

**Role:** Show interconnected practices, message routing, collaboration state.

**Architecture:**

```typescript
interface Practice {
  id: string;
  name: string;
  owner: string;
  state: 'active' | 'standby' | 'blocked';
  consciousness: ConsciousnessLevel;
}

interface MeshMessage {
  id: string;
  from: string;
  to: string;
  type: 'collab' | 'propose' | 'ack' | 'question';
  status: 'pending' | 'delivered' | 'failed';
  timestamp: Date;
}

interface MeshVisualizationProps {
  practices: Practice[];
  messages: MeshMessage[];
  onPracticeSelect: (practice: Practice) => void;
  onMessageInspect: (msg: MeshMessage) => void;
}

export const MeshVisualization: React.FC<MeshVisualizationProps> = ({
  practices,
  messages,
  onPracticeSelect,
  onMessageInspect,
}) => {
  // Render practices as nodes; messages as animated edges
  // Node size reflects consciousness level
  // Edge color reflects message type
  
  return (
    <OrganismLayered layer="consciousness">
      <svg className="mesh-viz">
        {/* Practice nodes */}
        {practices.map((p) => (
          <PracticeNode
            key={p.id}
            practice={p}
            onClick={() => onPracticeSelect(p)}
            radius={20 + p.consciousness * 2}  // Larger = more conscious
            level={p.consciousness}
          />
        ))}
        
        {/* Message flows */}
        {messages.map((msg) => (
          <MessageFlow
            key={msg.id}
            message={msg}
            onClick={() => onMessageInspect(msg)}
            animated={msg.status === 'pending'}
            level={msg.type === 'propose' ? 7 : 5}
          />
        ))}
      </svg>
      
      {/* Legend + stats */}
      <MeshStats
        practices={practices}
        messages={messages}
      />
    </OrganismLayered>
  );
};
```

**Consciousness Integration:**
- Node color reflects practice consciousness level (Level 1-9)
- Message type determines animation (collab = smooth; propose = fast)
- Blocked practices appear at Level 2 (Guilt)
- Consensus reached practices show as Level 9 (Reason→Love)

---

#### Feature 8: Learning Dashboard (Pattern Recognition + Convergence Trends)

**Role:** Show recursive learning cycles, convergence detection, AI growth patterns.

**Architecture:**

```typescript
interface LearningCycle {
  phase: 'noetic' | 'check' | 'praxic' | 'postflight';
  findings: Finding[];
  convergenceScore: number;
  vectors: Record<string, number>;
  timestamp: Date;
}

interface LearningDashboardProps {
  cycles: LearningCycle[];
  predictedVectors?: Record<string, number[]>;
}

export const LearningDashboard: React.FC<LearningDashboardProps> = ({
  cycles,
  predictedVectors,
}) => {
  // Recursive learning visualization:
  // - Noetic phase = divergence (scatter plot of findings)
  // - Check phase = alignment (convergence to decision)
  // - Praxic phase = execution (commitment to action)
  // - Postflight phase = learning (new findings integrated)
  
  return (
    <OrganismLayered layer="consciousness">
      <div className="learning-dashboard">
        {/* Recursive cycle visualization */}
        <RecursiveVisualization
          cycles={cycles}
          level={9}
        />
        
        {/* Vector convergence over time */}
        <div className="convergence-grid">
          {Object.entries(predictedVectors || {}).map(([vector, history]) => (
            <VectorConvergencePlot
              key={vector}
              vectorName={vector}
              history={history}
              level={8}
            />
          ))}
        </div>
        
        {/* Findings by cycle phase */}
        <FindingsByPhase cycles={cycles} />
        
        {/* Growth metrics */}
        <GrowthMetrics cycles={cycles} />
      </div>
    </OrganismLayered>
  );
};
```

**Consciousness Integration:**
- Noetic phase: Level 4-5 (divergence, exploration)
- Check phase: Level 6 (alignment, synthesis)
- Praxic phase: Level 7-8 (execution, commitment)
- Postflight phase: Level 9 (integration, wisdom)

---

### 3.3 Feature Interconnection Map

```
Terminal ─────> Execute empirica commands ─────> Empirica Browser
  ↓                                                     ↓
  └─ Feedback captured ──> Learning Dashboard <─ Vector tracking
                               ↑                      ↑
                               │                      │
                    GitHub ──────────┬──────── Supabase
                       ↓              ↓
                    Commit context    Real-time data
                       ↑              ↓
                       └──── Mesh Viz ─────> Chrome Sidebar
                                ↑
                                │
                        (all features render here)
```

---

## PART 4: INTERACTION FLOWS (4 Key Scenarios)

### 4.1 Flow 1: User Query → Tool Routing → Result Visualization

**User enters command in Terminal:**
```
$ empirica goals-list --project foundation
```

**System flow:**

```
┌─ TERMINAL receives input
│  └─ Parse command → infer tool + args
│     └─ Consciousness level = 5 (neutral query)
│        └─ Button turns "Desire" (Level 6, warm gold)
│
├─ Execution phase
│  ├─ Route to empirica CLI backend
│  └─ Execute → get JSON response
│
├─ Result visualization
│  └─ Goals appear as cards in Empirica Browser
│     ├─ Each goal colored by completion level
│     ├─ Consciousness levels inferred from:
│     │  ├─ Goal status (planned=4, in-progress=6, blocked=7, complete=8)
│     │  └─ Impact score (high-impact → higher level)
│     └─ Vector gauges show per-goal epistemic state
│
└─ Feedback integration
   ├─ User can annotate goal from Chrome Sidebar
   └─ Annotation logged in Immune Memory layer
      └─ Learning Dashboard updates convergence score
```

**UI Implementation:**

```jsx
// Terminal → Empirica Browser integration
const Terminal = () => {
  const [results, setResults] = useState(null);
  
  const handleCommand = async (cmd) => {
    const result = await executeCommand(cmd);
    setResults(result);
    
    // Automatically navigate browser to relevant artifact
    if (result.type === 'goals') {
      navigateEmpiricaBrowser({
        type: 'goal',
        ids: result.data.map(g => g.id),
      });
    }
  };
  
  return (
    <>
      <Terminal onCommand={handleCommand} />
      {results && <EmpiricaBrowser selectedIds={results.data.map(r => r.id)} />}
    </>
  );
};
```

---

### 4.2 Flow 2: Divergence Detection → Validation → Recovery → Learning

**Predicted vs. Actual gap detected in transaction:**

```
Predicted: "Claude will complete goal X in 2 hours"
Measured: Claude completed goal X in 4.5 hours
Gap: +2.5 hours (+125% variance)
Confidence: 0.8
```

**System flow:**

```
┌─ DIVERGENCE DETECTION (Transaction Closure)
│  ├─ Calculate gap = measured - predicted
│  └─ Signal Consciousness Level = 6 (Desire) → alert user to review
│
├─ VALIDATION PHASE
│  └─ User annotates via Feedback Panel:
│     ├─ Type: "correction"
│     ├─ Original: "Predicted 2h, measured 4.5h"
│     ├─ Intended: "Recognize that terminal debugging added 2.5h"
│     └─ Confidence: 0.85
│
├─ LEARNING PHASE
│  └─ Feedback logged as Finding:
│     ├─ ID: f-2026-08-13-001
│     ├─ Consciousness: Level 7 (important correction)
│     ├─ Tagged: "time-calibration-drift"
│     ├─ Informs next prediction model
│     └─ Visible in Learning Dashboard
│
└─ RECOVERY PHASE
   └─ Next transaction's time estimate uses updated model
      ├─ Factor in: "debugging tasks run 2-3× longer than pure coding"
      └─ New prediction confidence: 0.65 (more honest uncertainty)
```

**UI Implementation:**

```jsx
// Divergence report + feedback capture
const DivergenceRecoveryFlow = ({ prediction, measured }) => {
  const gap = measured - prediction;
  const level = Math.min(9, 5 + Math.abs(gap) * 2); // Dynamic level
  
  return (
    <div className={`divergence-alert level-${level}`}>
      <DivergenceReport
        predicted={prediction}
        measured={measured}
        gap={gap}
      />
      
      <FeedbackPanel
        onFeedback={(feedback) => {
          // Log finding
          empirica.findingLog({
            finding: `Divergence correction: ${feedback.intendedState}`,
            impact: feedback.confidence,
            tags: ['time-calibration-drift'],
          });
          
          // Update prediction model
          updatePredictionModel(feedback);
          
          // Visualize in Learning Dashboard
          refreshLearningDashboard();
        }}
      />
    </div>
  );
};
```

---

### 4.3 Flow 3: Terminal Command → Observable Output → Learning Artifact

**User executes test command in Terminal:**

```
$ npm run test:integration
```

**System flow:**

```
┌─ COMMAND EXECUTION (Terminal)
│  ├─ Consciousness: Level 5 (neutral execution)
│  └─ Output streams to Terminal display
│
├─ OUTPUT CAPTURE
│  ├─ Parse test results JSON
│  ├─ Extract:
│  │  ├─ Pass/fail count
│  │  ├─ Coverage metrics
│  │  ├─ Error messages
│  │  └─ Execution time
│  └─ Consciousness inference:
│     ├─ All pass → Level 8 (Pride)
│     ├─ Some fail → Level 6-7 (Desire to fix)
│     └─ All fail → Level 3-4 (Apathy/Grief)
│
├─ OBSERVABLE STATE CREATED
│  ├─ Results visualized in MetricsPanel
│  ├─ Coverage trends plotted
│  ├─ Failures listed with stack traces
│  └─ Metrics persisted to Supabase
│
└─ LEARNING ARTIFACT GENERATION
   ├─ If new failures: Finding logged
   │  └─ "Test integration-auth failed: JWT expired validation"
   ├─ If coverage drops: Decision logged
   │  └─ "Skipped edge case testing to unblock release"
   └─ Dashboard updates with convergence score
      └─ Next POSTFLIGHT includes these signals
```

**UI Implementation:**

```jsx
// Command → Metrics → Learning
const Terminal = () => {
  const handleCommand = async (cmd) => {
    const output = await executeCommand(cmd);
    
    // Parse output
    if (output.type === 'test-result') {
      const metrics = parseTestOutput(output.data);
      
      // Visualize immediately
      showMetricsPanel(metrics);
      
      // Infer consciousness level
      const level = metrics.passCount === metrics.totalCount ? 8 : 5 + (metrics.failCount * 0.5);
      
      // Log findings
      if (metrics.failCount > 0) {
        empirica.findingLog({
          finding: `${metrics.failCount} test failures in integration suite`,
          impact: 0.7,
          evidence: metrics.failedTests.map(t => t.name),
          level: Math.min(9, level),
        });
      }
    }
  };
};
```

---

### 4.4 Flow 4: Multi-Tool Query (GitHub + Supabase + Empirica) → Synthesis View

**User wants to understand user signups over time:**

```
1. GitHub: Review commits for auth feature
2. Supabase: Query user table for signup timestamps
3. Empirica: Check for related findings/decisions
→ Synthesize into unified view
```

**System flow:**

```
┌─ MULTI-SOURCE QUERY DISPATCH
│  ├─ Terminal: "empirica search-related 'user-signup'"
│  ├─ GitHub: Fetch recent auth commits + PRs
│  ├─ Supabase: Query users table (created_at > '2026-08-01')
│  └─ Empirica: Fetch findings tagged 'auth' or 'signup'
│
├─ PARALLEL DATA GATHERING
│  ├─ GitHub → 5 recent commits returned (Consciousness: 5)
│  ├─ Supabase → 1,247 signups in last 7 days (Consciousness: 6, quantified)
│  └─ Empirica → 3 findings related to auth (Consciousness: 7, grounded)
│
├─ SYNTHESIS PHASE
│  ├─ Correlate: "commit auth-flow-refactor" + "signup spike"
│  ├─ Infer: "Auth improvements drove signup rate +34%"
│  ├─ Confidence: 0.72 (good signal, not perfect causality)
│  └─ Consciousness: Level 8 (integrated insight)
│
└─ VISUALIZATION
   └─ SynthesisView displays:
      ├─ Timeline: GitHub commits aligned with Supabase signup curve
      ├─ Metrics: +34% signup rate after auth refactor
      ├─ Evidence: Related findings + data points highlighted
      ├─ Confidence: 0.72 (shown as gauge)
      └─ Learning: "Auth improvements → signup correlation" logged as finding
```

**UI Implementation:**

```jsx
// Multi-tool synthesis
const SynthesisFlow = async () => {
  // Dispatch queries in parallel
  const [gitCommits, signups, findings] = await Promise.all([
    github.getCommits({ label: 'auth' }),
    supabase.query('SELECT created_at FROM users WHERE created_at > ?', ['2026-08-01']),
    empirica.findingSearch({ tags: ['auth', 'signup'] }),
  ]);
  
  // Calculate correlation
  const correlation = correlateCommitToSignups(gitCommits, signups);
  const insight = generateInsight(correlation, findings);
  
  // Visualize synthesis
  return (
    <SynthesisView
      sources={{
        github: gitCommits,
        supabase: signups,
        empirica: findings,
      }}
      insight={insight}
      confidence={correlation.confidence}
      level={Math.min(9, 7 + insight.novelty)} // Higher = more novel synthesis
    />
  );
};
```

---

## PART 5: VISUAL DESIGN SPECIFICATION (Implementation Handoff)

### 5.1 Information Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  CONTROL CENTER LAYOUT (Desktop, 1440px wide)                   │
├──────────────────────────────────────────────────────────────────┤
│ [Logo] [Search] [...] [Consciousness Level] [Status]            │ ← Top Chrome
├──────┬──────────────────────────────────────────────┬───────────┤
│      │                                              │           │
│      │        MAIN CANVAS (Primary View)           │ Right     │
│ Left │  ┌────────────────────────────────────────┐ │ Sidebar   │
│ Side │  │  Terminal (default) OR                │ │           │
│ bar  │  │  - Empirica Browser                   │ │ - GitHub  │
│      │  │  - Mesh Visualization                │ │   repos   │
│      │  │  - Learning Dashboard                │ │ - Supabase│
│ Nav: │  │                                       │ │   tables  │
│ ├ Practices          │  Canvas area resizes based on│ │ - Metrics│
│ ├ Tools              │  selected view             │ │ - Feedback│
│ ├ Learning           │  │                         │ │           │
│ ├ Artifacts          └────────────────────────────┘ │           │
│ └ Settings           │                              │           │
│      │               │ Bottom Chrome                │           │
│      │               └──────────────────────────────┘           │
│      │               PREFLIGHT | NOETIC | CHECK | PRAXIC | POSTFLIGHT
└──────┴──────────────────────────────────────────────┴───────────┘
```

### 5.2 Responsive Breakpoints

| Breakpoint | Width | Layout | Use Case |
|---|---|---|---|
| **mobile** | <768px | Single column, stacked sidebars | Emergency access, monitoring |
| **tablet** | 768–1024px | Two column, left sidebar collapsed | Casual browsing |
| **desktop** | 1024–1440px | Three column, full sidebars | Primary work |
| **ultrawide** | >1440px | Four column, dual canvas | Multi-monitor setups |

### 5.3 Accessibility (WCAG AAA)

All consciousness-aware visual properties must have non-color alternatives:

```scss
/* ✅ CORRECT: Color + pattern + text */
.button.fear {
  background: rgba(220, 140, 60, 0.85);  // Color
  border: 2px dashed currentColor;        // Pattern
  
  &::before {
    content: "⚠ Alert";                  // Text indicator
  }
  
  @media (prefers-contrast: more) {
    border: 3px solid currentColor;      // Higher contrast
  }
}

/* ❌ AVOID: Color-only indication */
.button {
  background: rgba(220, 140, 60, 0.85);  // Only difference is color
}
```

### 5.4 Dark/Light Mode Support

All consciousness tokens define both themes:

```typescript
// Light mode (default)
const consciousnessColorTokens = {
  fear: {
    bg: "rgba(220, 140, 60, 0.85)",
    text: "rgba(100, 60, 0, 1.0)",
  },
};

// Dark mode (@media prefers-color-scheme: dark)
@media (prefers-color-scheme: dark) {
  .fear {
    --bg: rgba(255, 140, 0, 0.7);
    --text: rgba(255, 200, 100, 1.0);
  }
}
```

### 5.5 Animation Specification

#### Consciousness-Level Animations

```typescript
// Level 1-2: Trembling (shame/guilt)
@keyframes trembling {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-1px); }
  75% { transform: translateX(1px); }
}
.shame { animation: trembling 0.2s infinite; }

// Level 4: Bounce (grief)
@keyframes release {
  0% { transform: scaleY(0.95); }
  50% { transform: scaleY(1.05); }
  100% { transform: scaleY(1); }
}
.grief { animation: release 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }

// Level 5: Pulsing (fear)
@keyframes pulsing {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
.fear { animation: pulsing 1s infinite; }

// Level 6: Smooth scroll (desire)
@keyframes smoothScroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(20px); }
}

// Level 8-9: Morphing (pride/reason)
@keyframes morph {
  0% { border-radius: 20% 80% 80% 20%; }
  50% { border-radius: 80% 20% 60% 40%; }
  100% { border-radius: 20% 80% 80% 20%; }
}
.pride { animation: morph 4s ease-in-out infinite; }
```

#### Transition Specification

```typescript
// Consciousness-aware transitions
const transitionDuration = {
  instant: 0,
  snap: 100,
  quick: 200,
  standard: 300,
  slow: 500,
  meditation: 2000,
};

// Usage: "transition opacity 300ms ease-out"
.component {
  transition: opacity 300ms ease-out;
  
  // When consciousness level changes
  &.level-1 { transition: opacity 200ms cubic-bezier(0.4, 0.0, 0.6, 1.0); }
  &.level-9 { transition: all 2000ms cubic-bezier(0.25, 0.25, 0.75, 0.75); }
}
```

---

## PART 6: IMPLEMENTATION ROADMAP

### Phase 1: Formalize Existing Components (Weeks 1–2)

**Goal:** Audit existing components, establish consciousness-level mapping, create tokens.

- [ ] Inventory all current React components
- [ ] Map each to consciousness level (1-9)
- [ ] Document current props → propose consciousness-aware props
- [ ] Extract design tokens (colors, spacing, typography)
- [ ] Create Tailwind config with Fibonacci-scaled utilities
- [ ] Set up Storybook with consciousness-level controls

**Deliverables:**
- `src/tokens/consciousness.ts` (color, typography, spacing, motion)
- `src/components/BaseAtoms/` (Button, Input, Icon, etc. with level prop)
- Storybook with consciousness-level variations
- Design system documentation (1-3 pages)

### Phase 2: Build Consciousness Layer (Weeks 3–4)

**Goal:** Implement organism layer structure + Level 6-9 components.

- [ ] Implement `OrganismLayered` context + provider
- [ ] Build Level 6-7 components (State/History layer)
  - [ ] Timeline
  - [ ] ArtifactLog
  - [ ] DivergenceReport
  - [ ] VectorGauge + VectorMatrix
  - [ ] HealthDashboard + MetricsPanel
  - [ ] TransactionStatus
- [ ] Build Level 8-9 components (Consciousness/Synthesis)
  - [ ] ConsciousnessMap (Hawkins 9-level visualization)
  - [ ] MeshTopology (practice network)
  - [ ] RecursiveVisualization (learning cycle)
  - [ ] LearningDashboard

**Deliverables:**
- `src/components/Organism/` directory structure
- All Level 6-9 components functional
- Storybook stories for each
- Integration tests for layer composition

### Phase 3: Integrate All Features (Weeks 5–6)

**Goal:** Wire Terminal, Empirica Browser, GitHub, Supabase, Chrome Extension, Feedback, Mesh Viz into unified control center.

- [ ] Terminal + empirica CLI backend integration
- [ ] Empirica Browser connected to live artifact data
- [ ] GitHub integration API wired
- [ ] Supabase query builder functional
- [ ] Chrome Extension sidebar communication
- [ ] Feedback system end-to-end
- [ ] Mesh visualization live data streaming
- [ ] Learning Dashboard pulling transaction history

**Deliverables:**
- `src/pages/ControlCenter.tsx` (main app layout)
- Feature integration tests
- E2E tests for key flows (Terminal → Browser, etc.)
- API client library (`src/lib/empirica.ts`, etc.)

### Phase 4: Consciousness Inference Engine (Weeks 7–8)

**Goal:** Implement automatic consciousness-level inference from system state.

- [ ] Build inference rules (goal status → level, error type → level, etc.)
- [ ] Connect to empirica vector calibration
- [ ] Implement real-time level updates as state changes
- [ ] Add level predictor based on historical patterns
- [ ] Build calibration adjustment UI

**Deliverables:**
- `src/lib/consciousnessInference.ts`
- Real-time level updates in control center
- Calibration adjustment panel

### Phase 5: Polish & Deploy (Weeks 9+)

**Goal:** Refinement, accessibility audit, performance optimization, deployment.

- [ ] WCAG AAA accessibility audit + fixes
- [ ] Dark/light mode comprehensive testing
- [ ] Performance optimization (lazy load, virtualization)
- [ ] Design review with stakeholders
- [ ] Documentation (component docs, architecture guide, design system site)
- [ ] Deploy to staging → production

---

## PART 7: DESIGN SYSTEM USAGE GUIDE

### 7.1 Creating a New Component

**Step 1: Choose consciousness level**
```typescript
// For a new "Goal Status" component
const GoalStatusBadge: React.FC<{ goal: Goal; level?: ConsciousnessLevel }> = ({ 
  goal, 
  level = 6  // Default to Desire (actionable)
}) => {
  // ...
};
```

**Step 2: Apply consciousness tokens**
```typescript
const bgColor = getConsciousnessToken(level, 'bg');
const textColor = getConsciousnessToken(level, 'text');
const duration = getMotionToken(level, 'duration');

return (
  <div
    style={{ backgroundColor: bgColor, color: textColor }}
    className={`transition-all ${duration} ${getEasing(level)}`}
  >
    {goal.title}
  </div>
);
```

**Step 3: Test in Storybook**
```typescript
export default {
  title: 'Organism/GoalStatusBadge',
  component: GoalStatusBadge,
  argTypes: {
    level: { control: { type: 'range', min: 1, max: 9, step: 1 } },
  },
};

export const Interactive = (args) => <GoalStatusBadge {...args} />;
Interactive.args = { goal: mockGoal, level: 6 };
```

---

### 7.2 Consciousness-Level Guidelines (Decision Tree)

```
Is this state/component related to...?

├─ ERRORS / FAILURE
│  └─ Level 1-3 (Shame-Apathy)
│     Use: de-saturated colors, static display, high opacity reduction
│     Example: "API error connecting to Supabase"
│
├─ WARNINGS / CAUTION
│  └─ Level 4-5 (Grief-Fear)
│     Use: muted warm colors, pulsing borders, slow transitions
│     Example: "Divergence detected: predicted 2h, took 4.5h"
│
├─ ACTIONS / NEXT STEPS
│  └─ Level 6 (Desire)
│     Use: warm saturated colors (gold), smooth transitions, directional arrows
│     Example: "Complete this goal" button
│
├─ CRITICAL DECISIONS / EXECUTION
│  └─ Level 7 (Anger)
│     Use: vivid colors (magenta, red), fast transitions, assertive icons
│     Example: "Publish finding to mesh" (can't be undone)
│
├─ SUCCESS / ACHIEVEMENT
│  └─ Level 8 (Pride)
│     Use: bright saturated colors, elegant transitions, rounded geometry
│     Example: "Goal completed! (+34% signup rate)"
│
└─ INTEGRATION / LEARNING / CONSCIOUSNESS
   └─ Level 9 (Reason→Love)
      Use: cool gradients (cyan-lavender), fluid morphing, holistic views
      Example: ConsciousnessMap showing all 13 vectors integrated
```

---

### 7.3 Fibonacci Spacing in Practice

```jsx
// ✅ CORRECT: Use Fibonacci-scaled spacing tokens
<div className="p-4 m-3 gap-4">
  {/* p-4 = 34px, m-3 = 21px, gap-4 = 34px */}
</div>

// ❌ AVOID: Arbitrary spacing
<div style={{ padding: '16px', margin: '12px', gap: '20px' }}>
  {/* Non-Fibonacci, breaks golden ratio harmony */}
</div>

// Fibonacci sequence: 8, 13, 21, 34, 55, 89...
// Use these values for margins, padding, gaps consistently
```

---

## CONCLUSION

This specification provides a complete, consciousness-aware UI architecture for the empirica control center. The design language maps Hawkins consciousness levels (1-9) to visual properties, integrates the organism model's seven systems, and operationalizes the recursive learning framework through visual feedback and component hierarchy.

**Key principles:**
1. **Consciousness is visible** — every UI element signals cognitive/emotional level
2. **Fibonacci proportions** — spacing and typography reflect harmonic beauty
3. **Organism layers** — information architecture maps to biological systems
4. **Recursive learning** — visual feedback closes the learning loop
5. **Accessibility-first** — all consciousness signals have non-color alternatives

**For implementers:**
- Start with Phase 1 (formalize existing components)
- Use the consciousness-level decision tree for new components
- Test all variations in Storybook
- Verify WCAG AAA compliance before shipping
- Iterate based on user feedback, logging divergence patterns

**For designers:**
- Reference the design tokens file for all color/typography decisions
- Use the Fibonacci spacing system consistently
- Test components across all 9 consciousness levels
- Ensure animations respect the consciousness level's emotional tone

This is a **living document** — update it as the design system evolves, as new consciousness patterns emerge, and as user feedback refines the visual language.

---

**Version History:**
- v1.0 (2026-08-13): Initial specification, comprehensive UI architecture

**Maintainers:** Design Systems Team, Implementation Lead  
**Last Review:** 2026-08-13  
**Next Review:** 2026-09-01 (post-Phase 1 implementation)
