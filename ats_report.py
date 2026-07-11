def generate_ats_report(ats_result):

    report = []


    score = ats_result["score"]


    report.append(
        f"🤖 Wynik ATS: {score}/100"
    )


    report.append("")


    if score >= 80:

        report.append(
            "🟢 CV jest dobrze dopasowane do systemów ATS."
        )

    elif score >= 50:

        report.append(
            "🟡 CV ma dobre podstawy, ale wymaga kilku poprawek."
        )

    else:

        report.append(
            "🔴 CV wymaga większej optymalizacji pod tę ofertę."
        )



    report.append("")


    if ats_result["found_keywords"]:

        report.append(
            "✅ Znalezione słowa kluczowe:"
        )


        for keyword in ats_result["found_keywords"]:

            report.append(
                f"• {keyword}"
            )



    report.append("")


    if ats_result["missing_keywords"]:

        report.append(
            "❌ Brakujące słowa kluczowe:"
        )


        for keyword in ats_result["missing_keywords"]:

            report.append(
                f"• {keyword}"
            )


    report.append("")


    if ats_result["sections_found"]:

        report.append(
            "✅ Wykryte sekcje CV:"
        )


        for section in ats_result["sections_found"]:

            report.append(
                f"• {section}"
            )



    if ats_result["sections_missing"]:

        report.append("")


        report.append(
            "⚠️ Brakujące sekcje:"
        )


        for section in ats_result["sections_missing"]:

            report.append(
                f"• {section}"
            )



    return report