import streamlit as st
import pandas as pd

from database import (
    get_learning_plan,
    update_learning_status,
    update_learning_priority,
    delete_learning_task,
    get_roadmap_progress,
    update_roadmap_step,
    update_learning_status_by_skill,
    save_weekly_goal,
    get_weekly_goal,
    get_total_completed_roadmap_steps,
    delete_weekly_goal
)

from learning_roadmaps import get_skill_roadmap


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
    st.subheader("📅 Cel tygodniowy")

    weekly_goal = get_weekly_goal(
        st.session_state.username
    )

    if weekly_goal:
        target_steps = weekly_goal[0]
        start_completed = weekly_goal[1]
        deadline = weekly_goal[2]

        total_completed = (
            get_total_completed_roadmap_steps(
                st.session_state.username
            )
        )

        completed_for_goal = max(
            0,
            total_completed - start_completed
        )

        goal_progress = min(
            completed_for_goal / target_steps,
            1.0
        )

        st.metric(
            "Postęp celu",
            f"{completed_for_goal}/{target_steps} kroków"
        )

        st.progress(goal_progress)

        st.caption(
            f"Termin celu: {deadline}"
        )

        if completed_for_goal >= target_steps:
            st.success(
                "🎉 Cel tygodniowy osiągnięty!"
            )
        else:
            remaining = (
                target_steps - completed_for_goal
            )

            st.info(
                f"Do celu pozostało: "
                f"{remaining} kroków roadmapy."
            )

        if st.button(
            "🗑 Usuń cel tygodniowy",
            key="delete_weekly_goal"
        ):
            delete_weekly_goal(
                st.session_state.username
            )
            st.rerun()

    with st.expander(
        "⚙️ Ustaw nowy cel tygodniowy"
    ):
        goal_steps = st.number_input(
            "Liczba kroków roadmapy",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            key="weekly_goal_steps"
        )

        goal_deadline = st.date_input(
            "Termin celu",
            key="weekly_goal_deadline"
        )

        if st.button(
            "🎯 Zapisz cel",
            key="save_weekly_goal"
        ):
            save_weekly_goal(
                st.session_state.username,
                goal_steps,
                goal_deadline.isoformat()
            )

            st.success(
                "Cel tygodniowy został zapisany."
            )
            st.rerun()

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

            with st.expander(
                f"🗺️ Roadmapa: {row['Umiejętność']}"
            ):
                roadmap = get_skill_roadmap(
                    row["Umiejętność"]
                )

                roadmap_progress = get_roadmap_progress(
                    st.session_state.username,
                    row["Umiejętność"]
                )

                completed_steps = sum(
                    roadmap_progress.get(
                        step_number,
                        False
                    )
                    for step_number in range(
                        len(roadmap)
                    )
                )

                roadmap_percent = (
                    completed_steps / len(roadmap)
                    if roadmap
                    else 0
                )

                st.progress(roadmap_percent)

                st.caption(
                    f"Postęp roadmapy: "
                    f"{completed_steps}/{len(roadmap)} "
                    f"({roadmap_percent * 100:.0f}%)"
                )

                for step_number, step in enumerate(
                    roadmap
                ):
                    is_completed = (
                        roadmap_progress.get(
                            step_number,
                            False
                        )
                    )

                    checked = st.checkbox(
                        f"{step_number + 1}. {step}",
                        value=is_completed,
                        key=(
                            f"roadmap_{task_id}_"
                            f"{step_number}"
                        )
                    )

                    if checked != is_completed:
                        update_roadmap_step(
                            st.session_state.username,
                            row["Umiejętność"],
                            step_number,
                            checked
                        )

                        updated_progress = (
                            roadmap_progress.copy()
                        )
                        updated_progress[
                            step_number
                        ] = checked

                        updated_completed = sum(
                            updated_progress.get(
                                number,
                                False
                            )
                            for number in range(
                                len(roadmap)
                            )
                        )

                        if updated_completed == len(roadmap):
                            new_status = "Ukończone"
                        elif updated_completed > 0:
                            new_status = "W trakcie"
                        else:
                            new_status = "Do nauki"

                        update_learning_status_by_skill(
                            st.session_state.username,
                            row["Umiejętność"],
                            new_status
                        )

                        st.rerun()
