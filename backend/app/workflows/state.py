from typing import TypedDict, Optional, List, Dict, Any


class EngineeringState(TypedDict):
    requirement: str

    project_plan: Optional[Dict[str, Any]]

    architecture: Optional[Dict[str, Any]]

    generated_files: List[Dict[str, str]]

    validation_results: Optional[Dict[str, Any]]

    debug_results: Optional[Dict[str, Any]]

    repaired_files: List[Dict[str, str]]

    test_results: Optional[Dict[str, Any]]

    security_results: Optional[Dict[str, Any]]

    execution_results: Optional[Dict[str, Any]]

    errors: List[str]

    current_agent: str

    status: str

    retry_count: int

    workspace_root: str