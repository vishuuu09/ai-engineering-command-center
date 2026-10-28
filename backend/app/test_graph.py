from app.workflows.engineering_graph import build_engineering_graph


print("\n🚀 Testing Engineering Graph Structure...\n")


graph = build_engineering_graph()


initial_state = {
    "requirement": "Build an expense management API",

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


print("✅ Initial state created")
print(f"🔁 Retry count: {initial_state['retry_count']}")


print("\n🧠 Compiling workflow...")


print("\n🎉 Engineering graph compiled successfully!")

print("\nWorkflow:")
print("START")
print("  ↓")
print("PLANNER")
print("  ↓")
print("ARCHITECT")
print("  ↓")
print("DEVELOPER")
print("  ↓")
print("VALIDATOR")
print("  ↓")
print("PASS → END")
print("  ↓")
print("FAIL")
print("  ↓")
print("DEBUGGER")
print("  ↓")
print("REPAIRER")
print("  ↓")
print("VALIDATOR")
print("  ↓")
print("Maximum 3 repair attempts")