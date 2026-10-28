from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models.project import ProjectPlan


load_dotenv()


llm = ChatOpenAI(
    model="gpt-6-luna"
)


planner_llm = llm.with_structured_output(ProjectPlan)


def create_project_plan(requirement: str) -> ProjectPlan:

    prompt = f"""
You are the Product Planning Agent inside an autonomous
software engineering platform.

Your job is to analyze a user's software requirement and
create a practical engineering project plan.

User requirement:

{requirement}

Analyze the requirement carefully.

Determine:
- project name
- project description
- major features
- appropriate technologies
- database
- testing requirements
- deployment requirements

Do not invent unnecessary complexity.
Prefer practical production-ready technologies.
"""

    result = planner_llm.invoke(prompt)

    return result