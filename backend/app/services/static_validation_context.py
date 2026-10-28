from typing import Dict, List


class StaticValidationContext:

    def build_context(
        self,
        validation_result: Dict[str, object]
    ) -> str:

        if not validation_result:
            return ""

        passed = validation_result.get(
            "passed",
            False
        )

        score = validation_result.get(
            "score",
            0
        )

        issues = validation_result.get(
            "issues",
            []
        )

        warnings = validation_result.get(
            "warnings",
            []
        )

        recommendations = validation_result.get(
            "recommendations",
            []
        )

        lines: List[str] = []

        lines.append(
            "STATIC VALIDATION RESULT"
        )

        lines.append(
            "========================="
        )

        lines.append(
            f"PASSED: {passed}"
        )

        lines.append(
            f"SCORE: {score}"
        )

        lines.append("")

        lines.append(
            "ISSUES:"
        )

        if issues:

            for issue in issues:

                lines.append(
                    f"- {issue}"
                )

        else:

            lines.append(
                "- None"
            )

        lines.append("")

        lines.append(
            "WARNINGS:"
        )

        if warnings:

            for warning in warnings:

                lines.append(
                    f"- {warning}"
                )

        else:

            lines.append(
                "- None"
            )

        lines.append("")

        lines.append(
            "RECOMMENDATIONS:"
        )

        if recommendations:

            for recommendation in recommendations:

                lines.append(
                    f"- {recommendation}"
                )

        else:

            lines.append(
                "- None"
            )

        return "\n".join(
            lines
        )