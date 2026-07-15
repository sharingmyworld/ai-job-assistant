import json
from datetime import datetime

import streamlit as st

from database import (
    delete_user_account,
    export_user_data,
    get_statistics,
)
from auth import change_password, login_user


def show_profile():
    username = st.session_state.username

    stats = get_statistics(username)

    count = stats[0] or 0
    average = stats[1] or 0
    best = stats[2] or 0

    st.header("👤 Profil")

    st.write(f"**Login:** {username}")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Analizy", count)

    with col2:
        st.metric(
            "Średni wynik",
            f"{average:.1f}%"
        )

    with col3:
        st.metric(
            "Najlepszy wynik",
            f"{best:.1f}%"
        )

    st.divider()
    st.subheader("📦 Eksport danych")

    st.write(
        "Pobierz swoje analizy, plan nauki, aplikacje "
        "oraz dane przygotowania do rozmów w jednym pliku JSON."
    )

    try:
        export_payload = export_user_data(
            username
        )

        export_json = json.dumps(
            export_payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

        export_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

        st.download_button(
            "⬇️ Eksportuj moje dane",
            data=export_json,
            file_name=(
                f"ai_job_assistant_"
                f"{username}_{export_date}.json"
            ),
            mime="application/json",
            key="download_user_data",
        )

        total_records = sum(
            len(records)
            for records in export_payload[
                "data"
            ].values()
        )

        st.caption(
            f"Eksport obejmuje {total_records} rekordów."
        )
    except Exception:
        st.error(
            "Nie udało się przygotować eksportu danych."
        )

    st.divider()
    st.subheader("🔒 Zmień hasło")

    current_password = st.text_input(
        "Obecne hasło",
        type="password",
        key="current_password"
    )

    new_password = st.text_input(
        "Nowe hasło",
        type="password",
        key="new_password"
    )

    repeat_password = st.text_input(
        "Powtórz nowe hasło",
        type="password",
        key="repeat_password"
    )

    if st.button(
        "Zmień hasło",
        key="change_password_button"
    ):
        if len(new_password) < 8:
            st.warning(
                "Nowe hasło musi mieć co najmniej 8 znaków."
            )
        elif new_password != repeat_password:
            st.warning(
                "Nowe hasła nie są takie same."
            )
        else:
            success, message = change_password(
                username,
                current_password,
                new_password
            )

            if success:
                st.success(message)
            else:
                st.error(message)


    st.divider()
    st.subheader("⚠️ Strefa niebezpieczna")

    st.warning(
        "Usunięcie konta jest trwałe. Zostaną usunięte "
        "analizy CV, plan nauki, aplikacje oraz dane rozmów."
    )

    confirm_delete = st.checkbox(
        "Rozumiem, że tej operacji nie można cofnąć.",
        key="confirm_account_delete",
    )

    delete_password = st.text_input(
        "Potwierdź hasłem",
        type="password",
        key="delete_account_password",
    )

    delete_phrase = st.text_input(
        "Wpisz USUŃ KONTO",
        key="delete_account_phrase",
    )

    if st.button(
        "🗑️ Usuń konto i wszystkie dane",
        type="primary",
        key="delete_account_button",
    ):
        if not confirm_delete:
            st.warning(
                "Potwierdź, że rozumiesz skutki usunięcia konta."
            )
        elif delete_phrase.strip() != "USUŃ KONTO":
            st.warning("Wpisz dokładnie: USUŃ KONTO")
        elif not login_user(username, delete_password):
            st.error("Nieprawidłowe hasło.")
        else:
            try:
                delete_user_account(username)

                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.analysis_done = False
                st.session_state.score = 0
                st.session_state.found = []
                st.session_state.missing = []
                st.session_state.suggestions = []
                st.session_state.ats_result = {}
                st.session_state.ats_report = []
                st.session_state.cv_text = ""
                st.session_state.job_offer = ""
                st.session_state.account_deleted = True
                st.rerun()
            except Exception:
                st.error(
                    "Nie udało się usunąć konta. "
                    "Spróbuj ponownie później."
                )
