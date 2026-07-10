from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    score,
    found,
    missing,
    suggestions
):

    document = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()

    content = []


    content.append(
        Paragraph(
            "AI Job Assistant Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1, 20)
    )


    content.append(
        Paragraph(
            f"Dopasowanie CV: {score:.0f}%",
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1, 10)
    )


    content.append(
        Paragraph(
            "Znalezione umiejętności:",
            styles["Heading2"]
        )
    )


    for skill in found:

        content.append(
            Paragraph(
                f"- {skill}",
                styles["Normal"]
            )
        )


    content.append(
        Spacer(1, 10)
    )


    content.append(
        Paragraph(
            "Brakujące umiejętności:",
            styles["Heading2"]
        )
    )


    for skill in missing:

        content.append(
            Paragraph(
                f"- {skill}",
                styles["Normal"]
            )
        )


    content.append(
        Spacer(1, 10)
    )


    content.append(
        Paragraph(
            "Sugestie poprawy:",
            styles["Heading2"]
        )
    )


    for suggestion in suggestions:

        content.append(
            Paragraph(
                suggestion,
                styles["Normal"]
            )
        )


    document.build(
        content
    )
    