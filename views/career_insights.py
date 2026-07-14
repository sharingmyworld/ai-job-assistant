import streamlit as st
import pandas as pd
from collections import Counter

from database import get_career_insights_data


def _split_skills(skills_text):
    if not skills_text:
        return []

    return [
        skill.strip()
        for skill in str(skills_text).split(",")
        if skill.strip()
    ]


def show_career_insights():
    st.header("🧠 Career Insights")

    st.write(
        "Wnioski są tworzone na podstawie historii analiz CV, "
        "planu nauki i trackera aplikacji."
    )

    data = get_career_insights_data(
        st.session_state.username
    )

    analyses = data["analyses"]
    learning_plan = data["learning_plan"]
    applications = data["applications"]

    if not analyses and not learning_plan and not applications:
        st.info(
            "Brak wystarczających danych. Wykonaj analizy CV "
            "i dodaj aplikacje, aby zobaczyć wnioski."
        )
        return

    st.subheader("📊 Podsumowanie")

    analysis_count = len(analyses)
    application_count = len(applications)
    learning_count = len(learning_plan)

    avg_score = (
        sum(row[0] for row in analyses) / analysis_count
        if analysis_count
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Analizy CV",
            analysis_count
        )

    with col2:
        st.metric(
            "Średnie dopasowanie",
            f"{avg_score:.1f}%"
        )

    with col3:
        st.metric(
            "Aplikacje",
            application_count
        )

    with col4:
        st.metric(
            "Umiejętności w planie",
            learning_count
        )

    st.divider()
    st.subheader("🎯 Najczęstsze braki")

    missing_counter = Counter()

    for _, _, missing_text, _ in analyses:
        missing_counter.update(
            skill.lower()
            for skill in _split_skills(missing_text)
        )

    if missing_counter:
        missing_rows = [
            {
                "Umiejętność": skill.title(),
                "Liczba wystąpień": count
            }
            for skill, count in missing_counter.most_common(10)
        ]

        missing_df = pd.DataFrame(missing_rows)

        st.bar_chart(
            missing_df.set_index(
                "Umiejętność"
            )
        )

        top_skill, top_count = (
            missing_counter.most_common(1)[0]
        )

        share = (
            top_count / analysis_count * 100
            if analysis_count
            else 0
        )

        st.info(
            f"Najczęściej brakującą umiejętnością jest "
            f"**{top_skill.title()}** — pojawiła się w "
            f"{share:.0f}% analiz."
        )
    else:
        st.success(
            "W historii nie ma zapisanych brakujących umiejętności."
        )

    st.divider()
    st.subheader("💼 Najlepiej dopasowane stanowiska")

    title_scores = {}

    for score, title, _, _ in analyses:
        clean_title = (
            title.strip()
            if title and title.strip()
            else "Bez nazwy stanowiska"
        )

        title_scores.setdefault(
            clean_title,
            []
        ).append(float(score))

    if title_scores:
        title_rows = [
            {
                "Stanowisko": title,
                "Średnie dopasowanie": (
                    sum(scores) / len(scores)
                )
            }
            for title, scores in title_scores.items()
        ]

        title_df = pd.DataFrame(
            title_rows
        ).sort_values(
            by="Średnie dopasowanie",
            ascending=False
        )

        st.bar_chart(
            title_df.set_index(
                "Stanowisko"
            )
        )

        best_title = title_df.iloc[0]

        st.success(
            f"Najwyższe średnie dopasowanie masz do stanowiska "
            f"**{best_title['Stanowisko']}**: "
            f"{best_title['Średnie dopasowanie']:.1f}%."
        )
    else:
        st.info(
            "Brak danych o stanowiskach."
        )

    st.divider()
    st.subheader("📨 Skuteczność aplikacji")

    if applications:
        active_apps = [
            row
            for row in applications
            if row[2] not in {
                "Planowana",
                "Wycofana"
            }
        ]

        interviews = [
            row
            for row in active_apps
            if row[2] in {
                "Rozmowa HR",
                "Rozmowa techniczna",
                "Oferta"
            }
        ]

        offers = [
            row
            for row in active_apps
            if row[2] == "Oferta"
        ]

        interview_rate = (
            len(interviews) / len(active_apps) * 100
            if active_apps
            else 0
        )

        offer_rate = (
            len(offers) / len(active_apps) * 100
            if active_apps
            else 0
        )

        app_col1, app_col2 = st.columns(2)

        with app_col1:
            st.metric(
                "Przejście do rozmowy",
                f"{interview_rate:.1f}%"
            )

        with app_col2:
            st.metric(
                "Przejście do oferty",
                f"{offer_rate:.1f}%"
            )

        scored_interviews = [
            float(row[3])
            for row in interviews
            if row[3] is not None and row[3] > 0
        ]

        scored_without_interview = [
            float(row[3])
            for row in active_apps
            if (
                row[2] in {"Wysłana", "Odrzucona"}
                and row[3] is not None
                and row[3] > 0
            )
        ]

        if scored_interviews:
            avg_interview_score = (
                sum(scored_interviews)
                / len(scored_interviews)
            )

            st.info(
                f"Średnie dopasowanie CV dla aplikacji "
                f"zakończonych rozmową wynosi "
                f"**{avg_interview_score:.1f}%**."
            )

        if (
            scored_interviews
            and scored_without_interview
        ):
            avg_without = (
                sum(scored_without_interview)
                / len(scored_without_interview)
            )

            difference = (
                avg_interview_score - avg_without
            )

            if difference > 0:
                st.success(
                    f"Aplikacje z rozmową mają średnio o "
                    f"**{difference:.1f} p.p.** wyższe "
                    f"dopasowanie CV."
                )
            else:
                st.info(
                    "Na obecnych danych wyższe dopasowanie CV "
                    "nie daje jeszcze wyraźnie większej szansy "
                    "na rozmowę."
                )
    else:
        st.info(
            "Brak danych z trackera aplikacji."
        )

    st.divider()
    st.subheader("🗂️ Skuteczność wersji CV")

    version_scores = {}

    for score, _, _, cv_version in analyses:
        version_name = (
            cv_version.strip()
            if cv_version and cv_version.strip()
            else "Bez nazwy wersji"
        )

        version_scores.setdefault(
            version_name,
            []
        ).append(float(score))

    if version_scores:
        version_rows = [
            {
                "Wersja CV": version,
                "Średnie dopasowanie": (
                    sum(scores) / len(scores)
                ),
                "Liczba analiz": len(scores)
            }
            for version, scores in version_scores.items()
        ]

        version_df = pd.DataFrame(
            version_rows
        ).sort_values(
            by="Średnie dopasowanie",
            ascending=False
        )

        st.bar_chart(
            version_df.set_index(
                "Wersja CV"
            )["Średnie dopasowanie"]
        )

        best_version = version_df.iloc[0]

        st.success(
            f"Najlepsza wersja CV to "
            f"**{best_version['Wersja CV']}** "
            f"ze średnim dopasowaniem "
            f"{best_version['Średnie dopasowanie']:.1f}%."
        )
    else:
        st.info(
            "Brak danych o wersjach CV."
        )

    st.divider()
    st.subheader("📚 Rekomendowany następny krok")

    active_learning = [
        row
        for row in learning_plan
        if row[2] != "Ukończone"
    ]

    priority_order = {
        "Wysoki": 1,
        "Średni": 2,
        "Niski": 3
    }

    if active_learning:
        active_learning.sort(
            key=lambda row: (
                priority_order.get(
                    row[1],
                    4
                ),
                row[0].lower()
            )
        )

        next_skill = active_learning[0]

        st.warning(
            f"Najlepszy kolejny krok: rozpocznij lub kontynuuj "
            f"naukę **{next_skill[0]}** "
            f"(priorytet: {next_skill[1]})."
        )
    elif learning_plan:
        st.success(
            "Wszystkie umiejętności w planie nauki "
            "są oznaczone jako ukończone."
        )
    else:
        st.info(
            "Plan nauki jest pusty."
        )
