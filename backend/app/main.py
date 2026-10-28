
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.project import ProjectRequest, ProjectPlan
from app.agents.planner import create_project_plan
from app.models.project import TaskBreakdownRequest, TaskBreakdownResponse
from app.agents.task_breakdown import create_task_breakdown
from app.database import save_task_breakdown
from fastapi import HTTPException
from app.database import get_saved_projects, get_saved_tasks, update_saved_task_status,save_task_breakdown, get_recent_activities
from pydantic import BaseModel

app = FastAPI(
    title="AI Engineering Command Center",
    version="0.1.0",
)

# Allow the local Vite development server to access this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    return {
        "message": "AI Engineering Command Center is running"
    }


@app.post("/projects", response_model=ProjectPlan)
def create_project(request: ProjectRequest):
    plan = create_project_plan(
        request.requirement
    )

    return plan


@app.post(
    "/tasks/breakdown",
    response_model=TaskBreakdownResponse,
)
def breakdown_project_tasks(request: TaskBreakdownRequest):
    # Generate the task breakdown using your existing free logic.
    plan = create_task_breakdown(request)

    # Save the project and its tasks to SQLite.
    save_task_breakdown(
        project_name=plan.project_name,
        requirement=request.requirement,
        tasks=plan.tasks,
    )

    # Return the same response your frontend already expects.
    return plan


class TaskStatusUpdate(BaseModel):
    status: str


@app.get("/projects/saved")
def list_saved_projects():
    return {"projects": get_saved_projects()}


@app.get("/projects/saved/{project_id}/tasks")
def list_project_tasks(project_id: int):
    projects = get_saved_projects()

    if not any(project["id"] == project_id for project in projects):
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "tasks": get_saved_tasks(project_id),
    }


@app.patch("/projects/saved/{project_id}/tasks/{task_code}/status")
def change_saved_task_status(
    project_id: int,
    task_code: str,
    request: TaskStatusUpdate,
):
    projects = get_saved_projects()

    if not any(project["id"] == project_id for project in projects):
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        updated = update_saved_task_status(
            project_id=project_id,
            task_code=task_code,
            status=request.status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "message": "Task status saved successfully",
        "project_id": project_id,
        "task_code": task_code,
        "status": request.status,
    }



@app.get("/activities")
def list_recent_activities(limit: int = 50):
    return {
        "activities": get_recent_activities(limit)
    }



@app.get("/projects/progress")
def get_project_progress():
    projects = get_saved_projects()
    project_results = []

    total_tasks = 0
    total_done = 0
    total_in_progress = 0
    total_pending = 0
    total_hours = 0.0
    completed_hours = 0.0

    for project in projects:
        tasks = get_saved_tasks(project["id"])

        done = sum(1 for task in tasks if task["status"] == "Done")
        in_progress = sum(
            1 for task in tasks if task["status"] == "In Progress"
        )
        pending = sum(
            1 for task in tasks if task["status"] == "Pending"
        )

        hours = sum(float(task["estimated_hours"]) for task in tasks)
        done_hours = sum(
            float(task["estimated_hours"])
            for task in tasks
            if task["status"] == "Done"
        )

        count = len(tasks)
        completion = round((done / count) * 100, 1) if count else 0

        project_results.append({
            "id": project["id"],
            "project_name": project["project_name"],
            "created_at": project["created_at"],
            "total_tasks": count,
            "completed_tasks": done,
            "in_progress_tasks": in_progress,
            "pending_tasks": pending,
            "completion_percentage": completion,
            "total_estimated_hours": round(hours, 1),
            "completed_estimated_hours": round(done_hours, 1),
        })

        total_tasks += count
        total_done += done
        total_in_progress += in_progress
        total_pending += pending
        total_hours += hours
        completed_hours += done_hours

    return {
        "summary": {
            "total_projects": len(projects),
            "total_tasks": total_tasks,
            "completed_tasks": total_done,
            "in_progress_tasks": total_in_progress,
            "pending_tasks": total_pending,
            "completion_percentage": (
                round((total_done / total_tasks) * 100, 1)
                if total_tasks else 0
            ),
            "total_estimated_hours": round(total_hours, 1),
            "completed_estimated_hours": round(completed_hours, 1),
        },
        "projects": project_results,
    }


@app.get("/analytics")
def get_task_analytics():
    projects = get_saved_projects()

    status_counts = {
        "Done": 0,
        "In Progress": 0,
        "Pending": 0,
    }

    project_analytics = []
    total_hours = 0.0
    completed_hours = 0.0
    unfinished_tasks = []

    for project in projects:
        tasks = get_saved_tasks(project["id"])

        done = sum(1 for task in tasks if task["status"] == "Done")
        in_progress = sum(
            1 for task in tasks if task["status"] == "In Progress"
        )
        pending = sum(
            1 for task in tasks if task["status"] == "Pending"
        )

        hours = sum(float(task["estimated_hours"]) for task in tasks)
        done_hours = sum(
            float(task["estimated_hours"])
            for task in tasks
            if task["status"] == "Done"
        )

        status_counts["Done"] += done
        status_counts["In Progress"] += in_progress
        status_counts["Pending"] += pending

        total_hours += hours
        completed_hours += done_hours

        for task in tasks:
            if task["status"] != "Done":
                unfinished_tasks.append({
                    "project_id": project["id"],
                    "project_name": project["project_name"],
                    "task_code": task["task_code"],
                    "title": task["title"],
                    "priority": task["priority"],
                    "status": task["status"],
                    "estimated_hours": task["estimated_hours"],
                })

        project_analytics.append({
            "project_id": project["id"],
            "project_name": project["project_name"],
            "total_tasks": len(tasks),
            "completed_tasks": done,
            "in_progress_tasks": in_progress,
            "pending_tasks": pending,
            "completion_percentage": (
                round(done / len(tasks) * 100, 1) if tasks else 0
            ),
            "total_estimated_hours": round(hours, 1),
            "completed_estimated_hours": round(done_hours, 1),
        })

    return {
        "summary": {
            "total_projects": len(projects),
            "total_tasks": sum(status_counts.values()),
            "status_counts": status_counts,
            "total_estimated_hours": round(total_hours, 1),
            "completed_estimated_hours": round(completed_hours, 1),
            "unfinished_tasks_count": len(unfinished_tasks),
        },
        "projects": project_analytics,
        "unfinished_tasks": unfinished_tasks,
    }
