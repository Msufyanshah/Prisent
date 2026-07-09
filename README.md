# Prisent AI 🚀

> Autonomous LinkedIn content generation and scheduling platform.

Prisent AI is an agentic system that transforms a creator's knowledge, audience goals, and brand voice into high-quality, engagement-optimized LinkedIn posts. By researching trends, mimicking the user's specific writing style, and performing automated depth reviews, the platform runs publishing pipelines autonomously under human-in-the-loop supervision.

---

## 📖 Table of Contents
1. [System Architecture](#-system-architecture)
2. [Key Features](#-key-features)
3. [Tech Stack](#-tech-stack)
4. [Folder Structure](#-folder-structure)
5. [Getting Started (Local Development)](#-getting-started-local-development)
6. [Testing & Verification](#-testing--verification)
7. [Depth Score Rules](#-depth-score-rules)
8. [Production Deployment](#-production-deployment)

---

## 🏗️ System Architecture

Prisent AI coordinates five major operational phases: Onboarding, Agentic Generation, Human Review, Celery-scheduled Publishing, and Analytics sync.

```mermaid
graph TD
    User[LinkedIn Creator] -->|1. Setup Persona & Upload Posts| WebUI[Frontend UI]
    WebUI -->|2. Store metadata| PostgreSQL[(PostgreSQL DB)]
    WebUI -->|3. Seed style examples| Qdrant[(Qdrant Vector DB)]
    
    CeleryBeat[Celery Beat Scheduler] -->|Trigger Auto-gen| CeleryWorker[Celery Agent Worker]
    WebUI -->|Trigger Manual Gen| CeleryWorker
    
    subgraph Agent Pipeline
        CeleryWorker --> Research[1. Research Agent]
        Research --> Writer[2. Writer Agent]
        Writer -->|Query style vector| Qdrant
        Writer --> Reviewer[3. Reviewer Agent]
        Reviewer -->|Depth Score < 85 / Feedback| Writer
        Reviewer -->|Approve| PostgreSQL
    end
    
    PostgreSQL -->|Schedule Check| CeleryBeat
    CeleryBeat -->|OAuth Publish| LinkedIn[LinkedIn API]
    LinkedIn -->|Metrics Sync| CeleryBeat
```

---

## 🌟 Key Features

### 👤 Onboarding & Persona Setup
- **Rich User Profile**: Set Niche, Content Pillars, Tone, Target Audience, Goals, Frequency, and Unique Differentiators.
- **Voice Memory Seeding**: Upload at least 3 historical posts. They are embedded with OpenAI's `text-embedding-3-small` and saved in a Qdrant collection to serve as brand voice style exemplars.

### 🤖 Multi-Agent Pipeline
- **Research Agent**: Traverses context to retrieve topic angles.
- **Writer Agent**: Pulls style matches from Qdrant vector database and synthesizes a drafted post.
- **Reviewer Agent**: Critiques the draft using a LinkedIn algorithm-based scoring heuristic. Refines the content in an autonomous loop (max 2 retries) until it achieves the target quality threshold.

### 📅 Automatic Scheduling & Publishing
- **Celery Scheduler**: Evaluates active posting schedules every 5 minutes.
- **Auto-Publishing**: Securely decrypts LinkedIn tokens and publishes drafts directly using the LinkedIn UGC Posts API.
- **Self-Healing**: Gracefully reports failures (e.g. expired tokens) back to the dashboard with actionable recovery hooks.

### 📊 Performance Analytics
- **Continuous Metrics Sync**: Regularly fetches impressions, reactions, comments, and shares.
- **AI Insights**: Provides automated advice (e.g., "*Storytelling posts are getting 2.5x more impressions on Thursdays*") using GPT-4o-mini.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.12+), SQLAlchemy (ORM), Alembic (Migrations)
- **Asynchronous Processing**: Celery, Redis (Message Broker)
- **Vector Storage**: Qdrant Vector Database
- **Relational Storage**: PostgreSQL
- **AI Runtimes**: OpenAI API (GPT-4o-mini & Text Embeddings)
- **Frontend**: Google Stitch responsive designs (HTML & CSS)

---

## 📁 Folder Structure

```
Prisent/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Entrypoint & Exception Handlers
│   │   ├── config.py          # Environment settings (Pydantic Settings)
│   │   ├── database.py        # SQLAlchemy engine and session configurations
│   │   ├── models/            # SQLAlchemy Database Models (User, Persona, etc.)
│   │   ├── routes/            # Router endpoints (Auth, Health, Persona, Posts)
│   │   ├── services/          # Business logic & Qdrant vector store setups
│   │   └── utils/             # JSON API envelopes and helpers
│   ├── tests/                 # Integration & Smoke Test scripts
│   ├── docker-compose.yml     # Local services container orchestration
│   ├── alembic.ini            # Database migration configuration
│   └── requirements.txt       # Python package dependencies
├── frontend/
│   └── README.md              # Frontend overview & design integrations
├── README.md                  # Main project guide
└── README.md.txt              # SpecKit-Plus reference
```

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- **Python 3.12+**
- **Docker & Docker Compose**

### 2. Environment Configuration
Create a `.env` file in the `backend/` directory based on the following template:

```ini
ENV=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/prisent
REDIS_URL=redis://localhost:6379/0
QDRANT_HOST=localhost
QDRANT_PORT=6363
OPENAI_API_KEY=your-openai-api-key
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
JWT_SECRET=your-jwt-secret-key
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### 3. Spin Up Infrastructure Services
Start PostgreSQL, Redis, and Qdrant locally:
```bash
cd backend
docker compose up -d
```

### 4. Install Dependencies & Migrate
Initialize your virtual environment, install requirements, and run database migrations:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

### 5. Launch FastAPI Server
Run the local development server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Verify the server status:
- API Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health` (should return `{"status": "ok", "service": "prisent"}`)

---

## 🧪 Testing & Verification

Integration and smoke tests are implemented as standalone Python scripts under the `backend/tests/` directory.

> [!IMPORTANT]
> Ensure the FastAPI server is running (`localhost:8000`) before launching test scripts.

Execute the tests:
```bash
python backend/tests/test_auth.py
python backend/tests/test_persona.py
python backend/tests/test_pipeline.py
python backend/tests/test_voice_memory.py
```

---

## 📈 Depth Score Rules

Prisent AI implements a strict grading heuristic that evaluates drafts against LinkedIn's algorithmic preference rules:

| Rule | Constraint |
| :--- | :--- |
| **Hook Limit** | The hook must be under 49 characters. |
| **Word Count** | Optimal length is between 150 and 300 words. |
| **Banned Phrases** | Avoid transactional CTAs (e.g., "*comment YES*", "*repost this*", "*drop a like*"). |
| **Ending Style** | Must conclude with a genuine, value-based question or insight. |
| **Line Breaks** | Single line breaks only to optimize mobile readability. |
| **Embellishment** | Maximum of 3 emojis per post, used sparingly. |
| **Promotional Content** | No promotional links or text in the first 3 lines. |

---

## 🛠️ Production Deployment

When deploying to hosting environments (like Railway, Render, or AWS):
1. Configure environment variables matching `.env`.
2. Spin up production PostgreSQL, Redis, and Qdrant clusters.
3. Configure Celery Beat to continuously run the scheduler:
   ```bash
   celery -A app.tasks worker --beat --loglevel=info
   ```
