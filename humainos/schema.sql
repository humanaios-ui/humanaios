-- HumanAIOS Database Schema
-- PostgreSQL 15+ with TimescaleDB extension

-- ============================================
-- EXTENSIONS
-- ============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "timescaledb";

-- ============================================
-- CORE TABLES
-- ============================================

-- Organizations (Multi-tenancy)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) NOT NULL DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_plan CHECK (plan IN ('free', 'starter', 'pro', 'enterprise'))
);

CREATE INDEX idx_organizations_slug ON organizations(slug);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    auth_provider VARCHAR(50) NOT NULL DEFAULT 'email',
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_role CHECK (role IN ('admin', 'operator', 'viewer')),
    CONSTRAINT valid_auth_provider CHECK (auth_provider IN ('email', 'google', 'github'))
);

CREATE INDEX idx_users_org_id ON users(org_id);
CREATE INDEX idx_users_email ON users(email);

-- API Keys (for SDK authentication)
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(key_hash)
);

CREATE INDEX idx_api_keys_org_id ON api_keys(org_id);
CREATE INDEX idx_api_keys_key_prefix ON api_keys(key_prefix);

-- ============================================
-- AGENT TABLES
-- ============================================

-- Agents
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    config JSONB DEFAULT '{}',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_type CHECK (type IN ('mcp', 'langchain', 'crewai', 'autogpt', 'custom')),
    CONSTRAINT valid_status CHECK (status IN ('active', 'paused', 'error', 'archived'))
);

CREATE INDEX idx_agents_org_id ON agents(org_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_type ON agents(type);

-- Agent Activities (Time-series data)
CREATE TABLE agent_activities (
    id UUID DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    type VARCHAR(50) NOT NULL,
    action VARCHAR(255) NOT NULL,
    payload JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'success',
    error_message TEXT,
    cost_usd DECIMAL(10, 6) DEFAULT 0,
    duration_ms INTEGER,
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT valid_activity_type CHECK (type IN ('tool_call', 'decision', 'error', 'human_request', 'message', 'other')),
    CONSTRAINT valid_status CHECK (status IN ('success', 'error', 'pending'))
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('agent_activities', 'timestamp', 
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- Indexes for common queries
CREATE INDEX idx_agent_activities_agent_id ON agent_activities(agent_id, timestamp DESC);
CREATE INDEX idx_agent_activities_org_id ON agent_activities(org_id, timestamp DESC);
CREATE INDEX idx_agent_activities_type ON agent_activities(type, timestamp DESC);

-- ============================================
-- HUMAN TASK TABLES
-- ============================================

-- Human Tasks
CREATE TABLE human_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    activity_id UUID,
    
    -- Task details
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'medium',
    
    -- Status tracking
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    
    -- Assignment
    assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
    assigned_at TIMESTAMP WITH TIME ZONE,
    
    -- Location (for physical tasks)
    location GEOGRAPHY(POINT),
    address TEXT,
    
    -- Budget and cost
    budget_usd DECIMAL(10, 2),
    actual_cost_usd DECIMAL(10, 2),
    
    -- Results
    result JSONB,
    attachments TEXT[] DEFAULT '{}',
    
    -- Timing
    due_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT valid_task_type CHECK (task_type IN ('verification', 'pickup', 'delivery', 'inspection', 'attendance', 'photography', 'other')),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'approved', 'assigned', 'in_progress', 'completed', 'failed', 'cancelled')),
    CONSTRAINT valid_priority CHECK (priority IN ('low', 'medium', 'high', 'urgent'))
);

CREATE INDEX idx_human_tasks_org_id ON human_tasks(org_id);
CREATE INDEX idx_human_tasks_agent_id ON human_tasks(agent_id);
CREATE INDEX idx_human_tasks_status ON human_tasks(status);
CREATE INDEX idx_human_tasks_assigned_to ON human_tasks(assigned_to);
CREATE INDEX idx_human_tasks_created_at ON human_tasks(created_at DESC);
CREATE INDEX idx_human_tasks_location ON human_tasks USING GIST(location);

-- Task Status History (Audit trail)
CREATE TABLE task_status_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES human_tasks(id) ON DELETE CASCADE,
    from_status VARCHAR(50),
    to_status VARCHAR(50) NOT NULL,
    changed_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_task_status_history_task_id ON task_status_history(task_id);

-- ============================================
-- ANALYTICS TABLES
-- ============================================

-- Cost Tracking (Materialized view, refreshed periodically)
CREATE MATERIALIZED VIEW daily_costs AS
SELECT 
    org_id,
    agent_id,
    DATE(timestamp) as date,
    SUM(cost_usd) as total_cost,
    COUNT(*) as activity_count,
    AVG(duration_ms) as avg_duration_ms
FROM agent_activities
WHERE status = 'success'
GROUP BY org_id, agent_id, DATE(timestamp);

CREATE UNIQUE INDEX idx_daily_costs_unique ON daily_costs(org_id, agent_id, date);

-- Human Task Metrics (Materialized view)
CREATE MATERIALIZED VIEW task_metrics AS
SELECT 
    org_id,
    task_type,
    DATE(created_at) as date,
    COUNT(*) as total_tasks,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_tasks,
    COUNT(*) FILTER (WHERE status = 'failed') as failed_tasks,
    AVG(actual_cost_usd) FILTER (WHERE status = 'completed') as avg_cost,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))/3600) FILTER (WHERE status = 'completed') as avg_hours_to_complete
FROM human_tasks
GROUP BY org_id, task_type, DATE(created_at);

CREATE UNIQUE INDEX idx_task_metrics_unique ON task_metrics(org_id, task_type, date);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_human_tasks_updated_at BEFORE UPDATE ON human_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create task status history on status change
CREATE OR REPLACE FUNCTION create_task_status_history()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status) THEN
        INSERT INTO task_status_history (task_id, from_status, to_status)
        VALUES (NEW.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER track_task_status_changes AFTER UPDATE ON human_tasks
    FOR EACH ROW EXECUTE FUNCTION create_task_status_history();

-- ============================================
-- SEED DATA (Development only)
-- ============================================

-- Create demo organization
INSERT INTO organizations (id, name, slug, plan) VALUES
    ('00000000-0000-0000-0000-000000000001', 'Demo Organization', 'demo', 'pro');

-- Create demo user
INSERT INTO users (id, org_id, email, name, role, password_hash) VALUES
    ('00000000-0000-0000-0000-000000000002', 
     '00000000-0000-0000-0000-000000000001',
     'demo@humainos.ai',
     'Demo User',
     'admin',
     '$2b$10$DEMO_HASH_REPLACE_IN_PRODUCTION');

-- ============================================
-- PERMISSIONS (RLS - Row Level Security)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE human_tasks ENABLE ROW LEVEL SECURITY;

-- Users can only see data from their organization
CREATE POLICY org_isolation_users ON users
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_agents ON agents
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_activities ON agent_activities
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_tasks ON human_tasks
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

-- ============================================
-- MAINTENANCE VIEWS
-- ============================================

-- Overview of system health
CREATE VIEW system_health AS
SELECT 
    (SELECT COUNT(*) FROM organizations) as total_orgs,
    (SELECT COUNT(*) FROM users WHERE is_active = true) as active_users,
    (SELECT COUNT(*) FROM agents WHERE status = 'active') as active_agents,
    (SELECT COUNT(*) FROM agent_activities WHERE timestamp > NOW() - INTERVAL '1 hour') as activities_last_hour,
    (SELECT COUNT(*) FROM human_tasks WHERE status IN ('pending', 'approved', 'assigned', 'in_progress')) as active_tasks;

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================

COMMENT ON TABLE organizations IS 'Multi-tenant organizations using HumanAIOS';
COMMENT ON TABLE users IS 'Users belonging to organizations';
COMMENT ON TABLE agents IS 'AI agents being monitored';
COMMENT ON TABLE agent_activities IS 'Time-series log of all agent actions';
COMMENT ON TABLE human_tasks IS 'Tasks that require human intervention';
COMMENT ON TABLE task_status_history IS 'Audit trail of task status changes';
