from app.agents.planner import create_project_plan
from app.agents.architect import create_architecture
from app.agents.developer import generate_project
from app.agents.validator import validate_project


requirement = """
Build a URL shortener API.

Users should be able to submit a long URL
and receive a shortened URL.

The system should support:

- URL creation
- URL redirection
- basic analytics
- testing
- Docker deployment
"""


print("\n🚀 Creating project plan...\n")

project_plan = create_project_plan(
    requirement
)


print("\n🏗️ Creating architecture...\n")

architecture = create_architecture(
    project_plan
)


print("\n💻 Generating project...\n")

project = generate_project(
    project_plan,
    architecture
)


print(
    f"\nGenerated {len(project.files)} files."
)


print("\n🧪 Validating project...\n")

validation = validate_project(
    project_plan,
    architecture,
    project
)


print("\n================ VALIDATION ================\n")

print(
    validation.model_dump_json(indent=2)
)