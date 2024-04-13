import csv
import pandas as pd
import streamlit as st

def log_choice(context, sender, receiver, choice, content):
    """Logs the user's choice to a CSV file."""
    with open('email_choices.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([context, sender, receiver, choice, content])
        

def get_first_row(csv_path):
    data = pd.read_csv(csv_path)
    return data.iloc[0]

def display_email(content, key, background_color = "#ffffe6"):
    """Display an email with the given content and background color."""
    st.markdown(f"""
        <div style='background-color:{background_color}; color: black; padding: 10px; border-radius: 10px;'>
            <p style='white-space: pre-wrap;'>{content}</p>
        </div>
        """, unsafe_allow_html=True)
    if st.button(f'Choose Email {key}'):
        return True
    return False

def set_button_style():
    """Sets the button style for the Streamlit app. (currently makes both buttons blue)"""
    button_style = """
    <style>
        .stButton>button {
            border: 2px solid #4a8aeb;
            color: white;
            background-color: #4a8aeb;
            padding: 10px 24px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            border: 2px solid #0b6cc1;
            background-color: #0b6cc1;
        }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)