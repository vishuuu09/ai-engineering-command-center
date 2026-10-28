import tempfile

from app.services.execution_planner import ExecutionPlanner


def run_test(generated_files):
    with tempfile.TemporaryDirectory(
        prefix="execution_planner_test_"
    ) as workspace:
        planner = ExecutionPlanner(workspace_root=workspace)
        return planner.plan(generated_files)


def test_project_with_tests():
    generated_files = [
        {
            "path": "src/main.py",
            "content": "",
            "purpose": "Application entry point",
        },
        {
            "path": "src/config.py",
            "content": "",
            "purpose": "Configuration",
        },
        {
            "path": "tests/test_main.py",
            "content": "",
            "purpose": "Application tests",
        },
    ]

    plan = run_test(generated_files)

    print("\nTest 1:")
    print(plan)

    assert plan["type"] == "tests"
    assert plan["command"] == ["python", "-m", "pytest"]
    assert "tests/test_main.py" in plan["target_files"]

    print("PASS: Test files correctly selected")


def test_application_entry_point():
    generated_files = [
        {
            "path": "src/main.py",
            "content": "",
            "purpose": "Application entry point",
        },
        {
            "path": "src/config.py",
            "content": "",
            "purpose": "Configuration",
        },
    ]

    plan = run_test(generated_files)

    print("\nTest 2:")
    print(plan)

    assert plan["type"] == "application"
    assert plan["command"] == ["python", "src/main.py"]
    assert plan["target_files"] == ["src/main.py"]

    print("PASS: Application entry point correctly selected")


def test_no_executable_files():
    generated_files = [
        {
            "path": "README.md",
            "content": "",
            "purpose": "Documentation",
        }
    ]

    plan = run_test(generated_files)

    print("\nTest 3:")
    print(plan)

    assert plan["type"] == "none"
    assert plan["command"] == []
    assert plan["target_files"] == []

    print("PASS: Non-executable project handled correctly")


def test_python_fallback():
    generated_files = [
        {
            "path": "src/helper.py",
            "content": "",
            "purpose": "Python helper",
        }
    ]

    plan = run_test(generated_files)

    print("\nTest 4:")
    print(plan)

    assert plan["type"] == "python"
    assert plan["command"] == ["python", "src/helper.py"]
    assert plan["target_files"] == ["src/helper.py"]

    print("PASS: Python fallback correctly selected")


if __name__ == "__main__":
    print("\nTesting Execution Planner...")

    test_project_with_tests()
    test_application_entry_point()
    test_no_executable_files()
    test_python_fallback()

    print("\n" + "=" * 50)
    print("ALL EXECUTION PLANNER TESTS PASSED")
    print("=" * 50)
