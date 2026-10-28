from app.services.workspace_reader import WorkspaceReader


print("\n📖 Testing selected-file reading...\n")


reader = WorkspaceReader(
    "workspace_debugger_local"
)


selected_files = [
    "docker-compose.yml",
    "Dockerfile",
    "package.json"
]


context = reader.read_files(
    selected_files
)


print(context)


# Verify selected files are present
assert "FILE: docker-compose.yml" in context
assert "FILE: Dockerfile" in context
assert "FILE: package.json" in context

# Verify unrelated file was not requested
assert "FILE: src/app.py" not in context
assert "FILE: tests/test_app.py" not in context


print(
    "\n✅ Selected-file reading test passed!"
)

print(
    "🎯 Only requested files were loaded."
)