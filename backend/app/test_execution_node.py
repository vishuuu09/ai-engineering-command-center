from app.services.workspace import ProjectWorkspace
from app.workflows.nodes import execution_node


print("\n🧪 Testing Execution Node...\n")


workspace_root = "workspace_execution_test"


workspace = ProjectWorkspace(
    workspace_root
)


workspace.write_file(
    "src/hello.py",
    """
print("Hello from AI Engineering Command Center")
"""
)


state = {
    "generated_files": [
        {
            "path": "src/hello.py",
            "content": """
print("Hello from AI Engineering Command Center")
""",
            "purpose": "Test program"
        }
    ]
}


# execution_node currently uses "workspace"
# so create the same file there too.

workspace = ProjectWorkspace(
    "workspace"
)


workspace.write_file(
    "src/hello.py",
    """
print("Hello from AI Engineering Command Center")
"""
)


state = {
    "generated_files": [
        {
            "path": "src/hello.py",
            "content": """
print("Hello from AI Engineering Command Center")
""",
            "purpose": "Test program"
        }
    ]
}


result = execution_node(
    state
)


print("\n📊 Execution Result:")
print(result)


assert result[
    "execution_results"
]["success"] is True


assert (
    "Hello from AI Engineering Command Center"
    in result["execution_results"]["stdout"]
)


print(
    "\n🎉 EXECUTION NODE TEST PASSED!"
)


print(
    "✅ Generated file → Workspace → Sandbox → ExecutionResult"
)