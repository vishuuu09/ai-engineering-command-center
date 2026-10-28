from app.workflows.local_graph import (
    build_local_graph,
    repair_result_router,
)


def create_initial_state():
    """Return a fresh state for local workflow testing."""
    return {
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
        "execution_results": None,
        "errors": [],
        "current_agent": "system",
        "status": "initialized",
        "retry_count": 0,
    }


def test_repair_result_router():
    """Check routing decisions for successful and failed repairs."""
    print("\nTesting repair result routing...\n")

    failed_state = {
        **create_initial_state(),
        "status": "repair_failed",
    }

    route = repair_result_router(failed_state)

    assert route == "stop", (
        f"Expected 'stop' after failed repair, got {route!r}"
    )

    print("PASS: Failed repair routes to stop.")

    repaired_state = {
        **create_initial_state(),
        "status": "repaired",
    }

    route = repair_result_router(repaired_state)

    assert route == "execution", (
        f"Expected 'execution' after successful repair, got {route!r}"
    )

    print("PASS: Successful repair routes to execution.")


def test_compiled_graph_stops_after_repair_failure():
    """
    Exercise the compiled graph with a repairer that deliberately fails.

    The real planner, developer, execution, validator, and debugger are
    replaced with test nodes so this test does not write to the workspace
    or run sandbox commands.
    """
    print("\nTesting compiled graph failure handling...\n")

    from langgraph.graph import StateGraph, END
    from app.workflows.state import EngineeringState

    def pass_node(state):
        return {}

    def failed_repair_node(state):
        print("TEST: Simulating a rejected repair.")
        return {
            "status": "repair_failed",
            "repaired_files": [],
            "errors": ["Test repair deliberately rejected."],
        }

    graph = StateGraph(EngineeringState)

    graph.add_node("start", pass_node)
    graph.add_node("repairer", failed_repair_node)
    graph.add_node("execution", pass_node)

    graph.set_entry_point("start")
    graph.add_edge("start", "repairer")

    graph.add_conditional_edges(
        "repairer",
        repair_result_router,
        {
            "execution": "execution",
            "stop": END,
        },
    )

    graph.add_edge("execution", END)

    compiled_graph = graph.compile()
    result = compiled_graph.invoke(create_initial_state())

    assert result["status"] == "repair_failed", (
        f"Expected failed status to be preserved, got {result['status']!r}"
    )

    assert result["errors"] == [
        "Test repair deliberately rejected."
    ], f"Unexpected errors: {result['errors']!r}"

    print("PASS: Compiled graph preserved the repair failure.")
    print("PASS: Failed repair followed the stop branch.")


def main():
    print("\nTesting repair failure handling...\n")

    test_repair_result_router()
    test_compiled_graph_stops_after_repair_failure()

    print("\n" + "=" * 50)
    print("ALL REPAIR FAILURE TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()
