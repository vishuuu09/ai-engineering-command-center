import subprocess
import sys

from pathlib import Path
from typing import Dict, List

from app.services.sandbox_policy import SandboxPolicy
from app.services.execution_limits import (
    ExecutionLimits,
    DEFAULT_EXECUTION_LIMITS
)


class SandboxRunner:

    def __init__(
        self,
        workspace_root: str = "workspace",
        limits: ExecutionLimits = DEFAULT_EXECUTION_LIMITS
    ):
        self.root = Path(
            workspace_root
        ).resolve()

        self.policy = SandboxPolicy(
            workspace_root
        )

        self.limits = limits

    # ========================================================
    # OUTPUT PROTECTION
    # ========================================================

    def _limit_output(
        self,
        output: str
    ) -> str:

        if len(output) <= self.limits.max_output_characters:
            return output

        truncated = output[
            :self.limits.max_output_characters
        ]

        return (
            truncated
            + "\n\n"
            + "[OUTPUT TRUNCATED BY SANDBOX]"
        )

    # ========================================================
    # PYTHON FILE EXECUTION
    # ========================================================

    def run_python_file(
        self,
        relative_path: str,
        timeout: int | None = None
    ) -> Dict[str, object]:

        allowed, reason = (
            self.policy.validate_path(
                relative_path
            )
        )

        if not allowed:
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": reason
            }

        file_path = (
            self.root / relative_path
        )

        if not file_path.exists():
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    f"File not found: "
                    f"{relative_path}"
                )
            }

        if not file_path.is_file():
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    f"Path is not a file: "
                    f"{relative_path}"
                )
            }

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

        except Exception as exc:
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc)
            }

        allowed, reason = (
            self.policy.validate_python_content(
                content
            )
        )

        if not allowed:
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": reason
            }

        execution_timeout = (
            timeout
            if timeout is not None
            else self.limits.python_timeout_seconds
        )

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    relative_path
                ],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=execution_timeout
            )

            stdout = self._limit_output(
                result.stdout
            )

            stderr = self._limit_output(
                result.stderr
            )

            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": stdout,
                "stderr": stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    f"Execution timed out after "
                    f"{execution_timeout} seconds."
                )
            }

        except Exception as exc:

            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc)
            }

    # ========================================================
    # GENERAL COMMAND EXECUTION
    # ========================================================

    def run_command(
        self,
        command: List[str],
        timeout: int | None = None
    ) -> Dict[str, object]:

        allowed, reason = (
            self.policy.validate_command(
                command
            )
        )

        if not allowed:
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": reason
            }

        for argument in command[1:]:

            if (
                ".." in argument
                or "/" in argument
                or "\\" in argument
            ):

                if (
                    argument.endswith(".py")
                    or argument.endswith(".txt")
                    or argument.endswith(".json")
                    or argument.endswith(".yaml")
                    or argument.endswith(".yml")
                ):

                    allowed, reason = (
                        self.policy.validate_path(
                            argument
                        )
                    )

                    if not allowed:
                        return {
                            "success": False,
                            "return_code": -1,
                            "stdout": "",
                            "stderr": reason
                        }

        execution_timeout = (
            timeout
            if timeout is not None
            else self.limits.command_timeout_seconds
        )

        try:

            command = list(command)

            if (
                command
                and command[0] == "python"
            ):
                command[0] = sys.executable

            result = subprocess.run(
                command,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=execution_timeout
            )

            stdout = self._limit_output(
                result.stdout
            )

            stderr = self._limit_output(
                result.stderr
            )

            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": stdout,
                "stderr": stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    f"Execution timed out after "
                    f"{execution_timeout} seconds."
                )
            }

        except Exception as exc:

            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc)
            }

    # ========================================================
    # EXECUTION PLAN
    # ========================================================

    def run_plan(
        self,
        plan: Dict[str, object],
        timeout: int | None = None
    ) -> Dict[str, object]:

        command = plan.get(
            "command",
            []
        )

        if not command:
            return {
                "success": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    "No executable command "
                    "was planned."
                )
            }

        return self.run_command(
            command,
            timeout
        )