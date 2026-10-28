from typing import List

from app.services.workspace_reader import WorkspaceReader


class RepairContext:

    def __init__(
        self,
        workspace_root: str = "workspace"
    ):
        self.reader = WorkspaceReader(
            workspace_root
        )

    def get_repair_context(
        self,
        affected_files: List[str]
    ) -> str:

        if not affected_files:
            return ""

        return self.reader.read_files(
            affected_files
        )