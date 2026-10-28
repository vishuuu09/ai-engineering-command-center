from app.services.workspace import ProjectWorkspace
from app.services.sandbox import SandboxRunner


WORKSPACE = "workspace_sandbox_security"


print("\n🧪 Testing Secure Sandbox...\n")


workspace = ProjectWorkspace(
    WORKSPACE
)

# ---------------------------------------------------------
# Safe Python program
# ---------------------------------------------------------

workspace.write_file(
    "safe.py",
    """
print("SAFE_EXECUTION")
""".strip()
)


runner = SandboxRunner(
    WORKSPACE
)


result = runner.run_python_file(
    "safe.py"
)

print(
    f"Safe execution → {result['success']}"
)

assert result["success"] is True
assert "SAFE_EXECUTION" in result["stdout"]


# ---------------------------------------------------------
# Dangerous Python program
# ---------------------------------------------------------

workspace.write_file(
    "dangerous.py",
    """
import subprocess

subprocess.run(["whoami"])
""".strip()
)


result = runner.run_python_file(
    "dangerous.py"
)

print(
    f"Dangerous Python → {result['success']}"
)

print(
    f"Reason → {result['stderr']}"
)

assert result["success"] is False
assert "Blocked Python module" in result["stderr"]


# ---------------------------------------------------------
# Path traversal
# ---------------------------------------------------------

result = runner.run_python_file(
    "../../secret.py"
)

print(
    f"Path traversal → {result['success']}"
)

assert result["success"] is False
assert "escapes the sandbox" in result["stderr"]


# ---------------------------------------------------------
# Dangerous command
# ---------------------------------------------------------

result = runner.run_command(
    ["del", "important.txt"]
)

print(
    f"Dangerous command → {result['success']}"
)

assert result["success"] is False
assert "Blocked command" in result["stderr"]


print(
    "\n🎉 SECURE SANDBOX TEST PASSED!"
)