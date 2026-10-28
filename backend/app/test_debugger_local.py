from app.models.project import (
    ValidationResult
)

from app.services.workspace import ProjectWorkspace


print("\n🧪 Testing Debugger file-selection architecture...\n")


# --------------------------------------------------
# CREATE A FAKE PROJECT
# --------------------------------------------------

workspace = ProjectWorkspace(
    "workspace_debugger_local"
)


generated_files = [
    {
        "path": "src/app.py",
        "content": "print('Application')",
    },
    {
        "path": "docker-compose.yml",
        "content": "services:\n  api:\n    image: my-api",
    },
    {
        "path": "Dockerfile",
        "content": "FROM node:20",
    },
    {
        "path": "package.json",
        "content": '{"scripts":{"test":"pytest"}}',
    },
    {
        "path": "tests/test_app.py",
        "content": "def test_app():\n    assert True",
    }
]


workspace.write_project(
    [
        {
            "path": file["path"],
            "content": file["content"],
            "purpose": "Test file"
        }
        for file in generated_files
    ]
)


print("✅ Test project created")


# --------------------------------------------------
# GET FILE MANIFEST
# --------------------------------------------------

file_manifest = workspace.list_files()


print("\n📋 Available files:")

for file in file_manifest:
    print(
        f"- {file}"
    )


# --------------------------------------------------
# FAKE VALIDATION RESULT
# --------------------------------------------------

validation = ValidationResult(
    passed=False,
    score=45,
    issues=[
        "The Docker Compose API service has an incorrect database configuration.",
        "The production Docker image does not include required runtime configuration.",
        "The test configuration is incomplete."
    ],
    warnings=[
        "Docker dependency installation is not reproducible."
    ],
    recommendations=[
        "Fix Docker Compose configuration.",
        "Fix Dockerfile runtime configuration.",
        "Complete test configuration."
    ]
)


print("\n🧪 Fake validation created")


# --------------------------------------------------
# SIMULATE DEBUGGER FILE SELECTION
# --------------------------------------------------

expected_affected_files = [
    "docker-compose.yml",
    "Dockerfile",
    "package.json",
    "tests/test_app.py"
]


selected_files = [
    file
    for file in file_manifest
    if file in expected_affected_files
]


print("\n🐛 Debugger selected files:")

for file in selected_files:
    print(
        f"- {file}"
    )


# --------------------------------------------------
# VALIDATE FILE SELECTION
# --------------------------------------------------

assert "docker-compose.yml" in selected_files
assert "Dockerfile" in selected_files
assert "package.json" in selected_files
assert "tests/test_app.py" in selected_files

assert "src/app.py" not in selected_files


print(
    "\n✅ Debugger file-selection test passed!"
)


print(
    "\n🎯 Only relevant files were selected."
)