def generate_suggestions(found, missing):

    suggestions = []


    cv_phrases = {

        "warehouse":
            "Managed warehouse operations including packing, shipping, inventory control and logistics tasks.",

        "customer service":
            "Provided customer support, handled client requests and maintained positive customer relationships.",

        "python":
            "Developed Python solutions and automated tasks using programming techniques.",

        "excel":
            "Used Excel spreadsheets for data analysis, reporting and process tracking.",

        "english":
            "Communicated effectively in English in professional and international environments.",

        "ai":
            "Worked with artificial intelligence concepts and machine learning technologies."
    }



    if missing:

        suggestions.append(
            "❌ Brakujące umiejętności:"
        )


        for skill in missing:

            suggestions.append(
                f"• {skill}"
            )


            if skill in cv_phrases:

                suggestions.append(
                    "✍️ Przykładowy wpis do CV:"
                )

                suggestions.append(
                    cv_phrases[skill]
                )


                suggestions.append("")



    else:

        suggestions.append(
            "🎉 Nie znaleziono brakujących kluczowych umiejętności."
        )



    if found:

        suggestions.append(
            "✅ Umiejętności, które warto mocniej podkreślić:"
        )


        for skill in found:

            suggestions.append(
                f"• Rozwiń doświadczenie związane z: {skill}"
            )



    suggestions.append("")

    suggestions.append(
        "📌 Wskazówka ATS: używaj słów kluczowych dokładnie tak, jak pojawiają się w ogłoszeniu."
    )


    return suggestions