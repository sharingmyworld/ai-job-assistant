import streamlit as st
import pandas as pd

from database import (
    get_statistics,
    get_progress,
    get_learning_plan,
    get_roadmap_progress,
    get_weekly_goal,
    get_total_completed_roadmap_steps,
    get_upcoming_application_events
)

from learning_roadmaps import get_skill_roadmap


@st.cache_data(ttl=30, show_spinner=False)
def _cached_statistics(username):
    return get_statistics(username)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_progress(username):
    return get_progress(username)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_learning_plan(username):
    return get_learning_plan(username)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_roadmap_progress(username, skill):
    return get_roadmap_progress(username, skill)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_weekly_goal(username):
    return get_weekly_goal(username)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_completed_steps(username):
    return get_total_completed_roadmap_steps(username)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_upcoming_events(username, limit):
    return get_upcoming_application_events(
        username,
        limit=limit
    )


def show_dashboard():
    username = st.session_state.username

    stats = _cached_statistics(username)

    count = stats[0] or 0
    average = stats[1] or 0
    best = stats[2] or 0

    st.header(
        f"👋 Witaj {username}"
    )

    st.write(
        "Tutaj możesz śledzić swoje postępy."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Liczba analiz",
            count
        )

    with col2:
        st.metric(
            "Średni wynik",
            f"{average:.1f}%"
        )

    with col3:
        st.metric(
            "Najlepszy wynik",
            f"{best:.1f}%"
        )

    progress = _cached_progress(username)

    if len(progress) > 1:
        df = pd.DataFrame(
            progress,
            columns=[
                "Data",
                "Wynik"
            ]
        )

        st.divider()

        st.subheader(
            "📈 Postęp analiz"
        )

        st.line_chart(
            df.set_index("Data")
        )


    upcoming_events = _cached_upcoming_events(
        username,
        5
    )

    if upcoming_events:
        from datetime import date

        st.divider()
        st.subheader("📅 Najbliższe wydarzenia rekrutacyjne")

        today = date.today()

        for event in upcoming_events:
            _, company, position, event_date, event_type, status = event

            parsed_date = pd.to_datetime(
                event_date,
                errors="coerce"
            )

            if pd.isna(parsed_date):
                continue

            days_left = (
                parsed_date.date() - today
            ).days

            if days_left < 0:
                when_text = (
                    f"{abs(days_left)} dni po terminie"
                )
            elif days_left == 0:
                when_text = "dzisiaj"
            elif days_left == 1:
                when_text = "jutro"
            else:
                when_text = f"za {days_left} dni"

            if days_left < 0:
                st.error(
                    f"{event_type} — {position} — "
                    f"{company} ({when_text})"
                )
            elif days_left <= 2:
                st.warning(
                    f"{event_type} — {position} — "
                    f"{company} ({when_text})"
                )
            else:
                st.info(
                    f"{event_type} — {position} — "
                    f"{company} ({when_text})"
                )

    st.divider()

    st.subheader("🎯 Postęp nauki")

    tasks = _cached_learning_plan(username)

    if not tasks:
        st.info(
            "Plan nauki jest pusty. "
            "Wykonaj analizę CV, aby dodać umiejętności."
        )
        return

    learning_df = pd.DataFrame(
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

    total = len(learning_df)

    to_learn = int(
        (
            learning_df["Status"]
            == "Do nauki"
        ).sum()
    )

    in_progress = int(
        (
            learning_df["Status"]
            == "W trakcie"
        ).sum()
    )

    completed = int(
        (
            learning_df["Status"]
            == "Ukończone"
        ).sum()
    )

    learning_progress = (
        completed / total
        if total
        else 0
    )

    learn1, learn2, learn3, learn4 = st.columns(4)

    with learn1:
        st.metric(
            "Umiejętności",
            total
        )

    with learn2:
        st.metric(
            "Do nauki",
            to_learn
        )

    with learn3:
        st.metric(
            "W trakcie",
            in_progress
        )

    with learn4:
        st.metric(
            "Ukończone",
            completed
        )

    st.progress(learning_progress)

    st.caption(
        f"Ogólny postęp planu: "
        f"{learning_progress * 100:.0f}%"
    )

    active_tasks = learning_df[
        learning_df["Status"] != "Ukończone"
    ]

    if not active_tasks.empty:
        priority_order = {
            "Wysoki": 1,
            "Średni": 2,
            "Niski": 3
        }

        active_tasks = active_tasks.copy()

        active_tasks["Kolejność"] = (
            active_tasks["Priorytet"]
            .map(priority_order)
            .fillna(4)
        )

        next_task = active_tasks.sort_values(
            by=[
                "Kolejność",
                "ID"
            ]
        ).iloc[0]

        st.info(
            f"🔥 Następny priorytet: "
            f"{next_task['Umiejętność']} "
            f"({next_task['Priorytet']})"
        )


    weekly_goal = _cached_weekly_goal(username)

    if weekly_goal:
        target_steps = weekly_goal[0]
        start_completed = weekly_goal[1]
        deadline = weekly_goal[2]

        total_completed_steps = (
            _cached_completed_steps(
                username
            )
        )

        completed_for_goal = max(
            0,
            total_completed_steps - start_completed
        )

        goal_progress = min(
            completed_for_goal / target_steps,
            1.0
        )

        st.divider()
        st.subheader("📅 Cel tygodniowy")

        st.metric(
            "Postęp celu",
            f"{completed_for_goal}/{target_steps} kroków"
        )

        st.progress(goal_progress)

        st.caption(
            f"Termin: {deadline}"
        )

        if completed_for_goal >= target_steps:
            st.success(
                "🎉 Cel tygodniowy osiągnięty!"
            )
        else:
            st.info(
                f"Pozostało "
                f"{target_steps - completed_for_goal} "
                f"kroków do celu."
            )

    st.divider()

    st.subheader("🗺️ Postęp roadmap")

    for _, row in learning_df.iterrows():
        skill = row["Umiejętność"]

        roadmap = get_skill_roadmap(skill)

        roadmap_progress = _cached_roadmap_progress(
            username,
            skill
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

        st.write(
            f"**{skill}** — "
            f"{completed_steps}/{len(roadmap)}"
        )

        st.progress(roadmap_percent)
