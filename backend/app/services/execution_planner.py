from pathlib import Path
from typing import Dict, List


class ExecutionPlanner:

    def __init__(self, workspace_root: str = "workspace"):
        self.root = Path(workspace_root)

    def get_workspace_files(self) -> List[str]:
        """
        Return the current physical files in the workspace.
        This always reflects the latest repaired files.
        """

        if not self.root.exists():
            return []

        files = []

        for path in self.root.rglob("*"):
            if path.is_file():
                relative_path = path.relative_to(
                    self.root
                )

                files.append(
                    relative_path.as_posix()
                )

        return sorted(files)

    def plan(
        self,
        generated_files: List[Dict[str, str]] | None = None
    ) -> Dict[str, object]:

        # ----------------------------------------------------
        # IMPORTANT:
        # Prefer the physical workspace.
        # ----------------------------------------------------

        file_paths = self.get_workspace_files()

        # ----------------------------------------------------
        # Fallback to state if workspace is empty
        # ----------------------------------------------------

        if not file_paths and generated_files:

            file_paths = [
                file["path"]
                for file in generated_files
            ]

        # ----------------------------------------------------
        # Python files
        # ----------------------------------------------------

        python_files = [
            path
            for path in file_paths
            if path.endswith(".py")
        ]

        # ----------------------------------------------------
        # Test files
        # ----------------------------------------------------

        test_files = [
            path
            for path in python_files
            if (
                path.startswith("tests/")
                or path.startswith("test/")
                or path.startswith("tests\\")
                or path.startswith("test\\")
                or path.startswith("test_")
                or path.endswith("_test.py")
            )
        ]

        if test_files:
            return {
                "type": "tests",
                "command": [
                    "python",
                    "-m",
                    "pytest"
                ],
                "target_files": test_files
            }

        # ----------------------------------------------------
        # Common application entry points
        # ----------------------------------------------------

        entry_points = [
            "src/main.py",
            "main.py",
            "app/main.py"
        ]

        for entry_point in entry_points:

            if entry_point in file_paths:

                return {
                    "type": "application",
                    "command": [
                        "python",
                        entry_point
                    ],
                    "target_files": [
                        entry_point
                    ]
                }

        # ----------------------------------------------------
        # Fallback Python file
        # ----------------------------------------------------

        if python_files:

            return {
                "type": "python",
                "command": [
                    "python",
                    python_files[0]
                ],
                "target_files": [
                    python_files[0]
                ]
            }

        # ----------------------------------------------------
        # Nothing executable
        # ----------------------------------------------------

        return {
            "type": "none",
            "command": [],
            "target_files": []
        }