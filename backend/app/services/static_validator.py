from pathlib import Path
import ast
import re
from typing import Dict, List


class StaticValidationResult:
    def __init__(
        self,
        passed: bool,
        score: int,
        issues: List[str],
        warnings: List[str],
        recommendations: List[str],
    ):
        self.passed = passed
        self.score = score
        self.issues = issues
        self.warnings = warnings
        self.recommendations = recommendations

    def to_dict(self) -> Dict[str, object]:

        return {
            "passed": self.passed,
            "score": self.score,
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }


class StaticValidator:

    SECRET_PATTERNS = [
        r"sk-[A-Za-z0-9]{20,}",
        r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]",
        r"secret[_-]?key\s*=\s*['\"][^'\"]+['\"]",
        r"password\s*=\s*['\"][^'\"]+['\"]",
        r"access[_-]?token\s*=\s*['\"][^'\"]+['\"]",
    ]

    PYTHON_DEPENDENCY_MAP = {
        "fastapi": "fastapi",
        "flask": "flask",
        "django": "django",
        "langchain": "langchain",
        "langchain_openai": "langchain-openai",
        "langgraph": "langgraph",
        "pydantic": "pydantic",
        "dotenv": "python-dotenv",
        "requests": "requests",
        "numpy": "numpy",
        "pandas": "pandas",
        "pytest": "pytest",
    }

    def __init__(
        self,
        workspace_root: str = "workspace"
    ):
        self.root = Path(
            workspace_root
        ).resolve()

    # ========================================================
    # FILE DISCOVERY
    # ========================================================

    def get_files(self) -> List[str]:

        if not self.root.exists():
            return []

        files = []

        for path in self.root.rglob("*"):

            if path.is_file():

                relative = path.relative_to(
                    self.root
                )

                files.append(
                    relative.as_posix()
                )

        return sorted(files)

    # ========================================================
    # READ FILE
    # ========================================================

    def read_file(
        self,
        relative_path: str
    ) -> str:

        path = (
            self.root / relative_path
        )

        try:

            return path.read_text(
                encoding="utf-8"
            )

        except Exception:

            return ""

    # ========================================================
    # EMPTY FILE CHECK
    # ========================================================

    def check_empty_files(
        self,
        files: List[str]
    ) -> List[str]:

        issues = []

        for relative_path in files:

            content = self.read_file(
                relative_path
            )

            if not content.strip():

                issues.append(
                    f"Empty file detected: "
                    f"{relative_path}"
                )

        return issues

    # ========================================================
    # PYTHON SYNTAX CHECK
    # ========================================================

    def check_python_syntax(
        self,
        files: List[str]
    ) -> List[str]:

        issues = []

        python_files = [
            path
            for path in files
            if path.endswith(".py")
        ]

        for relative_path in python_files:

            content = self.read_file(
                relative_path
            )

            if not content.strip():
                continue

            try:

                ast.parse(
                    content,
                    filename=relative_path
                )

            except SyntaxError as exc:

                issues.append(
                    f"Python syntax error in "
                    f"{relative_path}: "
                    f"{exc.msg} at line "
                    f"{exc.lineno}"
                )

        return issues

    # ========================================================
    # PYTHON IMPORT CHECK
    # ========================================================

    def check_python_imports(
        self,
        files: List[str]
    ) -> List[str]:

        issues = []

        python_files = [
            path
            for path in files
            if path.endswith(".py")
        ]

        for relative_path in python_files:

            content = self.read_file(
                relative_path
            )

            if not content.strip():
                continue

            try:

                tree = ast.parse(
                    content,
                    filename=relative_path
                )

            except SyntaxError:

                continue

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.Import
                ):

                    for alias in node.names:

                        self._check_import(
                            alias.name,
                            relative_path,
                            files,
                            issues
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom
                ):

                    if node.module:

                        self._check_import(
                            node.module,
                            relative_path,
                            files,
                            issues
                        )

        return issues

    def _check_import(
        self,
        module_name: str,
        relative_path: str,
        files: List[str],
        issues: List[str]
    ):

        root_module = (
            module_name.split(".")[0]
        )

        standard_library = {
            "os",
            "sys",
            "json",
            "re",
            "ast",
            "pathlib",
            "typing",
            "datetime",
            "time",
            "math",
            "random",
            "subprocess",
            "threading",
            "asyncio",
            "logging",
            "dataclasses",
            "collections",
        }

        if root_module in standard_library:
            return

        local_module_exists = any(
            path.startswith(
                f"{root_module}/"
            )
            or path == (
                f"{root_module}.py"
            )
            for path in files
        )

        if local_module_exists:
            return

        dependency = (
            self.PYTHON_DEPENDENCY_MAP.get(
                module_name
            )
            or self.PYTHON_DEPENDENCY_MAP.get(
                root_module
            )
        )

        dependency_files = [
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
        ]

        declared = False

        for dependency_file in dependency_files:

            if dependency_file not in files:
                continue

            dependency_content = (
                self.read_file(
                    dependency_file
                ).lower()
            )

            if dependency:

                if dependency.lower() in (
                    dependency_content
                ):

                    declared = True
                    break

        if dependency and not declared:

            issues.append(
                f"Possible undeclared dependency "
                f"'{dependency}' imported by "
                f"{relative_path}"
            )

    # ========================================================
    # SECRET CHECK
    # ========================================================

    def check_secrets(
        self,
        files: List[str]
    ) -> List[str]:

        issues = []

        ignored_files = {
            ".env.example",
            "README.md",
            "README.txt",
        }

        for relative_path in files:

            if relative_path in ignored_files:
                continue

            content = self.read_file(
                relative_path
            )

            for pattern in self.SECRET_PATTERNS:

                if re.search(
                    pattern,
                    content,
                    re.IGNORECASE
                ):

                    issues.append(
                        f"Potential hardcoded secret "
                        f"detected in "
                        f"{relative_path}"
                    )

                    break

        return issues

    # ========================================================
    # TEST DISCOVERY
    # ========================================================

    def check_tests(
        self,
        files: List[str]
    ) -> List[str]:

        warnings = []

        test_files = [
            path
            for path in files
            if (
                path.startswith("tests/")
                or path.startswith("test/")
                or path.startswith("test_")
                or path.endswith("_test.py")
            )
        ]

        source_files = [
            path
            for path in files
            if (
                path.endswith(".py")
                and not (
                    path.startswith("tests/")
                    or path.startswith("test/")
                    or path.startswith("test_")
                    or path.endswith("_test.py")
                )
            )
        ]

        if source_files and not test_files:

            warnings.append(
                "No automated test files detected."
            )

        return warnings

    # ========================================================
    # ENVIRONMENT CHECK
    # ========================================================

    def check_environment_files(
        self,
        files: List[str]
    ) -> List[str]:

        warnings = []

        if (
            ".env" in files
            and ".env.example" not in files
        ):

            warnings.append(
                "A .env file exists without "
                "an .env.example template."
            )

        return warnings

    # ========================================================
    # MAIN VALIDATION
    # ========================================================

    def validate(
        self
    ) -> StaticValidationResult:

        issues = []
        warnings = []
        recommendations = []

        files = self.get_files()

        if not files:

            return StaticValidationResult(
                passed=False,
                score=0,
                issues=[
                    "Workspace contains no files."
                ],
                warnings=[],
                recommendations=[
                    "Generate the project "
                    "before validation."
                ],
            )

        issues.extend(
            self.check_empty_files(
                files
            )
        )

        issues.extend(
            self.check_python_syntax(
                files
            )
        )

        issues.extend(
            self.check_python_imports(
                files
            )
        )

        issues.extend(
            self.check_secrets(
                files
            )
        )

        warnings.extend(
            self.check_tests(
                files
            )
        )

        warnings.extend(
            self.check_environment_files(
                files
            )
        )

        if issues:

            recommendations.append(
                "Repair blocking static "
                "validation issues before "
                "continuing."
            )

        if warnings:

            recommendations.append(
                "Review static validation "
                "warnings before deployment."
            )

        total_checks = 4

        failed_checks = min(
            len(issues),
            total_checks
        )

        score = max(
            0,
            100 - (
                failed_checks * 20
            )
        )

        passed = (
            len(issues) == 0
        )

        return StaticValidationResult(
            passed=passed,
            score=score,
            issues=issues,
            warnings=warnings,
            recommendations=recommendations,
        )