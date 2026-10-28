from app.workflows.nodes import validation_router


def test_validation_router_complete():
    print("\n🧪 Testing Validation Router...")

    state = {
        "validation_results": {
            "passed": True,
            "score": 100,
            "issues": [],
            "warnings": [],
            "recommendations": [],
        },
        "execution_results": {
            "success": True,
            "return_code": 0,
            "stdout": "",
            "stderr": "",
            "failure_type": "success",
        },
        "retry_count": 0,
    }

    result = validation_router(state)
    print(f"Passing validation → {result}")
    assert result == "complete"


def test_validation_router_repair():
    state = {
        "validation_results": {
            "passed": False,
            "score": 60,
            "issues": ["Syntax error detected."],
            "warnings": [],
            "recommendations": [],
        },
        "execution_results": {
            "success": False,
            "return_code": 1,
            "stdout": "",
            "stderr": "SyntaxError",
            "failure_type": "syntax_error",
        },
        "retry_count": 0,
    }

    result = validation_router(state)
    print(f"Failed validation → {result}")
    assert result == "debugger"


def test_validation_router_stops_after_max_retries():
    state = {
        "validation_results": {
            "passed": False,
            "score": 50,
            "issues": ["Unresolved issue."],
            "warnings": [],
            "recommendations": [],
        },
        "execution_results": {
            "success": False,
            "return_code": 1,
            "stdout": "",
            "stderr": "RuntimeError",
            "failure_type": "runtime_error",
        },
        "retry_count": 3,
    }

    result = validation_router(state)
    print(f"Maximum retries reached → {result}")
    assert result == "stop"


def test_validation_router_permission_error():
    state = {
        "validation_results": {
            "passed": False,
            "score": 40,
            "issues": ["Permission problem."],
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

    result = validation_router(state)
    print(f"Permission error → {result}")
    assert result == "stop"


if __name__ == "__main__":
    test_validation_router_complete()
    test_validation_router_repair()
    test_validation_router_stops_after_max_retries()
    test_validation_router_permission_error()
    print("\n🎉 VALIDATION ROUTER TESTS PASSED!")
