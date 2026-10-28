from typing import Dict, Any

from app.agents.planner import create_project_plan
from app.agents.architect import create_architecture
from app.agents.developer import generate_project
from app.agents.validator import validate_project
from app.agents.debugger import debug_project
from app.agents.repairer import repair_project

from app.models.project import (
    ProjectPlan,
    ArchitecturePlan,
    GeneratedProject,
    ValidationResult,
)

from app.services.workspace import ProjectWorkspace
from app.services.workspace_reader import WorkspaceReader
from app.services.repair_context import RepairContext
from app.services.execution_planner import ExecutionPlanner
from app.services.sandbox import SandboxRunner
from app.services.failure_classifier import FailureClassifier
from app.services.repair_decision import RepairDecision
from app.services.static_validator import StaticValidator
from app.services.static_validation_context import (
    StaticValidationContext
)
from app.services.repair_guard import RepairGuard


# ============================================================
# CONFIGURATION
# ============================================================

WORKSPACE_ROOT = "workspace"


# ============================================================
# PLANNER
# ============================================================

def planner_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🧠 PLANNER AGENT")

    requirement = state["requirement"]

    project_plan = create_project_plan(
        requirement
    )

    return {
        "project_plan": project_plan.model_dump(),
        "current_agent": "planner",
        "status": "planned",
    }


# ============================================================
# ARCHITECT
# ============================================================

def architect_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🏗️ ARCHITECT AGENT")

    project_plan = ProjectPlan(
        **state["project_plan"]
    )

    architecture = create_architecture(
        project_plan
    )

    return {
        "architecture": architecture.model_dump(),
        "current_agent": "architect",
        "status": "architected",
    }


# ============================================================
# DEVELOPER
# ============================================================

def developer_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n💻 DEVELOPER AGENT")

    project_plan = ProjectPlan(
        **state["project_plan"]
    )

    architecture = ArchitecturePlan(
        **state["architecture"]
    )

    generated_project = generate_project(
        project_plan,
        architecture
    )

    generated_files = [
        file.model_dump()
        for file in generated_project.files
    ]

    workspace = ProjectWorkspace(
        WORKSPACE_ROOT
    )

    workspace.write_project(
        generated_files
    )

    print(
        f"📁 Generated project written to "
        f"{WORKSPACE_ROOT}/"
    )

    return {
        "generated_files": generated_files,
        "current_agent": "developer",
        "status": "generated",
    }


# ============================================================
# EXECUTION
# ============================================================

def execution_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n▶️ EXECUTION ENGINE")

    planner = ExecutionPlanner(
        WORKSPACE_ROOT
    )

    plan = planner.plan(
        generated_files=state.get(
            "generated_files",
            []
        )
    )

    print(
        f"📋 Execution type: "
        f"{plan.get('type')}"
    )

    if not plan.get("command"):

        result = {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": (
                "No executable command "
                "was planned."
            ),
        }

        return {
            "execution_results": result,
            "current_agent": "execution",
            "status": "execution_failed",
        }

    sandbox = SandboxRunner(
        WORKSPACE_ROOT
    )

    result = sandbox.run_plan(
        plan
    )

    classifier = FailureClassifier()

    failure_type = classifier.classify(
        result
    )

    result["failure_type"] = failure_type

    print(
        f"🔎 Failure classification: "
        f"{failure_type}"
    )

    if result["success"]:

        print(
            "✅ Sandbox execution successful"
        )

    else:

        print(
            "❌ Sandbox execution failed"
        )

        print(
            f"   {result.get('stderr', '')}"
        )

    return {
        "execution_results": result,
        "current_agent": "execution",
        "status": (
            "execution_passed"
            if result["success"]
            else "execution_failed"
        ),
    }


# ============================================================
# STATIC VALIDATOR
# ============================================================

def static_validator_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🔍 STATIC VALIDATOR")

    validator = StaticValidator(
        WORKSPACE_ROOT
    )

    result = validator.validate()

    result_dict = result.to_dict()

    print(
        f"Static validation passed → "
        f"{result.passed}"
    )

    print(
        f"Static validation score → "
        f"{result.score}"
    )

    if result.issues:

        print(
            "❌ Static validation issues:"
        )

        for issue in result.issues:

            print(
                f"   - {issue}"
            )

    if result.warnings:

        print(
            "⚠️ Static validation warnings:"
        )

        for warning in result.warnings:

            print(
                f"   - {warning}"
            )

    if result.passed:

        print(
            "✅ Static validation passed"
        )

    else:

        print(
            "❌ Static validation failed"
        )

    return {
        "validation_results": result_dict,
        "current_agent": "static_validator",
        "status": (
            "static_validation_passed"
            if result.passed
            else "static_validation_failed"
        ),
    }


# ============================================================
# LLM VALIDATOR
# ============================================================

def validator_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🧠 LLM VALIDATOR")

    static_result = state.get(
        "validation_results"
    )

    # --------------------------------------------------------
    # Static validation must pass first.
    # --------------------------------------------------------

    if static_result and not static_result.get(
        "passed",
        False
    ):

        print(
            "⛔ LLM validation skipped."
        )

        print(
            "Static validation must pass first."
        )

        return {
            "validation_results": {
                "passed": False,
                "score": static_result.get(
                    "score",
                    0
                ),
                "issues": static_result.get(
                    "issues",
                    []
                ),
                "warnings": static_result.get(
                    "warnings",
                    []
                ),
                "recommendations": static_result.get(
                    "recommendations",
                    []
                ),
            },
            "current_agent": "validator",
            "status": "validation_failed",
        }

    project_plan = ProjectPlan(
        **state["project_plan"]
    )

    architecture = ArchitecturePlan(
        **state["architecture"]
    )

    generated_project = GeneratedProject(
        files=state["generated_files"]
    )

    result = validate_project(
        project_plan,
        architecture,
        generated_project
    )

    result_dict = result.model_dump()

    print(
        f"LLM validation passed → "
        f"{result.passed}"
    )

    print(
        f"LLM validation score → "
        f"{result.score}"
    )

    if result.issues:

        print(
            "❌ LLM validation issues:"
        )

        for issue in result.issues:

            print(
                f"   - {issue}"
            )

    if result.warnings:

        print(
            "⚠️ LLM validation warnings:"
        )

        for warning in result.warnings:

            print(
                f"   - {warning}"
            )

    return {
        "validation_results": result_dict,
        "current_agent": "validator",
        "status": (
            "validation_passed"
            if result.passed
            else "validation_failed"
        ),
    }


# ============================================================
# DEBUGGER
# ============================================================

def debugger_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🐞 DEBUGGER AGENT")

    project_plan = ProjectPlan(
        **state["project_plan"]
    )

    architecture = ArchitecturePlan(
        **state["architecture"]
    )

    generated_project = GeneratedProject(
        files=state["generated_files"]
    )

    validation_result = ValidationResult(
        **state["validation_results"]
    )

    execution_result = state.get(
        "execution_results"
    )

    # --------------------------------------------------------
    # Read actual physical workspace
    # --------------------------------------------------------

    workspace = ProjectWorkspace(
        WORKSPACE_ROOT
    )

    available_files = workspace.list_files()

    print(
        "\n📂 Workspace files:"
    )

    for file in available_files:

        print(
            f"   - {file}"
        )

    # --------------------------------------------------------
    # Build deterministic static-validation context
    # --------------------------------------------------------

    static_context_builder = (
        StaticValidationContext()
    )

    static_validation_context = (
        static_context_builder.build_context(
            state.get(
                "validation_results",
                {}
            )
        )
    )

    if static_validation_context:

        print(
            "\n🔍 Static validation evidence:"
        )

        print(
            static_validation_context
        )

    # --------------------------------------------------------
    # Ask Debugger Agent
    # --------------------------------------------------------

    debug_result = debug_project(
        project_plan,
        architecture,
        generated_project,
        validation_result,
        execution_result,
        static_validation_context
    )

    debug_dict = debug_result.model_dump()

    # --------------------------------------------------------
    # Safety check:
    # Debugger may only reference physical files.
    # --------------------------------------------------------

    valid_affected_files = []

    for path in debug_dict.get(
        "affected_files",
        []
    ):

        if path in available_files:

            valid_affected_files.append(
                path
            )

    debug_dict[
        "affected_files"
    ] = valid_affected_files

    valid_fixes = []

    for fix in debug_dict.get(
        "fixes",
        []
    ):

        file_path = fix.get(
            "file_path"
        )

        if file_path in available_files:

            valid_fixes.append(
                fix
            )

    debug_dict[
        "fixes"
    ] = valid_fixes

    print(
        "\n🎯 Debugger identified:"
    )

    for path in valid_affected_files:

        print(
            f"   - {path}"
        )

    return {
        "debug_results": debug_dict,
        "current_agent": "debugger",
        "status": "debugged",
    }


# ============================================================
# REPAIRER
# ============================================================

def repairer_node(
    state: Dict[str, Any]
) -> Dict[str, Any]:

    print("\n🔧 REPAIRER AGENT")

    project_plan = ProjectPlan(
        **state["project_plan"]
    )

    architecture = ArchitecturePlan(
        **state["architecture"]
    )

    debug_results = state.get(
        "debug_results",
        {}
    )

    affected_files = debug_results.get(
        "affected_files",
        []
    )

    if not affected_files:

        message = (
            "Debugger did not identify "
            "any valid physical files."
        )

        print(
            f"⚠️ {message}"
        )

        return {
            "repaired_files": [],
            "current_agent": "repairer",
            "status": "repair_failed",
            "errors": [message],
        }

    # --------------------------------------------------------
    # Read actual physical files
    # --------------------------------------------------------

    repair_context = RepairContext(
        WORKSPACE_ROOT
    )

    context = (
        repair_context.get_repair_context(
            affected_files
        )
    )

    # --------------------------------------------------------
    # Ask Repairer Agent for complete files
    # --------------------------------------------------------

    repair_result = repair_project(
        project_plan,
        architecture,
        debug_results,
        context
    )

    proposed_files = [
        file.model_dump()
        for file in repair_result.repaired_files
    ]

    # --------------------------------------------------------
    # Validate proposed repairs before writing anything
    # --------------------------------------------------------

    workspace = ProjectWorkspace(
        WORKSPACE_ROOT
    )

    guard = RepairGuard(
        WORKSPACE_ROOT
    )

    validated_proposals = []
    rejected_repairs = []
    repaired_paths = []

    for file in proposed_files:

        path = file.get(
            "path",
            ""
        )

        content = file.get(
            "content",
            ""
        )

        # Only allow files explicitly identified by the debugger.
        if path not in affected_files:

            rejected_repairs.append({
                "path": path or "<missing path>",
                "errors": [
                    "Repair target was not identified "
                    "as an affected file."
                ],
            })

            continue

        # Validate path, target existence, content and Python syntax.
        check = guard.validate_repair(
            path,
            content
        )

        if not check.get(
            "allowed",
            False
        ):

            rejected_repairs.append({
                "path": path,
                "errors": check.get(
                    "errors",
                    ["Repair was rejected."]
                ),
            })

            continue

        validated_proposals.append(
            (path, content)
        )

    # --------------------------------------------------------
    # Apply only repairs that passed the guard
    # --------------------------------------------------------

    for path, content in validated_proposals:

        workspace.write_file(
            path,
            content
        )

        repaired_paths.append(
            path
        )

        print(
            f"✅ Repaired physical file: {path}"
        )

    # --------------------------------------------------------
    # Report rejected repairs
    # --------------------------------------------------------

    for rejected in rejected_repairs:

        print(
            f"⛔ Rejected repair: "
            f"{rejected['path']}"
        )

        for error in rejected["errors"]:

            print(
                f"   - {error}"
            )

    print(
        "\n📁 Repaired physical files:"
    )

    for path in repaired_paths:

        print(
            f"   - {path}"
        )

    # --------------------------------------------------------
    # Rebuild generated file state from disk
    # --------------------------------------------------------

    reader = WorkspaceReader(
        WORKSPACE_ROOT
    )

    updated_generated_files = []

    for path in reader.list_files():

        updated_generated_files.append(
            {
                "path": path,
                "content": reader.read_file(
                    path
                ),
                "purpose": "Physical workspace file",
            }
        )

    # --------------------------------------------------------
    # Build repair results and error report
    # --------------------------------------------------------

    applied_repairs = [
        file
        for file in proposed_files
        if file.get("path") in repaired_paths
    ]

    errors = [
        (
            f"Rejected repair for {item['path']}: "
            + "; ".join(item["errors"])
        )
        for item in rejected_repairs
    ]

    if rejected_repairs:

        print(
            f"⚠️ Rejected repair proposals: "
            f"{len(rejected_repairs)}"
        )

    if not repaired_paths:

        print(
            "❌ No proposed repairs passed "
            "the Repair Guard."
        )

    return {
        "generated_files": updated_generated_files,
        "repaired_files": applied_repairs,
        "current_agent": "repairer",
        "status": (
            "repaired"
            if repaired_paths
            else "repair_failed"
        ),
        "errors": errors,
        "retry_count": (
            state.get(
                "retry_count",
                0
            ) + 1
        ),
    }


# ============================================================
# VALIDATION ROUTER
# ============================================================

def validation_router(
    state: Dict[str, Any]
) -> str:
    """
    Route validation results to repair, completion, or safe termination.
    """

    validation_result = state.get(
        "validation_results"
    )

    # If validation results are missing, request investigation.
    if not validation_result:
        return "debugger"

    # Successful validation ends the workflow normally.
    if validation_result.get(
        "passed",
        False
    ):
        return "complete"

    retry_count = state.get(
        "retry_count",
        0
    )

    execution_result = state.get(
        "execution_results",
        {}
    )

    decision_engine = RepairDecision()

    decision = decision_engine.decide(
        validation_result,
        execution_result,
        retry_count,
    )

    print(
        "\n🧭 REPAIR DECISION"
    )

    print(
        f"Action: {decision['action']}"
    )

    print(
        f"Reason: {decision['reason']}"
    )

    # Recoverable failure: route to debugger and repairer.
    if decision["action"] == "repair":
        return "debugger"

    # Maximum retries or permission error: stop safely.
    if decision["action"] == "stop":
        return "stop"

    # Successful completion only applies to a non-failure decision.
    return "complete"