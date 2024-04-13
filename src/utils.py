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