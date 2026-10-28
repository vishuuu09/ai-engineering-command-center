from app.services.repair_decision import RepairDecision


def run_test(name, condition, details=""):
    if not condition:
        raise AssertionError(f"FAILED: {name}. {details}")

    print(f"PASS: {name}")


def main():
    print("\nTesting RepairDecision...\n")

    decision_engine = RepairDecision()

    # 1. Successful validation should complete the workflow.
    result = decision_engine.decide(
        validation_result={"passed": True},
        execution_result={"success": True, "failure_type": "success"},
        retry_count=0,
    )

    run_test(
        "Successful validation completes",
        result["action"] == "complete",
        str(result),
    )

    # 2. The workflow should stop at the retry limit.
    result = decision_engine.decide(
        validation_result={"passed": False},
        execution_result={
            "success": False,
            "failure_type": "runtime_error",
        },
        retry_count=RepairDecision.MAX_RETRIES,
    )

    run_test(
        "Maximum retry limit stops repairs",
        result["action"] == "stop",
        str(result),
    )

    # 3. Permission errors must not trigger automatic repairs.
    result = decision_engine.decide(
        validation_result={"passed": False},
        execution_result={
            "success": False,
            "failure_type": "permission_error",
        },
        retry_count=0,
    )

    run_test(
        "Permission errors stop automatic repair",
        result["action"] == "stop",
        str(result),
    )

    # 4. Timeouts should trigger investigation while retries remain.
    result = decision_engine.decide(
        validation_result={"passed": False},
        execution_result={
            "success": False,
            "failure_type": "timeout",
        },
        retry_count=0,
    )

    run_test(
        "Timeout requests a repair attempt",
        result["action"] == "repair" and result["retry"] is True,
        str(result),
    )

    # 5. Recoverable errors should request repair.
    recoverable_errors = [
        "missing_dependency",
        "syntax_error",
        "runtime_error",
        "test_failure",
        "unknown_error",
    ]

    for failure_type in recoverable_errors:
        result = decision_engine.decide(
            validation_result={"passed": False},
            execution_result={
                "success": False,
                "failure_type": failure_type,
            },
            retry_count=0,
        )

        run_test(
            f"{failure_type} requests repair",
            result["action"] == "repair" and result["retry"] is True,
            str(result),
        )

    # 6. Failed validation with successful execution still needs
    # another attempt when retries remain.
    result = decision_engine.decide(
        validation_result={"passed": False},
        execution_result={
            "success": True,
            "failure_type": "success",
        },
        retry_count=1,
    )

    run_test(
        "Validation failure requests repair",
        result["action"] == "repair",
        str(result),
    )

    print("\n" + "=" * 50)
    print("ALL REPAIR DECISION TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()