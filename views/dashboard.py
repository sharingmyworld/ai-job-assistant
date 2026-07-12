import streamlit as st

from database import get_statistics


def show_dashboard():

    stats = get_statistics(
        st.session_state.username
    )

    count = stats[0] or 0
    average = stats[1] or 0
    best = stats[2] or 0

    st.header(
        f"👋 Witaj {st.session_state.username}"
    )

    st.write(
        "Tutaj możesz śledzić swoje postępy."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Liczba analiz",
            count
        )

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