from typing import List, Dict

from app.services.workspace_reader import WorkspaceReader


class DebugContextBuilder:

    def __init__(self, workspace_root: str = "workspace"):
        self.reader = WorkspaceReader(workspace_root)

    def build_context(
        self,
        fixes: List[Dict[str, str]]
    ) -> str:

        file_paths = []

        for fix in fixes:

            path = fix.get("file_path")

            if path and path not in file_paths:
                file_paths.append(path)

        if not file_paths:
            return ""

        return self.reader.read_files(
            file_paths
        )