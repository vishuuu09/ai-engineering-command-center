from app.workflows.engineering_graph import repair_result_router


def test_failed_repair_stops():
    result = repair_result_router({"status": "repair_failed"})
    assert result == "stop"
    print("PASS: Failed repair stops the workflow.")


def test_successful_repair_continues():
    result = repair_result_router({"status": "repaired"})
    assert result == "execution"
    print("PASS: Successful repair continues to execution.")


def test_missing_status_stops():
    result = repair_result_router({})
    assert result == "stop"
    print("PASS: Missing status stops the workflow.")


def test_unexpected_status_stops():
    result = repair_result_router({"status": "unknown"})
    assert result == "stop"
    print("PASS: Unexpected status stops the workflow.")


if __name__ == "__main__":
    test_failed_repair_stops()
    test_successful_repair_continues()
    test_missing_status_stops()
    test_unexpected_status_stops()
    print("\nALL PRODUCTION ROUTING TESTS PASSED")
