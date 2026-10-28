from app.services.failure_classifier import (
    FailureClassifier
)


print("\n🧪 Testing Failure Classifier...\n")


classifier = FailureClassifier()


# Missing dependency
result = classifier.classify({
    "success": False,
    "stderr": (
        "ModuleNotFoundError: "
        "No module named 'fastapi'"
    )
})

print(
    f"Missing dependency → {result}"
)

assert result == "missing_dependency"


# Syntax error
result = classifier.classify({
    "success": False,
    "stderr": (
        "SyntaxError: invalid syntax"
    )
})

print(
    f"Syntax error → {result}"
)

assert result == "syntax_error"


# Runtime error
result = classifier.classify({
    "success": False,
    "stderr": (
        "Traceback (most recent call last):\n"
        "ValueError: invalid value"
    )
})

print(
    f"Runtime error → {result}"
)

assert result == "runtime_error"


# Test failure
result = classifier.classify({
    "success": False,
    "stderr": (
        "AssertionError: expected 5"
    )
})

print(
    f"Test failure → {result}"
)

assert result == "test_failure"


# Timeout
result = classifier.classify({
    "success": False,
    "stderr": (
        "Execution timed out after 30 seconds."
    )
})

print(
    f"Timeout → {result}"
)

assert result == "timeout"


# Success
result = classifier.classify({
    "success": True,
    "stderr": ""
})

print(
    f"Success → {result}"
)

assert result == "success"


print(
    "\n🎉 FAILURE CLASSIFIER TEST PASSED!"
)