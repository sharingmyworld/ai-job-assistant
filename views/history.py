import streamlit as st
import pandas as pd

from database import (
    get_history_with_title,
    delete_analysis
)


def _parse_skills(skills_text):
    if not skills_text:
        return set()

    return {
        skill.strip()
        for skill in str(skills_text).split(",")
        if skill.strip()
    }


def _format_analysis_label(row):
    date_text = (
        row["Data"].strftime("%Y-%m-%d %H:%M")
        if pd.notna(row["Data"])
        else "Brak daty"
    )

    title = (
        row["Stanowisko"].strip()
        if row["Stanowisko"]
        else "Bez nazwy"
    )

    return (
        f"#{int(row['ID'])} | {title} | "
        f"{date_text} | {row['Wynik']:.0f}%"
    )


def _show_skill_list(title, skills, empty_text, mode):
    st.markdown(f"#### {title}")

    if not skills:
        st.info(empty_text)
        return

    for skill in skills:
        if mode == "success":
            st.success(skill)
        elif mode == "error":
            st.error(skill)
        else:
            st.write(f"• {skill}")


def _show_comparison(df):
    st.subheader("⚖️ Porównaj dwie analizy")

    if len(df) < 2:
        st.info(
            "Do porównania potrzebujesz co najmniej dwóch analiz."
        )
        return

    options = {
        _format_analysis_label(row): int(row["ID"])
        for _, row in df.iterrows()
    }

    labels = list(options.keys())

    col1, col2 = st.columns(2)

    with col1:
        first_label = st.selectbox(
            "Analiza A",
            labels,
            index=1 if len(labels) > 1 else 0,
            key="history_compare_a"
        )

    with col2:
        second_label = st.selectbox(
            "Analiza B",
            labels,
            index=0,
            key="history_compare_b"
        )

    first_id = options[first_label]
    second_id = options[second_label]

    if first_id == second_id:
        st.warning("Wybierz dwie różne analizy.")
        return

    first_row = df.loc[df["ID"] == first_id].iloc[0]
    second_row = df.loc[df["ID"] == second_id].iloc[0]

    first_score = float(first_row["Wynik"])
    second_score = float(second_row["Wynik"])
    score_difference = second_score - first_score

    first_skills = _parse_skills(
        first_row["Umiejętności"]
    )
    second_skills = _parse_skills(
        second_row["Umiejętności"]
    )

    first_missing = _parse_skills(
        first_row["Brakujące"]
    )
    second_missing = _parse_skills(
        second_row["Brakujące"]
    )

    new_skills = sorted(
        second_skills - first_skills,
        key=str.lower
    )
    lost_skills = sorted(
        first_skills - second_skills,
        key=str.lower
    )
    common_skills = sorted(
        first_skills & second_skills,
        key=str.lower
    )

    resolved_missing = sorted(
        first_missing - second_missing,
        key=str.lower
    )
    new_missing = sorted(
        second_missing - first_missing,
        key=str.lower
    )
    still_missing = sorted(
        first_missing & second_missing,
        key=str.lower
    )

    missing_difference = (
        len(second_missing) - len(first_missing)
    )

    st.caption(
        "Zmiana jest liczona od analizy A do analizy B."
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Wynik A",
            f"{first_score:.0f}%"
        )

    with metric2:
        st.metric(
            "Wynik B",
            f"{second_score:.0f}%"
        )

    with metric3:
        st.metric(
            "Zmiana wyniku",
            f"{score_difference:+.0f} p.p."
        )

    missing1, missing2, missing3 = st.columns(3)

    with missing1:
        st.metric(
            "Braki A",
            len(first_missing)
        )

    with missing2:
        st.metric(
            "Braki B",
            len(second_missing)
        )

    with missing3:
        st.metric(
            "Zmiana braków",
            f"{missing_difference:+d}"
        )

    if missing_difference < 0:
        st.success(
            f"Liczba braków spadła o "
            f"{abs(missing_difference)}."
        )
    elif missing_difference > 0:
        st.warning(
            f"Liczba braków wzrosła o "
            f"{missing_difference}."
        )
    else:
        st.info(
            "Liczba brakujących umiejętności "
            "nie zmieniła się."
        )

    st.markdown("### 🧩 Porównanie znalezionych umiejętności")

    found1, found2, found3 = st.columns(3)

    with found1:
        _show_skill_list(
            "🆕 Nowe umiejętności",
            new_skills,
            "Brak nowych umiejętności.",
            "success"
        )

    with found2:
        _show_skill_list(
            "➖ Utracone umiejętności",
            lost_skills,
            "Brak utraconych umiejętności.",
            "error"
        )

    with found3:
        _show_skill_list(
            "🤝 Wspólne umiejętności",
            common_skills,
            "Brak wspólnych umiejętności.",
            "normal"
        )

    st.markdown("### 🎯 Porównanie braków")

    missing_col1, missing_col2, missing_col3 = st.columns(3)

    with missing_col1:
        _show_skill_list(
            "✅ Uzupełnione braki",
            resolved_missing,
            "Brak uzupełnionych braków.",
            "success"
        )

    with missing_col2:
        _show_skill_list(
            "❌ Nowe braki",
            new_missing,
            "Brak nowych braków.",
            "error"
        )

    with missing_col3:
        _show_skill_list(
            "📌 Nadal brakujące",
            still_missing,
            "Brak wspólnych braków.",
            "normal"
        )


def show_history():
    st.header("📚 Historia analiz")

    history = get_history_with_title(
        st.session_state.username
    )

    if not history:
        st.info("Brak zapisanych analiz.")
        return

    df = pd.DataFrame(
        history,
        columns=[
            "ID",
            "Data",
            "Wynik",
            "Umiejętności",
            "Stanowisko",
            "Brakujące"
        ]
    )

    df["Data"] = pd.to_datetime(
        df["Data"],
        errors="coerce"
    )

    _show_comparison(df)

    st.divider()
    st.subheader("🔎 Filtrowanie")

    col1, col2 = st.columns(2)

    with col1:
        text_filter = st.text_input(
            "Szukaj po stanowisku lub umiejętności",
            placeholder="np. Python, SQL, Data Analyst"
        )

    with col2:
        score_range = st.slider(
            "Zakres wyniku",
            min_value=0,
            max_value=100,
            value=(0, 100)
        )

    valid_dates = df["Data"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        date_range = st.date_input(
            "Zakres dat",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        date_range = None

    filtered_df = df.copy()

    filtered_df = filtered_df[
        filtered_df["Wynik"].between(
            score_range[0],
            score_range[1]
        )
    ]

    if text_filter.strip():
        query = text_filter.strip()

        skill_match = (
            filtered_df["Umiejętności"]
            .fillna("")
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        )

        missing_match = (
            filtered_df["Brakujące"]
            .fillna("")
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        )

        title_match = (
            filtered_df["Stanowisko"]
            .fillna("")
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        )

        filtered_df = filtered_df[
            skill_match
            | missing_match
            | title_match
        ]

    if (
        date_range
        and isinstance(date_range, (tuple, list))
        and len(date_range) == 2
    ):
        start_date, end_date = date_range

        filtered_df = filtered_df[
            filtered_df["Data"].dt.date.between(
                start_date,
                end_date
            )
        ]

    st.divider()

    st.write(
        f"Znaleziono analiz: {len(filtered_df)}"
    )

    csv_df = filtered_df.copy()

    csv_df["Data"] = csv_df["Data"].dt.strftime(
        "%Y-%m-%d %H:%M"
    )

    csv = csv_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇ Pobierz przefiltrowaną historię CSV",
        data=csv,
        file_name=(
            f"{st.session_state.username}"
            "_historia.csv"
        ),
        mime="text/csv"
    )

    st.divider()

    if filtered_df.empty:
        st.info(
            "Brak analiz spełniających wybrane kryteria."
        )
        return

    filtered_df = filtered_df.sort_values(
        by="Data",
        ascending=False
    )

    for _, row in filtered_df.iterrows():
        col1, col2 = st.columns([8, 1])

        with col1:
            date_text = (
                row["Data"].strftime("%Y-%m-%d %H:%M")
                if pd.notna(row["Data"])
                else "Brak daty"
            )

            title = (
                row["Stanowisko"].strip()
                if row["Stanowisko"]
                else "Bez nazwy stanowiska"
            )

            missing_skills = _parse_skills(
                row["Brakujące"]
            )

            st.subheader(f"💼 {title}")
            st.write(f"📅 {date_text}")
            st.write(
                f"📊 Dopasowanie: "
                f"{row['Wynik']:.0f}%"
            )
            st.write(
                f"❌ Liczba braków: "
                f"{len(missing_skills)}"
            )

            if row["Umiejętności"]:
                st.write(
                    f"🧩 Umiejętności: "
                    f"{row['Umiejętności']}"
                )

            if row["Brakujące"]:
                st.write(
                    f"📌 Brakujące: "
                    f"{row['Brakujące']}"
                )

        with col2:
            if st.button(
                "🗑",
                key=f"delete_{int(row['ID'])}"
            ):
                delete_analysis(
                    int(row["ID"])
                )

                st.success(
                    "Analiza została usunięta."
                )

                st.rerun()

        st.divider()
