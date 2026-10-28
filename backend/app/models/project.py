from pydantic import BaseModel, Field
from typing import List


class ProjectPlan(BaseModel):
    name: str = Field(description="Name of the software project")

    description: str = Field(
        description="Short description of what the software should do"
    )

    features: List[str] = Field(
        description="Main functional features of the project"
    )

    technologies: List[str] = Field(
        description="Recommended technologies for the project"
    )

    database: str = Field(
        description="Recommended database"
    )

    testing_requirements: List[str] = Field(
        description="Testing requirements"
    )

    deployment_requirements: List[str] = Field(
        description="Deployment requirements"
    )


class ProjectRequest(BaseModel):
    requirement: str = Field(
        min_length=10,
        description="Software requirement provided by the user"
    )


class ArchitecturePlan(BaseModel):
    architecture_overview: str = Field(
        description="High-level architecture description"
    )

    backend: str = Field(
        description="Backend technology and architecture"
    )

    frontend: str = Field(
        description="Frontend technology and architecture"
    )

    database: str = Field(
        description="Database architecture"
    )

    authentication: str = Field(
        description="Authentication and authorization approach"
    )

    infrastructure: List[str] = Field(
        description="Infrastructure components"
    )

    file_structure: List[str] = Field(
        description="Expected project files and directories"
    )

class GeneratedFile(BaseModel):
    path: str = Field(
        description="Relative path of the generated file"
    )

    content: str = Field(
        description="Complete source code/content of the file"
    )

    purpose: str = Field(
        description="Short explanation of what this file does"
    )

class GeneratedProject(BaseModel):
    files: List[GeneratedFile] = Field(
        description="Files generated for the project"
    )
class ValidationResult(BaseModel):

    passed: bool = Field(
        description="Whether the generated project is valid"
    )

    score: int = Field(
        description="Overall quality score from 0 to 100"
    )

    issues: List[str] = Field(
        description="Problems found in the generated project"
    )

    warnings: List[str] = Field(
        description="Non-blocking warnings"
    )

    recommendations: List[str] = Field(
        description="Recommended improvements"
    )

class DebugFix(BaseModel):

    file_path: str = Field(
        description="Relative path of the file that needs to be fixed"
    )

    issue: str = Field(
        description="Specific issue found in this file"
    )

    fix: str = Field(
        description="Specific change required to fix the issue"
    )


class DebugResult(BaseModel):

    affected_files: List[str] = Field(
        description="Relative paths of files that need to be inspected or modified"
    )

    fixes: List[DebugFix] = Field(
        description="Concrete fixes required in the affected files"
    )

    summary: str = Field(
        description="Short summary of what needs to be fixed"
    )

    should_retry: bool = Field(
        description="Whether the project should be repaired and validated again"
    )

class RepairFile(BaseModel):

    path: str = Field(
        description="Relative path of the file being repaired"
    )

    content: str = Field(
        description="Complete corrected content of the file"
    )

    explanation: str = Field(
        description="Short explanation of the repair"
    )


class RepairResult(BaseModel):

    repaired_files: List[RepairFile] = Field(
        description="Complete corrected files"
    )

    summary: str = Field(
        description="Summary of the repairs performed"
    )

    changes_made: bool = Field(
        description="Whether any changes were made"
    )

class ExecutionResult(BaseModel):
    success: bool = Field(
        description="Whether the command executed successfully"
    )
    return_code: int = Field(
        description="Process exit code"
    )
    stdout: str = Field(
        description="Standard output from the process"
    )
    stderr: str = Field(
        description="Standard error from the process"
    )

class DevelopmentTask(BaseModel):
    id: str = Field(
        description="Unique identifier for the task"
    )

    title: str = Field(
        description="Short, actionable development task title"
    )

    description: str = Field(
        description="Detailed explanation of the work required"
    )

    priority: str = Field(
        description="Task priority: High, Medium, or Low"
    )

    estimated_hours: float = Field(
        gt=0,
        description="Estimated engineering effort in hours"
    )

    dependencies: List[str] = Field(
        default_factory=list,
        description="IDs of tasks that must be completed first"
    )

    status: str = Field(
        default="Pending",
        description="Task status: Pending, In Progress, or Done"
    )


class TaskBreakdownRequest(BaseModel):
    requirement: str = Field(
        min_length=10,
        description="Software requirement to break into development tasks"
    )


class TaskBreakdownResponse(BaseModel):
    project_name: str = Field(
        description="Name of the project"
    )

    tasks: List[DevelopmentTask] = Field(
        description="Ordered list of actionable development tasks"
    )

    total_estimated_hours: float = Field(
        ge=0,
        description="Sum of the estimated hours for all tasks"
    )
