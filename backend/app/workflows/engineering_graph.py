from langgraph.graph import StateGraph, START, END

from app.workflows.state import EngineeringState

from app.workflows.nodes import (
    planner_node,
    architect_node,
    developer_node,
    execution_node,
    validator_node,
    debugger_node,
    repairer_node,
    validation_router,
)


def repair_result_router(state: EngineeringState) -> str:
    """Continue only after a repair explicitly succeeds; otherwise stop safely."""
    status = state.get("status")

    if status == "repaired":
        return "execution"

    if status == "repair_failed":
        print(
            "\nRepair failed or was rejected. "
            "Stopping the production workflow."
        )
        return "stop"

    print(
        f"\nUnexpected repair status: {status!r}. "
        "Stopping the production workflow."
    )
    return "stop"


def build_engineering_graph():
    """Build the production autonomous engineering workflow."""
    graph = StateGraph(EngineeringState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("architect", architect_node)
    graph.add_node("developer", developer_node)
    graph.add_node("execution", execution_node)
    graph.add_node("validator", validator_node)
    graph.add_node("debugger", debugger_node)
    graph.add_node("repairer", repairer_node)

    # Initial workflow
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "architect")
    graph.add_edge("architect", "developer")
    graph.add_edge("developer", "execution")
    graph.add_edge("execution", "validator")

    # Validation routing
    graph.add_conditional_edges(
        "validator",
        validation_router,
        {
            "debugger": "debugger",
            "complete": END,
            "stop": END,
        },
    )

    # Repair cycle with failure handling
    graph.add_edge("debugger", "repairer")
    graph.add_conditional_edges(
        "repairer",
        repair_result_router,
        {
            "execution": "execution",
            "stop": END,
        },
    )

    return graph.compile()
