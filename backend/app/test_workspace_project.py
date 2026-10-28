from app.services.workspace import ProjectWorkspace


generated_files = [
    {
        "path": "src/main.py",
        "content": "print('AI Engineering Command Center')",
        "purpose": "Application entry point"
    },
    {
        "path": "src/utils/helpers.py",
        "content": "def hello():\n    return 'Hello'",
        "purpose": "Utility functions"
    },
    {
        "path": "tests/test_main.py",
        "content": "def test_example():\n    assert True",
        "purpose": "Basic application test"
    },
    {
        "path": "README.md",
        "content": "# Generated Project\n\nAI-generated project.",
        "purpose": "Project documentation"
    }
]


print("\n🚀 Testing project workspace integration...\n")


workspace = ProjectWorkspace(
    "workspace_project_test"
)


written_files = workspace.write_project(
    generated_files
)


print("✅ Project written successfully")

print("\n📁 Written files:")

for file in written_files:
    print("-", file)


print("\n📋 Workspace files:")

for file in workspace.list_files():
    print("-", file)


print("\n📖 Reading one generated file:\n")

content = workspace.read_file(
    "src/main.py"
)

print(content)


print("\n🎉 Project workspace integration test passed!")