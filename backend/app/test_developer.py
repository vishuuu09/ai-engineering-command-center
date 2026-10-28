from app.agents.planner import create_project_plan
from app.agents.architect import create_architecture
from app.agents.developer import generate_project


requirement = """
Build a simple URL shortener API.

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


print("\n💻 Generating project files...\n")

project = generate_project(
    project_plan,
    architecture
)


print("\n================ GENERATED FILES ================\n")


for file in project.files:

    print(f"\n📄 {file.path}")

    print(f"Purpose: {file.purpose}")

    print("-" * 60)

    print(file.content[:1000])

    print("-" * 60)