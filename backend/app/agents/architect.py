from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models.project import (
    ProjectPlan,
    ArchitecturePlan
)


load_dotenv()


llm = ChatOpenAI(
    model="gpt-6-luna"
)


architect_llm = llm.with_structured_output(
    ArchitecturePlan
)


def create_architecture(
    project_plan: ProjectPlan
) -> ArchitecturePlan:

    prompt = f"""
You are the Software Architect Agent inside an
autonomous software engineering platform.

Another AI agent has already analyzed the user's
software requirement and created the following project plan.

PROJECT PLAN:

{project_plan.model_dump_json(indent=2)}

Your job is to transform this project plan into a
practical production-oriented software architecture.

Design the following:

1. Overall architecture
2. Backend architecture
3. Frontend architecture
4. Database architecture
5. Authentication and authorization
6. Infrastructure
7. Project file structure

IMPORTANT RULES:

- Do not add unnecessary technologies.
- Prefer simple, maintainable architecture.
- Prefer technologies that match the project requirements.
- Make the architecture realistic enough for production.
- The file structure should be specific and useful to a developer.
"""

    result = architect_llm.invoke(prompt)

    return result