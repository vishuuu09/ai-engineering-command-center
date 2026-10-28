
from pathlib import Path


class WorkspaceEditor:

    def __init__(
        self,
        root: str = "workspace"
    ):
        self.root = Path(root).resolve()

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

        return str(file_path)

    # ========================================================
    # REPLACE EXISTING FILE
    # ========================================================

    def replace_file(
        self,
        relative_path: str,
        content: str
    ) -> str:

        file_path = self._safe_path(
            relative_path
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Cannot replace missing file: "
                f"{relative_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Path is not a file: "
                f"{relative_path}"
            )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(file_path)
