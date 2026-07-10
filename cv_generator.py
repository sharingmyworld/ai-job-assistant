def generate_cv_improvements(found, missing):

    result = []

    result.append("✨ Propozycje ulepszenia CV")
    result.append("")

    if found:
        result.append("Twoje mocne strony:")
        
        for skill in found:
            result.append(f"• {skill}")

        result.append("")

    if missing:

        result.append("Warto rozważyć dodanie:")

        for skill in missing:
            result.append(f"• {skill}")

        result.append("")

    result.append("Przykładowy profil zawodowy:")

    profile = "Kandydat posiadający doświadczenie w "

    if found:
        profile += ", ".join(found)

    else:
        profile += "pracy zawodowej"

    profile += ". Gotowy do dalszego rozwoju i zdobywania nowych kompetencji."

    result.append(profile)

    result.append("")

    result.append("Przykładowa zmiana opisu doświadczenia:")

    experience = (
        "Posiadam doświadczenie w realizacji zadań związanych z "
        "organizacją pracy, wykorzystaniem wymaganych umiejętności "
        "oraz efektywną realizacją powierzonych obowiązków."
    )

    result.append(experience)

    return result