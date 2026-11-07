# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Web Development Lab02!")
st.header("CS 1301")
st.header("Web Development-Section D")
st.header("Name: Justin Li")
# INTRODUCTORY TEXT
st.write("""
Welcome to my Streamlit Web Development Lab02 app! You can navigate between the pages using the sidebar to the left. The following pages are:

- **Visuals Page**: a static bar chart of lifetime copies sold per game.
- **Survey Page**: Go here to input new data into our CSV file.

This project is part of CS 1301's Lab 2.
""")


image_path = os.path.join(BASE_DIR, "images", "images.jpg")
st.image(image_path)
