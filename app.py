import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


from streamlit_cookies_manager import (
    EncryptedCookieManager
)

from auth import (
    create_users_table,
    register_user,
    login_user,
)
from database import (
    create_database,
    create_remember_token,
    validate_remember_token,
    revoke_remember_token
)


st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🤖",
    layout="wide",
)


cookie_password = os.environ.get(
    "AI_JOB_COOKIE_PASSWORD"
)

if not cookie_password:
    st.error(
        "Brak zmiennej AI_JOB_COOKIE_PASSWORD. "
        "Ustaw bezpieczny klucz przed uruchomieniem aplikacji."
    )
    st.stop()


cookies = EncryptedCookieManager(
    prefix="ai_job_assistant/",
    password=cookie_password,
)

if not cookies.ready():
    st.stop()


@st.cache_resource
def initialize_database():
    create_database()
    create_users_table()
    return True


initialize_database()


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


if not st.session_state.logged_in:
    saved_token = cookies.get(
        "remember_token"
    )

    remembered_username = validate_remember_token(
        saved_token
    )

    if remembered_username:
        st.session_state.logged_in = True
        st.session_state.username = (
            remembered_username
        )


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

        remember_me = st.checkbox(
            "Nie wylogowuj mnie",
            key="remember_me"
        )

        if st.button("Zaloguj się"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                if remember_me:
                    remember_token = (
                        create_remember_token(
                            username,
                            days=30
                        )
                    )

                    cookies[
                        "remember_token"
                    ] = remember_token
                    cookies.save()

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
            elif len(new_password) < 8:
                st.warning(
                    "Hasło musi mieć co najmniej 8 znaków."
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
        "🗂️ Wersje CV",
        "🎤 Przygotowanie do rozmowy",
        "🎭 Mock Interview",
        "👤 Profil",
    ],
)

st.sidebar.divider()

if st.sidebar.button("🚪 Wyloguj się"):
    saved_token = cookies.get(
        "remember_token"
    )

    revoke_remember_token(
        saved_token
    )

    if "remember_token" in cookies:
        del cookies["remember_token"]
        cookies.save()

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

elif page == "🗂️ Wersje CV":
    from views.cv_versions import show_cv_versions
    show_cv_versions()

elif page == "🎤 Przygotowanie do rozmowy":
    from views.interview_prep import show_interview_prep
    show_interview_prep()

elif page == "🎭 Mock Interview":
    from views.mock_interview import show_mock_interview
    show_mock_interview()

elif page == "👤 Profil":
    from views.profile import show_profile
    show_profile()
