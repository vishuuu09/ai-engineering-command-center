from app.services.workspace_reader import WorkspaceReader


print("\n📖 Testing workspace reader...\n")


reader = WorkspaceReader(
    "workspace_project_test"
)


content = reader.read_file(
    "src/main.py"
)

print("✅ Single file read:")
print(content)


contents = reader.read_files(
    [
        "src/main.py",
        "src/utils/helpers.py",
        "tests/test_main.py"
    ]
)

print("\n✅ Multiple files read:")
print(contents)


print("\n🎉 Workspace reader test passed!")