import streamlit as st

from database import get_statistics
from auth import change_password


def show_profile():

    stats = get_statistics(
        st.session_state.username
    )

    count = stats[0] or 0
    average = stats[1] or 0
    best = stats[2] or 0

    st.header("👤 Profil")

    st.write(f"**Login:** {st.session_state.username}")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Analizy", count)

    with col2:
        st.metric("Średni wynik", f"{average:.1f}%")

    with col3:
        st.metric("Najlepszy wynik", f"{best:.1f}%")

    st.divider()

    st.divider()

    st.subheader(
        "🔒 Zmień hasło"
    )

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
        "Zmień hasło"
    ):

        if len(new_password) < 4:

            st.warning(
                "Nowe hasło musi mieć co najmniej 4 znaki."
            )

        elif new_password != repeat_password:

            st.warning(
                "Nowe hasła nie są takie same."
            )

        else:

            success, message = change_password(
                st.session_state.username,
                current_password,
                new_password
            )

            if success:

                st.success(
                    message
                )

            else:

                st.error(
                    message
                )