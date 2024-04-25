import csv
import pandas as pd
import streamlit as st

def log_choice(id, message_id, chosen_email):
    """Logs the user's choice to a CSV file."""
    with open('email_choices.csv', 'a', newline='') as file:
        fieldnames = ['id', 'message_id', 'chosen_email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Check if we need to write the header
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                'id': id, 
                'message_id': message_id, 
                'chosen_email': chosen_email
            }
        )

def get_first_row(csv_path, index):
    data = pd.read_csv(csv_path)
    if 0 <= index < len(data):
        return data.iloc[index]
    return None

def total_rows(csv_path):
    data = pd.read_csv(csv_path)
    return len(data)

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

def calculate_text_area_height(text, max_chars_per_line=100):
    """Calculate the height needed to display the text without scrolling."""
    lines = text.count('\n') + 1  # Basic line count based on line breaks
    # Account for long lines that wrap
    for line in text.split('\n'):
        lines += len(line) // max_chars_per_line
    return max(3, lines) * 20  # Approx. 20 pixels per line
