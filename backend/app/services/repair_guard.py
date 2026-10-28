
import ast
from pathlib import Path
from typing import Dict, List

from app.services.sandbox_policy import SandboxPolicy


class RepairGuard:

    def __init__(self, workspace_root: str = "workspace"):
        self.root = Path(workspace_root).resolve()
        self.policy = SandboxPolicy(str(self.root))

    def validate_repair(
        self,
        relative_path: str,
        content: str
    ) -> Dict[str, object]:

        errors: List[str] = []

        if not relative_path:
            return {
                "allowed": False,
                "errors": ["Repair path cannot be empty."]
            }

        target = (self.root / relative_path).resolve()

        try:
            target.relative_to(self.root)
        except ValueError:
            return {
                "allowed": False,
                "errors": ["Repair path escapes the workspace."]
            }

        if not target.exists():
            return {
                "allowed": False,
                "errors": [
                    "Repair target must already exist in the workspace."
                ]
            }

        if not target.is_file():
            return {
                "allowed": False,
                "errors": ["Repair target is not a file."]
            }

        if not isinstance(content, str) or not content.strip():
            return {
                "allowed": False,
                "errors": ["Repair content cannot be empty."]
            }

        if target.suffix.lower() == ".py":
            try:
                ast.parse(content, filename=relative_path)
            except SyntaxError as exc:
                errors.append(
                    f"Python syntax error at line {exc.lineno}: {exc.msg}"
                )

            allowed, reason = self.policy.validate_python_content(
                content
            )

            if not allowed:
                errors.append(reason)

        return {
            "allowed": len(errors) == 0,
            "errors": errors
        }
