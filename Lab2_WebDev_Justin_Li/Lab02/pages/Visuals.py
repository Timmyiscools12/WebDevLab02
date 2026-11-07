import json
import os

import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

BASE = os.path.dirname(os.path.dirname(__file__))
JSON_PATH = os.path.join(BASE, "data.json")
CSV_PATH = os.path.join(BASE, "data.csv")

st.title("📊 Visuals")

# ---------------------------------------------------------------- Part 1
st.header("Part 1: Best-Selling Games (data.json)")

with open(JSON_PATH, encoding="utf-8") as f:
    games = pd.DataFrame(json.load(f)["games"])

st.subheader("Copies sold by game (static)")
sales = games.sort_values("copies_sold_millions", ascending=False)
st.bar_chart(sales, x="name", y="copies_sold_millions",
             x_label="Game", y_label="Copies sold (millions)")

st.subheader("Score vs. sales by genre (dynamic)")

if "json_genres" not in st.session_state:
    st.session_state.json_genres = sorted(games["genre"].unique())
if "json_min_year" not in st.session_state:
    st.session_state.json_min_year = int(games["release_year"].min())

with st.form("json_filters"):
    chosen_genres = st.multiselect(
        "Genres", sorted(games["genre"].unique()),
        default=st.session_state.json_genres,
    )
    min_year = st.slider(
        "Released in or after", int(games["release_year"].min()),
        int(games["release_year"].max()), st.session_state.json_min_year,
    )
    if st.form_submit_button("Update chart"):
        st.session_state.json_genres = chosen_genres
        st.session_state.json_min_year = min_year

filtered = games[
    games["genre"].isin(st.session_state.json_genres)
    & (games["release_year"] >= st.session_state.json_min_year)
]

if filtered.empty:
    st.warning("No games match those filters.")
else:
    fig = px.scatter(
        filtered, x="metacritic", y="copies_sold_millions", color="genre",
        hover_name="name", size="copies_sold_millions",
        title="Metacritic Score vs. Copies Sold",
        labels={"metacritic": "Metacritic score",
                "copies_sold_millions": "Copies sold (millions)",
                "genre": "Genre"},
    )
    st.plotly_chart(fig, width="stretch")

st.divider()

# ---------------------------------------------------------------- Part 2
st.header("Part 2: Survey Results (data.csv)")

try:
    survey = pd.read_csv(CSV_PATH)
except (FileNotFoundError, pd.errors.EmptyDataError):
    survey = pd.DataFrame()

if survey.empty:
    st.info("No survey responses yet. Fill out the Survey page first!")
else:
    survey["hours_per_week"] = pd.to_numeric(
        survey["hours_per_week"], errors="coerce"
    )

    st.caption(f"{len(survey)} responses so far.")
    st.subheader("Survey Distribution")
    genre_counts = survey["favorite_genre"].value_counts().reset_index()
    genre_counts.columns = ["favorite_genre", "responses"]

    genre_pie = px.pie(
        genre_counts,
        names="favorite_genre",
        values="responses",
        title="Share of Respondents by Genre"
    )
    platform_counts = survey["favorite_platform"].value_counts().reset_index()
    platform_counts.columns = ["favorite_platform", "responses"]

    platform_pie = px.pie(
        platform_counts,
        names="favorite_platform",
        values="responses",
        title="Share of Respondents by Platform"
    )
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(genre_pie, width="stretch")

    with col2:
        st.plotly_chart(platform_pie, width="stretch")

    st.divider()
    st.subheader("Average Weekly Playtime (Dynamic)")

    if "csv_group" not in st.session_state:
        st.session_state.csv_group = "favorite_genre"

    def set_group():
        st.session_state.csv_group = st.session_state.csv_group_choice
    st.radio(
        "Group by",
        ["favorite_genre", "favorite_platform"],
        index=["favorite_genre", "favorite_platform"].index(
            st.session_state.csv_group
        ),
        key="csv_group_choice",
        on_change=set_group,
        horizontal=True
    )
    group = st.session_state.csv_group
    avg = survey.groupby(group, as_index=False)["hours_per_week"].mean()
    bar = (
        alt.Chart(avg)
        .mark_bar()
        .encode(
            x=alt.X(f"{group}:N", title=group.capitalize()),
            y=alt.Y("hours_per_week:Q", title="Average hours per week"),
            tooltip=[
                group,
                alt.Tooltip("hours_per_week:Q", format=".1f")
            ],
        )
        .properties(
            title=f"Average Weekly Playtime by {group.capitalize()}"
        )
    )
    st.altair_chart(bar, width="stretch")
