import streamlit as st
import pandas as pd
from datetime import date

from database import (
    add_job_application,
    get_job_applications,
    update_job_application_status,
    update_job_application_notes,
    delete_job_application
)


STATUSES = [
    "Planowana",
    "Wysłana",
    "Rozmowa HR",
    "Rozmowa techniczna",
    "Oferta",
    "Odrzucona",
    "Wycofana"
]


def show_applications():
    st.header("📨 Tracker aplikacji")

    st.write(
        "Zapisuj firmy, stanowiska i etapy procesu rekrutacyjnego."
    )

    with st.expander(
        "➕ Dodaj aplikację",
        expanded=False
    ):
        col1, col2 = st.columns(2)

        with col1:
            company = st.text_input(
                "Firma",
                key="application_company"
            )

            position = st.text_input(
                "Stanowisko",
                key="application_position"
            )

        with col2:
            status = st.selectbox(
                "Status",
                STATUSES,
                key="application_status"
            )

            application_date = st.date_input(
                "Data aplikacji",
                value=date.today(),
                key="application_date"
            )

        job_url = st.text_input(
            "Link do oferty",
            placeholder="https://...",
            key="application_url"
        )

        notes = st.text_area(
            "Notatki",
            placeholder=(
                "Kontakt do rekrutera, termin rozmowy, "
                "ważne informacje..."
            ),
            key="application_notes"
        )

        if st.button(
            "💾 Zapisz aplikację",
            key="save_application"
        ):
            if not company.strip():
                st.warning("Podaj nazwę firmy.")
            elif not position.strip():
                st.warning("Podaj nazwę stanowiska.")
            else:
                add_job_application(
                    st.session_state.username,
                    company,
                    position,
                    status,
                    application_date.isoformat(),
                    job_url,
                    notes
                )

                st.success(
                    "Aplikacja została zapisana."
                )
                st.rerun()

    applications = get_job_applications(
        st.session_state.username
    )

    if not applications:
        st.info(
            "Nie masz jeszcze zapisanych aplikacji."
        )
        return

    df = pd.DataFrame(
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
            "Dopasowanie"
        ]
    )

    st.divider()
    st.subheader("📊 Podsumowanie")

    total = len(df)
    sent = int(
        df["Status"].isin(
            [
                "Wysłana",
                "Rozmowa HR",
                "Rozmowa techniczna",
                "Oferta",
                "Odrzucona"
            ]
        ).sum()
    )
    interviews = int(
        df["Status"].isin(
            [
                "Rozmowa HR",
                "Rozmowa techniczna"
            ]
        ).sum()
    )
    offers = int(
        (df["Status"] == "Oferta").sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Wszystkie", total)

    with col2:
        st.metric("Wysłane", sent)

    with col3:
        st.metric("Rozmowy", interviews)

    with col4:
        st.metric("Oferty", offers)

    status_counts = (
        df["Status"]
        .value_counts()
        .reindex(STATUSES, fill_value=0)
    )

    st.bar_chart(status_counts)

    st.divider()
    st.subheader("🔎 Filtrowanie")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        search_text = st.text_input(
            "Szukaj firmy lub stanowiska",
            key="applications_search"
        )

    with filter_col2:
        selected_status = st.selectbox(
            "Filtr statusu",
            ["Wszystkie"] + STATUSES,
            key="applications_status_filter"
        )

    filtered_df = df.copy()

    if search_text.strip():
        query = search_text.strip()

        company_match = (
            filtered_df["Firma"]
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        )

        position_match = (
            filtered_df["Stanowisko"]
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        )

        filtered_df = filtered_df[
            company_match | position_match
        ]

    if selected_status != "Wszystkie":
        filtered_df = filtered_df[
            filtered_df["Status"] == selected_status
        ]

    st.write(
        f"Znaleziono aplikacji: {len(filtered_df)}"
    )

    if filtered_df.empty:
        st.info(
            "Brak aplikacji spełniających wybrane kryteria."
        )
        return

    st.divider()

    for _, row in filtered_df.iterrows():
        application_id = int(row["ID"])

        with st.container(border=True):
            header_col, delete_col = st.columns([9, 1])

            with header_col:
                st.subheader(
                    f"💼 {row['Stanowisko']} — {row['Firma']}"
                )

                st.caption(
                    f"Data aplikacji: {row['Data aplikacji']}"
                )

                if pd.notna(row["Dopasowanie"]):
                    st.write(
                        f"📊 Dopasowanie CV: "
                        f"{row['Dopasowanie']:.1f}%"
                    )

            with delete_col:
                if st.button(
                    "🗑",
                    key=f"delete_application_{application_id}"
                ):
                    delete_job_application(
                        application_id
                    )
                    st.rerun()

            current_status = row["Status"]

            new_status = st.selectbox(
                "Status procesu",
                STATUSES,
                index=STATUSES.index(
                    current_status
                ),
                key=f"application_status_{application_id}"
            )

            if new_status != current_status:
                update_job_application_status(
                    application_id,
                    new_status
                )
                st.rerun()

            if row["Link"]:
                st.link_button(
                    "🔗 Otwórz ofertę",
                    row["Link"]
                )

            updated_notes = st.text_area(
                "Notatki",
                value=row["Notatki"] or "",
                key=f"application_notes_{application_id}"
            )

            if st.button(
                "💾 Zapisz notatki",
                key=f"save_notes_{application_id}"
            ):
                update_job_application_notes(
                    application_id,
                    updated_notes
                )

                st.success(
                    "Notatki zostały zapisane."
                )
                st.rerun()
