from typing import List, Dict

from app.services.workspace import ProjectWorkspace
from app.services.workspace_reader import WorkspaceReader


class DebuggerContext:

    def __init__(
        self,
        workspace_root: str = "workspace"
    ):
        self.workspace = ProjectWorkspace(
            workspace_root
        )

        self.reader = WorkspaceReader(
            workspace_root
        )

    def get_file_manifest(self) -> List[str]:

        return self.workspace.list_files()

    def read_selected_files(
        self,
        file_paths: List[str]
    ) -> str:

        return self.reader.read_files(
            file_paths
        )

    def prepare_context(
        self,
        file_paths: List[str]
    ) -> Dict[str, object]:

        manifest = self.get_file_manifest()

        valid_files = [
            path
            for path in file_paths
            if path in manifest
        ]

        contents = self.read_selected_files(
            valid_files
        )

        return {
            "available_files": manifest,
            "selected_files": valid_files,
            "contents": contents
        }