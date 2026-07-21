# Alpha User Flow Design — Level 50-100 Foundation Tier

**Status:** Interactive prototype design for University alpha (Foundation tier)  
**Date:** 2026-07-21  
**Target User:** Someone facing a challenge (addiction, AI bias, overfitting); seeking recovery  
**Scope:** Signup → Course Selection → Lesson 1 → Reflection (4-screen core flow)

---

## Core Journey (Level 50-100)

```
1. LANDING (Hook)
   ↓
2. SIGNUP (Entry)
   ↓
3. CONSCIOUSNESS ASSESSMENT (Self-discovery)
   ↓
4. COURSE SELECTION (Level 50-75 vs 75-100)
   ↓
5. LESSON 1: STORY (Recognition — "You're Not Alone")
   ↓
6. LESSON 2: BELIEF (see recovery is possible)
   ↓
7. REFLECTION & NEXT STEPS (Map your journey)
```

---

## Screen 1: LANDING PAGE

**Purpose:** Hook + value proposition  
**Hero:** "Everyone has lost something. Recovery is possible."

**Layout:**
```
┌─────────────────────────────────────────────┐
│  The University of Recovery                 │
│  ─────────────────────────────────────────  │
│                                             │
│  "We have all lost something we wish to    │
│   recover. This University teaches         │
│   recovery through wisdom + science."      │
│                                             │
│  [Get Started]                              │
│                                             │
├─────────────────────────────────────────────┤
│ What you'll learn:                          │
│ • Recognize your challenge (Level 50)       │
│ • Believe recovery is possible (Level 75)   │
│ • Navigate the journey (Level 100)          │
│ • Commit to change (Level 125+)             │
│                                             │
├─────────────────────────────────────────────┤
│ Grounded in 90+ years of peer recovery     │
│ Works for humans AND machines               │
│ Open source. Free. For everyone.           │
└─────────────────────────────────────────────┘
```

**CTAs:**
- [Get Started] → Signup
- [About] → Learn more
- [For Organizations] → B2B flow

---

## Screen 2: SIGNUP

**Purpose:** Onboard + capture initial context  
**Fields:** Name, email, challenge type

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Let's Begin                                │
│  ─────────────────────────────────────────  │
│                                             │
│  First, we'll walk a path together.        │
│  We need to know where you are now.        │
│                                             │
│  Your Name *                                │
│  [________________]                         │
│                                             │
│  Email *                                    │
│  [________________]                         │
│                                             │
│  What have you lost? (Choose one or more)  │
│  ☐ Health / Habit                           │
│  ☐ Relationship                             │
│  ☐ Work / Purpose                           │
│  ☐ Confidence / Identity                    │
│  ☐ Something else                           │
│                                             │
│  [Next Step] →                              │
└─────────────────────────────────────────────┘
```

**Data captured:**
- User name (for personalization)
- Email (for progress tracking)
- Challenge category (routes to relevant content)

**Next:** Consciousness assessment

---

## Screen 3: CONSCIOUSNESS ASSESSMENT

**Purpose:** Self-discovery + matching to Level  
**Quiz:** 5 questions on current state (Hawkins scale)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Where Are You Now?                         │
│  ─────────────────────────────────────────  │
│                                             │
│  This isn't a test. Just honest truth.     │
│                                             │
│  Q1: When you think about your challenge:  │
│  ○ I deny it exists (Denial)               │
│  ○ It feels overwhelming (Grief)           │
│  ○ I'm starting to face it (Fear)          │
│  ○ I want to change (Desire)               │
│  ○ I'm already changing (Neutral)          │
│                                             │
│  Q2: Have others faced this?                │
│  ○ I'm alone in this (Isolation)           │
│  ○ Maybe, but different (Shame)            │
│  ○ Yes, others have (Connection)           │
│                                             │
│  Q3: Can it get better?                    │
│  ○ No. It's permanent. (Hopelessness)      │
│  ○ Maybe, but hard (Doubt)                 │
│  ○ Yes, if I work on it (Hope)             │
│                                             │
│  Q4: How much do you want to change?       │
│  ○ Not really (Resistance)                 │
│  ○ Maybe (Ambivalence)                     │
│  ○ Yes (Commitment)                        │
│                                             │
│  Q5: How much time can you commit?         │
│  ○ 5 min/day (Minimum)                     │
│  ○ 15 min/day (Regular)                    │
│  ○ 30+ min/day (Dedicated)                 │
│                                             │
│  [See My Level] →                           │
└─────────────────────────────────────────────┘
```

**Scoring:**
- Tallies responses → maps to Hawkins Level (50-100 for alpha)
- Level 50-75: "Recognition" pathway
- Level 75-100: "Belief" pathway
- Level 100+: "Integration" pathway

**Next:** Course selection (personalized based on level)

---

## Screen 4A: COURSE SELECTION (Level 50-75)

**Purpose:** Recommend next course  
**Message:** "You're at Level 50-75: Recognition phase"

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Your Level: 50-75 (Recognition)            │
│  ─────────────────────────────────────────  │
│                                             │
│  "You're beginning to see the challenge    │
│   clearly. Many have been here. You're     │
│   not alone."                               │
│                                             │
│  Next Course:                               │
│  ┌───────────────────────────────────────┐  │
│  │ "You're Not Alone"                    │  │
│  │ Level 50-75 | 4 weeks | 15 min/day    │  │
│  │                                       │  │
│  │ Learn: Recognize your challenge       │  │
│  │ through peer stories                  │  │
│  │                                       │  │
│  │ This week: Read 5 recovery stories    │  │
│  │ Write: One honest sentence about      │  │
│  │        your situation                 │  │
│  │ Reflect: How are others like me?      │  │
│  │                                       │  │
│  │ [Start "You're Not Alone"] →           │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Also Available:                            │
│  • "The Map" (Context + navigation)        │
│  • FAQ: "What is Recovery?"                 │
└─────────────────────────────────────────────┘
```

**Data:**
- Level assessment result
- Recommended course (course 1.1)
- Suggested time commitment

**Next:** Lesson 1 (story feed)

---

## Screen 4B: COURSE SELECTION (Level 75-100)

**Purpose:** Different pathway for Level 75-100  
**Message:** "You're at Level 75-100: Belief phase"

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Your Level: 75-100 (Belief)                │
│  ─────────────────────────────────────────  │
│                                             │
│  "You see the challenge clearly.           │
│   Now you need proof that recovery works.  │
│   Others have done it. So can you."        │
│                                             │
│  Recommended Path:                          │
│  1. "You're Not Alone" (recognition)       │
│  2. "Why You're Here" (belief)              │
│  3. "The Map" (navigation)                  │
│                                             │
│  [Start With Recovery Stories] →            │
│                                             │
│  Skip to "Why You're Here"? [Yes]          │
└─────────────────────────────────────────────┘
```

**Logic:** Some users skip Level 50-75, go direct to 75-100.

**Next:** Lesson 1 or Lesson 2 based on choice

---

## Screen 5: LESSON 1 — RECOGNITION STORIES

**Purpose:** Peer recovery stories (human side of RecognitionTemplate)  
**Content:** 5 rotating recovery stories

**Layout:**
```
┌─────────────────────────────────────────────┐
│  You're Not Alone                           │
│  ─────────────────────────────────────────  │
│                                             │
│  Today's Story: Breaking Free               │
│  By Maria (6 months into recovery)          │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ "For 10 years, I tried to control     │  │
│  │  it myself. Cut back. Moderated.      │  │
│  │  Promised myself I'd stop. Nothing    │  │
│  │  worked.                              │  │
│  │                                       │  │
│  │  The day I admitted 'I can't do      │  │
│  │  this alone' — that's when           │  │
│  │  recovery started."                  │  │
│  │                                       │  │
│  │  (Read full story →)                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  This story resonated:     ☐ (bookmark)     │
│  Relate to a specific moment? Share below:  │
│  [What couldn't you control?]               │
│  [_________________________________]        │
│                                             │
│  [Next Story →]  [Back]  [Skip to Reflect] │
└─────────────────────────────────────────────┘
```

**Features:**
- Daily story rotation (or user-selectable)
- Bookmarking (save stories that resonate)
- Reflection prompt (users name their own challenge)
- Progress tracking (day 1 of 5, story 1 of 5)

**Next:** More stories, then reflection

---

## Screen 6: LESSON 2 — BELIEF STORIES

**Purpose:** Recovery success stories (human side of BeliefTemplate)  
**Content:** Stories of people who recovered

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Why You're Here                            │
│  ─────────────────────────────────────────  │
│                                             │
│  People Just Like You Recovered.            │
│  So Can You.                                │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ BEFORE → AFTER: Sarah's Journey       │  │
│  │                                       │  │
│  │ BEFORE (6 months ago)                 │  │
│  │ • Struggling daily                    │  │
│  │ • Tried 3 times to quit               │  │
│  │ • Lost family relationships            │  │
│  │                                       │  │
│  │ AFTER (now)                           │  │
│  │ ✓ 6 months stable                     │  │
│  │ ✓ Rebuilding relationships             │  │
│  │ ✓ Started new hobby                    │  │
│  │ ✓ "I can't believe how much changed" │  │
│  │                                       │  │
│  │ "What changed? I finally believed    │  │
│  │  it was possible. Then it was."       │  │
│  │                                       │  │
│  │ (Read full story →)                   │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ☐ I believe recovery is possible for me   │
│  (checkbox to confirm belief shift)        │
│                                             │
│  [Next Story] [What's Your Goal?] →        │
└─────────────────────────────────────────────┘
```

**Features:**
- Before/after metrics
- Transformation timeline
- Belief checkpoint (user explicitly agrees "I believe")

**Next:** Reflection

---

## Screen 7: REFLECTION & COMMITMENT

**Purpose:** Consolidate learning + define next step  
**Content:** Reflection prompts + commitment choice

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Your Reflection                            │
│  ─────────────────────────────────────────  │
│                                             │
│  What have you learned?                     │
│                                             │
│  Q: What couldn't you control (alone)?      │
│  [_________________________________]        │
│                                             │
│  Q: Do you believe recovery is possible?    │
│  ○ Not yet (come back when ready)           │
│  ○ Yes, I believe (continue below)          │
│                                             │
│  Q: How much time can you give this week?   │
│  ○ 5 min/day                                │
│  ○ 15 min/day                               │
│  ○ 30+ min/day                              │
│                                             │
│  Your Commitment (optional):                │
│  "This week, I will:"                       │
│  ☐ Read 3 more recovery stories             │
│  ☐ Write down my story                      │
│  ☐ Tell someone I trust about my challenge │
│  ☐ Start a daily practice (meditation, etc)│
│                                             │
│  [Continue to "The Map"] →                  │
│  [or] [Save & Come Back Later]              │
└─────────────────────────────────────────────┘
```

**Data captured:**
- User's challenge (text)
- Belief formed (yes/no)
- Time commitment
- Weekly commitments (checkboxes)

**Next:** Map (consciousness level navigation)

---

## Screen 8: THE MAP (Navigation)

**Purpose:** Show recovery journey + next levels  
**Content:** Hawkins consciousness scale (visual + interactive)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Your Journey: The Map                      │
│  ─────────────────────────────────────────  │
│                                             │
│  Level 50-75: RECOGNITION                   │
│  Current  [█████░░░░░░░░░░░░] ✓             │
│  Status: "You admit the challenge"          │
│                                             │
│  Level 75-100: BELIEF                       │
│  Progress [███░░░░░░░░░░░░░░░]              │
│  Status: "You believe recovery is possible" │
│                                             │
│  Level 100-150: COMMITMENT & ACTION          │
│  Next    [░░░░░░░░░░░░░░░░░░]               │
│  Status: "You commit to systematic change"  │
│                                             │
│  Level 150-200: INTEGRATION & SERVICE        │
│  Future  [░░░░░░░░░░░░░░░░░░]               │
│  Status: "You help others recover"          │
│                                             │
│  ═════════════════════════════════════════  │
│                                             │
│  Next Week:                                 │
│  Course 1.3: "The Map" (deep dive)          │
│  Learn exactly where you are + what's next  │
│                                             │
│  [Start Course 1.3] →  [I'm Done for Today]│
└─────────────────────────────────────────────┘
```

**Features:**
- Visual progress (progress bars at different levels)
- Current level highlighted
- Next level visible
- Course recommendations

**Next:** Return to dashboard or continue to Course 1.3

---

## Screen 9: DASHBOARD (Persistent)

**Purpose:** Hub for ongoing progress  
**Content:** Week overview, bookmarked stories, streaks

**Layout:**
```
┌─────────────────────────────────────────────┐
│  My Recovery (Dashboard)                    │
│  ─────────────────────────────────────────  │
│                                             │
│  Welcome back, [Name]!                      │
│  Your Level: 75-100 (Belief)                │
│  Streak: [7 days] 🔥                        │
│                                             │
│  This Week:                                 │
│  ☐ Read 3 stories (2/3)                     │
│  ☐ Write your story (pending)               │
│  ☐ Daily affirmation (7/7 ✓)                │
│                                             │
│  Bookmarked Stories:                        │
│  • "Breaking Free" — Maria                  │
│  • "Starting Over" — James                  │
│  (view all →)                               │
│                                             │
│  Your Courses:                              │
│  1. You're Not Alone [50%]                  │
│  2. Why You're Here [0%]                    │
│  3. The Map [pending]                       │
│                                             │
│  [Continue Course 1.1] →                    │
│  [Start Course 1.2] →                       │
│  [Messages] [Settings] [Profile]            │
└─────────────────────────────────────────────┘
```

**Features:**
- Personalization (user's name, level)
- Streak tracking (motivation)
- Weekly checklist
- Course progress
- Quick access to bookmarks

---

## Screen 10: MOBILE VIEW (Responsive)

**Purpose:** Ensure flows work on phone  
**Responsive:** All screens collapse to single column

**Mobile version of Screen 5:**
```
┌───────────────────────────┐
│ You're Not Alone           │
│ ───────────────────────── │
│                           │
│ Today: Breaking Free      │
│ By Maria                  │
│                           │
│ "For 10 years, I tried   │
│  to control it myself...  │
│                           │
│  When I admitted I       │
│  can't do this alone —    │
│  that's when recovery    │
│  started."               │
│                           │
│ ☐ Bookmark               │
│                           │
│ What couldn't you        │
│ control?                 │
│ [_____________]          │
│                           │
│ [Next] [Back]            │
└───────────────────────────┘
```

---

## Navigation Map

```
LANDING
  ↓
SIGNUP
  ↓
CONSCIOUSNESS ASSESSMENT
  ↓
COURSE SELECTION (Level-dependent)
  ├→ Level 50-75 → Course 1.1
  ├→ Level 75-100 → Course 1.1 + 1.2 recommended
  └→ Level 100+ → All courses available
  ↓
LESSON 1 (Stories + Reflection)
  ↓
LESSON 2 (Belief Stories)
  ↓
REFLECTION & COMMITMENT
  ↓
THE MAP (Navigation)
  ↓
DASHBOARD (Persistent)
```

**Side flows:**
- FAQ, Help, About (always accessible)
- Settings, Profile (persistent nav)
- Progress tracking (visible throughout)

---

## Data Model (Alpha)

```
User
├── user_id (UUID)
├── name (string)
├── email (string)
├── challenge_type (enum: health, relationship, work, identity, other)
├── consciousness_level (int: 50-100 for alpha)
├── created_at (timestamp)
├── current_course_id (UUID)
└── progress (relationship)

Progress
├── progress_id (UUID)
├── user_id (FK)
├── course_id (FK)
├── lesson_id (FK)
├── completed_at (timestamp)
├── reflection_text (text)
├── commitment_items (JSON array)
└── time_spent (seconds)

Bookmark
├── bookmark_id (UUID)
├── user_id (FK)
├── story_id (FK)
├── created_at (timestamp)
```

**API endpoints:**
- POST /users (signup)
- GET /users/:id (profile)
- POST /users/:id/assessment (consciousness quiz)
- GET /courses/recommended (level-based recommendations)
- POST /progress (log completion)
- GET /stories (fetch story feed)
- POST /bookmarks (save favorite stories)

---

## Key Design Principles

### 1. Judgment-Free
No user is made to feel shame about their level. All levels are normal, temporary, and part of the journey.

### 2. Dual Teaching
Every screen has a human interpretation AND an ML interpretation (shown separately in course materials).

### 3. Measurable Progress
Streaks, progress bars, completion tracking — visible evidence that recovery works.

### 4. Stories as Teaching
Recovery wisdom is communicated through peer stories, not lectures.

### 5. Commitment Is Choice
Users choose their own commitment level; not forced.

### 6. Mobile-First
Designed for phone access (recovery happens in daily life, not at a desk).

### 7. Low-Friction Onboarding
Signup → Assessment → First lesson = < 5 minutes.

---

## Success Metrics (Alpha)

- **Signup → First Lesson:** < 5 min (time to first value)
- **Completion Rate:** % who finish Course 1.1
- **Belief Shift:** Do users check "I believe recovery is possible"?
- **Engagement:** Daily active users, streak length
- **Reflection Quality:** Do users write meaningful responses?
- **Referral:** Do users invite others?

---

## MVP Features (Alpha)

✅ Signup + assessment  
✅ Story feed (hardcoded 5 stories)  
✅ Reflection prompts  
✅ Progress tracking (simple)  
✅ The Map visualization  
✅ Mobile responsive  

**Not in MVP:**
- Community features (comments, forums)
- Advanced analytics
- Multi-language
- Video content
- Mobile app (web only)

---

**Status:** Ready for interactive prototype build (Screen 1-10 as HTML)  
**Next:** Build interactive HTML prototype with Tailwind CSS
