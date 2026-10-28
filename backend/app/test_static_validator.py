from pathlib import Path
import shutil

from app.services.static_validator import (
    StaticValidator
)


TEST_WORKSPACE = (
    "workspace_static_validation_test"
)


def setup_workspace():

    root = Path(
        TEST_WORKSPACE
    )

    if root.exists():

        shutil.rmtree(root)

    (root / "src").mkdir(
        parents=True
    )

    (root / "tests").mkdir(
        parents=True
    )

    return root


def test_static_validator():

    print(
        "\n🧪 Testing Static Validator..."
    )

    root = setup_workspace()

    # --------------------------------------------------------
    # Valid Python file
    # --------------------------------------------------------

    (
        root / "src" / "main.py"
    ).write_text(
        """
def hello():
    return "hello"

print(hello())
""",
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Test file
    # --------------------------------------------------------

    (
        root / "tests" / "test_main.py"
    ).write_text(
        """
from src.main import hello

def test_hello():
    assert hello() == "hello"
""",
        encoding="utf-8"
    )

    validator = StaticValidator(
        TEST_WORKSPACE
    )

    result = validator.validate()

    print(
        f"Validation passed → "
        f"{result.passed}"
    )

    print(
        f"Score → "
        f"{result.score}"
    )

    print(
        f"Issues → "
        f"{result.issues}"
    )

    print(
        f"Warnings → "
        f"{result.warnings}"
    )

    assert result.passed is True

    # --------------------------------------------------------
    # Introduce syntax error
    # --------------------------------------------------------

    (
        root / "src" / "broken.py"
    ).write_text(
        """
def broken(
    print("broken")
""",
        encoding="utf-8"
    )

    result = validator.validate()

    print(
        "\nAfter introducing syntax error:"
    )

    print(
        f"Validation passed → "
        f"{result.passed}"
    )

    print(
        f"Issues → "
        f"{result.issues}"
    )

    assert result.passed is False

    assert any(
        "syntax error" in issue.lower()
        for issue in result.issues
    )

    print(
        "\n🎉 STATIC VALIDATOR TEST PASSED!"
    )


if __name__ == "__main__":

    test_static_validator()