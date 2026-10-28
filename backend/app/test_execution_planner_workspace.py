from app.services.execution_planner import ExecutionPlanner
from app.services.workspace import ProjectWorkspace


WORKSPACE = "workspace_execution_test"


print("\n🧪 Testing Workspace-Aware Execution Planner...\n")


workspace = ProjectWorkspace(
    WORKSPACE
)


# Initial project
workspace.write_file(
    "src/main.py",
    """
print("initial application")
""".strip()
)

workspace.write_file(
    "tests/test_main.py",
    """
def test_example():
    assert True
""".strip()
)


planner = ExecutionPlanner(
    WORKSPACE
)


plan = planner.plan()


print("Initial execution plan:")
print(plan)


assert plan["type"] == "tests"
assert plan["command"] == [
    "python",
    "-m",
    "pytest"
]


# Simulate a repair
workspace.write_file(
    "tests/test_repaired.py",
    """
def test_repaired():
    assert 2 + 2 == 4
""".strip()
)


current_files = planner.get_workspace_files()


print("\nCurrent physical workspace files:")

for file in current_files:
    print(f" - {file}")


assert "tests/test_repaired.py" in current_files


new_plan = planner.plan()


print("\nExecution plan after repair:")
print(new_plan)


assert new_plan["type"] == "tests"


print(
    "\n🎉 WORKSPACE-AWARE "
    "EXECUTION PLANNER TEST PASSED!"
)