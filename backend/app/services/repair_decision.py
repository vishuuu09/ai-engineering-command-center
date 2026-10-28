from typing import Dict


class RepairDecision:
    MAX_RETRIES = 3

    def decide(
        self,
        validation_result: Dict[str, object],
        execution_result: Dict[str, object],
        retry_count: int
    ) -> Dict[str, object]:

        if validation_result.get("passed", False):
            return {
                "action": "complete",
                "reason": "Validation passed.",
                "retry": False
            }

        if retry_count >= self.MAX_RETRIES:
            return {
                "action": "stop",
                "reason": "Maximum repair attempts reached.",
                "retry": False
            }

        failure_type = execution_result.get(
            "failure_type",
            "unknown_error"
        )

        if failure_type == "permission_error":
            return {
                "action": "stop",
                "reason": "Permission errors should not be automatically repaired.",
                "retry": False
            }

        if failure_type == "timeout":
            return {
                "action": "repair",
                "reason": "Execution timed out and requires investigation.",
                "retry": True
            }

        if failure_type in {
            "missing_dependency",
            "syntax_error",
            "runtime_error",
            "test_failure",
            "unknown_error"
        }:
            return {
                "action": "repair",
                "reason": f"Recoverable failure detected: {failure_type}.",
                "retry": True
            }

        return {
            "action": "repair",
            "reason": "Validation failed and the project requires another repair attempt.",
            "retry": True
        }