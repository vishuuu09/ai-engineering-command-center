import tempfile
from pathlib import Path

from app.services.repair_guard import RepairGuard


def run_test(name, condition, details=""):
    """Print a test result and fail immediately if it is unexpected."""
    if not condition:
        raise AssertionError(f"FAILED: {name}. {details}")

    print(f"PASS: {name}")


def main():
    print("\nTesting RepairGuard...\n")

    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir).resolve()

        # Create existing files because RepairGuard only permits
        # modifications to existing targets.
        (workspace / "safe.py").write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )

        (workspace / "broken.py").write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )

        (workspace / "dangerous.py").write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )

        guard = RepairGuard(str(workspace))

        # -------------------------------------------------
        # 1. Valid Python repair
        # -------------------------------------------------
        result = guard.validate_repair(
            "safe.py",
            "VALUE = 42\n",
        )

        run_test(
            "Valid Python repair is allowed",
            result["allowed"] is True,
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 2. Invalid Python syntax
        # -------------------------------------------------
        result = guard.validate_repair(
            "broken.py",
            "def broken(:\n    pass\n",
        )

        run_test(
            "Invalid Python syntax is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

        run_test(
            "Syntax error is reported",
            any(
                "syntax error" in error.lower()
                for error in result["errors"]
            ),
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 3. Dangerous Python import
        # -------------------------------------------------
        result = guard.validate_repair(
            "dangerous.py",
            "import subprocess\n"
            "subprocess.run(['whoami'])\n",
        )

        run_test(
            "Blocked Python import is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 4. Path traversal
        # -------------------------------------------------
        result = guard.validate_repair(
            "../outside.py",
            "VALUE = 1\n",
        )

        run_test(
            "Path traversal is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

        run_test(
            "Path traversal reason is reported",
            any(
                "escapes the workspace" in error.lower()
                for error in result["errors"]
            ),
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 5. Missing repair target
        # -------------------------------------------------
        result = guard.validate_repair(
            "missing.py",
            "VALUE = 1\n",
        )

        run_test(
            "Missing repair target is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 6. Empty repair content
        # -------------------------------------------------
        result = guard.validate_repair(
            "safe.py",
            "",
        )

        run_test(
            "Empty repair content is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

        # -------------------------------------------------
        # 7. Empty repair path
        # -------------------------------------------------
        result = guard.validate_repair(
            "",
            "VALUE = 1\n",
        )

        run_test(
            "Empty repair path is rejected",
            result["allowed"] is False,
            str(result["errors"]),
        )

    print("\n" + "=" * 50)
    print("ALL REPAIR GUARD TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()
