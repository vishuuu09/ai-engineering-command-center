from app.services.execution_context import (
    ExecutionContextBuilder
)


print("\n🧪 Testing Execution Context Builder...\n")


builder = ExecutionContextBuilder()


execution_result = {
    "success": False,
    "return_code": 1,
    "stdout": "",
    "stderr": (
        "ModuleNotFoundError: "
        "No module named 'fastapi'"
    )
}


context = builder.build_context(
    execution_result
)


print(context)


assert "ModuleNotFoundError" in context
assert "fastapi" in context
assert "RETURN CODE" in context


print(
    "\n🎉 EXECUTION CONTEXT TEST PASSED!"
)

print(
    "🐞 Real sandbox failures can now be "
    "passed to the Debugger."
)