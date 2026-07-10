import pandas as pd
import streamlit as st


def show_skill_chart(found, missing):

    data = {
        "Status": [
            "Znalezione",
            "Brakujące"
        ],
        "Liczba": [
            len(found),
            len(missing)
        ]
    }


    df = pd.DataFrame(data)


    st.subheader(
        "📊 Porównanie umiejętności"
    )


    st.bar_chart(
        df.set_index("Status")
    )



def show_found_skills_chart(found):

    if not found:
        return


    data = {
        "Umiejętność": found,
        "Wystąpienie": [1] * len(found)
    }


    df = pd.DataFrame(data)


    st.subheader(
        "✅ Znalezione kompetencje"
    )


    st.bar_chart(
        df.set_index("Umiejętność")
    )