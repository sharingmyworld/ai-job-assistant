import streamlit as st

from cv_reader import read_pdf
from analyzer import analyze_cv
from database import create_database, save_analysis, get_history
from cv_improver import generate_suggestions
from cv_generator import generate_cv_improvements


create_database()


st.set_page_config(
    page_title="AI Job Assistant",
    layout="wide"
)


st.title("AI Job Assistant")

st.write(
    "Sprawdź dopasowanie CV do oferty pracy i otrzymaj propozycje ulepszeń."
)


uploaded_file = st.file_uploader(
    "Wgraj CV (PDF)",
    type=["pdf"]
)


job_offer = st.text_area(
    "Wklej treść oferty pracy",
    height=250
)


if st.button("Analizuj CV"):

    if uploaded_file is None:

        st.warning("Najpierw wgraj CV.")

    elif job_offer.strip() == "":

        st.warning("Wklej ofertę pracy.")

    else:

        with open("uploaded_cv.pdf", "wb") as file:

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


        st.success(
            f"Dopasowanie CV: {score:.0f}%"
        )


        st.divider()


        st.subheader("Znalezione umiejętności")

        if found:

            for skill in found:
                st.write(f"- {skill}")

        else:

            st.write(
                "Nie znaleziono wymaganych umiejętności."
            )


        st.divider()


        st.subheader("Brakujące umiejętności")


        if missing:

            for skill in missing:
                st.write(f"- {skill}")

        else:

            st.write(
                "Brak brakujących umiejętności."
            )


        st.divider()


        st.subheader("Sugestie poprawy CV")


        suggestions = generate_suggestions(
            found,
            missing
        )


        for suggestion in suggestions:

            st.write(
                suggestion
            )


        st.divider()


        st.subheader("Generator ulepszenia CV")


        improvements = generate_cv_improvements(
            found,
            missing
        )


        for item in improvements:

            st.write(
                item
            )


        save_analysis(
            score,
            found
        )


st.divider()


st.subheader("Historia analiz")


history = get_history()


if history:

    for row in reversed(history):

        st.write(
            f"Data: {row[1]} | Wynik: {row[2]:.0f}% | Umiejętności: {row[3]}"
        )

else:

    st.info(
        "Brak zapisanych analiz."
    )