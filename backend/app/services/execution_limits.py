from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionLimits:
    """
    Central resource limits for sandbox execution.
    """

    python_timeout_seconds: int = 10
    command_timeout_seconds: int = 30
    max_output_characters: int = 50_000


DEFAULT_EXECUTION_LIMITS = ExecutionLimits()