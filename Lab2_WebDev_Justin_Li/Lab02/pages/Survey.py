import csv
import os

import streamlit as st

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.csv")
FIELDS = ["name", "favorite_genre", "favorite_platform", "hours_per_week", "favorite_game"]

GENRES = ["Action", "RPG", "Sandbox", "Sports", "Racing", "Platformer", "Other"]
PLATFORMS = ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile"]

st.title("📝 Gaming Survey")
st.write("Answer a few quick questions. Your response is saved to `data.csv`.")

with st.form("survey_form", clear_on_submit=True):
    name = st.text_input("Your first name")
    favorite_game = st.text_input("What is your favorite video game?")
    genre = st.selectbox("Favorite genre", GENRES)
    platform = st.selectbox("Main platform", PLATFORMS)
    hours = st.text_input("About how many hours per week do you play? (number)")
    submitted = st.form_submit_button("Submit")

if submitted:
    hours = hours.strip()
    if not name.strip() or not favorite_game.strip():
        st.error("Please fill in your name and favorite game.")
    else:
        try:
            hours_val = float(hours)
            if hours_val < 0 or hours_val > 168:
                raise ValueError
        except ValueError:
            st.error("Hours per week must be a number between 0 and 168.")
        else:
            file_exists = os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0
            with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(FIELDS)
                writer.writerow([name, genre, platform, hours_val, favorite_game])
            st.success("Thanks! Your response was saved.")
