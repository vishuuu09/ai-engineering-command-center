from typing import Dict


class FailureClassifier:

    def classify(
        self,
        execution_result: Dict[str, object]
    ) -> str:

        if execution_result.get("success"):
            return "success"

        stderr = str(
            execution_result.get(
                "stderr",
                ""
            )
        ).lower()

        if "modulenotfounderror" in stderr:
            return "missing_dependency"

        if "syntaxerror" in stderr:
            return "syntax_error"

        if "traceback" in stderr:
            return "runtime_error"

        if "assertionerror" in stderr:
            return "test_failure"

        if "timed out" in stderr:
            return "timeout"

        if "permission denied" in stderr:
            return "permission_error"

        return "unknown_error"