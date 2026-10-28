from app.workflows.nodes import validation_router


print("\n🧪 Testing Validation Router...\n")


# --------------------------------------------------
# TEST 1: Validation PASSED
# --------------------------------------------------

passed_state = {
    "validation_results": {
        "passed": True,
        "score": 95,
        "issues": [],
        "warnings": [],
        "recommendations": [],
    },
    "retry_count": 0,
}

result = validation_router(passed_state)

print(f"Test 1 → {result}")
assert result == "complete"
print("✅ PASS: validation correctly routes to END")


# --------------------------------------------------
# TEST 2: Validation FAILED
# --------------------------------------------------

failed_state = {
    "validation_results": {
        "passed": False,
        "score": 45,
        "issues": ["Database configuration is incorrect"],
        "warnings": [],
        "recommendations": [],
    },
    "execution_results": {
        "success": False,
        "return_code": 1,
        "stdout": "",
        "stderr": "Database configuration is incorrect",
        "failure_type": "runtime_error",
    },
    "retry_count": 0,
}

result = validation_router(failed_state)

print(f"\nTest 2 → {result}")
assert result == "debugger"
print("✅ PASS: failed validation correctly routes to DEBUGGER")


# --------------------------------------------------
# TEST 3: Second repair attempt
# --------------------------------------------------

retry_state = {
    "validation_results": {
        "passed": False,
        "score": 65,
        "issues": ["Authentication configuration is incorrect"],
        "warnings": [],
        "recommendations": [],
    },
    "execution_results": {
        "success": False,
        "return_code": 1,
        "stdout": "",
        "stderr": "Authentication configuration is incorrect",
        "failure_type": "runtime_error",
    },
    "retry_count": 1,
}

result = validation_router(retry_state)

print(f"\nTest 3 → {result}")
assert result == "debugger"
print("✅ PASS: another repair attempt correctly routes to DEBUGGER")


# --------------------------------------------------
# TEST 4: Maximum retries reached
# --------------------------------------------------

max_retry_state = {
    "validation_results": {
        "passed": False,
        "score": 70,
        "issues": ["Remaining validation issue"],
        "warnings": [],
        "recommendations": [],
    },
    "execution_results": {
        "success": False,
        "return_code": 1,
        "stdout": "",
        "stderr": "Remaining validation issue",
        "failure_type": "runtime_error",
    },
    "retry_count": 3,
}

result = validation_router(max_retry_state)

print(f"\nTest 4 → {result}")
assert result == "stop"
print("✅ PASS: maximum retry limit safely stops workflow")


# --------------------------------------------------
# TEST 5: Permission errors stop automatic repair
# --------------------------------------------------

permission_state = {
    "validation_results": {
        "passed": False,
        "score": 40,
        "issues": ["Permission problem"],
        "warnings": [],
        "recommendations": [],
    },
    "execution_results": {
        "success": False,
        "return_code": -1,
        "stdout": "",
        "stderr": "Permission denied",
        "failure_type": "permission_error",
    },
    "retry_count": 0,
}

result = validation_router(permission_state)

print(f"\nTest 5 → {result}")
assert result == "stop"
print("✅ PASS: permission errors safely stop automatic repair")


print("\n" + "=" * 55)
print("🎉 VALIDATION ROUTER TESTS PASSED!")
print("=" * 55)

print("""
PASS
 ↓
END

FAIL (repairable)
 ↓
DEBUGGER
 ↓
REPAIRER
 ↓
VALIDATOR

MAX RETRIES / PERMISSION ERROR
 ↓
STOP
 ↓
END
""")
