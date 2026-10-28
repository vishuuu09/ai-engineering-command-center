
from app.models.project import (
    DevelopmentTask,
    TaskBreakdownRequest,
    TaskBreakdownResponse,
)


def create_task_breakdown(
    request: TaskBreakdownRequest,
) -> TaskBreakdownResponse:
    requirement = request.requirement.strip()
    text = requirement.lower()

    tasks_data = [
        {
            "title": "Analyze requirements and define scope",
            "description": (
                "Review the requirement, identify core features, "
                "define acceptance criteria, and document assumptions."
            ),
            "priority": "High",
            "estimated_hours": 3.0,
            "dependencies": [],
        },
        {
            "title": "Design system architecture and database",
            "description": (
                "Define frontend and backend responsibilities, API "
                "contracts, data entities, and database relationships."
            ),
            "priority": "High",
            "estimated_hours": 5.0,
            "dependencies": ["T1"],
        },
        {
            "title": "Set up the development environment",
            "description": (
                "Configure the application structure, dependencies, "
                "environment variables, Git workflow, and local setup."
            ),
            "priority": "High",
            "estimated_hours": 3.0,
            "dependencies": ["T1"],
        },
        {
            "title": "Implement backend APIs",
            "description": (
                "Build REST endpoints, business logic, input validation, "
                "consistent error handling, and API documentation."
            ),
            "priority": "High",
            "estimated_hours": 8.0,
            "dependencies": ["T2", "T3"],
        },
        {
            "title": "Build the frontend interface",
            "description": (
                "Create responsive pages, reusable components, forms, "
                "navigation, and loading and error states."
            ),
            "priority": "High",
            "estimated_hours": 8.0,
            "dependencies": ["T2", "T3"],
        },
    ]

    if any(word in text for word in ["login", "authentication", "register", "jwt"]):
        tasks_data.append({
            "title": "Implement authentication and authorization",
            "description": (
                "Add registration, login, secure password hashing, "
                "token handling, and protected endpoints."
            ),
            "priority": "High",
            "estimated_hours": 6.0,
            "dependencies": ["T4"],
        })

    if any(word in text for word in ["task", "deadline", "assign", "priority"]):
        tasks_data.append({
            "title": "Implement task and project management",
            "description": (
                "Support creating, assigning, updating, prioritizing, "
                "filtering, and completing tasks and tracking project status."
            ),
            "priority": "High",
            "estimated_hours": 7.0,
            "dependencies": ["T4", "T5"],
        })

    if any(word in text for word in ["dashboard", "analytics", "chart", "report"]):
        tasks_data.append({
            "title": "Build dashboard and analytics",
            "description": (
                "Display project progress, task statistics, status summaries, "
                "and charts using available application data."
            ),
            "priority": "Medium",
            "estimated_hours": 4.0,
            "dependencies": ["T5", "T7"] if len(tasks_data) >= 7 else ["T4", "T5"],
        })

    if any(word in text for word in ["email", "notification", "deadline"]):
        tasks_data.append({
            "title": "Implement notifications",
            "description": (
                "Configure notification delivery and deadline reminders, "
                "including failure handling and scheduling where required."
            ),
            "priority": "Medium",
            "estimated_hours": 4.0,
            "dependencies": ["T4"],
        })

    if any(word in text for word in ["docker", "deployment", "deploy", "ci/cd", "github actions"]):
        tasks_data.append({
            "title": "Configure deployment and CI/CD",
            "description": (
                "Prepare Docker configuration, environment-based settings, "
                "automated checks, and a deployment workflow."
            ),
            "priority": "Medium",
            "estimated_hours": 5.0,
            "dependencies": ["T4", "T5"],
        })

    if any(word in text for word in ["test", "testing", "unit test", "integration"]):
        tasks_data.append({
            "title": "Write and run automated tests",
            "description": (
                "Test validation, business logic, API behavior, and important "
                "user flows. Fix defects discovered during testing."
            ),
            "priority": "High",
            "estimated_hours": 6.0,
            "dependencies": ["T4", "T5"],
        })
    else:
        tasks_data.append({
            "title": "Test and validate the application",
            "description": (
                "Verify core workflows, API responses, error handling, "
                "and frontend behavior. Fix any issues found."
            ),
            "priority": "High",
            "estimated_hours": 5.0,
            "dependencies": ["T4", "T5"],
        })

    tasks_data.append({
        "title": "Document setup and usage",
        "description": (
            "Document prerequisites, installation, configuration, "
            "API usage, and instructions for running the application."
        ),
        "priority": "Low",
        "estimated_hours": 2.0,
        "dependencies": [f"T{len(tasks_data)}"],
    })

    tasks = [
        DevelopmentTask(
            id=f"T{index}",
            title=item["title"],
            description=item["description"],
            priority=item["priority"],
            estimated_hours=item["estimated_hours"],
            dependencies=item["dependencies"],
            status="Pending",
        )
        for index, item in enumerate(tasks_data, start=1)
    ]

    project_name = (
        "Task Management Platform"
        if "task management" in text
        else "Project Development Plan"
    )

    return TaskBreakdownResponse(
        project_name=project_name,
        tasks=tasks,
        total_estimated_hours=sum(task.estimated_hours for task in tasks),
    )
