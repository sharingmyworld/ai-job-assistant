import streamlit as st
import pandas as pd

from answer_evaluator import evaluate_answer

from database import (
    get_job_applications,
    get_mock_interview_answers,
    save_mock_interview_answer,
    reset_mock_interview
)


QUESTION_BANK = {
    "python": [
        "Wyjaśnij różnicę między listą a krotką w Pythonie.",
        "Jak działa obsługa wyjątków w Pythonie?",
        "Jak przetestowałbyś funkcję przetwarzającą dane?"
    ],
    "sql": [
        "Jaka jest różnica między WHERE a HAVING?",
        "Wyjaśnij różnicę między INNER JOIN i LEFT JOIN.",
        "Jak podszedłbyś do optymalizacji wolnego zapytania?"
    ],
    "data": [
        "Jak sprawdzasz jakość danych przed analizą?",
        "Jak radzisz sobie z brakującymi wartościami?",
        "Jak prezentujesz wynik analizy osobie nietechnicznej?"
    ],
    "backend": [
        "Jak zaprojektowałbyś REST API?",
        "Jak obsłużyć walidację i błędy w API?",
        "Jak diagnozujesz problem z wydajnością backendu?"
    ],
    "default": [
        "Opowiedz o projekcie, z którego jesteś najbardziej dumny.",
        "Opisz trudny problem i sposób jego rozwiązania.",
        "Dlaczego interesuje Cię to stanowisko?"
    ]
}


def _get_questions(position):
    position_lower = str(position).lower()
    questions = []

    groups = {
        "python": ["python", "django", "flask"],
        "sql": ["sql", "database", "analityk", "analyst"],
        "data": ["data", "analityk", "analyst", "power bi"],
        "backend": ["backend", "back-end", "api"]
    }

    for group, keywords in groups.items():
        if any(
            keyword in position_lower
            for keyword in keywords
        ):
            questions.extend(
                QUESTION_BANK[group]
            )

    if not questions:
        questions.extend(
            QUESTION_BANK["default"]
        )

    questions.extend(
        [
            "Opowiedz krótko o sobie.",
            "Jakie są Twoje mocne strony?",
            "Nad czym obecnie pracujesz rozwojowo?"
        ]
    )

    return list(dict.fromkeys(questions))[:8]


def show_mock_interview():
    st.header("🎭 Mock Interview")

    st.write(
        "Odpowiadaj na pytania jedno po drugim. "
        "Sesja zapisuje się w bazie."
    )

    applications = get_job_applications(
        st.session_state.username
    )

    if not applications:
        st.info(
            "Brak aplikacji w trackerze."
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
            "Wersja CV"
        ]
    )

    df["Etykieta"] = (
        df["Stanowisko"]
        + " — "
        + df["Firma"]
    )

    selected_label = st.selectbox(
        "Wybierz aplikację",
        df["Etykieta"].tolist(),
        key="mock_application"
    )

    selected = df[
        df["Etykieta"] == selected_label
    ].iloc[0]

    application_id = int(
        selected["ID"]
    )

    username = st.session_state.username
    position = selected["Stanowisko"]

    questions = _get_questions(
        position
    )

    saved_answers = get_mock_interview_answers(
        username,
        application_id
    )

    answered_count = sum(
        1
        for item in saved_answers.values()
        if item["answer"].strip()
    )

    current_question = min(
        answered_count,
        len(questions) - 1
    )

    st.subheader(
        f"💼 {position} — {selected['Firma']}"
    )

    progress = (
        answered_count / len(questions)
        if questions
        else 0
    )

    st.progress(progress)

    st.caption(
        f"Postęp sesji: "
        f"{answered_count}/{len(questions)}"
    )

    if answered_count < len(questions):
        question_number = current_question + 1
        question = questions[current_question]

        st.markdown(
            f"### Pytanie {question_number}"
        )

        st.info(question)

        saved_answer = saved_answers.get(
            question_number,
            {}
        ).get(
            "answer",
            ""
        )

        answer = st.text_area(
            "Twoja odpowiedź",
            value=saved_answer,
            height=220,
            key=(
                f"mock_answer_"
                f"{application_id}_"
                f"{question_number}"
            )
        )

        if st.button(
            "➡️ Zapisz i przejdź dalej",
            key=(
                f"save_mock_"
                f"{application_id}_"
                f"{question_number}"
            )
        ):
            if not answer.strip():
                st.warning(
                    "Wpisz odpowiedź."
                )
            else:
                score, feedback = evaluate_answer(
                    question,
                    answer
                )

                save_mock_interview_answer(
                    username,
                    application_id,
                    question_number,
                    question,
                    answer,
                    score,
                    feedback
                )

                st.session_state[
                    f"mock_feedback_{application_id}"
                ] = feedback

                st.rerun()
    else:
        st.success(
            "🎉 Sesja Mock Interview ukończona!"
        )

    if saved_answers:
        st.divider()
        st.subheader("📊 Wynik sesji")

        scores = [
            item["score"]
            for item in saved_answers.values()
            if item["answer"].strip()
        ]

        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric(
                "Średnia ocena",
                f"{average_score:.1f}/5"
            )

        with metric2:
            st.metric(
                "Odpowiedzi",
                f"{answered_count}/{len(questions)}"
            )

        if average_score < 2.5:
            st.warning(
                "Odpowiedzi są krótkie lub mało konkretne. "
                "Dodawaj przykłady i rezultaty."
            )
        elif average_score < 4:
            st.info(
                "Przygotowanie wygląda dobrze. "
                "Warto dopracować konkretne przykłady."
            )
        else:
            st.success(
                "Odpowiedzi są rozbudowane i konkretne."
            )

        with st.expander(
            "📚 Zobacz zapisane odpowiedzi"
        ):
            for number, item in sorted(
                saved_answers.items()
            ):
                st.markdown(
                    f"**{number}. {item['question']}**"
                )

                st.write(
                    item["answer"]
                )

                st.caption(
                    f"Ocena odpowiedzi: "
                    f"{item['score']}/5"
                )

                if item.get("feedback"):
                    st.info(
                        item["feedback"]
                    )

                st.divider()

    if st.button(
        "🔄 Rozpocznij sesję od nowa",
        key=f"reset_mock_{application_id}"
    ):
        reset_mock_interview(
            username,
            application_id
        )

        st.rerun()
