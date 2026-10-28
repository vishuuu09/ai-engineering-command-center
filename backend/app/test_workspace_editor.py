from app.services.workspace_editor import WorkspaceEditor
from app.services.workspace_reader import WorkspaceReader


print("\n✏️ Testing Workspace Editor...\n")


editor = WorkspaceEditor(
    "workspace_debugger_local"
)


reader = WorkspaceReader(
    "workspace_debugger_local"
)


# Create a file
editor.write_file(
    "src/config.py",
    "DATABASE_URL = 'old-url'"
)

print("✅ File created")


# Verify original content
content = reader.read_file(
    "src/config.py"
)

print("\nOriginal content:")
print(content)


# Replace the file
editor.replace_file(
    "src/config.py",
    "DATABASE_URL = 'new-url'"
)

print("\n✅ File replaced")


# Verify updated content
updated_content = reader.read_file(
    "src/config.py"
)

print("\nUpdated content:")
print(updated_content)


assert updated_content == (
    "DATABASE_URL = 'new-url'"
)


print(
    "\n🎉 Workspace Editor test passed!"
)