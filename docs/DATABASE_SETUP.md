# Database Setup Guide

## Prerequisites

1. **Create a Supabase Project**
   - Go to https://supabase.com
   - Create a new project
   - Note your project URL and API keys

2. **Get Database Connection String**
   - In Supabase Dashboard → Settings → Database
   - Copy the connection string under "Connection string"
   - Format: `postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres`

## Configuration

1. **Update .env file** with your credentials:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_KEY=your-anon-key
```

## Initialize Database

### Method 1: Using Supabase SQL Editor (Recommended)

1. Open Supabase Dashboard → SQL Editor
2. Copy and paste `migrations/001_create_articles_table.sql`
3. Click "Run"
4. Copy and paste `migrations/002_seed_data.sql`
5. Click "Run"

### Method 2: Using Python Script

```bash
# Make sure virtual environment is activated
python scripts/init_db.py
```

## Test Connection

```bash
# Test database connection and see article counts
python scripts/test_db.py
```

Expected output:
```
✅ Connection successful!
Total articles: 3
Draft articles: 2
Published articles: 1

Recent articles:
  [DRAFT] Summer Concert Series Announcement
  [DRAFT] Spring Fundraiser 2026 - Coming Soon
  [PUBLISHED] 2024 Sing for Hope Pianos in NYC...
```

## Database Schema

### Articles Table

Key fields:
- `id` - Auto-incrementing primary key
- `news_title` - Article title (required)
- `newscontent` - Article content HTML (required)
- `news_image` - Hero image URL
- `draft` - Boolean (true=draft, false=published)
- `created_at` - Auto-set on creation
- `news_updated` - Auto-updated on changes

### Auto-Generated Fields

- `news_url` - Auto-generated from title (kebab-case)
- `news_excerpt` - Auto-generated from first 300 chars if not provided
- `news_updated` - Auto-updated on every update

### Indexes

- `draft` - For filtering by status
- `created_at` - For sorting by date
- `news_title` - For title searches
- Full-text search on title + excerpt + content

## Troubleshooting

### Connection refused
- Check DATABASE_URL is correct
- Ensure IP is allowed in Supabase (Settings → Database → Connection Pooling)

### Tables already exist
- Safe to re-run migrations (uses `IF NOT EXISTS`)
- Or drop tables manually and re-run

### Seed data fails
- Check if data already exists
- Modify unique constraints or delete existing data

## Next Steps

After database is set up:
1. ✅ Move to Step 1.3 - Implement Article CRUD tool
2. ✅ Create first CrewAI tool
3. ✅ Test basic operations
