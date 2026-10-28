from pathlib import Path
import shutil

from app.services.workspace import (
    ProjectWorkspace
)


TEST_WORKSPACE = (
    "workspace_security_test"
)


def cleanup():

    root = Path(
        TEST_WORKSPACE
    )

    if root.exists():

        shutil.rmtree(root)


def test_workspace_security():

    print(
        "\n🧪 Testing Workspace Security..."
    )

    cleanup()

    workspace = ProjectWorkspace(
        TEST_WORKSPACE
    )

    # --------------------------------------------------------
    # Safe write
    # --------------------------------------------------------

    workspace.write_file(
        "src/main.py",
        "print('hello')"
    )

    print(
        "Safe write → PASS"
    )

    assert (
        "src/main.py"
        in workspace.list_files()
    )

    # --------------------------------------------------------
    # Safe read
    # --------------------------------------------------------

    content = workspace.read_file(
        "src/main.py"
    )

    print(
        f"Safe read → {content}"
    )

    assert content == "print('hello')"

    # --------------------------------------------------------
    # Path traversal
    # --------------------------------------------------------

    try:

        workspace.write_file(
            "../../outside.py",
            "malicious"
        )

        raise AssertionError(
            "Path traversal was not blocked."
        )

    except ValueError as exc:

        print(
            f"Path traversal → BLOCKED"
        )

        print(
            f"Reason → {exc}"
        )

    # --------------------------------------------------------
    # Absolute path
    # --------------------------------------------------------

    try:

        workspace.write_file(
            str(
                Path.cwd().parent
                / "outside.py"
            ),
            "malicious"
        )

        raise AssertionError(
            "Absolute path escape was not blocked."
        )

    except ValueError as exc:

        print(
            "Absolute path escape → BLOCKED"
        )

        print(
            f"Reason → {exc}"
        )

    cleanup()

    print(
        "\n🎉 WORKSPACE SECURITY TEST PASSED!"
    )


if __name__ == "__main__":

    test_workspace_security()