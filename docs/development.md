# Newsletter Manager - Development Guide

## Quick Start

### 1. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env with your credentials
# - Supabase URL and key
# - LLM API keys (OpenAI/Anthropic/Google)
# - Slack credentials (when ready)
```

### 4. Set up database

```bash
# Create migration (after setting up database)
python scripts/init_db.py
```

### 5. Run the application

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload
```

Application will be running at: http://localhost:8000

## Project Structure

```
sfh-newsmanager/
├── src/
│   ├── agents/          # CrewAI agent definitions
│   ├── tools/           # CrewAI tools (article CRUD, etc.)
│   ├── tasks/           # CrewAI task definitions
│   ├── crews/           # Workflow orchestrations
│   ├── channels/        # Slack, Email handlers
│   ├── database/        # Database models and client
│   └── config/          # Settings configuration
├── tests/               # Test files
├── scripts/             # Utility scripts
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Development Workflow

### Running tests

```bash
pytest
```

### Code formatting

```bash
# Format code
black .

# Check linting
ruff check .

# Type checking
mypy src/
```

### Pre-commit hooks

```bash
# Install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

## Next Steps

1. ✅ Project structure created
2. ⏳ Database schema migration
3. ⏳ First CrewAI tool (Article CRUD)
4. ⏳ First agent definition
5. ⏳ Basic testing

See `IMPLEMENTATION_PLAN.md` for detailed roadmap.
