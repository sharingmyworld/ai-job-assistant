import streamlit as st

from core.analyzer import analyze_cv
from core.cv_reader import read_pdf

from ats_checker import check_ats
from ats_report import generate_ats_report
from cv_improver import generate_suggestions

from database import (
    save_analysis,
    add_skills_to_learning_plan
)
from job_title_detector import detect_job_title

from charts import (
    show_skill_chart,
    show_found_skills_chart
)

from report_generator import generate_report


def show_analysis():
    st.header("📄 Analiza CV")

    st.write(
        "Porównaj swoje CV z ofertą pracy i sprawdź dopasowanie."
    )

    if "detected_job_title" not in st.session_state:
        st.session_state.detected_job_title = ""

    job_offer = st.text_area(
        "📄 Wklej ofertę pracy",
        height=250,
        key="analysis_job_offer"
    )

    if st.button(
        "✨ Wykryj stanowisko",
        key="detect_job_title_button"
    ):
        detected_title = detect_job_title(
            job_offer
        )

        st.session_state.detected_job_title = (
            detected_title
        )

        if detected_title:
            st.success(
                f"Wykryto stanowisko: {detected_title}"
            )
        else:
            st.info(
                "Nie udało się pewnie wykryć stanowiska. "
                "Wpisz je ręcznie."
            )

    job_title = st.text_input(
        "💼 Nazwa stanowiska lub firmy",
        value=st.session_state.detected_job_title,
        placeholder="np. Junior Python Developer — ABC Tech",
        key="analysis_job_title"
    )

    uploaded_file = st.file_uploader(
        "📄 Wybierz CV (PDF)",
        type=["pdf"],
        key="analysis_cv_uploader"
    )

    analyze = st.button(
        "🔍 Analizuj CV",
        key="analyze_cv_button"
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

        final_job_title = job_title.strip()

        if not final_job_title:
            final_job_title = detect_job_title(
                job_offer
            )

        if not final_job_title:
            final_job_title = (
                "Bez nazwy stanowiska"
            )

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
            found,
            final_job_title,
            missing
        )

        add_skills_to_learning_plan(
            st.session_state.username,
            missing
        )

        st.session_state.analysis_done = True
        st.session_state.score = score
        st.session_state.found = found
        st.session_state.missing = missing
        st.session_state.suggestions = suggestions
        st.session_state.ats_result = ats_result
        st.session_state.ats_report = ats_report
        st.session_state.detected_job_title = (
            final_job_title
        )

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
    st.header("💡 Sugestie")

    for line in suggestions:
        st.write(line)

    st.divider()
    st.header("📋 Raport ATS")

    st.metric(
        "ATS Score",
        f"{ats_result['score']}%"
    )

    for line in ats_report:
        st.write(line)

    st.divider()
    st.header("📄 Raport PDF")

    if st.button(
        "📄 Generuj raport PDF",
        key="generate_pdf_button"
    ):
        generate_report(
            "ATS_Report.pdf",
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
            "ATS_Report.pdf",
            "rb"
        ) as file:
            st.download_button(
                "📥 Pobierz raport PDF",
                data=file,
                file_name="ATS_Report.pdf",
                mime="application/pdf",
                key="download_pdf_button"
            )
    except FileNotFoundError:
        st.info(
            "Najpierw wygeneruj raport PDF."
        )
