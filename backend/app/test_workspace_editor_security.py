
from pathlib import Path
import shutil

from app.services.workspace_editor import WorkspaceEditor


TEST_WORKSPACE = "workspace_editor_security_test"


def test_workspace_editor_security():

    print("\n🧪 Testing Workspace Editor Security...")

    root = Path(TEST_WORKSPACE)

    if root.exists():
        shutil.rmtree(root)

    editor = WorkspaceEditor(TEST_WORKSPACE)

    # Test writing a file
    editor.write_file(
        "src/main.py",
        "print('hello')"
    )

    assert (
        root / "src" / "main.py"
    ).read_text(encoding="utf-8") == "print('hello')"

    print("Safe write → PASS")

    # Test replacing an existing file
    editor.replace_file(
        "src/main.py",
        "print('updated')"
    )

    assert (
        root / "src" / "main.py"
    ).read_text(encoding="utf-8") == "print('updated')"

    print("Safe replacement → PASS")

    # Test refusing to replace a missing file
    try:
        editor.replace_file(
            "src/missing.py",
            "content"
        )
        raise AssertionError(
            "Replacing a missing file should fail."
        )
    except FileNotFoundError:
        print("Missing file replacement → BLOCKED")

    # Test path traversal
    try:
        editor.write_file(
            "../../outside.py",
            "malicious"
        )
        raise AssertionError(
            "Path traversal should be blocked."
        )
    except ValueError:
        print("Path traversal → BLOCKED")

    shutil.rmtree(root)

    print("\n🎉 WORKSPACE EDITOR SECURITY TEST PASSED!")


if __name__ == "__main__":
    test_workspace_editor_security()
