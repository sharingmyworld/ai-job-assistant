import streamlit as st
import pandas as pd

from database import (
    get_learning_plan,
    update_learning_status,
    update_learning_priority,
    delete_learning_task
)


STATUSES = [
    "Do nauki",
    "W trakcie",
    "Ukończone"
]

PRIORITIES = [
    "Wysoki",
    "Średni",
    "Niski"
]


def show_learning_plan():
    st.header("🎯 Plan nauki")

    st.write(
        "Plan jest automatycznie tworzony z brakujących "
        "umiejętności wykrytych podczas analizy CV."
    )

    tasks = get_learning_plan(
        st.session_state.username
    )

    if not tasks:
        st.info(
            "Plan nauki jest pusty. Wykonaj analizę CV, "
            "aby dodać brakujące umiejętności."
        )
        return

    df = pd.DataFrame(
        tasks,
        columns=[
            "ID",
            "Umiejętność",
            "Priorytet",
            "Status",
            "Utworzono",
            "Zaktualizowano"
        ]
    )

    total = len(df)
    completed = int(
        (df["Status"] == "Ukończone").sum()
    )
    in_progress = int(
        (df["Status"] == "W trakcie").sum()
    )
    to_learn = int(
        (df["Status"] == "Do nauki").sum()
    )

    progress = (
        completed / total
        if total
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Wszystkie", total)

    with col2:
        st.metric("Do nauki", to_learn)

    with col3:
        st.metric("W trakcie", in_progress)

    with col4:
        st.metric("Ukończone", completed)

    st.progress(progress)

    st.caption(
        f"Postęp planu: {progress * 100:.0f}%"
    )

    st.divider()
    st.subheader("🔎 Filtrowanie")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_status = st.selectbox(
            "Status",
            ["Wszystkie"] + STATUSES,
            key="learning_status_filter"
        )

    with filter_col2:
        selected_priority = st.selectbox(
            "Priorytet",
            ["Wszystkie"] + PRIORITIES,
            key="learning_priority_filter"
        )

    filtered_df = df.copy()

    if selected_status != "Wszystkie":
        filtered_df = filtered_df[
            filtered_df["Status"] == selected_status
        ]

    if selected_priority != "Wszystkie":
        filtered_df = filtered_df[
            filtered_df["Priorytet"] == selected_priority
        ]

    st.divider()

    if filtered_df.empty:
        st.info(
            "Brak zadań spełniających wybrane kryteria."
        )
        return

    for _, row in filtered_df.iterrows():
        task_id = int(row["ID"])

        with st.container(border=True):
            title_col, delete_col = st.columns([9, 1])

            with title_col:
                st.subheader(
                    f"📘 {row['Umiejętność']}"
                )

            with delete_col:
                if st.button(
                    "🗑",
                    key=f"delete_learning_{task_id}"
                ):
                    delete_learning_task(task_id)
                    st.rerun()

            edit_col1, edit_col2 = st.columns(2)

            current_priority = row["Priorytet"]
            current_status = row["Status"]

            with edit_col1:
                priority = st.selectbox(
                    "Priorytet",
                    PRIORITIES,
                    index=PRIORITIES.index(
                        current_priority
                    ),
                    key=f"priority_{task_id}"
                )

            with edit_col2:
                status = st.selectbox(
                    "Status",
                    STATUSES,
                    index=STATUSES.index(
                        current_status
                    ),
                    key=f"status_{task_id}"
                )

            if priority != current_priority:
                update_learning_priority(
                    task_id,
                    priority
                )
                st.rerun()

            if status != current_status:
                update_learning_status(
                    task_id,
                    status
                )
                st.rerun()

            st.caption(
                f"Dodano: {row['Utworzono']} | "
                f"Ostatnia zmiana: {row['Zaktualizowano']}"
            )
