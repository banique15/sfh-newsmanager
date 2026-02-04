# Newsletter Manager AI Agent

**AI-powered newsletter management system for Sing for Hope using CrewAI**

---

## 📁 Project Structure

```
sfh-newsmanager/
│
├── docs/                    # 📚 Documentation & Specifications
│   ├── blueprint/          # Master blueprints & behavioral guidelines
│   ├── agents-spec/        # Agent specifications (markdown)
│   ├── tool-specs/         # Tool specifications (JSON)
│   ├── workflow-specs/     # Workflow specifications (markdown)
│   ├── instructions/       # Task instructions (core_tasks, edge_cases)
│   ├── IMPLEMENTATION_PLAN.md
│   ├── IMPLEMENTATION_TASKS.md
│   ├── PROJECT_SUMMARY.md
│   ├── DATABASE_SETUP.md
│   └── development.md      # Development guide
│
├── examples/               # 📝 Reference & Example Data
│   ├── articles/          # Example article JSON
│   ├── prompts/           # Example prompts
│   ├── responses/         # Example Slack/Email responses
│   └── user_requests/     # Example user requests
│
├── src/                    # 💻 Application Code
│   ├── agents/            # CrewAI agent implementations
│   ├── tools/             # CrewAI tool implementations
│   ├── workflows/         # Workflow orchestrations
│   ├── database/          # Database models & client
│   ├── channels/          # Slack, Email handlers
│   └── config/            # Settings & configuration
│
├── config/                 # ⚙️ Configuration Templates
│   ├── .env.template      # Environment variables template
│   └── settings.json      # Application settings template
│
├── migrations/            # 🗄️ Database Migrations
├── scripts/               # 🔧 Utility Scripts
├── tests/                 # 🧪 Test Files
│
└── main.py                # 🚀 Application Entry Point
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy environment template
copy config\.env.template .env

# Edit .env with your credentials:
# - DATABASE_URL (PostgreSQL from Supabase)
# - SUPABASE_URL and SUPABASE_KEY
# - OPENAI_API_KEY (or ANTHROPIC_API_KEY or GOOGLE_API_KEY)
```

### 3. Initialize Database

See [docs/DATABASE_SETUP.md](docs/DATABASE_SETUP.md) for detailed instructions.

```bash
# Option 1: Using Supabase SQL Editor (recommended)
# Copy migrations/001_create_articles_table.sql into Supabase SQL Editor

# Option 2: Using Python script
python scripts/init_db.py
```

### 4. Test

```bash
# Test database connection
python scripts/test_db.py

# Test CRUD tools
python scripts/test_tools.py
```

### 5. Run

```bash
# Development mode
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

Visit: http://localhost:8000

---

## 📖 Documentation

- **[Development Guide](docs/development.md)** - Getting started for developers
- **[Database Setup](docs/DATABASE_SETUP.md)** - Database configuration
- **[Implementation plan](docs/IMPLEMENTATION_PLAN.md)** - 8-phase development roadmap
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Complete project specification
- **[Master Blueprint](docs/blueprint/Master%20AI%20Blue%20Prints.md)** - Original requirements

---

## 🏗️ Tech Stack

- **CrewAI** - Multi-agent orchestration
- **FastAPI** - API framework
- **Supabase** - PostgreSQL database & storage
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation & settings
- **Python 3.11+**

---

## 📌 Current Status

✅ **Phase 1: Foundation & Core CRUD** (Completed)
- [x] Project setup & structure
- [x] Database schema & migrations
- [x] Article CRUD tools (CrewAI)
- [x] Search & listing tools

⏳ **Phase 2: Basic Agent & LLM** (Next)
- [ ] LLM setup
- [ ] Intent detection tool
- [ ] Basic agent loop

See [docs/IMPLEMENTATION_TASKS.md](docs/IMPLEMENTATION_TASKS.md) for full checklist.

---

## 🤝 Contributing

See [docs/development.md](docs/development.md) for development workflow and guidelines.

---

## 📄 License

Copyright © 2026 Sing for Hope