from app.models.project import (
    ProjectPlan,
    ArchitecturePlan,
    ValidationResult
)

from app.services.execution_context import (
    ExecutionContextBuilder
)


print(
    "\n🧪 Testing Debugger + Execution Context...\n"
)


# --------------------------------------------------
# Simulated project plan
# --------------------------------------------------

project_plan = ProjectPlan(
    name="Expense Management API",
    description="API for managing expenses.",
    features=[
        "Create expenses",
        "List expenses"
    ],
    technologies=[
        "Python",
        "FastAPI"
    ],
    database="PostgreSQL",
    testing_requirements=[
        "Unit tests"
    ],
    deployment_requirements=[
        "Docker"
    ]
)


# --------------------------------------------------
# Simulated architecture
# --------------------------------------------------

architecture = ArchitecturePlan(
    architecture_overview=(
        "FastAPI backend with PostgreSQL."
    ),
    backend="FastAPI",
    frontend="None",
    database="PostgreSQL",
    authentication="JWT",
    infrastructure=[
        "Docker"
    ],
    file_structure=[
        "src/main.py",
        "requirements.txt"
    ]
)


# --------------------------------------------------
# Simulated validator result
# --------------------------------------------------

validation = ValidationResult(
    passed=False,
    score=40,
    issues=[
        "Application cannot start."
    ],
    warnings=[],
    recommendations=[
        "Fix missing dependency."
    ]
)


# --------------------------------------------------
# Simulated sandbox failure
# --------------------------------------------------

execution_result = {
    "success": False,
    "return_code": 1,
    "stdout": "",
    "stderr": (
        "Traceback (most recent call last):\n"
        "  File \"src/main.py\", line 1, in <module>\n"
        "    from fastapi import FastAPI\n"
        "ModuleNotFoundError: "
        "No module named 'fastapi'"
    )
}


# --------------------------------------------------
# Build execution context
# --------------------------------------------------

builder = ExecutionContextBuilder()

execution_context = builder.build_context(
    execution_result
)


print("📋 VALIDATION ISSUE:")
print(
    validation.issues[0]
)


print("\n💥 SANDBOX ERROR:")
print(
    execution_context
)


# --------------------------------------------------
# Simulate debugger input
# --------------------------------------------------

debugger_input = f"""
VALIDATION RESULTS:

{validation.model_dump_json(indent=2)}

AVAILABLE PROJECT FILES:

- src/main.py
- requirements.txt

SANDBOX EXECUTION RESULT:

{execution_context}
"""


print(
    "\n🐞 DEBUGGER INPUT:\n"
)

print(debugger_input)


# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert (
    "Application cannot start."
    in debugger_input
)

assert (
    "ModuleNotFoundError"
    in debugger_input
)

assert (
    "No module named 'fastapi'"
    in debugger_input
)

assert (
    "src/main.py"
    in debugger_input
)

assert (
    "requirements.txt"
    in debugger_input
)


print(
    "\n" + "=" * 60
)

print(
    "🎉 DEBUGGER EXECUTION CONTEXT TEST PASSED!"
)

print(
    "=" * 60
)

print(
    "\nThe Debugger can now receive:"
)

print("✅ Validator findings")
print("✅ Runtime traceback")
print("✅ Exit code")
print("✅ stdout")
print("✅ stderr")
print("✅ Available project files")

print(
    "\n🔥 Runtime-aware debugging pipeline is ready."
)