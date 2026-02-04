-- Newsletter Manager Database Schema
-- Based on examples/articles/article_structure.json

-- Create news table
CREATE TABLE IF NOT EXISTS news (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Core fields
    idx INTEGER DEFAULT 0,
    news_title VARCHAR(200) NOT NULL,
    news_excerpt TEXT,
    newscontent TEXT NOT NULL,
    news_content JSONB,
    
    -- Image fields
    news_image VARCHAR,
    news_image_caption VARCHAR,
    
    -- URL and author
    news_url VARCHAR,
    news_author VARCHAR,
    
    -- Timestamps
    news_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    news_updated TIMESTAMP WITH TIME ZONE,
    
    -- Status fields
    draft BOOLEAN NOT NULL DEFAULT TRUE,
    news_status VARCHAR,
    featured BOOLEAN DEFAULT FALSE,
    featured_order INTEGER,
    
    -- Additional fields
    news_categories JSONB,
    related_program VARCHAR,
    tiny TEXT,
    sun JSONB
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_news_draft ON news(draft);
CREATE INDEX IF NOT EXISTS idx_news_created_at ON news(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_news_title ON news(news_title);
CREATE INDEX IF NOT EXISTS idx_news_news_url ON news(news_url);
CREATE INDEX IF NOT EXISTS idx_news_featured ON news(featured, featured_order);

-- Create full-text search index
CREATE INDEX IF NOT EXISTS idx_news_search ON news 
USING GIN (to_tsvector('english', news_title || ' ' || COALESCE(news_excerpt, '') || ' ' || newscontent));

-- Function to auto-generate slug from title
CREATE OR REPLACE FUNCTION generate_slug(title TEXT) 
RETURNS TEXT AS $$
BEGIN
    RETURN LOWER(
        REGEXP_REPLACE(
            REGEXP_REPLACE(title, '[^a-zA-Z0-9\s-]', '', 'g'),
            '\s+', '-', 'g'
        )
    );
END;
$$ LANGUAGE plpgsql;

-- Function to auto-generate excerpt from content (first 300 chars)
CREATE OR REPLACE FUNCTION generate_excerpt(content TEXT, max_length INTEGER DEFAULT 300) 
RETURNS TEXT AS $$
DECLARE
    excerpt_text TEXT;
BEGIN
    -- Remove HTML tags
    excerpt_text := REGEXP_REPLACE(content, '<[^>]+>', '', 'g');
    
    -- Trim and truncate
    excerpt_text := TRIM(excerpt_text);
    
    IF LENGTH(excerpt_text) > max_length THEN
        excerpt_text := SUBSTRING(excerpt_text, 1, max_length) || '...';
    END IF;
    
    RETURN excerpt_text;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-generate news_url if not provided
CREATE OR REPLACE FUNCTION set_news_url() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.news_url IS NULL OR NEW.news_url = '' THEN
        NEW.news_url := generate_slug(NEW.news_title);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_news_url
    BEFORE INSERT OR UPDATE ON news
    FOR EACH ROW
    EXECUTE FUNCTION set_news_url();

-- Trigger to auto-generate news_excerpt if not provided
CREATE OR REPLACE FUNCTION set_news_excerpt() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.news_excerpt IS NULL OR NEW.news_excerpt = '' THEN
        NEW.news_excerpt := generate_excerpt(NEW.newscontent, 300);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_news_excerpt
    BEFORE INSERT OR UPDATE ON news
    FOR EACH ROW
    EXECUTE FUNCTION set_news_excerpt();

-- Trigger to update news_updated timestamp
CREATE OR REPLACE FUNCTION update_news_updated() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.news_updated := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_news_updated
    BEFORE UPDATE ON news
    FOR EACH ROW
    EXECUTE FUNCTION update_news_updated();

-- Enable Row Level Security (RLS) - configure based on your needs
ALTER TABLE news ENABLE ROW LEVEL SECURITY;

-- Example policy: Allow authenticated users to read all news
CREATE POLICY "Allow authenticated read access" ON news
    FOR SELECT
    TO authenticated
    USING (true);

-- Example policy: Allow authenticated users to insert/update news
CREATE POLICY "Allow authenticated write access" ON news
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

COMMENT ON TABLE news IS 'News articles for Sing for Hope website';
COMMENT ON COLUMN news.draft IS 'true = draft (not visible), false = published (visible on website)';
COMMENT ON COLUMN news.news_url IS 'URL slug, auto-generated from title if not provided';
COMMENT ON COLUMN news.news_excerpt IS 'Auto-generated from first 300 chars of content if not provided';
