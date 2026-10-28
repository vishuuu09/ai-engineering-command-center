from pathlib import Path
from typing import List


class SandboxPolicy:

    # Commands that should never be executed
    BLOCKED_COMMANDS = {
        "del",
        "erase",
        "rmdir",
        "rd",
        "format",
        "shutdown",
        "restart",
        "taskkill",
        "reg",
        "diskpart",
    }

    # Dangerous Python modules that generated code should not
    # be allowed to import inside our basic sandbox.
    BLOCKED_PYTHON_MODULES = {
        "subprocess",
        "shutil",
        "ctypes",
        "winreg",
    }

    def __init__(self, workspace_root: str = "workspace"):
        self.workspace_root = Path(
            workspace_root
        ).resolve()

    def validate_command(
        self,
        command: List[str]
    ) -> tuple[bool, str]:

        if not command:
            return (
                False,
                "Command cannot be empty."
            )

        executable = Path(
            command[0]
        ).name.lower()

        if executable in self.BLOCKED_COMMANDS:
            return (
                False,
                f"Blocked command: {executable}"
            )

        return (
            True,
            "Command allowed."
        )

    def validate_path(
        self,
        relative_path: str
    ) -> tuple[bool, str]:

        if not relative_path:
            return (
                False,
                "Path cannot be empty."
            )

        requested_path = (
            self.workspace_root / relative_path
        ).resolve()

        try:
            requested_path.relative_to(
                self.workspace_root
            )
        except ValueError:
            return (
                False,
                "Path escapes the sandbox workspace."
            )

        return (
            True,
            "Path allowed."
        )

    def validate_python_content(
        self,
        content: str
    ) -> tuple[bool, str]:

        lowered = content.lower()

        for module in self.BLOCKED_PYTHON_MODULES:

            patterns = [
                f"import {module}",
                f"from {module} import",
            ]

            for pattern in patterns:

                if pattern in lowered:
                    return (
                        False,
                        f"Blocked Python module: {module}"
                    )

        return (
            True,
            "Python content allowed."
        )