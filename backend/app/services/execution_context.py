from typing import Dict, Any


class ExecutionContextBuilder:

    def build_context(
        self,
        execution_result: Dict[str, Any]
    ) -> str:

        if not execution_result:
            return ""

        success = execution_result.get(
            "success",
            False
        )

        return f"""
EXECUTION SUCCESS:
{success}

RETURN CODE:
{execution_result.get("return_code")}

STDOUT:
{execution_result.get("stdout", "")}

STDERR:
{execution_result.get("stderr", "")}
""".strip()