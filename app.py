import streamlit as st

from auth import (
    create_users_table,
    register_user,
    login_user,
)
from database import create_database


st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🤖",
    layout="wide",
)


create_database()
create_users_table()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "found" not in st.session_state:
    st.session_state.found = []

if "missing" not in st.session_state:
    st.session_state.missing = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "ats_result" not in st.session_state:
    st.session_state.ats_result = {}

if "ats_report" not in st.session_state:
    st.session_state.ats_report = []

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""

if "job_offer" not in st.session_state:
    st.session_state.job_offer = ""


st.title("🤖 AI Job Assistant")


if not st.session_state.logged_in:
    st.header("🔐 Logowanie")

    tab_login, tab_register = st.tabs(
        [
            "Logowanie",
            "Rejestracja",
        ]
    )

    with tab_login:
        username = st.text_input(
            "Login",
            key="login_username",
        )

        password = st.text_input(
            "Hasło",
            type="password",
            key="login_password",
        )

        if st.button("Zaloguj się"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(f"Witaj {username}!")
                st.rerun()
            else:
                st.error(
                    "Nieprawidłowy login lub hasło."
                )

    with tab_register:
        new_username = st.text_input(
            "Nowy login",
            key="register_username",
        )

        new_password = st.text_input(
            "Nowe hasło",
            type="password",
            key="register_password",
        )

        if st.button("Utwórz konto"):
            if len(new_username.strip()) < 3:
                st.warning(
                    "Login musi mieć co najmniej 3 znaki."
                )
            elif len(new_password) < 4:
                st.warning(
                    "Hasło musi mieć co najmniej 4 znaki."
                )
            else:
                success = register_user(
                    new_username,
                    new_password,
                )

                if success:
                    st.success(
                        "Konto zostało utworzone. "
                        "Możesz się zalogować."
                    )
                else:
                    st.error(
                        "Użytkownik o takiej nazwie "
                        "już istnieje."
                    )

    st.stop()


st.sidebar.title("👤 Konto")

st.sidebar.success(
    f"Zalogowany jako:\n\n"
    f"{st.session_state.username}"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "📄 Analiza CV",
        "📚 Historia",
        "🎯 Plan nauki",
        "📨 Aplikacje",
        "🧠 Career Insights",
        "👤 Profil",
    ],
)

st.sidebar.divider()

if st.sidebar.button("🚪 Wyloguj się"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.analysis_done = False

    st.rerun()


if page == "🏠 Dashboard":
    from views.dashboard import show_dashboard

    show_dashboard()

elif page == "📄 Analiza CV":
    from views.analysis import show_analysis

    show_analysis()

elif page == "📚 Historia":
    from views.history import show_history

    show_history()

elif page == "🎯 Plan nauki":
    from views.learning_plan import show_learning_plan

    show_learning_plan()

elif page == "📨 Aplikacje":
    from views.applications import show_applications

    show_applications()

elif page == "🧠 Career Insights":
    from views.career_insights import show_career_insights

    show_career_insights()

elif page == "👤 Profil":
    from views.profile import show_profile

    show_profile()
