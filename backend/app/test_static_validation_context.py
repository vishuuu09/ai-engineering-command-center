from app.services.static_validation_context import (
    StaticValidationContext
)


def test_static_validation_context():

    print(
        "\n🧪 Testing Static Validation Context..."
    )

    validator = StaticValidationContext()

    validation_result = {
        "passed": False,
        "score": 60,
        "issues": [
            "Python syntax error in src/broken.py"
        ],
        "warnings": [
            "No automated tests detected."
        ],
        "recommendations": [
            "Repair blocking static validation issues."
        ],
    }

    context = validator.build_context(
        validation_result
    )

    print("\nGenerated context:\n")

    print(context)

    assert (
        "PASSED: False"
        in context
    )

    assert (
        "SCORE: 60"
        in context
    )

    assert (
        "src/broken.py"
        in context
    )

    assert (
        "No automated tests detected."
        in context
    )

    assert (
        "Repair blocking static validation issues."
        in context
    )

    print(
        "\n🎉 STATIC VALIDATION CONTEXT TEST PASSED!"
    )


if __name__ == "__main__":

    test_static_validation_context()