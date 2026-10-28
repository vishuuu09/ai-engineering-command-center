from app.agents.planner import create_project_plan

requirement = """
Build an expense management API for employees.

Users should be able to register, log in,
create expenses, update expenses,
delete expenses and view monthly expense reports.
"""

plan = create_project_plan(requirement)

print("\nPROJECT PLAN\n")
print(plan.model_dump_json(indent=2))