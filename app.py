import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)


import streamlit as st

from core.cv_reader import read_pdf
from core.analyzer import analyze_cv
from database import create_database, save_analysis, get_history
from cv_improver import generate_suggestions
from cv_generator import generate_cv_improvements
from charts import show_skill_chart, show_found_skills_chart
from report_generator import generate_report

create_database()


st.set_page_config(
    page_title="AI Job Assistant",
    layout="wide"
)


st.title("🤖 AI Job Assistant")
st.write(
    "Analiza dopasowania CV do oferty pracy."
)


uploaded_file = st.file_uploader(
    "📄 Wgraj CV PDF",
    type=["pdf"]
)


job_offer = st.text_area(
    "💼 Wklej ofertę pracy",
    height=250
)


if st.button("🔍 Analizuj CV"):

    if uploaded_file is None:

        st.warning(
            "Najpierw wgraj CV."
        )

    elif not job_offer.strip():

        st.warning(
            "Wklej ofertę pracy."
        )

    else:

        with open(
            "uploaded_cv.pdf",
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )


        cv_text = read_pdf(
            "uploaded_cv.pdf"
        )


        score, found, missing = analyze_cv(
            cv_text,
            job_offer
        )


        st.divider()

        st.header(
            "📊 Wynik analizy"
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


        st.divider()


        show_skill_chart(
            found,
            missing
        )


        show_found_skills_chart(
            found
        )


        st.divider()


        st.subheader(
            "✅ Znalezione umiejętności"
        )


        if found:

            for skill in found:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "Brak znalezionych umiejętności."
            )


        st.subheader(
            "❌ Brakujące umiejętności"
        )


        if missing:

            for skill in missing:

                st.write(
                    f"• {skill}"
                )

        else:

            st.success(
                "Brak brakujących umiejętności."
            )


        st.divider()


        st.subheader(
            "💡 Sugestie poprawy CV"
        )


        suggestions = generate_suggestions(
            found,
            missing
        )
        for suggestion in suggestions:
            st.write(
                suggestion
            )
        suggestion
    

