def generate_suggestions(found, missing):

    suggestions = []

    if missing:

        suggestions.append("Rozważ dodanie do CV następujących umiejętności:")

        for skill in missing:
            suggestions.append(f"• {skill}")

        suggestions.append("")

        suggestions.append(
            "Jeżeli posiadasz doświadczenie z tymi technologiami lub obowiązkami, warto dodać je do sekcji Umiejętności lub Doświadczenie."
        )

    else:

        suggestions.append(
            "🎉 Twoje CV zawiera wszystkie wymagane umiejętności z tej oferty."
        )

    return suggestions