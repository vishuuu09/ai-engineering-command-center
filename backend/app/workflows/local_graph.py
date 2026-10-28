from langgraph.graph import StateGraph, END

from app.workflows.state import EngineeringState

from app.workflows.mock_nodes import (
    mock_planner_node,
    mock_architect_node,
    mock_developer_node,
    mock_execution_node,
    mock_validator_node,
    mock_debugger_node,
    mock_repairer_node,
    mock_validation_router,
)


def repair_result_router(state: EngineeringState) -> str:
    """
    Stop the workflow if a repair fails or is rejected.
    Continue execution only when the repair succeeds.
    """
    if state.get("status") == "repair_failed":
        print(
            "\n🛑 Repair failed or was rejected. "
            "Stopping workflow."
        )
        return "stop"

    return "execution"


def build_local_graph():
    """
    Build a local autonomous engineering graph.

    Uses mock agents for deterministic local testing.
    Does not call production LLM agents.
    """

    graph = StateGraph(EngineeringState)

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    graph.add_node("planner", mock_planner_node)
    graph.add_node("architect", mock_architect_node)
    graph.add_node("developer", mock_developer_node)
    graph.add_node("execution", mock_execution_node)
    graph.add_node("validator", mock_validator_node)
    graph.add_node("debugger", mock_debugger_node)
    graph.add_node("repairer", mock_repairer_node)

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

    graph.set_entry_point("planner")

    # --------------------------------------------------------
    # Initial generation and execution
    # --------------------------------------------------------

    graph.add_edge("planner", "architect")
    graph.add_edge("architect", "developer")
    graph.add_edge("developer", "execution")
    graph.add_edge("execution", "validator")

    # --------------------------------------------------------
    # Validation routing
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "validator",
        mock_validation_router,
        {
            "debugger": "debugger",
            "complete": END,
        },
    )

    # --------------------------------------------------------
    # Autonomous repair loop
    # --------------------------------------------------------

    graph.add_edge("debugger", "repairer")

    # Stop after a failed repair; otherwise execute again.
    graph.add_conditional_edges(
        "repairer",
        repair_result_router,
        {
            "execution": "execution",
            "stop": END,
        },
    )

    return graph.compile()
