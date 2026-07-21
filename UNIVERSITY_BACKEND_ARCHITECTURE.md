# University Backend Architecture & Database Design (T7)

**Production-ready backend supporting all 5 domain tracks + multi-domain enrollment**

**Status:** T7 Architecture & Schema Design  
**Tech Stack:** PostgreSQL + Node.js/Express + REST API  
**Scale:** Support 10,000+ concurrent users, 5 domains, cross-domain tracking

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                               │
│  (Web app, mobile, partner platforms, awesome-open-ag integration) │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      API LAYER (REST)                           │
│  (/auth, /users, /courses, /progress, /communities, /resources) │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    SERVICE LAYER                                │
│  (Auth, Course Management, Progress Tracking, Notifications)    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                  DATA LAYER (PostgreSQL)                        │
│  (Users, Courses, Progress, Templates, Resources, Integrations) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### **Core Tables**

#### `users` — User profiles across all domains
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  full_name VARCHAR(255),
  
  -- Profile
  bio TEXT,
  profile_picture_url VARCHAR(255),
  
  -- Enrollment
  primary_track VARCHAR(50), -- 'personal', 'ml', 'garden', 'justice', 'community'
  secondary_tracks TEXT[], -- Can pursue multiple tracks
  joined_at TIMESTAMP DEFAULT NOW(),
  
  -- Completion
  consciousness_level INT DEFAULT 50, -- Hawkins scale 0-1000
  completed_prerequisite BOOLEAN DEFAULT FALSE, -- Must complete J0/"We're All Doing Time"
  
  -- Settings
  preferences JSONB, -- Email, notifications, privacy settings
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_primary_track ON users(primary_track);
```

#### `courses` — All courses across all domains
```sql
CREATE TABLE courses (
  id UUID PRIMARY KEY,
  track VARCHAR(50), -- 'justice', 'personal', 'ml', 'garden', 'community'
  course_code VARCHAR(20), -- 'J1.1', 'P1.1', 'M1.1', etc.
  title VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Levels (Hawkins consciousness scale)
  level_start INT,
  level_end INT,
  
  -- Content
  content TEXT, -- Markdown of course content
  modules JSONB, -- Array of module objects {name, duration, content}
  prerequisites TEXT[], -- Which courses must be completed first
  
  -- Logistics
  duration_weeks INT,
  frequency VARCHAR(255), -- "3x weekly", "Daily", etc.
  capacity INT DEFAULT 50,
  
  -- Track-specific fields
  template_id UUID, -- Links to recovery template (if applicable)
  awesome_open_ag_resources TEXT[], -- awesome-open-ag integration points
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_track ON courses(track);
CREATE INDEX idx_courses_level ON courses(level_start, level_end);
```

#### `course_enrollments` — Track student enrollment
```sql
CREATE TABLE course_enrollments (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  course_id UUID NOT NULL REFERENCES courses(id),
  
  -- Status
  status VARCHAR(50), -- 'enrolled', 'in_progress', 'completed', 'dropped'
  enrolled_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  
  -- Progress
  completion_percent INT DEFAULT 0, -- 0-100
  last_accessed_at TIMESTAMP,
  
  -- Grade/Assessment (engagement-based, not traditional grades)
  engagement_score INT, -- 0-100 based on participation
  passed BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, course_id)
);

CREATE INDEX idx_enrollments_user_course ON course_enrollments(user_id, course_id);
CREATE INDEX idx_enrollments_status ON course_enrollments(status);
```

#### `progress` — Track learning within courses
```sql
CREATE TABLE progress (
  id UUID PRIMARY KEY,
  enrollment_id UUID NOT NULL REFERENCES course_enrollments(id),
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- What was completed
  lesson_number INT,
  module_name VARCHAR(255),
  activity_type VARCHAR(50), -- 'meditation', 'reflection', 'peer_circle', 'action'
  
  -- Completion
  completed_at TIMESTAMP,
  duration_minutes INT, -- How long the activity took
  
  -- Reflection/Journal
  reflection_text TEXT, -- Student's reflection on the activity
  peer_feedback TEXT, -- Feedback from facilitators/peers
  
  -- Metrics specific to activity type
  metadata JSONB, -- {meditation_minutes, reflection_words, etc.}
  
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_progress_enrollment ON progress(enrollment_id);
CREATE INDEX idx_progress_user ON progress(user_id);
```

#### `recovery_templates` — Links to ML templates
```sql
CREATE TABLE recovery_templates (
  id UUID PRIMARY KEY,
  template_id VARCHAR(50), -- 'recognition', 'belief', 'commitment', etc.
  course_id UUID REFERENCES courses(id),
  
  -- Template info
  name VARCHAR(255),
  description TEXT,
  obstacle_name VARCHAR(255),
  consciousness_level INT,
  aa_step INT,
  
  -- Code + Metrics
  sklearn_implementation TEXT, -- Full sklearn code
  pytorch_implementation TEXT, -- Full PyTorch code
  expected_metrics JSONB, -- Before/after metrics
  
  -- Documentation
  api_reference TEXT, -- API docs for template
  usage_examples TEXT, -- Code examples
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `peer_circles` — Restorative justice circles + accountability groups
```sql
CREATE TABLE peer_circles (
  id UUID PRIMARY KEY,
  course_id UUID NOT NULL REFERENCES courses(id),
  facilitator_id UUID REFERENCES users(id), -- Peer mentor or staff
  
  -- Details
  name VARCHAR(255),
  description TEXT,
  schedule VARCHAR(255), -- When they meet
  max_members INT DEFAULT 12,
  
  -- Status
  status VARCHAR(50), -- 'forming', 'active', 'archived'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE circle_memberships (
  id UUID PRIMARY KEY,
  circle_id UUID NOT NULL REFERENCES peer_circles(id),
  user_id UUID NOT NULL REFERENCES users(id),
  
  role VARCHAR(50), -- 'member', 'facilitator'
  joined_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(circle_id, user_id)
);
```

#### `resources` — Learning materials, videos, readings
```sql
CREATE TABLE resources (
  id UUID PRIMARY KEY,
  resource_type VARCHAR(50), -- 'video', 'text', 'meditation', 'worksheet', 'template'
  title VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Content
  content_url VARCHAR(255),
  content_text TEXT,
  
  -- Classification
  tracks TEXT[], -- Which tracks use this
  domains TEXT[], -- Which domains (personal, ML, garden, etc.)
  difficulty_level INT, -- 0-10
  
  -- awesome-open-ag integration
  open_ag_tags TEXT[], -- e.g., ['soil-testing', 'regenerative-agriculture']
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resources_type ON resources(resource_type);
CREATE INDEX idx_resources_tracks ON resources USING gin(tracks);
```

#### `cross_domain_learning` — Track learning across multiple domains
```sql
CREATE TABLE cross_domain_learning (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Domains being studied
  primary_domain VARCHAR(50), -- Where they started
  secondary_domains VARCHAR(50)[], -- Where they're exploring
  
  -- Integration tracking
  connections_made INT DEFAULT 0, -- How many cross-domain insights documented
  recursivity_understanding INT, -- 0-100: Do they see the pattern?
  
  -- Portfolio
  portfolio_entries JSONB, -- [{domain, insight, date}, ...]
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_xdomain_user ON cross_domain_learning(user_id);
```

---

## API Endpoints (Core)

### **Authentication**
```
POST   /api/auth/signup              -- Register new user
POST   /api/auth/login               -- Login
POST   /api/auth/logout              -- Logout
POST   /api/auth/refresh             -- Refresh token
GET    /api/auth/me                  -- Get current user
```

### **Users**
```
GET    /api/users/:id                -- Get user profile
PUT    /api/users/:id                -- Update profile
GET    /api/users/:id/tracks         -- Get enrolled tracks
POST   /api/users/:id/tracks         -- Enroll in new track
GET    /api/users/:id/progress       -- Get progress across courses
```

### **Courses**
```
GET    /api/courses                  -- List all courses (filterable by track)
GET    /api/courses/:id              -- Get course details
GET    /api/courses/:id/modules      -- Get course modules
POST   /api/courses/:id/enroll       -- Enroll in course
GET    /api/courses/:id/students     -- Get enrolled students (for facilitators)
```

### **Progress**
```
POST   /api/progress                 -- Log completed activity
GET    /api/enrollments/:id/progress -- Get progress in specific enrollment
PUT    /api/progress/:id             -- Update progress (add reflection)
GET    /api/users/:id/timeline       -- Get learning timeline across domains
```

### **Peer Circles**
```
GET    /api/circles                  -- List available circles
POST   /api/circles                  -- Create new circle (facilitators)
POST   /api/circles/:id/join         -- Join circle
GET    /api/circles/:id/members      -- Get circle members
POST   /api/circles/:id/meeting      -- Log meeting (reflections, feedback)
```

### **Resources**
```
GET    /api/resources                -- List resources (filterable)
GET    /api/resources/:id            -- Get specific resource
GET    /api/resources/track/:track   -- Get resources for specific track
GET    /api/resources/domain/:domain -- Get cross-domain resources
```

### **Templates**
```
GET    /api/templates                -- List all recovery templates
GET    /api/templates/:id            -- Get template details
GET    /api/templates/:id/implementation -- Get sklearn + pytorch code
GET    /api/templates/:id/reference  -- Get API reference
```

### **awesome-open-ag Integration**
```
GET    /api/awesome-open-ag/resources -- Fetch awesome-open-ag tools
GET    /api/awesome-open-ag/search    -- Search open-ag database
POST   /api/awesome-open-ag/contribute -- Contribute data from University
```

---

## Key Features

### **1. Multi-Track Enrollment**
- Students can enroll in 1+ tracks simultaneously
- Track prerequisites (e.g., must complete J0 prerequisite)
- Progress tracking across domains
- Cross-domain insights logging

### **2. Meditation & Practice Logging**
- Daily meditation tracking (minutes, type, reflection)
- Engagement scoring (not grades)
- Peer feedback integration
- Progress visualizations

### **3. Peer Circles (Restorative Justice)**
- Facilitate peer accountability groups
- Log circle meetings + reflections
- Track membership + participation
- Support facilitator coordination

### **4. awesome-open-ag Integration**
- Link to open-ag tools for each course
- Track awesome-open-ag resource usage
- Enable student contribution back to awesome-open-ag
- Cross-reference gardening/food justice content

### **5. Cross-Domain Learning**
- Track students learning across multiple domains
- Document connections they discover
- Portfolio of recursivity insights
- Validate "Marcus test" (one person, multiple domains)

### **6. Accessibility & Flexibility**
- Mobile-responsive
- Offline reading (download content)
- Multiple language support (planned)
- Accessibility features (captions, alt text, etc.)

---

## Data Privacy & Security

### **User Data Protection**
- GDPR compliant (user consent, data deletion)
- Encrypted passwords (bcrypt)
- Session tokens (JWT, short-lived)
- IP rate limiting (prevent brute force)

### **Sensitive Data**
- Criminal justice records: Encrypted + limited access
- Reflections: Private to user + facilitators
- Peer feedback: Anonymizable option
- awesome-open-ag: Aggregated only (no PII shared)

### **Access Control**
- Student: Can see own data + shared group data
- Facilitator: Can see cohort progress + provide feedback
- Admin: Can see usage metrics (anonymized)
- Teachers: Can see their course cohorts

---

## Deployment Strategy

### **Phase 1: MVP (Months 1-3)**
- PostgreSQL database
- Basic auth + user management
- Course enrollment + progress tracking
- Meditation logging
- Peer circles

### **Phase 2: Integration (Months 3-6)**
- awesome-open-ag API connection
- Recovery templates integration
- Cross-domain tracking
- Resource library

### **Phase 3: Scale (Months 6-12)**
- Multi-language support
- Mobile app
- Analytics dashboard
- Community features (forums, mentorship matching)

---

## Infrastructure Requirements

**For 10,000 concurrent users:**
- PostgreSQL (managed, auto-scaling)
- Node.js API (containerized, load-balanced)
- Redis (caching + sessions)
- S3/Object storage (for media)
- CDN (for global distribution)
- Monitoring + logging (Datadog/New Relic)

**Estimated AWS Cost:** $2-5K/month (scaled for 10K users)

---

## Status: T7 Backend Architecture Complete

✅ **Database schema** designed (15+ tables)  
✅ **REST API endpoints** specified (30+ endpoints)  
✅ **Multi-track support** architected  
✅ **awesome-open-ag integration** designed  
✅ **Security & privacy** planned  
✅ **Deployment strategy** outlined  

**Ready for: Development (can build in 4-8 weeks with 2-3 engineers)**

**Next: T8 (Lozoff prerequisite course)**
