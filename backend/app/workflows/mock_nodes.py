from pathlib import Path
from typing import Any, Dict

from app.services.workspace import ProjectWorkspace
from app.services.execution_planner import ExecutionPlanner
from app.services.sandbox import SandboxRunner
from app.services.failure_classifier import FailureClassifier
from app.services.repair_decision import RepairDecision
from app.services.repair_guard import RepairGuard


WORKSPACE_ROOT = "workspace_local_graph"


def _get_workspace_root(state: Dict[str, Any]) -> str:
    """Return the workspace configured in the current workflow state."""
    return str(state.get("workspace_root") or WORKSPACE_ROOT)


# ============================================================
# MOCK PLANNER
# ============================================================

def mock_planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n🧠 MOCK PLANNER")

    project_plan = {
        "name": "Mock Autonomous Project",
        "description": (
            "A test project used to verify "
            "autonomous engineering and repair."
        ),
        "features": [
            "Application execution",
            "Automated validation",
            "Automatic debugging",
            "Automatic repair",
        ],
        "technologies": ["Python"],
        "database": "PostgreSQL",
        "testing_requirements": ["Run automated tests"],
        "deployment_requirements": ["Local execution"],
    }

    return {
        "project_plan": project_plan,
        "current_agent": "planner",
        "status": "planned",
    }


# ============================================================
# MOCK ARCHITECT
# ============================================================

def mock_architect_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n🏗️ MOCK ARCHITECT")

    architecture = {
        "architecture_overview": (
            "Simple Python application "
            "with configuration and tests."
        ),
        "backend": "Python",
        "frontend": "None",
        "database": "PostgreSQL",
        "authentication": "None",
        "infrastructure": [
            "Local workspace",
            "Python runtime",
        ],
        "file_structure": [
            "src/main.py",
            "src/config.py",
            "tests/test_main.py",
        ],
    }

    return {
        "architecture": architecture,
        "current_agent": "architect",
        "status": "architected",
    }


# ============================================================
# MOCK DEVELOPER
# ============================================================

def mock_developer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n💻 MOCK DEVELOPER")

    workspace_root = _get_workspace_root(state)
    workspace = ProjectWorkspace(workspace_root)

    generated_files = [
        {
            "path": "src/main.py",
            "content": (
                "from src.config import DATABASE_URL\n\n"
                "def get_database_url():\n"
                "    return DATABASE_URL\n\n"
                "if __name__ == '__main__':\n"
                "    print(get_database_url())\n"
            ),
            "purpose": "Application entry point.",
        },
        {
            "path": "src/config.py",
            "content": (
                'DATABASE_URL = '
                '"postgresql://localhost:5432/app"\n'
            ),
            "purpose": "Application database configuration.",
        },
        {
            "path": "tests/test_main.py",
            "content": (
                "from src.main import get_database_url\n\n"
                "def test_database_url():\n"
                "    assert get_database_url()\n"
            ),
            "purpose": "Basic application test.",
        },
    ]

    workspace.write_project(generated_files)

    print(f"📁 Generated project written to {workspace_root}/")

    return {
        "generated_files": generated_files,
        "current_agent": "developer",
        "status": "generated",
    }


# ============================================================
# MOCK EXECUTION
# ============================================================

def mock_execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n▶️ SANDBOX EXECUTION STARTED")

    workspace_root = _get_workspace_root(state)
    print(f"📁 Workspace: {workspace_root}")

    planner = ExecutionPlanner(workspace_root)
    plan = planner.plan(state.get("generated_files", []))

    print(f"📋 Execution type: {plan.get('type')}")

    if plan.get("type") == "none":
        result = {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": "No executable target found.",
        }
    else:
        sandbox = SandboxRunner(workspace_root)
        result = sandbox.run_plan(plan)

    classifier = FailureClassifier()
    failure_type = classifier.classify(result)
    result["failure_type"] = failure_type

    print(f"🔎 Failure classification: {failure_type}")

    if result.get("success"):
        print("✅ Sandbox execution successful")
    else:
        print("❌ Sandbox execution failed")
        if result.get("stderr"):
            print(f"STDERR:\n{result['stderr']}")

    return {
        "execution_results": result,
        "current_agent": "sandbox",
        "status": (
            "execution_success"
            if result.get("success")
            else "execution_failed"
        ),
    }


# ============================================================
# MOCK VALIDATOR
# ============================================================

def mock_validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n🔍 MOCK VALIDATOR")

    workspace_root = _get_workspace_root(state)
    config_path = Path(workspace_root) / "src" / "config.py"
    issues = []

    if not config_path.exists():
        issues.append("src/config.py is missing")
    else:
        content = config_path.read_text(encoding="utf-8")

        if "localhost:5432" in content:
            issues.append("database uses localhost")

    if issues:
        print(f"❌ Validation failed: {issues[0]}")

        validation = {
            "passed": False,
            "score": 50,
            "issues": issues,
            "warnings": [],
            "recommendations": [
                "Use the service hostname "
                "for the database connection."
            ],
        }
    else:
        print("✅ Validation passed")

        validation = {
            "passed": True,
            "score": 100,
            "issues": [],
            "warnings": [],
            "recommendations": [],
        }

    return {
        "validation_results": validation,
        "current_agent": "validator",
        "status": (
            "validation_passed"
            if validation["passed"]
            else "validation_failed"
        ),
    }


# ============================================================
# MOCK DEBUGGER
# ============================================================

def mock_debugger_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n🐞 MOCK DEBUGGER")

    workspace_root = _get_workspace_root(state)
    config_path = Path(workspace_root) / "src" / "config.py"

    affected_files = []
    fixes = []

    if config_path.exists():
        affected_files.append("src/config.py")

        fixes.append(
            {
                "file_path": "src/config.py",
                "issue": (
                    "Database connection uses localhost instead "
                    "of the container service hostname."
                ),
                "fix": (
                    "Replace localhost:5432 "
                    "with postgres:5432."
                ),
            }
        )

    print("🎯 Debugger identified src/config.py")

    debug_result = {
        "affected_files": affected_files,
        "fixes": fixes,
        "summary": (
            "Database configuration must use the postgres "
            "service hostname."
        ),
        "should_retry": bool(affected_files),
    }

    return {
        "debug_results": debug_result,
        "current_agent": "debugger",
        "status": "debugged",
    }


# ============================================================
# MOCK REPAIRER — GUARDED PHYSICAL REPAIR
# ============================================================

def mock_repairer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n🔧 MOCK REPAIRER")

    workspace_root = _get_workspace_root(state)
    config_path = Path(workspace_root) / "src" / "config.py"
    relative_path = "src/config.py"
    retry_count = state.get("retry_count", 0) + 1

    if not config_path.exists():
        message = "Repair failed: src/config.py does not exist."
        print(f"❌ {message}")

        return {
            "repaired_files": [],
            "retry_count": retry_count,
            "current_agent": "repairer",
            "status": "repair_failed",
            "errors": [message],
        }

    debug_results = state.get("debug_results") or {}
    affected_files = debug_results.get("affected_files", [])

    if relative_path not in affected_files:
        message = (
            "Repair rejected: src/config.py was not identified "
            "as an affected file by the debugger."
        )
        print(f"⛔ {message}")

        return {
            "repaired_files": [],
            "retry_count": retry_count,
            "current_agent": "repairer",
            "status": "repair_failed",
            "errors": [message],
        }

    content = config_path.read_text(encoding="utf-8")

    repaired_content = content.replace(
        "localhost:5432",
        "postgres:5432",
    )

    if repaired_content == content:
        message = (
            "No repair was applied: localhost:5432 "
            "was not found in src/config.py."
        )
        print(f"⚠️ {message}")

        return {
            "repaired_files": [],
            "retry_count": retry_count,
            "current_agent": "repairer",
            "status": "repair_failed",
            "errors": [message],
        }

    # Validate the proposed change before writing to disk.
    guard = RepairGuard(str(workspace_root))
    check = guard.validate_repair(
        relative_path,
        repaired_content,
    )

    if not check.get("allowed", False):
        errors = check.get(
            "errors",
            ["RepairGuard rejected the proposed change."],
        )

        print("⛔ Repair rejected by RepairGuard.")

        for error in errors:
            print(f"   - {error}")

        return {
            "repaired_files": [],
            "retry_count": retry_count,
            "current_agent": "repairer",
            "status": "repair_failed",
            "errors": errors,
        }

    # Write the file only after RepairGuard approves the change.
    config_path.write_text(
        repaired_content,
        encoding="utf-8",
    )

    print(
        "✅ Guarded physical repair completed: "
        "src/config.py"
    )

    repaired_files = [
        {
            "path": relative_path,
            "content": repaired_content,
            "explanation": (
                "Replaced localhost:5432 with postgres:5432 "
                "after RepairGuard approved the proposed content."
            ),
        }
    ]

    return {
        "repaired_files": repaired_files,
        "retry_count": retry_count,
        "current_agent": "repairer",
        "status": "repaired",
        "errors": [],
    }


# ============================================================
# MOCK VALIDATION ROUTER
# ============================================================

def mock_validation_router(state: Dict[str, Any]) -> str:
    validation = state.get("validation_results") or {}
    execution = state.get("execution_results") or {}
    retry_count = state.get("retry_count", 0)

    decision_engine = RepairDecision()

    decision = decision_engine.decide(
        validation_result=validation,
        execution_result=execution,
        retry_count=retry_count,
    )

    print("\n🧭 REPAIR DECISION")
    print(f"Action: {decision['action']}")
    print(f"Reason: {decision['reason']}")

    if decision["action"] == "complete":
        print("✅ Project completed successfully")
        return "complete"

    if decision["action"] == "repair":
        print("🔧 Repair required")
        return "debugger"

    print("🛑 Autonomous repair stopped")
    return "complete"