from pathlib import Path
from typing import List


class WorkspaceReader:

    def __init__(self, root: str = "workspace"):
        self.root = Path(root)

    def read_file(
        self,
        relative_path: str
    ) -> str:

        file_path = self.root / relative_path

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {relative_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Path is not a file: {relative_path}"
            )

        return file_path.read_text(
            encoding="utf-8"
        )

    def read_files(
        self,
        relative_paths: List[str]
    ) -> str:

        contents = []

        for path in relative_paths:

            content = self.read_file(path)

            contents.append(
                f"""
FILE: {path}

CONTENT:
{content}
"""
            )

        return "\n\n".join(contents)