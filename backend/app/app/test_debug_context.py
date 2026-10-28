from app.services.debug_context import DebugContextBuilder


fixes = [
    {
        "file_path": "src/main.py",
        "issue": "Example issue",
        "fix": "Example fix"
    },
    {
        "file_path": "tests/test_main.py",
        "issue": "Example test issue",
        "fix": "Example test fix"
    }
]


print("\n🧠 Building debug context...\n")


builder = DebugContextBuilder(
    "workspace_project_test"
)


context = builder.build_context(
    fixes
)


print(context)


print("\n🎉 Debug context test passed!")