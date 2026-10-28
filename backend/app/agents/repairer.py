from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models.project import (
    ProjectPlan,
    ArchitecturePlan,
    ValidationResult,
    DebugResult,
    RepairResult
)

load_dotenv()

llm = ChatOpenAI(model="gpt-6-luna")

repairer_llm = llm.with_structured_output(
    RepairResult
)


def repair_project(
    project_plan: ProjectPlan,
    architecture: ArchitecturePlan,
    validation: ValidationResult,
    debug_result: DebugResult,
    file_contents: str
) -> RepairResult:

    prompt = f"""
You are the Repair Agent inside an autonomous
software engineering platform.

A Developer Agent generated a software project.

A Validator Agent found problems.

A Debugger Agent identified the affected files
and the fixes required.

Your job is to repair the affected source files.

PROJECT PLAN:

{project_plan.model_dump_json(indent=2)}

ARCHITECTURE:

{architecture.model_dump_json(indent=2)}

VALIDATION RESULTS:

{validation.model_dump_json(indent=2)}

DEBUG RESULT:

{debug_result.model_dump_json(indent=2)}

RELEVANT FILE CONTENT:

{file_contents}

IMPORTANT RULES:

1. Repair only files identified by the Debugger.
2. Preserve the existing architecture.
3. Do not introduce unnecessary technologies.
4. Do not rewrite unrelated files.
5. Return COMPLETE file contents.
6. Do not return code snippets.
7. Do not use Markdown code fences.
8. Preserve existing functionality unless the fix
   requires changing it.
9. Keep changes minimal and production-oriented.
10. Every repaired file must use its exact relative path.
11. Never include secrets or API keys.
12. Return only files that actually require changes.

The repaired files will be written directly into
the project workspace.
"""

    result = repairer_llm.invoke(prompt)

    return result