-- StudentOS MCP — Study module schema
-- One simple table: notes

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- unique id, auto increments
    topic TEXT NOT NULL,                    -- e.g. "DBMS", "OS", "Networks"
    content TEXT NOT NULL,                  -- the actual note text
    tags TEXT,                              -- optional, comma-separated e.g. "important,exam"
    revisit_count INTEGER DEFAULT 0,        -- how many times you've revised this topic
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- A few sample notes so we have something to search/read/track while testing
INSERT INTO notes (topic, content, tags) VALUES
('DBMS', 'Normalization removes redundancy. 1NF: atomic values. 2NF: no partial dependency. 3NF: no transitive dependency.', 'exam,important'),
('OS', 'Deadlock needs 4 conditions: mutual exclusion, hold and wait, no preemption, circular wait.', 'exam'),
('Networks', 'TCP is connection-oriented and reliable. UDP is connectionless and faster but unreliable.', 'important'),
('DBMS', 'Indexes speed up SELECT queries but slow down INSERT/UPDATE because the index also needs updating.', 'exam');



-- Career module: one base resume + a running log of skills learned
CREATE TABLE IF NOT EXISTS resume (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill TEXT NOT NULL,
    learned_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS topic_tracking (
    topic TEXT PRIMARY KEY,
    revisit_count INTEGER DEFAULT 0
);