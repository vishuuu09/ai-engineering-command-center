from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models.project import (
    ProjectPlan,
    ArchitecturePlan,
    GeneratedProject
)


load_dotenv()


llm = ChatOpenAI(
    model="gpt-6-luna"
)


developer_llm = llm.with_structured_output(
    GeneratedProject
)


def generate_project(
    project_plan: ProjectPlan,
    architecture: ArchitecturePlan
) -> GeneratedProject:

    prompt = f"""
You are the Developer Agent inside an autonomous
software engineering platform.

You have received:

1. A project plan
2. A software architecture

Your job is to generate the initial source code
for the project.

PROJECT PLAN:

{project_plan.model_dump_json(indent=2)}

ARCHITECTURE:

{architecture.model_dump_json(indent=2)}

Generate the most important files required to
bootstrap the project.

IMPORTANT RULES:

- Follow the architecture exactly.
- Generate complete files, not snippets.
- Every file must have a valid relative path.
- Do not use absolute paths.
- Do not include Markdown code fences inside file content.
- Do not include secrets or API keys.
- Keep the implementation minimal but functional.
- Make files consistent with each other.
- Do not generate unnecessary files.
- Include configuration files required to run the project.

Start with the minimum set of files needed to
create a runnable project.
"""

    result = developer_llm.invoke(prompt)

    return result