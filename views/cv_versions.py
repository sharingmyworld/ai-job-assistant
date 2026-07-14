import streamlit as st
import pandas as pd

from database import (
    get_history_with_title,
    get_job_applications
)


def show_cv_versions():
    st.header("🗂️ Wersje CV")

    history = get_history_with_title(
        st.session_state.username
    )

    applications = get_job_applications(
        st.session_state.username
    )

    if not history:
        st.info(
            "Brak analiz z zapisanymi wersjami CV."
        )
        return

    history_df = pd.DataFrame(
        history,
        columns=[
            "ID",
            "Data",
            "Wynik",
            "Umiejętności",
            "Stanowisko",
            "Brakujące",
            "Wersja CV"
        ]
    )

    history_df["Wersja CV"] = (
        history_df["Wersja CV"]
        .fillna("")
        .replace("", "Bez nazwy wersji")
    )

    summary = (
        history_df.groupby("Wersja CV")
        .agg(
            Średnie_dopasowanie=("Wynik", "mean"),
            Najlepszy_wynik=("Wynik", "max"),
            Liczba_analiz=("ID", "count")
        )
        .reset_index()
        .sort_values(
            "Średnie_dopasowanie",
            ascending=False
        )
    )

    st.subheader("📊 Porównanie wersji")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    import altair as alt

    chart = (
        alt.Chart(summary)
        .mark_bar()
        .encode(
            x=alt.X(
                "Wersja CV:N",
                title="Wersja CV"
            ),
            y=alt.Y(
                "Średnie_dopasowanie:Q",
                title="Średnie dopasowanie (%)",
                scale=alt.Scale(
                    domain=[0, 100]
                )
            ),
            tooltip=[
                "Wersja CV",
                alt.Tooltip(
                    "Średnie_dopasowanie:Q",
                    title="Średnie dopasowanie",
                    format=".1f"
                ),
                alt.Tooltip(
                    "Najlepszy_wynik:Q",
                    title="Najlepszy wynik",
                    format=".1f"
                ),
                "Liczba_analiz"
            ]
        )
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

    best = summary.iloc[0]

    st.success(
        f"Najlepsza wersja: **{best['Wersja CV']}** — "
        f"średnie dopasowanie "
        f"{best['Średnie_dopasowanie']:.1f}%."
    )

    if applications:
        app_df = pd.DataFrame(
            applications,
            columns=[
                "ID",
                "Firma",
                "Stanowisko",
                "Status",
                "Data aplikacji",
                "Link",
                "Notatki",
                "Utworzono",
                "Zaktualizowano",
                "Dopasowanie",
                "Termin wydarzenia",
                "Typ wydarzenia",
                "Wersja CV"
            ]
        )

        app_df["Wersja CV"] = (
            app_df["Wersja CV"]
            .fillna("")
            .replace("", "Bez nazwy wersji")
        )

        st.divider()
        st.subheader("📨 Wyniki aplikacji według wersji CV")

        rows = []

        for version, group in app_df.groupby(
            "Wersja CV"
        ):
            active = group[
                ~group["Status"].isin(
                    ["Planowana", "Wycofana"]
                )
            ]

            interviews = active[
                active["Status"].isin(
                    [
                        "Rozmowa HR",
                        "Rozmowa techniczna",
                        "Oferta"
                    ]
                )
            ]

            offers = active[
                active["Status"] == "Oferta"
            ]

            rows.append(
                {
                    "Wersja CV": version,
                    "Aplikacje": len(active),
                    "Rozmowy": len(interviews),
                    "Oferty": len(offers),
                    "Skuteczność rozmów": (
                        len(interviews) / len(active) * 100
                        if len(active)
                        else 0
                    )
                }
            )

        result_df = pd.DataFrame(rows)

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )
