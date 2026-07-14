import streamlit as st
import pandas as pd
from datetime import date

from followup_assistant import (
    should_suggest_followup,
    generate_followup_message
)

from database import (
    add_job_application,
    get_job_applications,
    update_job_application_status,
    update_job_application_notes,
    update_job_application_event,
    update_job_application,
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
            "Dopasowanie",
            "Termin wydarzenia",
            "Typ wydarzenia",
            "Wersja CV"
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
    st.subheader("📈 Skuteczność aplikacji")

    active_df = df[
        ~df["Status"].isin(
            [
                "Planowana",
                "Wycofana"
            ]
        )
    ]

    active_count = len(active_df)

    response_count = int(
        active_df["Status"].isin(
            [
                "Rozmowa HR",
                "Rozmowa techniczna",
                "Oferta"
            ]
        ).sum()
    )

    interview_count = int(
        active_df["Status"].isin(
            [
                "Rozmowa HR",
                "Rozmowa techniczna",
                "Oferta"
            ]
        ).sum()
    )

    offer_count = int(
        (active_df["Status"] == "Oferta").sum()
    )

    rejection_count = int(
        (active_df["Status"] == "Odrzucona").sum()
    )

    response_rate = (
        response_count / active_count * 100
        if active_count
        else 0
    )

    interview_rate = (
        interview_count / active_count * 100
        if active_count
        else 0
    )

    offer_rate = (
        offer_count / active_count * 100
        if active_count
        else 0
    )

    rejection_rate = (
        rejection_count / active_count * 100
        if active_count
        else 0
    )

    rate1, rate2, rate3, rate4 = st.columns(4)

    with rate1:
        st.metric(
            "Odpowiedzi",
            f"{response_rate:.1f}%"
        )

    with rate2:
        st.metric(
            "Rozmowy",
            f"{interview_rate:.1f}%"
        )

    with rate3:
        st.metric(
            "Oferty",
            f"{offer_rate:.1f}%"
        )

    with rate4:
        st.metric(
            "Odrzucenia",
            f"{rejection_rate:.1f}%"
        )

    scored_df = active_df[
        active_df["Dopasowanie"].notna()
    ].copy()

    if not scored_df.empty:
        st.markdown(
            "#### 🎯 Dopasowanie CV a wynik rekrutacji"
        )

        interview_df = scored_df[
            scored_df["Status"].isin(
                [
                    "Rozmowa HR",
                    "Rozmowa techniczna",
                    "Oferta"
                ]
            )
        ]

        no_interview_df = scored_df[
            scored_df["Status"].isin(
                [
                    "Wysłana",
                    "Odrzucona"
                ]
            )
        ]

        avg_all_score = (
            scored_df["Dopasowanie"].mean()
        )

        avg_interview_score = (
            interview_df["Dopasowanie"].mean()
            if not interview_df.empty
            else None
        )

        avg_no_interview_score = (
            no_interview_df["Dopasowanie"].mean()
            if not no_interview_df.empty
            else None
        )

        score1, score2, score3 = st.columns(3)

        with score1:
            st.metric(
                "Średnie dopasowanie",
                f"{avg_all_score:.1f}%"
            )

        with score2:
            st.metric(
                "Średnie przy rozmowie",
                (
                    f"{avg_interview_score:.1f}%"
                    if avg_interview_score is not None
                    else "Brak danych"
                )
            )

        with score3:
            st.metric(
                "Średnie bez rozmowy",
                (
                    f"{avg_no_interview_score:.1f}%"
                    if avg_no_interview_score is not None
                    else "Brak danych"
                )
            )

        score_chart_df = (
            scored_df[
                [
                    "Stanowisko",
                    "Firma",
                    "Dopasowanie"
                ]
            ]
            .copy()
        )

        score_chart_df["Aplikacja"] = (
            score_chart_df["Stanowisko"]
            + " — "
            + score_chart_df["Firma"]
        )

        st.bar_chart(
            score_chart_df.set_index(
                "Aplikacja"
            )["Dopasowanie"]
        )

        if (
            avg_interview_score is not None
            and avg_no_interview_score is not None
        ):
            difference = (
                avg_interview_score
                - avg_no_interview_score
            )

            if difference > 0:
                st.success(
                    f"Aplikacje zakończone rozmową mają "
                    f"średnio o {difference:.1f} p.p. "
                    f"wyższe dopasowanie CV."
                )
            elif difference < 0:
                st.info(
                    "Na obecnych danych wyższe dopasowanie "
                    "CV nie przekłada się jeszcze na więcej rozmów."
                )
            else:
                st.info(
                    "Średnie dopasowanie jest obecnie takie samo."
                )
    else:
        st.info(
            "Brak wystarczających danych o dopasowaniu CV. "
            "Dodawaj oferty do trackera bezpośrednio z analizy CV."
        )

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

                if row["Wersja CV"]:
                    st.write(
                        f"🗂️ Wersja CV: {row['Wersja CV']}"
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

            with st.expander(
                "✏️ Edytuj aplikację"
            ):
                edit_company = st.text_input(
                    "Firma",
                    value=row["Firma"],
                    key=f"edit_company_{application_id}"
                )

                edit_position = st.text_input(
                    "Stanowisko",
                    value=row["Stanowisko"],
                    key=f"edit_position_{application_id}"
                )

                parsed_application_date = pd.to_datetime(
                    row["Data aplikacji"],
                    errors="coerce"
                )

                edit_application_date = st.date_input(
                    "Data aplikacji",
                    value=(
                        parsed_application_date.date()
                        if pd.notna(parsed_application_date)
                        else date.today()
                    ),
                    key=f"edit_date_{application_id}"
                )

                edit_job_url = st.text_input(
                    "Link do oferty",
                    value=row["Link"] or "",
                    key=f"edit_url_{application_id}"
                )

                current_match_score = (
                    float(row["Dopasowanie"])
                    if pd.notna(row["Dopasowanie"])
                    else 0.0
                )

                edit_match_score = st.number_input(
                    "Dopasowanie CV (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=current_match_score,
                    step=1.0,
                    key=f"edit_match_score_{application_id}"
                )

                if st.button(
                    "💾 Zapisz zmiany",
                    key=f"save_edit_{application_id}"
                ):
                    if not edit_company.strip():
                        st.warning(
                            "Podaj nazwę firmy."
                        )
                    elif not edit_position.strip():
                        st.warning(
                            "Podaj nazwę stanowiska."
                        )
                    else:
                        update_job_application(
                            application_id,
                            edit_company,
                            edit_position,
                            edit_application_date.isoformat(),
                            edit_job_url,
                            edit_match_score
                        )

                        st.success(
                            "Aplikacja została zaktualizowana."
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

            if should_suggest_followup(
                row["Data aplikacji"],
                row["Status"]
            ):
                st.warning(
                    "⏰ Od wysłania aplikacji minęło "
                    "co najmniej 7 dni. Warto wysłać follow-up."
                )

                with st.expander(
                    "✉️ Generuj wiadomość follow-up"
                ):
                    followup_language = st.selectbox(
                        "Język wiadomości",
                        ["Polski", "English"],
                        key=f"followup_language_{application_id}"
                    )

                    followup_message = generate_followup_message(
                        row["Firma"],
                        row["Stanowisko"],
                        followup_language
                    )

                    st.text_area(
                        "Gotowa wiadomość",
                        value=followup_message,
                        height=260,
                        key=f"followup_message_{application_id}"
                    )

            event_col1, event_col2 = st.columns(2)

            with event_col1:
                current_event_date = (
                    pd.to_datetime(
                        row["Termin wydarzenia"],
                        errors="coerce"
                    )
                )

                default_event_date = (
                    current_event_date.date()
                    if pd.notna(current_event_date)
                    else date.today()
                )

                event_date = st.date_input(
                    "Termin kolejnego działania",
                    value=default_event_date,
                    key=f"event_date_{application_id}"
                )

            with event_col2:
                event_types = [
                    "Brak",
                    "Follow-up",
                    "Rozmowa HR",
                    "Rozmowa techniczna",
                    "Zadanie rekrutacyjne",
                    "Decyzja",
                    "Inne"
                ]

                current_event_type = (
                    row["Typ wydarzenia"]
                    if row["Typ wydarzenia"] in event_types
                    else "Brak"
                )

                event_type = st.selectbox(
                    "Typ wydarzenia",
                    event_types,
                    index=event_types.index(
                        current_event_type
                    ),
                    key=f"event_type_{application_id}"
                )

            if st.button(
                "📅 Zapisz termin",
                key=f"save_event_{application_id}"
            ):
                saved_date = (
                    ""
                    if event_type == "Brak"
                    else event_date.isoformat()
                )

                saved_type = (
                    ""
                    if event_type == "Brak"
                    else event_type
                )

                update_job_application_event(
                    application_id,
                    saved_date,
                    saved_type
                )

                st.success(
                    "Termin został zapisany."
                )
                st.rerun()

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
