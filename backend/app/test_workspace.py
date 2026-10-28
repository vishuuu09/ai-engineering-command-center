from app.services.workspace import ProjectWorkspace


workspace = ProjectWorkspace(
    "workspace_test"
)


print("\n📁 Testing workspace...\n")


# Write a file
workspace.write_file(
    "src/hello.py",
    "print('Hello from AI Engineering Command Center')"
)

print("✅ File written")


# Read the file
content = workspace.read_file(
    "src/hello.py"
)

print("✅ File read")
print("Content:", content)


# List files
files = workspace.list_files()

print("\n📋 Files:")
for file in files:
    print("-", file)


print("\n🎉 Workspace test completed successfully!")