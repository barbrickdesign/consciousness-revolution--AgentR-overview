-- ARAYA MEMORY TABLE
-- Run this in Supabase Dashboard → SQL Editor
-- https://supabase.com/dashboard/project/lgibygzcbvrrykfaxvbg/sql/new

CREATE TABLE IF NOT EXISTS araya_memory (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'profile', 'user', 'assistant'
    content TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_araya_memory_user_id ON araya_memory(user_id);
CREATE INDEX IF NOT EXISTS idx_araya_memory_type ON araya_memory(type);
CREATE INDEX IF NOT EXISTS idx_araya_memory_created ON araya_memory(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE araya_memory ENABLE ROW LEVEL SECURITY;

-- Allow anon key to read and write (for serverless functions)
CREATE POLICY "Allow anon access" ON araya_memory
    FOR ALL USING (true);

-- Verify table created
SELECT * FROM araya_memory LIMIT 1;
