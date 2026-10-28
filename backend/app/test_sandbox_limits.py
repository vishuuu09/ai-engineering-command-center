from app.services.workspace import ProjectWorkspace
from app.services.sandbox import SandboxRunner
from app.services.execution_limits import ExecutionLimits


WORKSPACE = "workspace_sandbox_limits"


print("\n🧪 Testing Sandbox Execution Limits...\n")


limits = ExecutionLimits(
    python_timeout_seconds=2,
    command_timeout_seconds=5,
    max_output_characters=100
)


workspace = ProjectWorkspace(
    WORKSPACE
)


# =========================================================
# OUTPUT LIMIT TEST
# =========================================================

workspace.write_file(
    "large_output.py",
    """
print("A" * 1000)
""".strip()
)


runner = SandboxRunner(
    WORKSPACE,
    limits
)


result = runner.run_python_file(
    "large_output.py"
)


print(
    f"Execution successful → "
    f"{result['success']}"
)

print(
    f"Output length → "
    f"{len(result['stdout'])}"
)

print(
    result["stdout"]
)


assert result["success"] is True

assert (
    "[OUTPUT TRUNCATED BY SANDBOX]"
    in result["stdout"]
)


# =========================================================
# TIMEOUT TEST
# =========================================================

workspace.write_file(
    "infinite.py",
    """
while True:
    pass
""".strip()
)


result = runner.run_python_file(
    "infinite.py"
)


print(
    f"\nInfinite loop successful → "
    f"{result['success']}"
)

print(
    f"Timeout result → "
    f"{result['stderr']}"
)


assert result["success"] is False

assert (
    "timed out"
    in result["stderr"].lower()
)


print(
    "\n🎉 SANDBOX EXECUTION LIMITS TEST PASSED!"
)