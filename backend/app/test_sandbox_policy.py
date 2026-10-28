from app.services.sandbox_policy import SandboxPolicy


print("\n🧪 Testing Sandbox Security Policy...\n")


policy = SandboxPolicy(
    "workspace_security_test"
)


# ---------------------------------------------------------
# Allowed command
# ---------------------------------------------------------

allowed, reason = policy.validate_command(
    ["python", "main.py"]
)

print(
    f"Python command → {allowed} | {reason}"
)

assert allowed is True


# ---------------------------------------------------------
# Blocked command
# ---------------------------------------------------------

allowed, reason = policy.validate_command(
    ["del", "important.txt"]
)

print(
    f"Delete command → {allowed} | {reason}"
)

assert allowed is False


# ---------------------------------------------------------
# Allowed path
# ---------------------------------------------------------

allowed, reason = policy.validate_path(
    "src/main.py"
)

print(
    f"Workspace path → {allowed} | {reason}"
)

assert allowed is True


# ---------------------------------------------------------
# Path traversal protection
# ---------------------------------------------------------

allowed, reason = policy.validate_path(
    "../../secret.txt"
)

print(
    f"Path traversal → {allowed} | {reason}"
)

assert allowed is False


# ---------------------------------------------------------
# Allowed Python content
# ---------------------------------------------------------

allowed, reason = policy.validate_python_content(
    """
def hello():
    return "hello"
"""
)

print(
    f"Safe Python → {allowed} | {reason}"
)

assert allowed is True


# ---------------------------------------------------------
# Blocked Python module
# ---------------------------------------------------------

allowed, reason = policy.validate_python_content(
    """
import subprocess

subprocess.run(["whoami"])
"""
)

print(
    f"Dangerous Python → {allowed} | {reason}"
)

assert allowed is False


print(
    "\n🎉 SANDBOX SECURITY POLICY TEST PASSED!"
)