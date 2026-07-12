import streamlit as st

from core.analyzer import analyze_cv
from core.cv_reader import read_pdf

from ats_checker import check_ats
from ats_report import generate_ats_report
from cv_improver import generate_suggestions

from database import save_analysis

from charts import create_chart
from report_generator import generate_report


def show_analysis():

    st.header("📄 Analiza CV")

    st.write(
        "Porównaj swoje CV z ofertą pracy i sprawdź dopasowanie."
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

            return

        if not job_offer.strip():

            st.warning(
                "Wklej ofertę pracy."
            )

            return

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

        st.session_state.score = score
        st.session_state.found = found
        st.session_state.missing = missing

        st.session_state.suggestions = suggestions

        st.session_state.ats_result = ats_result
        st.session_state.ats_report = ats_report

    if not st.session_state.analysis_done:

        return

    score = st.session_state.score
    found = st.session_state.found
    missing = st.session_state.missing

    suggestions = st.session_state.suggestions

    ats_result = st.session_state.ats_result
    ats_report = st.session_state.ats_report
        st.divider()

    st.header("📊 Wynik analizy")

    st.metric(
        "Dopasowanie",
        f"{score:.1f}%"
    )

    chart = create_chart(
        score
    )

    st.pyplot(chart)

    st.subheader(
        "✅ Znalezione umiejętności"
    )

    if found:

        for skill in found:

            st.success(skill)

    else:

        st.warning(
            "Nie znaleziono pasujących umiejętności."
        )

    st.subheader(
        "❌ Brakujące umiejętności"
    )

    if missing:

        for skill in missing:

            st.error(skill)

    else:

        st.success(
            "Brak brakujących umiejętności."
        )

    st.divider()

    st.header(
        "💡 Sugestie"
    )

    for line in suggestions:

        st.write(line)

    st.divider()

    st.header(
        "📋 Raport ATS"
    )

    st.metric(
        "ATS Score",
        f"{ats_result['score']}%"
    )

    for line in ats_report:

        st.write(line)

    st.divider()

    st.header(
        "📄 Raport PDF"
    )

    generate_report(
        "ATS_Report.pdf",
        score,
        found,
        missing,
        suggestions
    )

    with open(
        "ATS_Report.pdf",
        "rb"
    ) as file:

        st.download_button(

            "📥 Pobierz raport PDF",

            data=file,

            file_name="ATS_Report.pdf",

            mime="application/pdf"

        )