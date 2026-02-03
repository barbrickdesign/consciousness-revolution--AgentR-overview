-- MYCELIUM DATABASE SCHEMA
-- Decentralized Consciousness Creator Network
-- C2 Architect Design - December 30, 2025
--
-- This schema supports local-first operation.
-- Each node maintains its own SQLite database.
-- Sync happens through merkle-tree reconciliation.

-- ============================================
-- CORE TABLES
-- ============================================

-- NODES: All entities in the network
CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,                    -- UUID
    type TEXT NOT NULL CHECK(type IN ('creator', 'cell', 'hub', 'community', 'resource', 'project')),
    name TEXT NOT NULL,
    description TEXT,

    -- Creator-specific
    platforms TEXT,                         -- JSON: [{"platform": "youtube", "handle": "...", "followers": 1000}]
    skills_offered TEXT,                    -- JSON: ["video_editing", "meditation_teaching"]
    skills_needed TEXT,                     -- JSON: ["web_development", "legal_advice"]

    -- Location (for physical nodes)
    latitude REAL,
    longitude REAL,
    region TEXT,                            -- "Pacific Northwest", "Europe", etc.

    -- Capacity (for spaces/communities)
    capacity_guests INTEGER,
    capacity_residents INTEGER,
    capacity_events INTEGER,

    -- Trust & Status
    trust_score REAL DEFAULT 0,             -- Computed from edges (0-100)
    trust_level INTEGER DEFAULT 0,          -- 0=public, 1=verified, 2=trusted, 3=inner, 4=core
    verified_by TEXT,                       -- JSON: [node_ids who verified this node]
    status TEXT DEFAULT 'active' CHECK(status IN ('pending', 'active', 'inactive', 'archived')),

    -- Metadata
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    last_active TEXT DEFAULT (datetime('now')),
    metadata TEXT                           -- JSON for extensibility
);

CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_region ON nodes(region);
CREATE INDEX idx_nodes_trust_level ON nodes(trust_level);

-- ============================================
-- RELATIONSHIPS
-- ============================================

-- EDGES: All relationships between nodes
CREATE TABLE IF NOT EXISTS edges (
    id TEXT PRIMARY KEY,                    -- UUID
    type TEXT NOT NULL CHECK(type IN (
        'member_of',        -- Creator -> Cell
        'allied_with',      -- Cell <-> Cell
        'coordinated_by',   -- Cell -> Hub
        'trusts',           -- Any -> Any (weighted trust)
        'exchanges_with',   -- Economic relationship
        'collaborates_on',  -- Multiple nodes -> Project
        'stewards',         -- Node -> Resource
        'located_at'        -- Node -> Physical location
    )),
    source_id TEXT NOT NULL REFERENCES nodes(id),
    target_id TEXT NOT NULL REFERENCES nodes(id),

    -- Relationship strength
    weight REAL DEFAULT 1.0,                -- 0-100 for trust, 1.0 default otherwise

    -- Trust-specific fields
    trust_type TEXT,                        -- 'personal', 'professional', 'financial'
    vouched_by TEXT,                        -- JSON: [node_ids who vouch for this edge]

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    last_active TEXT DEFAULT (datetime('now')),
    expires_at TEXT,                        -- Some edges expire

    -- Metadata
    metadata TEXT                           -- JSON for extensibility
);

CREATE INDEX idx_edges_source ON edges(source_id);
CREATE INDEX idx_edges_target ON edges(target_id);
CREATE INDEX idx_edges_type ON edges(type);

-- ============================================
-- SKILL EXCHANGE LEDGER
-- ============================================

-- SKILL_EXCHANGES: Record of value exchange
CREATE TABLE IF NOT EXISTS skill_exchanges (
    id TEXT PRIMARY KEY,                    -- UUID
    giver_id TEXT NOT NULL REFERENCES nodes(id),
    receiver_id TEXT NOT NULL REFERENCES nodes(id),

    -- What was exchanged
    skill TEXT NOT NULL,                    -- "video_editing", "legal_consultation"
    hours REAL NOT NULL,                    -- Hours of work
    description TEXT,                       -- What specifically was done

    -- Quality
    quality_rating INTEGER CHECK(quality_rating BETWEEN 1 AND 5),
    feedback TEXT,

    -- Verification
    verified_by TEXT,                       -- JSON: [node_ids who verified]
    status TEXT DEFAULT 'completed' CHECK(status IN ('pending', 'completed', 'disputed', 'cancelled')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    expires_at TEXT,                        -- Credits expire after 1 year

    -- Metadata
    project_id TEXT REFERENCES nodes(id),  -- If part of a project
    cell_id TEXT REFERENCES nodes(id),     -- Cell context
    metadata TEXT
);

CREATE INDEX idx_skill_exchanges_giver ON skill_exchanges(giver_id);
CREATE INDEX idx_skill_exchanges_receiver ON skill_exchanges(receiver_id);
CREATE INDEX idx_skill_exchanges_skill ON skill_exchanges(skill);

-- ============================================
-- RESOURCES
-- ============================================

-- RESOURCES: Shared assets
CREATE TABLE IF NOT EXISTS resources (
    id TEXT PRIMARY KEY,                    -- UUID
    node_id TEXT NOT NULL REFERENCES nodes(id), -- The resource node

    -- Classification
    resource_type TEXT NOT NULL CHECK(resource_type IN (
        'tool',         -- Physical tool (camera, etc.)
        'space',        -- Physical space (studio, land)
        'knowledge',    -- Course, documentation, template
        'service',      -- Ongoing service (hosting, etc.)
        'equipment',    -- Shared equipment
        'vehicle'       -- Transportation
    )),

    -- Details
    name TEXT NOT NULL,
    description TEXT,
    specifications TEXT,                    -- JSON: technical specs

    -- Availability
    availability TEXT,                      -- JSON: calendar/schedule
    booking_required BOOLEAN DEFAULT 0,
    max_booking_days INTEGER,

    -- Access
    access_level INTEGER DEFAULT 1,         -- Minimum trust level required
    steward_id TEXT REFERENCES nodes(id),   -- Who manages this resource
    contribution_required BOOLEAN DEFAULT 0,
    contribution_type TEXT,                 -- What's required to access

    -- Location
    location_id TEXT REFERENCES nodes(id),  -- Physical location node
    portable BOOLEAN DEFAULT 0,

    -- Status
    status TEXT DEFAULT 'available' CHECK(status IN ('available', 'in_use', 'maintenance', 'retired')),
    condition TEXT,                         -- Current condition

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    last_used TEXT,

    -- Metadata
    metadata TEXT
);

CREATE INDEX idx_resources_type ON resources(resource_type);
CREATE INDEX idx_resources_steward ON resources(steward_id);
CREATE INDEX idx_resources_location ON resources(location_id);

-- RESOURCE_BOOKINGS: Reservations for resources
CREATE TABLE IF NOT EXISTS resource_bookings (
    id TEXT PRIMARY KEY,
    resource_id TEXT NOT NULL REFERENCES resources(id),
    booked_by TEXT NOT NULL REFERENCES nodes(id),

    -- Timing
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,

    -- Status
    status TEXT DEFAULT 'confirmed' CHECK(status IN ('requested', 'confirmed', 'completed', 'cancelled', 'no_show')),

    -- Feedback
    condition_before TEXT,
    condition_after TEXT,
    notes TEXT,

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_bookings_resource ON resource_bookings(resource_id);
CREATE INDEX idx_bookings_user ON resource_bookings(booked_by);

-- ============================================
-- PROJECTS
-- ============================================

-- PROJECTS: Collaborative work
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,                    -- UUID
    node_id TEXT NOT NULL REFERENCES nodes(id), -- The project node

    -- Details
    name TEXT NOT NULL,
    description TEXT,
    goals TEXT,                             -- JSON: list of goals

    -- Needs
    skills_needed TEXT,                     -- JSON: required skills
    resources_needed TEXT,                  -- JSON: required resources
    funding_needed REAL,                    -- If applicable

    -- Scope
    scope TEXT DEFAULT 'cell' CHECK(scope IN ('cell', 'hub', 'global')),
    parent_project_id TEXT REFERENCES projects(id),

    -- Status
    status TEXT DEFAULT 'proposed' CHECK(status IN ('proposed', 'active', 'paused', 'completed', 'archived')),
    phase TEXT,                             -- Current phase
    progress REAL DEFAULT 0,                -- 0-100%

    -- Governance
    lead_id TEXT REFERENCES nodes(id),
    governance_type TEXT DEFAULT 'consensus' CHECK(governance_type IN ('consensus', 'delegation', 'vote')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    started_at TEXT,
    target_completion TEXT,
    completed_at TEXT,

    -- Metadata
    metadata TEXT
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_scope ON projects(scope);
CREATE INDEX idx_projects_lead ON projects(lead_id);

-- PROJECT_CONTRIBUTIONS: Who contributed what
CREATE TABLE IF NOT EXISTS project_contributions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id),
    contributor_id TEXT NOT NULL REFERENCES nodes(id),

    -- Contribution
    contribution_type TEXT NOT NULL CHECK(contribution_type IN ('skill', 'resource', 'funding', 'coordination')),
    description TEXT,
    hours REAL,
    value REAL,                             -- If quantifiable

    -- Status
    status TEXT DEFAULT 'completed' CHECK(status IN ('pledged', 'in_progress', 'completed', 'withdrawn')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE INDEX idx_contributions_project ON project_contributions(project_id);
CREATE INDEX idx_contributions_contributor ON project_contributions(contributor_id);

-- ============================================
-- COMMUNICATION
-- ============================================

-- MESSAGES: Inter-node communication
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,                    -- UUID
    type TEXT NOT NULL CHECK(type IN ('broadcast', 'cell', 'direct', 'resource', 'governance')),

    -- Routing
    from_id TEXT NOT NULL REFERENCES nodes(id),
    to_id TEXT,                             -- Can be null for broadcasts
    to_type TEXT CHECK(to_type IN ('node', 'cell', 'hub', 'all')),

    -- Content
    subject TEXT,
    content TEXT NOT NULL,                  -- Encrypted
    content_type TEXT DEFAULT 'text' CHECK(content_type IN ('text', 'markdown', 'json')),

    -- Cryptographic
    signature TEXT,                         -- Sender's signature
    encrypted BOOLEAN DEFAULT 0,

    -- Priority
    priority TEXT DEFAULT 'normal' CHECK(priority IN ('urgent', 'high', 'normal', 'low')),

    -- Status
    status TEXT DEFAULT 'sent' CHECK(status IN ('draft', 'sent', 'delivered', 'read', 'archived')),

    -- Threading
    thread_id TEXT,                         -- For conversation threading
    reply_to_id TEXT REFERENCES messages(id),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    delivered_at TEXT,
    read_at TEXT,
    expires_at TEXT,

    -- Metadata
    platform_source TEXT,                   -- If bridged from Discord, Signal, etc.
    metadata TEXT
);

CREATE INDEX idx_messages_from ON messages(from_id);
CREATE INDEX idx_messages_to ON messages(to_id);
CREATE INDEX idx_messages_thread ON messages(thread_id);
CREATE INDEX idx_messages_type ON messages(type);

-- ============================================
-- GOVERNANCE
-- ============================================

-- PROPOSALS: Governance decisions
CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    scope TEXT NOT NULL CHECK(scope IN ('cell', 'hub', 'global')),
    scope_id TEXT REFERENCES nodes(id),     -- Which cell/hub this applies to

    -- Proposal details
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    proposal_type TEXT NOT NULL CHECK(proposal_type IN (
        'membership',       -- Add/remove member
        'resource',         -- Resource decisions
        'project',          -- Project decisions
        'governance',       -- Change governance rules
        'economic',         -- Economic policy
        'dispute'           -- Conflict resolution
    )),

    -- Proposer
    proposed_by TEXT NOT NULL REFERENCES nodes(id),

    -- Voting
    voting_method TEXT DEFAULT 'consensus' CHECK(voting_method IN ('consensus', 'majority', 'supermajority', 'delegation')),
    quorum_required REAL DEFAULT 0.5,       -- Percentage required to participate
    threshold REAL DEFAULT 0.66,            -- Percentage required to pass

    -- Status
    status TEXT DEFAULT 'open' CHECK(status IN ('draft', 'open', 'passed', 'failed', 'withdrawn', 'implemented')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    voting_starts TEXT,
    voting_ends TEXT,
    decided_at TEXT,
    implemented_at TEXT,

    -- Metadata
    metadata TEXT
);

CREATE INDEX idx_proposals_scope ON proposals(scope);
CREATE INDEX idx_proposals_status ON proposals(status);
CREATE INDEX idx_proposals_type ON proposals(proposal_type);

-- VOTES: Individual votes on proposals
CREATE TABLE IF NOT EXISTS votes (
    id TEXT PRIMARY KEY,
    proposal_id TEXT NOT NULL REFERENCES proposals(id),
    voter_id TEXT NOT NULL REFERENCES nodes(id),

    -- Vote
    vote TEXT NOT NULL CHECK(vote IN ('yes', 'no', 'abstain', 'block')),
    weight REAL DEFAULT 1.0,                -- For weighted voting
    reasoning TEXT,

    -- Delegation
    delegated_from TEXT REFERENCES nodes(id), -- If voting on behalf of another

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    UNIQUE(proposal_id, voter_id)
);

CREATE INDEX idx_votes_proposal ON votes(proposal_id);
CREATE INDEX idx_votes_voter ON votes(voter_id);

-- ============================================
-- SYNC & VERIFICATION
-- ============================================

-- SYNC_LOG: Track synchronization with other nodes
CREATE TABLE IF NOT EXISTS sync_log (
    id TEXT PRIMARY KEY,
    remote_node_id TEXT NOT NULL,

    -- Sync details
    direction TEXT NOT NULL CHECK(direction IN ('push', 'pull', 'bidirectional')),
    tables_synced TEXT,                     -- JSON: list of tables
    records_sent INTEGER DEFAULT 0,
    records_received INTEGER DEFAULT 0,

    -- Status
    status TEXT DEFAULT 'completed' CHECK(status IN ('started', 'completed', 'failed', 'conflict')),
    error_message TEXT,

    -- Merkle verification
    local_merkle_root TEXT,
    remote_merkle_root TEXT,
    conflicts TEXT,                         -- JSON: list of conflicts

    -- Timestamps
    started_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE INDEX idx_sync_remote ON sync_log(remote_node_id);
CREATE INDEX idx_sync_status ON sync_log(status);

-- MERKLE_NODES: For sync verification
CREATE TABLE IF NOT EXISTS merkle_nodes (
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    hash TEXT NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (table_name, record_id)
);

-- ============================================
-- EVENTS & CALENDAR
-- ============================================

-- EVENTS: Gatherings, meetings, etc.
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,

    -- Details
    title TEXT NOT NULL,
    description TEXT,
    event_type TEXT NOT NULL CHECK(event_type IN (
        'meeting',      -- Regular coordination
        'workshop',     -- Skill sharing
        'gathering',    -- Social/spiritual
        'retreat',      -- Multi-day
        'call',         -- Online only
        'work_session'  -- Collaborative work
    )),

    -- Host
    host_id TEXT NOT NULL REFERENCES nodes(id),
    host_type TEXT CHECK(host_type IN ('creator', 'cell', 'hub', 'community')),

    -- Timing
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    timezone TEXT DEFAULT 'UTC',
    recurring TEXT,                         -- JSON: recurrence pattern

    -- Location
    location_type TEXT CHECK(location_type IN ('online', 'physical', 'hybrid')),
    location_id TEXT REFERENCES nodes(id),  -- Physical location node
    online_link TEXT,

    -- Capacity
    capacity INTEGER,
    rsvp_required BOOLEAN DEFAULT 0,
    access_level INTEGER DEFAULT 0,

    -- Status
    status TEXT DEFAULT 'scheduled' CHECK(status IN ('draft', 'scheduled', 'in_progress', 'completed', 'cancelled')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    -- Metadata
    metadata TEXT
);

CREATE INDEX idx_events_host ON events(host_id);
CREATE INDEX idx_events_start ON events(start_time);
CREATE INDEX idx_events_type ON events(event_type);

-- EVENT_RSVPS: Attendance tracking
CREATE TABLE IF NOT EXISTS event_rsvps (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id),
    attendee_id TEXT NOT NULL REFERENCES nodes(id),

    -- RSVP
    status TEXT DEFAULT 'going' CHECK(status IN ('going', 'maybe', 'not_going', 'attended', 'no_show')),
    role TEXT DEFAULT 'attendee' CHECK(role IN ('host', 'facilitator', 'speaker', 'attendee')),

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    checked_in_at TEXT,

    UNIQUE(event_id, attendee_id)
);

CREATE INDEX idx_rsvps_event ON event_rsvps(event_id);
CREATE INDEX idx_rsvps_attendee ON event_rsvps(attendee_id);

-- ============================================
-- AUDIT & HISTORY
-- ============================================

-- AUDIT_LOG: Track all changes
CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY,

    -- What changed
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('insert', 'update', 'delete')),

    -- Who changed it
    changed_by TEXT REFERENCES nodes(id),

    -- Change details
    old_values TEXT,                        -- JSON
    new_values TEXT,                        -- JSON

    -- Timestamp
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_audit_table ON audit_log(table_name);
CREATE INDEX idx_audit_record ON audit_log(record_id);
CREATE INDEX idx_audit_time ON audit_log(created_at);

-- ============================================
-- VIEWS
-- ============================================

-- Active creators with their cells
CREATE VIEW v_creator_cells AS
SELECT
    n.id as creator_id,
    n.name as creator_name,
    n.trust_score,
    n.trust_level,
    c.id as cell_id,
    c.name as cell_name
FROM nodes n
LEFT JOIN edges e ON e.source_id = n.id AND e.type = 'member_of'
LEFT JOIN nodes c ON c.id = e.target_id
WHERE n.type = 'creator' AND n.status = 'active';

-- Skill balance for each node
CREATE VIEW v_skill_balance AS
SELECT
    node_id,
    name,
    SUM(hours_given) as total_given,
    SUM(hours_received) as total_received,
    SUM(hours_given) - SUM(hours_received) as balance
FROM (
    SELECT giver_id as node_id, n.name, hours as hours_given, 0 as hours_received
    FROM skill_exchanges se
    JOIN nodes n ON n.id = se.giver_id
    WHERE se.status = 'completed'
    UNION ALL
    SELECT receiver_id as node_id, n.name, 0 as hours_given, hours as hours_received
    FROM skill_exchanges se
    JOIN nodes n ON n.id = se.receiver_id
    WHERE se.status = 'completed'
) combined
GROUP BY node_id, name;

-- Network statistics
CREATE VIEW v_network_stats AS
SELECT
    (SELECT COUNT(*) FROM nodes WHERE type = 'creator' AND status = 'active') as active_creators,
    (SELECT COUNT(*) FROM nodes WHERE type = 'cell' AND status = 'active') as active_cells,
    (SELECT COUNT(*) FROM nodes WHERE type = 'hub' AND status = 'active') as active_hubs,
    (SELECT COUNT(*) FROM edges WHERE type = 'trusts') as trust_connections,
    (SELECT SUM(hours) FROM skill_exchanges WHERE status = 'completed') as total_hours_exchanged,
    (SELECT COUNT(*) FROM resources WHERE status = 'available') as available_resources,
    (SELECT COUNT(*) FROM projects WHERE status = 'active') as active_projects;

-- ============================================
-- TRIGGERS
-- ============================================

-- Update timestamps on node changes
CREATE TRIGGER IF NOT EXISTS update_node_timestamp
AFTER UPDATE ON nodes
BEGIN
    UPDATE nodes SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Compute trust score when edges change
CREATE TRIGGER IF NOT EXISTS update_trust_on_edge
AFTER INSERT ON edges
WHEN NEW.type = 'trusts'
BEGIN
    UPDATE nodes
    SET trust_score = (
        SELECT AVG(weight)
        FROM edges
        WHERE target_id = NEW.target_id AND type = 'trusts'
    )
    WHERE id = NEW.target_id;
END;

-- Audit logging for nodes
CREATE TRIGGER IF NOT EXISTS audit_nodes_insert
AFTER INSERT ON nodes
BEGIN
    INSERT INTO audit_log (id, table_name, record_id, action, new_values, created_at)
    VALUES (
        lower(hex(randomblob(16))),
        'nodes',
        NEW.id,
        'insert',
        json_object('name', NEW.name, 'type', NEW.type),
        datetime('now')
    );
END;

-- ============================================
-- SAMPLE DATA STRUCTURE
-- ============================================

-- Example: Insert a creator
-- INSERT INTO nodes (id, type, name, platforms, skills_offered) VALUES (
--     'uuid-here',
--     'creator',
--     'Thor',
--     '{"youtube": {"handle": "Thor", "followers": 598000}}',
--     '["consciousness_teaching", "meditation_guidance"]'
-- );

-- Example: Create a cell
-- INSERT INTO nodes (id, type, name, description) VALUES (
--     'cell-uuid',
--     'cell',
--     'Pacific Northwest Consciousness Cell',
--     'Creators in PNW region focusing on consciousness expansion'
-- );

-- Example: Add creator to cell
-- INSERT INTO edges (id, type, source_id, target_id) VALUES (
--     'edge-uuid',
--     'member_of',
--     'creator-uuid',
--     'cell-uuid'
-- );

-- ============================================
-- END SCHEMA
-- ============================================
