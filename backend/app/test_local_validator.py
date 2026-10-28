from pathlib import Path
import shutil

from app.services.local_validator import LocalValidator


TEST_WORKSPACE = "workspace_local_validator"


def setup_workspace():

    root = Path(TEST_WORKSPACE)

    if root.exists():
        shutil.rmtree(root)

    (root / "src").mkdir(
        parents=True,
        exist_ok=True
    )

    (root / "src" / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8"
    )

    return root


def test_valid_project():

    root = setup_workspace()

    validator = LocalValidator(
        TEST_WORKSPACE
    )

    result = validator.validate()

    print("\nValid project result:")
    print(result)

    assert result["passed"] is True

    shutil.rmtree(root)


def test_syntax_error():

    root = setup_workspace()

    (root / "src" / "broken.py").write_text(
        "def broken(:\n",
        encoding="utf-8"
    )

    validator = LocalValidator(
        TEST_WORKSPACE
    )

    result = validator.validate()

    print("\nSyntax error result:")
    print(result)

    assert result["passed"] is False

    assert any(
        "syntax error" in issue.lower()
        for issue in result["issues"]
    )

    shutil.rmtree(root)


def test_empty_python_file():

    root = setup_workspace()

    (root / "src" / "empty.py").write_text(
        "",
        encoding="utf-8"
    )

    validator = LocalValidator(
        TEST_WORKSPACE
    )

    result = validator.validate()

    print("\nEmpty file result:")
    print(result)

    assert result["passed"] is False

    assert any(
        "empty" in issue.lower()
        for issue in result["issues"]
    )

    shutil.rmtree(root)


if __name__ == "__main__":

    test_valid_project()
    test_syntax_error()
    test_empty_python_file()

    print(
        "\n🎉 LOCAL VALIDATOR TEST PASSED!"
    )