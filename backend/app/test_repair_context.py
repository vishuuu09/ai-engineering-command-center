from app.services.repair_context import RepairContext


print("\n🔧 Testing Repair Context...\n")


context_builder = RepairContext(
    "workspace_repair_test"
)


affected_files = [
    "src/config.py"
]


context = context_builder.get_repair_context(
    affected_files
)


print(context)


assert "FILE: src/config.py" in context
assert "postgres:5432" in context


print(
    "\n✅ Repair Context test passed!"
)

print(
    "🎯 Debugger-selected files can now be supplied to the Repair Agent."
)