from app.models.project import (
    DebugResult,
    DebugFix
)

from app.services.repair_context import RepairContext
from app.services.workspace_editor import WorkspaceEditor
from app.services.workspace_reader import WorkspaceReader


print("\n🚀 Testing complete local repair pipeline...\n")


workspace_root = "workspace_full_repair_test"


# --------------------------------------------------
# 1. Create simulated project
# --------------------------------------------------

editor = WorkspaceEditor(workspace_root)

editor.write_file(
    "src/config.py",
    """
DATABASE_URL = "postgresql://localhost:5432/app"
"""
)

editor.write_file(
    "src/main.py",
    """
from src.config import DATABASE_URL

print(DATABASE_URL)
"""
)

print("📁 Simulated project created")


# --------------------------------------------------
# 2. Simulate Debugger result
# --------------------------------------------------

debug_result = DebugResult(
    affected_files=[
        "src/config.py"
    ],
    fixes=[
        DebugFix(
            file_path="src/config.py",
            issue="Database hostname points to localhost.",
            fix="Change the database hostname to the PostgreSQL service hostname."
        )
    ],
    summary="Database configuration needs repair.",
    should_retry=True
)

print("🐞 Simulated DebugResult created")


# --------------------------------------------------
# 3. Build repair context
# --------------------------------------------------

context_builder = RepairContext(
    workspace_root
)

file_contents = context_builder.get_repair_context(
    debug_result.affected_files
)

print("\n📖 Files supplied to Repair Agent:\n")
print(file_contents)


# --------------------------------------------------
# 4. Simulate repaired file
# --------------------------------------------------

repaired_content = """
DATABASE_URL = "postgresql://postgres:5432/app"
"""


# --------------------------------------------------
# 5. Apply repair
# --------------------------------------------------

editor.replace_file(
    "src/config.py",
    repaired_content
)

print("\n🔧 Repair applied")


# --------------------------------------------------
# 6. Verify
# --------------------------------------------------

reader = WorkspaceReader(
    workspace_root
)

updated = reader.read_file(
    "src/config.py"
)

print("\n📄 Updated file:\n")
print(updated)


assert "postgres:5432" in updated
assert "localhost:5432" not in updated


# Make sure unrelated file was untouched
main_file = reader.read_file(
    "src/main.py"
)

assert "DATABASE_URL" in main_file


print("\n" + "=" * 55)
print("🎉 COMPLETE LOCAL REPAIR PIPELINE PASSED!")
print("=" * 55)

print("\nDebugger")
print("   ↓")
print("Affected Files")
print("   ↓")
print("Repair Context")
print("   ↓")
print("Repair")
print("   ↓")
print("Workspace Editor")
print("   ↓")
print("Updated Source Code")