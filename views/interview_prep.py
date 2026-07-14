import streamlit as st
import pandas as pd

from database import (
    get_job_applications,
    get_interview_prep_data,
    save_interview_prep_item,
    save_interview_feedback,
    get_interview_feedback
)


TECH_QUESTIONS = {
    "python": [
        "Jaka jest różnica między listą a krotką w Pythonie?",
        "Jak działa obsługa wyjątków try/except?",
        "Czym różni się metoda instancji od metody statycznej?",
        "Jak zarządzasz zależnościami i środowiskiem projektu?",
        "Jak przetestowałbyś funkcję przetwarzającą dane?",
    ],
    "sql": [
        "Jaka jest różnica między WHERE a HAVING?",
        "Wyjaśnij INNER JOIN, LEFT JOIN i FULL JOIN.",
        "Do czego służą funkcje okienkowe?",
        "Jak znaleźć duplikaty w tabeli?",
        "Jak zoptymalizować wolne zapytanie SQL?",
    ],
    "data": [
        "Jak przygotowujesz dane przed analizą?",
        "Jak radzisz sobie z brakującymi wartościami?",
        "Jak dobierasz właściwy typ wykresu?",
        "Jak sprawdzasz jakość i poprawność danych?",
        "Jak wyjaśniłbyś wynik analizy osobie nietechnicznej?",
    ],
    "backend": [
        "Jak zaprojektowałbyś REST API?",
        "Czym różni się autoryzacja od uwierzytelniania?",
        "Jak obsłużyć błędy i walidację danych w API?",
        "Jak zapobiegać problemom z wydajnością bazy?",
        "Jak monitorować aplikację produkcyjną?",
    ],
    "frontend": [
        "Jak działa DOM?",
        "Czym różni się stan komponentu od propsów?",
        "Jak ograniczyć niepotrzebne renderowanie?",
        "Jak obsłużyć błędy wywołań API?",
        "Jak zapewnić responsywność interfejsu?",
    ],
    "devops": [
        "Jaka jest różnica między obrazem a kontenerem Docker?",
        "Jak działa pipeline CI/CD?",
        "Jak zarządzać sekretami w środowisku produkcyjnym?",
        "Jak monitorować dostępność aplikacji?",
        "Jak zaplanować bezpieczny rollback wdrożenia?",
    ],
    "default": [
        "Opowiedz o projekcie, z którego jesteś najbardziej dumny.",
        "Jak rozwiązujesz trudne problemy techniczne?",
        "Jak uczysz się nowych technologii?",
        "Jak organizujesz pracę nad zadaniem?",
        "Jak reagujesz na feedback?",
    ],
}


HR_QUESTIONS = [
    "Opowiedz krótko o sobie.",
    "Dlaczego interesuje Cię to stanowisko?",
    "Dlaczego chcesz pracować w tej firmie?",
    "Jakie są Twoje mocne strony?",
    "Nad czym obecnie pracujesz rozwojowo?",
    "Opowiedz o trudnej sytuacji i sposobie jej rozwiązania.",
    "Jak radzisz sobie z presją czasu?",
    "Jakiego środowiska pracy szukasz?",
    "Jakie masz oczekiwania finansowe?",
    "Kiedy możesz rozpocząć pracę?",
]


def _detect_question_groups(position):
    position_lower = str(position).lower()
    groups = []

    keyword_map = {
        "python": ["python", "django", "flask"],
        "sql": ["sql", "database", "analityk", "analyst"],
        "data": [
            "data",
            "analityk",
            "analyst",
            "business intelligence",
            "power bi",
        ],
        "backend": [
            "backend",
            "back-end",
            "api",
            "server",
        ],
        "frontend": [
            "frontend",
            "front-end",
            "react",
            "javascript",
            "typescript",
        ],
        "devops": [
            "devops",
            "docker",
            "kubernetes",
            "cloud",
            "aws",
            "azure",
        ],
    }

    for group, keywords in keyword_map.items():
        if any(keyword in position_lower for keyword in keywords):
            groups.append(group)

    if not groups:
        groups.append("default")

    return groups


def _get_technical_questions(position):
    groups = _detect_question_groups(position)
    questions = []

    for group in groups:
        questions.extend(
            TECH_QUESTIONS[group]
        )

    unique_questions = []

    for question in questions:
        if question not in unique_questions:
            unique_questions.append(question)

    return unique_questions[:10]


def _build_preparation_plan(position, match_score):
    plan = [
        "Przeczytaj ponownie ofertę i zaznacz 5 najważniejszych wymagań.",
        "Przygotuj 60-sekundowe przedstawienie swojego doświadczenia.",
        "Wybierz 2 projekty, które najlepiej pasują do stanowiska.",
        "Przygotuj odpowiedzi metodą STAR do 3 sytuacji zawodowych.",
        "Przećwicz pytania techniczne i zapisz krótkie odpowiedzi.",
        "Przygotuj 4 pytania do rekrutera lub zespołu.",
        "Sprawdź informacje o firmie, produkcie i kulturze organizacyjnej.",
        "Przygotuj środowisko, sprzęt i dokumenty przed rozmową.",
    ]

    if match_score is not None and match_score < 60:
        plan.insert(
            1,
            "Skup się na brakach względem oferty i przygotuj przykłady szybkiej nauki."
        )
    elif match_score is not None and match_score >= 80:
        plan.insert(
            1,
            "Podkreśl mocne dopasowanie i przygotuj konkretne dowody osiągnięć."
        )

    return plan


def show_interview_prep():
    st.header("🎤 Przygotowanie do rozmowy")

    st.write(
        "Wybierz aplikację, aby otrzymać plan przygotowań "
        "i zestaw pytań rekrutacyjnych."
    )

    applications = get_job_applications(
        st.session_state.username
    )

    if not applications:
        st.info(
            "Brak aplikacji. Najpierw dodaj ofertę do trackera."
        )
        return

    df = pd.DataFrame(
        applications,
        columns=[
            "ID",
            "Firma",
            "Stanowisko",
            "Status",
            "Data aplikacji",
            "Link",
            "Notatki",
            "Utworzono",
            "Zaktualizowano",
            "Dopasowanie",
            "Termin wydarzenia",
            "Typ wydarzenia",
            "Wersja CV",
        ],
    )

    df["Etykieta"] = (
        df["Stanowisko"]
        + " — "
        + df["Firma"]
        + " ["
        + df["Status"]
        + "]"
    )

    selected_label = st.selectbox(
        "Wybierz aplikację",
        df["Etykieta"].tolist(),
        key="interview_application",
    )

    selected = df.loc[
        df["Etykieta"] == selected_label
    ].iloc[0]

    application_id = int(selected["ID"])
    username = st.session_state.username

    saved_prep = get_interview_prep_data(
        username,
        application_id
    )

    position = selected["Stanowisko"]
    company = selected["Firma"]
    match_score = (
        float(selected["Dopasowanie"])
        if pd.notna(selected["Dopasowanie"])
        else None
    )

    st.subheader(
        f"💼 {position} — {company}"
    )

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Status",
            selected["Status"],
        )

    with info2:
        st.metric(
            "Dopasowanie CV",
            (
                f"{match_score:.1f}%"
                if match_score is not None
                else "Brak danych"
            ),
        )

    with info3:
        st.metric(
            "Wersja CV",
            (
                selected["Wersja CV"]
                if selected["Wersja CV"]
                else "Bez nazwy"
            ),
        )

    st.divider()
    st.subheader("🗓️ Plan przygotowania")

    preparation_plan = _build_preparation_plan(
        position,
        match_score,
    )

    completed_count = 0

    for index, step in enumerate(preparation_plan):
        item_key = f"prep_step_{index}"

        saved_checked = (
            saved_prep.get(
                item_key,
                "False"
            ) == "True"
        )

        checked = st.checkbox(
            f"{index + 1}. {step}",
            value=saved_checked,
            key=f"prep_{application_id}_{index}",
        )

        if checked != saved_checked:
            save_interview_prep_item(
                username,
                application_id,
                item_key,
                checked
            )
            st.rerun()

        if checked:
            completed_count += 1

    progress = (
        completed_count / len(preparation_plan)
        if preparation_plan
        else 0
    )

    st.progress(progress)
    st.caption(
        f"Postęp przygotowania: "
        f"{completed_count}/{len(preparation_plan)} "
        f"({progress * 100:.0f}%)"
    )

    st.divider()
    st.subheader("🧠 Pytania techniczne")

    technical_questions = _get_technical_questions(
        position
    )

    for index, question in enumerate(
        technical_questions,
        start=1,
    ):
        with st.expander(
            f"{index}. {question}"
        ):
            item_key = f"tech_answer_{index}"

            answer = st.text_area(
                "Twoja odpowiedź",
                value=saved_prep.get(
                    item_key,
                    ""
                ),
                key=(
                    f"tech_answer_"
                    f"{application_id}_{index}"
                ),
                height=120,
            )

            if st.button(
                "💾 Zapisz odpowiedź",
                key=f"save_tech_{application_id}_{index}"
            ):
                save_interview_prep_item(
                    username,
                    application_id,
                    item_key,
                    answer
                )
                st.success("Odpowiedź zapisana.")

    st.divider()
    st.subheader("🤝 Pytania HR")

    for index, question in enumerate(
        HR_QUESTIONS,
        start=1,
    ):
        with st.expander(
            f"{index}. {question}"
        ):
            item_key = f"hr_answer_{index}"

            answer = st.text_area(
                "Twoja odpowiedź",
                value=saved_prep.get(
                    item_key,
                    ""
                ),
                key=(
                    f"hr_answer_"
                    f"{application_id}_{index}"
                ),
                height=120,
            )

            if st.button(
                "💾 Zapisz odpowiedź",
                key=f"save_hr_{application_id}_{index}"
            ):
                save_interview_prep_item(
                    username,
                    application_id,
                    item_key,
                    answer
                )
                st.success("Odpowiedź zapisana.")

    st.divider()
    st.subheader("❓ Pytania do firmy")

    suggested_questions = [
        "Jak wygląda typowy dzień na tym stanowisku?",
        "Jakie są najważniejsze cele na pierwsze 3 miesiące?",
        "Jak wygląda współpraca w zespole?",
        "Jak mierzone są wyniki na tym stanowisku?",
        "Jakie są kolejne etapy procesu rekrutacyjnego?",
    ]

    for question in suggested_questions:
        st.write(f"• {question}")


    st.divider()
    st.subheader("🧾 Feedback po rozmowie")

    interview_feedback = get_interview_feedback(
        username,
        application_id
    )

    with st.expander(
        "➕ Dodaj lub zaktualizuj feedback",
        expanded=False
    ):
        from datetime import date

        feedback_date = st.date_input(
            "Data rozmowy",
            value=date.today(),
            key=f"feedback_date_{application_id}"
        )

        feedback_type = st.selectbox(
            "Typ rozmowy",
            [
                "Rozmowa HR",
                "Rozmowa techniczna",
                "Rozmowa z managerem",
                "Case study",
                "Zadanie rekrutacyjne",
                "Inne"
            ],
            key=f"feedback_type_{application_id}"
        )

        rating_col, difficulty_col = st.columns(2)

        with rating_col:
            self_rating = st.slider(
                "Jak oceniasz swoją rozmowę?",
                min_value=1,
                max_value=5,
                value=3,
                key=f"feedback_rating_{application_id}"
            )

        with difficulty_col:
            difficulty = st.slider(
                "Poziom trudności",
                min_value=1,
                max_value=5,
                value=3,
                key=f"feedback_difficulty_{application_id}"
            )

        feedback_result = st.selectbox(
            "Wynik rozmowy",
            [
                "Oczekuję na decyzję",
                "Przechodzę dalej",
                "Oferta",
                "Odrzucona",
                "Wycofana"
            ],
            key=f"feedback_result_{application_id}"
        )

        difficult_questions = st.text_area(
            "Najtrudniejsze pytania",
            placeholder=(
                "Jakie pytania sprawiły największą trudność?"
            ),
            key=f"feedback_questions_{application_id}"
        )

        strengths = st.text_area(
            "Co poszło dobrze?",
            placeholder=(
                "Mocne odpowiedzi, przykłady, komunikacja..."
            ),
            key=f"feedback_strengths_{application_id}"
        )

        improvements = st.text_area(
            "Co poprawić?",
            placeholder=(
                "Braki techniczne, zbyt ogólne odpowiedzi..."
            ),
            key=f"feedback_improvements_{application_id}"
        )

        next_steps = st.text_area(
            "Kolejne kroki",
            placeholder=(
                "Follow-up, przygotowanie do kolejnego etapu..."
            ),
            key=f"feedback_next_steps_{application_id}"
        )

        if st.button(
            "💾 Zapisz feedback",
            key=f"save_feedback_{application_id}"
        ):
            save_interview_feedback(
                username,
                application_id,
                feedback_date.isoformat(),
                feedback_type,
                self_rating,
                difficulty,
                feedback_result,
                difficult_questions,
                strengths,
                improvements,
                next_steps
            )

            st.success(
                "Feedback został zapisany."
            )
            st.rerun()

    if interview_feedback:
        st.markdown("#### 📚 Historia feedbacku")

        for feedback in interview_feedback:
            (
                feedback_id,
                interview_date,
                interview_type,
                self_rating,
                difficulty,
                result,
                difficult_questions,
                strengths,
                improvements,
                next_steps,
                created_at,
                updated_at
            ) = feedback

            with st.expander(
                f"{interview_date} — "
                f"{interview_type} — "
                f"{result}"
            ):
                metric1, metric2 = st.columns(2)

                with metric1:
                    st.metric(
                        "Samoocena",
                        f"{self_rating}/5"
                    )

                with metric2:
                    st.metric(
                        "Trudność",
                        f"{difficulty}/5"
                    )

                if difficult_questions:
                    st.markdown(
                        "**Najtrudniejsze pytania:**"
                    )
                    st.write(difficult_questions)

                if strengths:
                    st.markdown(
                        "**Co poszło dobrze:**"
                    )
                    st.write(strengths)

                if improvements:
                    st.markdown(
                        "**Co poprawić:**"
                    )
                    st.write(improvements)

                if next_steps:
                    st.markdown(
                        "**Kolejne kroki:**"
                    )
                    st.write(next_steps)

                st.caption(
                    f"Ostatnia aktualizacja: {updated_at}"
                )
    else:
        st.info(
            "Nie zapisano jeszcze feedbacku dla tej aplikacji."
        )
    st.divider()
    st.subheader("📝 Notatki przed rozmową")

    interview_notes = st.text_area(
        "Najważniejsze informacje, które chcesz zapamiętać",
        value=saved_prep.get(
            "interview_notes",
            ""
        ),
        height=200,
        key=f"interview_notes_{application_id}",
    )

    if st.button(
        "💾 Zapisz notatki",
        key=f"save_interview_notes_{application_id}"
    ):
        save_interview_prep_item(
            username,
            application_id,
            "interview_notes",
            interview_notes
        )

        st.success(
            "Notatki zostały zapisane."
        )
