from app.agents.planner import create_project_plan
from app.agents.architect import create_architecture


requirement = """
Build a powerful employee expense management API
with authentication, expense tracking, monthly analytics,
testing, Docker and deployment.
"""


print("\nCreating project plan...\n")

project_plan = create_project_plan(requirement)

print("\n================ PROJECT PLAN ================\n")

print(
    project_plan.model_dump_json(indent=2)
)


print("\nCreating architecture...\n")

architecture = create_architecture(
    project_plan
)

print("\n================ ARCHITECTURE ================\n")

print(
    architecture.model_dump_json(indent=2)
)