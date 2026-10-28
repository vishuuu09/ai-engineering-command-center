from app.services.debugger_context import DebuggerContext


print("\n🧠 Testing Debugger Context...\n")


context_builder = DebuggerContext(
    "workspace_debugger_local"
)


available_files = (
    context_builder.get_file_manifest()
)


print("📋 Available files:")

for file in available_files:
    print("-", file)


selected_files = [
    "docker-compose.yml",
    "Dockerfile"
]


context = context_builder.prepare_context(
    selected_files
)


print("\n🎯 Selected files:")

for file in context["selected_files"]:
    print("-", file)


print("\n📖 Selected file contents:")

print(
    context["contents"]
)


assert (
    "docker-compose.yml"
    in context["selected_files"]
)

assert (
    "Dockerfile"
    in context["selected_files"]
)

assert (
    "package.json"
    not in context["selected_files"]
)

assert (
    "src/app.py"
    not in context["selected_files"]
)


print(
    "\n✅ Debugger Context test passed!"
)

print(
    "🎯 Manifest + selection + file reading work together."
)