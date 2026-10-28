from app.workflows.local_graph import build_local_graph

from app.services.workspace_reader import WorkspaceReader

print(
    "\n🚀 Starting LOCAL autonomous engineering test...\n"
)


graph = build_local_graph()


initial_state = {
    "requirement": "Build an expense management API",

    "workspace_root": "workspace_local_graph",

    "project_plan": None,

    "architecture": None,

    "generated_files": [],

    "validation_results": None,

    "debug_results": None,

    "repaired_files": [],

    "test_results": None,

    "security_results": None,

    "errors": [],

    "current_agent": "system",

    "status": "initialized",

    "retry_count": 0
}


result = graph.invoke(
    initial_state
)


# ---------------------------------------------
# Inspect actual workspace
# ---------------------------------------------

reader = WorkspaceReader(
    "workspace_local_graph"
)

config = reader.read_file(
    "src/config.py"
)


print("\n📄 FINAL PHYSICAL FILE:")
print(config)


# ---------------------------------------------
# Assertions
# ---------------------------------------------

assert result[
    "validation_results"
]["passed"] is True

assert result[
    "retry_count"
] == 1

assert "postgres:5432" in config

assert "localhost:5432" not in config


print("\n" + "=" * 60)
print(
    "🎉 REAL LOCAL AUTONOMOUS REPAIR TEST PASSED!"
)
print("=" * 60)

print(
    "\nThe system successfully:"
)

print("1. Generated a project")
print("2. Wrote the project to the filesystem")
print("3. Detected a real configuration problem")
print("4. Identified the affected file")
print("5. Modified the physical file")
print("6. Validated the repaired file")
print("7. Stopped after validation passed")

print(
    "\n🔥 This is now an actual autonomous "
    "engineering loop — not just mocked state."
)