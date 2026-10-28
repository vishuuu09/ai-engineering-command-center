from app.agents.planner import create_project_plan
from app.agents.architect import create_architecture
from app.agents.developer import generate_project
from app.agents.validator import validate_project
from app.agents.debugger import debug_project

from app.services.workspace import ProjectWorkspace


requirement = """
Build a URL shortener API.

Users should be able to submit a long URL
and receive a shortened URL.

The system should support:

- URL creation
- URL redirection
- basic analytics
- testing
- Docker deployment
"""


print("\n🚀 Creating project plan...\n")

project_plan = create_project_plan(
    requirement
)


print("\n🏗️ Creating architecture...\n")

architecture = create_architecture(
    project_plan
)


print("\n💻 Generating project...\n")

project = generate_project(
    project_plan,
    architecture
)


print(
    f"\nGenerated {len(project.files)} files."
)


# --------------------------------------------------
# WRITE PROJECT TO WORKSPACE
# --------------------------------------------------

workspace = ProjectWorkspace(
    "workspace_debugger_test"
)


generated_files = [
    {
        "path": file.path,
        "content": file.content,
        "purpose": file.purpose
    }
    for file in project.files
]


workspace.write_project(
    generated_files
)


print(
    "\n📁 Project written to workspace."
)


# --------------------------------------------------
# VALIDATE PROJECT
# --------------------------------------------------

print("\n🧪 Validating project...\n")

validation = validate_project(
    project_plan,
    architecture,
    project
)


print(
    f"\nValidation Score: {validation.score}/100"
)


print("\nValidation Issues:")

for issue in validation.issues:
    print(
        f"- {issue}"
    )


# --------------------------------------------------
# BUILD FILE MANIFEST
# --------------------------------------------------

file_manifest = workspace.list_files()


print(
    "\n📋 Available project files:"
)

for file in file_manifest:
    print(
        f"- {file}"
    )


# --------------------------------------------------
# DEBUGGER
# --------------------------------------------------

print("\n🐛 Running Debugger...\n")


debug_result = debug_project(
    project_plan,
    architecture,
    validation,
    file_manifest
)


print(
    "\n================ DEBUG RESULT ================\n"
)


print(
    debug_result.model_dump_json(
        indent=2
    )
)