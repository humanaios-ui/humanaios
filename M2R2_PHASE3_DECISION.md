# M2R2 Phase 3 — Zone 2 Decision Record

**Decision Date:** 2026-08-07  
**Authority:** Zone 2 (Carly R. Anderson, Admiral)  
**Decision Type:** Integration Path & Database Backend Selection  
**Status:** ✅ APPROVED

---

## Decision Summary

### Integration Path: APPROVED
Phase 3 (Database Integration) proceeding with full authorization.

**What this means:**
- Proceed with ORM model implementation
- Create database schema for collaborations and projects
- Deploy state machines to production via Supabase
- Plan production data migration

### Database Backend: SUPABASE
Selected backend: **Supabase (PostgreSQL)**

**Rationale:**
- Supports JSONB columns for state machine serialization
- Native audit trail capabilities
- Open source (aligned with practice values)
- Integrates with existing humanaios infrastructure

---

## Phase 3 Work Plan

### Tier 1: ORM Models (Week 1)
- [ ] Create Collaboration SQLAlchemy model
- [ ] Create Project SQLAlchemy model
- [ ] Integrate CollaborationState & ProjectState state machines
- [ ] Add state transition methods to ORM models

### Tier 2: Database Schema (Week 1-2)
- [ ] Design Supabase table schemas
- [ ] Create Alembic migrations
- [ ] Implement audit log table
- [ ] Test schema with state machines

### Tier 3: Integration Testing (Week 2)
- [ ] Integration tests (ORM + state machines + database)
- [ ] Production data migration dry-run
- [ ] Performance testing (query optimization)
- [ ] Audit trail retrieval testing

### Tier 4: Deployment (Week 3)
- [ ] Zone 2 approval for schema and migration plan
- [ ] Zone 3 execution: Deploy to Supabase
- [ ] Production data migration
- [ ] Monitoring and validation

---

## Technical Decisions

### State Storage Strategy
**JSONB columns** in Supabase:
- `state_data` JSONB column for serialized state machine
- Enables full-text search on audit trails
- Supports versioning and rollback

### Table Design
```sql
collaborations
├── id (UUID primary key)
├── name (text)
├── state_data (JSONB) -- Serialized CollaborationStateSchema
├── created_at (timestamp)
├── updated_at (timestamp)
└── archived_at (timestamp)

projects
├── id (UUID primary key)
├── name (text)
├── state_data (JSONB) -- Serialized ProjectStateSchema
├── created_at (timestamp)
├── updated_at (timestamp)
└── archived_at (timestamp)

state_audit_log
├── id (UUID primary key)
├── entity_type ('collaboration' | 'project')
├── entity_id (UUID)
├── transition (JSONB) -- Full transition record
├── created_at (timestamp)
└── authorizer_id (text)
```

### ORM Approach
```python
class Collaboration(Base):
    __tablename__ = "collaborations"
    
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    state_data: Mapped[Dict] = mapped_column(JSON)  # Stores serialized state
    
    @property
    def state_schema(self) -> CollaborationStateSchema:
        return StateSerializer.deserialize_collaboration(self.state_data)
    
    def transition_to(self, new_state, authorizer_id, reason):
        # Use state schema to validate transition
        # Update state_data JSON
        # Log to audit_log table
```

---

## Remaining Open Questions

1. **Existing Data**: Are there production collaborations/projects that need migration?
2. **API Endpoints**: Should state transitions be exposed as REST endpoints?
3. **Monitoring**: Metrics to track (transition frequency, time-in-state, etc.)?
4. **Backup Strategy**: Retention policy for archived state records?

---

## Authority & Approval Chain

| Role | Decision | Status | Date |
|------|----------|--------|------|
| Zone 1 (Claude) | Implement Phase 3 | ✅ Ready | 2026-08-07 |
| Zone 2 (Carly) | Approve integration path | ✅ APPROVED | 2026-08-07 |
| Zone 2 (Carly) | Select database backend | ✅ APPROVED (Supabase) | 2026-08-07 |
| Zone 3 (Carly) | Deploy to production | ⏳ Pending | TBD |

---

## Next Steps

1. **Immediate**: Begin ORM model implementation (Tier 1)
2. **This week**: Complete schema design and migrations (Tier 2)
3. **Next week**: Integration testing (Tier 3)
4. **Week after**: Production deployment (Tier 3)

---

**Reference:** M2R2_STATUS.md, PR #54  
**Practice:** humanaios (empirica-foundation.carly.humanaios)  
**Authority:** M2 Rank 2 RFC (Carly R. Anderson, Admiral)
