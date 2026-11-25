# AI Engineering Command Center

An AI-powered software project planning and engineering management platform that converts natural-language software requirements into structured project plans and actionable development tasks.

The platform combines **LLM-powered project planning, structured task generation, persistent project tracking, and engineering analytics** through a centralized dashboard.

## Key Features

### 1. AI-Powered Project Planning
- Accepts software requirements in natural language.
- Uses LangChain and an OpenAI chat model to analyze requirements.
- Generates structured project plans using Pydantic models.
- Identifies project features, recommended technologies, database requirements, testing, and deployment considerations.

### 2. Automated Task Breakdown
- Converts project requirements into actionable development tasks.
- Assigns task priorities and estimated development hours.
- Identifies task dependencies.
- Generates tasks based on requirement-specific keywords and features.

### 3. Project Management
- Saves generated projects and tasks in SQLite.
- Retrieves previously created projects.
- Tracks task statuses: Pending, In Progress, and Done.
- Supports updating task status through REST APIs.

### 4. Engineering Analytics
- Tracks project completion percentages.
- Calculates estimated and completed development hours.
- Provides task-status summaries.
- Identifies unfinished and pending work.
- Maintains a recent activity history.

### 5. Backend API
- RESTful API architecture using FastAPI.
- Request and response validation using Pydantic.
- HTTP error handling for missing projects and tasks.
- CORS configuration for frontend integration.
- Interactive API documentation through Swagger UI.

## System Architecture

```text
             User Requirements
                    |
                    v
           React Frontend
                    |
                    v
             FastAPI Backend
                    |
          +---------+----------+
          |                    |
          v                    v
    Project Planner       Task Breakdown
          |                    |
          v                    v
    LangChain + LLM       Task Generation
          |                    |
          +---------+----------+
                    |
                    v
             Pydantic Models
                    |
                    v
               SQLite DB
                    |
          +---------+----------+
          |                    |
          v                    v
     Project Tracking     Analytics
          |                    |
          +---------+----------+
                    |
                    v
             Dashboard UI
```

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React, TypeScript, Vite |
| Generative AI | LangChain, LangChain OpenAI |
| AI Workflow | Structured LLM output |
| Data Validation | Pydantic |
| Database | SQLite |
| API | REST APIs, Swagger UI |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes configuration |
| Version Control | Git, GitHub |

## Project Structure

```text
ai-engineering-command-center/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── planner.py
│   │   │   └── task_breakdown.py
│   │   │
│   │   ├── models/
│   │   ├── database.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── k8s/
│
├── .github/
│   └── workflows/
│
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js and npm
- OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/vishuuu09/ai-engineering-command-center.git

cd ai-engineering-command-center
```

### 2. Configure the Backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

### 3. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the Frontend

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Open the Vite development URL shown in the terminal, usually:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend health welcome message |
| POST | `/projects` | Generate an AI-powered project plan |
| POST | `/tasks/breakdown` | Generate and save development tasks |
| GET | `/projects/saved` | Retrieve saved projects |
| GET | `/projects/saved/{project_id}/tasks` | Retrieve project tasks |
| PATCH | `/projects/saved/{project_id}/tasks/{task_code}/status` | Update task status |
| GET | `/projects/progress` | Retrieve project progress |
| GET | `/analytics` | Retrieve engineering analytics |
| GET | `/activities` | Retrieve recent activities |

## Database Design

The application uses SQLite with three primary tables:

- **Projects:** Stores project names, requirements, estimated hours, and creation timestamps.
- **Tasks:** Stores task descriptions, priorities, dependencies, estimated hours, and statuses.
- **Activities:** Records project creation and task status changes.

Foreign key relationships maintain consistency between projects, tasks, and activity records.

## Docker Support

The repository includes Docker configuration for containerizing the backend.

The configuration includes:
- Python 3.11 slim base image.
- Non-root application user.
- Health-check configuration.
- Resource limits.
- Read-only container filesystem.
- Temporary filesystem configuration.
- Restart policy.

Docker Compose configuration is available under `docker/`.

## Future Enhancements

- Multi-agent software development workflows.
- AI-assisted code generation and review.
- Automated test generation and execution.
- GitHub repository integration.
- Advanced project dependency visualization.
- CI/CD pipeline integration.
- Deployment and monitoring automation.

## Author

**Sai Vishal Mittapalli**

GitHub: [@vishuuu09](https://github.com/vishuuu09)

Project Repository: [AI Engineering Command Center](https://github.com/vishuuu09/ai-engineering-command-center)
