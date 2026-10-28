from pathlib import Path
import ast
from typing import Dict, List


class LocalValidator:

    def __init__(self, workspace_root: str = "workspace"):
        self.root = Path(workspace_root).resolve()

    def get_python_files(self) -> List[Path]:
        if not self.root.exists():
            return []

        return sorted(
            path
            for path in self.root.rglob("*.py")
            if path.is_file()
        )

    def check_syntax(
        self,
        path: Path
    ) -> List[str]:

        issues = []

        try:
            content = path.read_text(
                encoding="utf-8"
            )

            ast.parse(content)

        except SyntaxError as exc:

            relative_path = path.relative_to(
                self.root
            ).as_posix()

            issues.append(
                f"{relative_path}: "
                f"syntax error at line "
                f"{exc.lineno}: {exc.msg}"
            )

        except Exception as exc:

            relative_path = path.relative_to(
                self.root
            ).as_posix()

            issues.append(
                f"{relative_path}: "
                f"could not be parsed: {exc}"
            )

        return issues

    def check_empty_files(
        self,
        path: Path
    ) -> List[str]:

        issues = []

        try:
            content = path.read_text(
                encoding="utf-8"
            ).strip()

            if not content:

                relative_path = path.relative_to(
                    self.root
                ).as_posix()

                issues.append(
                    f"{relative_path}: "
                    f"Python file is empty."
                )

        except Exception:
            pass

        return issues

    def check_imports(
        self,
        path: Path
    ) -> List[str]:

        issues = []

        try:

            content = path.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(content)

        except Exception:

            return issues

        relative_path = path.relative_to(
            self.root
        ).as_posix()

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    module = alias.name

                    if module.startswith("."):
                        continue

            elif isinstance(node, ast.ImportFrom):

                if node.level > 0:
                    continue

                if node.module is None:
                    continue

        return issues

    def check_project_structure(
        self,
        files: List[str]
    ) -> List[str]:

        issues = []

        if not files:

            issues.append(
                "Project workspace contains no files."
            )

            return issues

        python_files = [
            path
            for path in files
            if path.endswith(".py")
        ]

        if not python_files:

            issues.append(
                "Project does not contain "
                "any Python source files."
            )

        return issues

    def validate(
        self
    ) -> Dict[str, object]:

        issues: List[str] = []
        warnings: List[str] = []

        if not self.root.exists():

            return {
                "passed": False,
                "issues": [
                    "Workspace directory does not exist."
                ],
                "warnings": [],
                "checked_files": []
            }

        files = []

        for path in self.root.rglob("*"):

            if path.is_file():

                files.append(
                    path.relative_to(
                        self.root
                    ).as_posix()
                )

        issues.extend(
            self.check_project_structure(
                files
            )
        )

        python_files = self.get_python_files()

        for path in python_files:

            issues.extend(
                self.check_syntax(path)
            )

            issues.extend(
                self.check_empty_files(path)
            )

            issues.extend(
                self.check_imports(path)
            )

        if not python_files:
            warnings.append(
                "No Python files were found."
            )

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "checked_files": files
        }