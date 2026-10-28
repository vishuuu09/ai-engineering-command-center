from app.models.project import (
    RepairFile,
    RepairResult
)

from app.services.workspace_editor import WorkspaceEditor
from app.services.workspace_reader import WorkspaceReader


print("\n🔧 Testing Repair Agent local pipeline...\n")


workspace_root = "workspace_repair_test"


editor = WorkspaceEditor(
    workspace_root
)

reader = WorkspaceReader(
    workspace_root
)


# --------------------------------------------------
# CREATE ORIGINAL FILE
# --------------------------------------------------

original_content = """
DATABASE_URL = "postgresql://localhost:5432/app"
"""


editor.write_file(
    "src/config.py",
    original_content
)


print("📄 Original file created")


# --------------------------------------------------
# SIMULATE REPAIR AGENT OUTPUT
# --------------------------------------------------

repair_result = RepairResult(
    repaired_files=[
        RepairFile(
            path="src/config.py",
            content="""
DATABASE_URL = "postgresql://postgres:5432/app"
""",
            explanation="Changed the database hostname from localhost to the PostgreSQL service hostname."
        )
    ],
    summary="Fixed the database connection configuration.",
    changes_made=True
)


print("🤖 Simulated RepairResult created")


# --------------------------------------------------
# APPLY REPAIR
# --------------------------------------------------

for repaired_file in repair_result.repaired_files:

    editor.replace_file(
        repaired_file.path,
        repaired_file.content
    )

    print(
        f"✅ Repaired: {repaired_file.path}"
    )


# --------------------------------------------------
# VERIFY REPAIR
# --------------------------------------------------

updated_content = reader.read_file(
    "src/config.py"
)


print("\n📖 Updated file:")

print(updated_content)


# --------------------------------------------------
# ASSERT CORRECT REPAIR
# --------------------------------------------------

assert (
    "postgres:5432"
    in updated_content
)

assert (
    "localhost:5432"
    not in updated_content
)


print(
    "\n🎉 Repair pipeline test passed!"
)

print(
    "🔧 RepairResult → WorkspaceEditor → Updated file works."
)