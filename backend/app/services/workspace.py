from pathlib import Path
from typing import List, Dict


class ProjectWorkspace:

    def __init__(
        self,
        root: str = "workspace"
    ):
        self.root = Path(
            root
        ).resolve()

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ========================================================
    # PATH SAFETY
    # ========================================================

    def _safe_path(
        self,
        relative_path: str
    ) -> Path:

        if not relative_path:

            raise ValueError(
                "Path cannot be empty."
            )

        requested_path = (
            self.root / relative_path
        ).resolve()

        try:

            requested_path.relative_to(
                self.root
            )

        except ValueError:

            raise ValueError(
                "Path escapes the workspace."
            )

        return requested_path

    # ========================================================
    # WRITE FILE
    # ========================================================

    def write_file(
        self,
        relative_path: str,
        content: str
    ) -> str:

        file_path = self._safe_path(
            relative_path
        )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(
            file_path
        )

    # ========================================================
    # READ FILE
    # ========================================================

    def read_file(
        self,
        relative_path: str
    ) -> str:

        file_path = self._safe_path(
            relative_path
        )

        if not file_path.exists():

            raise FileNotFoundError(
                f"File not found: "
                f"{relative_path}"
            )

        if not file_path.is_file():

            raise ValueError(
                f"Path is not a file: "
                f"{relative_path}"
            )

        return file_path.read_text(
            encoding="utf-8"
        )

    # ========================================================
    # LIST FILES
    # ========================================================

    def list_files(self) -> List[str]:

        files = []

        for path in self.root.rglob("*"):

            if path.is_file():

                relative_path = (
                    path.relative_to(
                        self.root
                    )
                )

                files.append(
                    relative_path.as_posix()
                )

        return sorted(
            files
        )

    # ========================================================
    # WRITE PROJECT
    # ========================================================

    def write_project(
        self,
        generated_files: List[Dict[str, str]]
    ) -> List[str]:

        written_files = []

        for file in generated_files:

            path = file.get(
                "path"
            )

            content = file.get(
                "content",
                ""
            )

            if not path:

                raise ValueError(
                    "Generated file is missing "
                    "a path."
                )

            written_path = self.write_file(
                path,
                content
            )

            written_files.append(
                written_path
            )

        return written_files