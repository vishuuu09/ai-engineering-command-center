from app.services.execution_limits import (
    ExecutionLimits,
    DEFAULT_EXECUTION_LIMITS
)


print("\n🧪 Testing Execution Limits...\n")


limits = DEFAULT_EXECUTION_LIMITS


print(
    f"Python timeout: "
    f"{limits.python_timeout_seconds}s"
)

print(
    f"Command timeout: "
    f"{limits.command_timeout_seconds}s"
)

print(
    f"Maximum output: "
    f"{limits.max_output_characters} characters"
)


assert limits.python_timeout_seconds == 10
assert limits.command_timeout_seconds == 30
assert limits.max_output_characters == 50_000


custom_limits = ExecutionLimits(
    python_timeout_seconds=5,
    command_timeout_seconds=15,
    max_output_characters=10_000
)


assert custom_limits.python_timeout_seconds == 5
assert custom_limits.command_timeout_seconds == 15
assert custom_limits.max_output_characters == 10_000


print(
    "\n🎉 EXECUTION LIMITS TEST PASSED!"
)