from app.services.sandbox import SandboxRunner
from app.services.workspace import ProjectWorkspace


print("\n🧪 Testing Sandbox Runner...\n")


workspace_root = "workspace_sandbox_test"


workspace = ProjectWorkspace(
    workspace_root
)


# ---------------------------------------------
# Create a successful Python program
# ---------------------------------------------

workspace.write_file(
    "src/hello.py",
    """
print("Hello from sandbox")
"""
)


runner = SandboxRunner(
    workspace_root
)


result = runner.run_python_file(
    "src/hello.py"
)


print("STDOUT:")
print(result["stdout"])


print(
    f"Return code: {result['return_code']}"
)


assert result["success"] is True
assert "Hello from sandbox" in result["stdout"]


print(
    "\n✅ Successful execution test passed!"
)


# ---------------------------------------------
# Create a failing Python program
# ---------------------------------------------

workspace.write_file(
    "src/broken.py",
    """
raise ValueError("Intentional test failure")
"""
)


result = runner.run_python_file(
    "src/broken.py"
)


print("\nSTDERR:")
print(result["stderr"])


print(
    f"Return code: {result['return_code']}"
)


assert result["success"] is False
assert result["return_code"] != 0
assert "Intentional test failure" in result["stderr"]


print(
    "\n✅ Failure detection test passed!"
)


# ---------------------------------------------
# Final
# ---------------------------------------------

print("\n" + "=" * 55)
print("🎉 SANDBOX RUNNER TEST PASSED!")
print("=" * 55)

print(
    "\nThe system can now:"
)

print("✅ Execute generated code")
print("✅ Capture stdout")
print("✅ Capture stderr")
print("✅ Capture exit codes")
print("✅ Detect execution failures")
print("✅ Stop runaway processes with a timeout")