import streamlit as st
import pandas as pd


from auth import (
    create_users_table,
    register_user,
    login_user
)
from core.analyzer import analyze_cv
from core.cv_reader import read_pdf

from cv_improver import generate_suggestions
from ats_checker import check_ats
from ats_report import generate_ats_report

from database import (
    create_database,
    save_analysis,
    get_history,
    get_statistics,
    get_progress,
    delete_analysis,
    get_better_than_percentage
)

from report_generator import generate_report

from charts import (
    show_skill_chart,
    show_found_skills_chart
)

from views.profile import show_profile


st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🤖",
    layout="wide"
)


create_database()
create_users_table()


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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


st.title("🤖 AI Job Assistant")
if not st.session_state.logged_in:

    st.header("🔐 Logowanie")

    tab_login, tab_register = st.tabs(
        [
            "Logowanie",
            "Rejestracja"
        ]
    )

    with tab_login:

        username = st.text_input(
            "Login",
            key="login_username"
        )

        password = st.text_input(
            "Hasło",
            type="password",
            key="login_password"
        )

        if st.button("Zaloguj się"):

            if login_user(
                username,
                password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(
                    f"Witaj {username}!"
                )

                st.rerun()

            else:

                st.error(
                    "Nieprawidłowy login lub hasło."
                )

    with tab_register:

        new_username = st.text_input(
            "Nowy login",
            key="register_username"
        )

        new_password = st.text_input(
            "Nowe hasło",
            type="password",
            key="register_password"
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
                    new_password
                )

                if success:

                    st.success(
                        "Konto zostało utworzone. Możesz się zalogować."
                    )

                else:

                    st.error(
                        "Użytkownik o takiej nazwie już istnieje."
                    )

    st.stop()
    
    st.sidebar.title("👤 Konto")

st.sidebar.success(
    f"Zalogowany jako:\n\n{st.session_state.username}"
)

st.sidebar.divider()

page = st.sidebar.radio(

    "Menu",

    [

        "🏠 Dashboard",

        "📄 Analiza CV",

        "📚 Historia",

        "👤 Profil"

    ]

)

st.sidebar.divider()

if st.sidebar.button("🚪 Wyloguj się"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

stats = get_statistics(
    st.session_state.username
)
if page == "🏠 Dashboard":

    from views.dashboard import show_dashboard

    show_dashboard()

if page == "👤 Profil":

    from views.profile import show_profile

    show_profile()

st.write(
    "Porównaj swoje CV z ofertą pracy..."
)

job_offer = st.text_area(
    "📄 Wklej ofertę pracy",
    height=250
)


uploaded_file = st.file_uploader(
    "📄 Wybierz CV (PDF)",
    type=["pdf"]
)


analyze = st.button(
    "🔍 Analizuj CV"
)
if analyze:

    if uploaded_file is None:

        st.warning(
            "Najpierw wybierz plik PDF z CV."
        )

    elif not job_offer.strip():

        st.warning(
            "Wklej ofertę pracy."
        )

    else:

        with open(
            "uploaded_cv.pdf",
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        cv_text = read_pdf(
            "uploaded_cv.pdf"
        )

        score, found, missing = analyze_cv(
            cv_text,
            job_offer
        )

        ats_result = check_ats(
            cv_text,
            job_offer
        )

        ats_report = generate_ats_report(
            ats_result
        )

        suggestions = generate_suggestions(
            found,
            missing
        )

        save_analysis(
            st.session_state.username,
            score,
            found
)

        st.session_state.analysis_done = True
        st.session_state.cv_text = cv_text
        st.session_state.job_offer = job_offer
        st.session_state.score = score
        st.session_state.found = found
        st.session_state.missing = missing
        st.session_state.suggestions = suggestions
        st.session_state.ats_result = ats_result
        st.session_state.ats_report = ats_report
if st.session_state.analysis_done:

    score = st.session_state.score
    found = st.session_state.found
    missing = st.session_state.missing
    suggestions = st.session_state.suggestions
    ats_result = st.session_state.ats_result
    ats_report = st.session_state.ats_report

    st.divider()

    st.header(
        "📊 Wynik analizy"
    )

    better_than = get_better_than_percentage(
        st.session_state.username,
        score
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Dopasowanie",
            f"{score:.0f}%"
        )

    with col2:

        st.metric(
            "Znalezione",
            len(found)
        )

    with col3:

        st.metric(
            "Brakujące",
            len(missing)
        )

    st.progress(
        score / 100
    )

    st.subheader(
        "🏆 Porównanie z poprzednimi analizami"
    )

    if better_than > 0:

        st.success(
            f"Ten wynik jest lepszy niż "
            f"{better_than:.0f}% Twoich poprzednich analiz."
        )

    else:

        history_count = len(
            get_history(
                st.session_state.username
            )
        )

        if history_count <= 1:

            st.info(
                "To Twoja pierwsza analiza. "
                "Ranking pojawi się po wykonaniu kolejnych analiz."
            )

        else:

            st.info(
                "Ten wynik nie jest wyższy od wcześniejszych wyników."
            )

    st.divider()

    show_skill_chart(
        found,
        missing
    )

    st.divider()

    show_found_skills_chart(
        found
    )
    st.divider()

    st.subheader(
        "✅ Znalezione umiejętności"
    )

    if found:

        for skill in found:

            st.success(
                skill
            )

    else:

        st.info(
            "Nie znaleziono wymaganych umiejętności."
        )


    st.subheader(
        "❌ Brakujące umiejętności"
    )

    if missing:

        for skill in missing:

            st.error(
                skill
            )

    else:

        st.success(
            "Brak brakujących umiejętności."
        )


    st.divider()


    st.subheader(
        "💡 Sugestie poprawy CV"
    )

    for suggestion in suggestions:

        st.write(
            suggestion
        )


    st.divider()


    st.subheader(
        "🤖 Analiza ATS"
    )

    st.metric(
        "ATS Score",
        f"{ats_result['score']}%"
    )


    st.write(
        "✅ Znalezione słowa kluczowe:"
    )

    if ats_result["found_keywords"]:

        for item in ats_result["found_keywords"]:

            st.write(
                f"• {item}"
            )

    else:

        st.write(
            "Brak."
        )


    st.write(
        "❌ Brakujące słowa kluczowe:"
    )

    if ats_result["missing_keywords"]:

        for item in ats_result["missing_keywords"]:

            st.write(
                f"• {item}"
            )

    else:

        st.write(
            "Brak."
        )
        st.divider()

    st.subheader(
        "📋 Raport ATS"
    )

    for line in ats_report:

        st.write(
            line
        )

    st.divider()

    st.subheader(
        "📄 Raport PDF"
    )

    if st.button(
        "📄 Generuj raport PDF"
    ):

        pdf_file = "AI_Job_Report.pdf"

        generate_report(
            pdf_file,
            score,
            found,
            missing,
            suggestions
        )

        st.success(
            "Raport został wygenerowany."
        )

try:

    with open(
        "AI_Job_Report.pdf",
        "rb"
    ) as pdf:

        st.download_button(
            label="⬇️ Pobierz raport PDF",
            data=pdf,
            file_name="AI_Job_Report.pdf",
            mime="application/pdf"
        )

except FileNotFoundError:

    pass

st.divider()

st.header(
    "📚 Historia analiz"
)

history = get_history(
    st.session_state.username
)

if history:

    df = pd.DataFrame(

        history,

        columns=[
            "ID",
            "Data",
            "Wynik",
            "Umiejętności"
        ]

    )

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "⬇ Pobierz historię CSV",

        data=csv,

        file_name=f"{st.session_state.username}_historia.csv",

        mime="text/csv"

    )

    st.divider()

if history:

    for row in reversed(history):

        col1, col2 = st.columns([8, 1])

        with col1:

            st.write(
                f"📅 {row[1]}"
            )

            st.write(
                f"📊 Dopasowanie: {row[2]:.0f}%"
            )

            if row[3]:

                st.write(
                    f"🧩 Umiejętności: {row[3]}"
                )

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{row[0]}"
            ):

                delete_analysis(
                    row[0]
                )

                st.success(
                    "Analiza została usunięta."
                )

                st.rerun()

    st.divider()

else:

    st.info(
        "Brak zapisanych analiz."
    )