from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models.project import (
    ProjectPlan,
    ArchitecturePlan,
    GeneratedProject,
    ValidationResult,
    DebugResult,
)

load_dotenv()

llm = ChatOpenAI(
    model="gpt-6-luna"
)

debugger_llm = llm.with_structured_output(
    DebugResult
)


def debug_project(
    project_plan: ProjectPlan,
    architecture: ArchitecturePlan,
    generated_project: GeneratedProject,
    validation_result: ValidationResult,
    execution_result: dict | None = None,
    static_validation_context: str = "",
) -> DebugResult:

    files_context = []

    for file in generated_project.files:

        files_context.append(
            f"""
============================================================
FILE: {file.path}
============================================================

PURPOSE:
{file.purpose}

CONTENT:
{file.content}
"""
        )

    project_files = "\n".join(
        files_context
    )

    execution_context = ""

    if execution_result:

        execution_context = f"""
============================================================
EXECUTION RESULT
============================================================

SUCCESS:
{execution_result.get("success")}

RETURN CODE:
{execution_result.get("return_code")}

FAILURE TYPE:
{execution_result.get("failure_type")}

STDOUT:
{execution_result.get("stdout", "")}

STDERR:
{execution_result.get("stderr", "")}
"""

    prompt = f"""
You are the Debugger Agent inside an autonomous
software engineering platform.

Your responsibility is to diagnose why a generated
software project failed validation or execution.

You must identify the ACTUAL files that need inspection
or modification.

Do not guess.

============================================================
PROJECT REQUIREMENT
============================================================

{project_plan.model_dump_json(indent=2)}

============================================================
ARCHITECTURE
============================================================

{architecture.model_dump_json(indent=2)}

============================================================
VALIDATION RESULT
============================================================

{validation_result.model_dump_json(indent=2)}

============================================================
STATIC VALIDATION EVIDENCE
============================================================

{static_validation_context}

============================================================
EXECUTION EVIDENCE
============================================================

{execution_context}

============================================================
GENERATED PROJECT FILES
============================================================

{project_files}

============================================================
DEBUGGING RULES
============================================================

1. Inspect the actual supplied file contents.

2. Use static validation evidence when available.

3. Use execution errors when available.

4. Identify only files that actually exist
   in the supplied project.

5. Do not invent filenames.

6. Do not report unrelated files.

7. Trace the failure to its most likely root cause.

8. Prefer the smallest number of affected files.

9. Each fix must be concrete and actionable.

10. Explain what is wrong and what must change.

11. If the problem is a dependency issue, identify
    the dependency configuration file when present.

12. If the problem is a configuration issue, identify
    the actual configuration file.

13. If the problem is a syntax error, identify the
    exact source file containing the syntax problem.

14. If the problem is caused by multiple files,
    include all relevant existing files.

15. Do not propose a complete rewrite unless necessary.

16. Do not expose secrets.

============================================================
DEBUGGING OBJECTIVE
============================================================

Determine:

- Which files are affected
- What is wrong in each file
- What concrete fix is required
- Whether another repair/validation attempt is needed

Your response must be a structured DebugResult.
"""

    result = debugger_llm.invoke(
        prompt
    )

    return result