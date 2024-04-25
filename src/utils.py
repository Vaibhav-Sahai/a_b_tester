import csv
import pandas as pd
import streamlit as st

DATA_CSV = 'data/data.csv'
EMAIL_CHOICES_CSV = 'data/email_choices.csv'

@st.cache_data
def log_choice(id, message_id, chosen_email, filepath=EMAIL_CHOICES_CSV):
    """Logs or updates the user's choice in a CSV file."""
    try:
        # Load the existing data
        data = pd.read_csv(filepath)
    except FileNotFoundError:
        # If the file doesn't exist, create it with initial columns
        data = pd.DataFrame(columns=['id', 'message_id', 'chosen_email'])

    # Check if the entry exists
    mask = (data['id'] == id) & (data['message_id'] == message_id)
    if mask.any():
        # If exists, update the choice
        data.loc[mask, 'chosen_email'] = chosen_email
    else:
        # Otherwise, append a new row
        new_row = pd.DataFrame({'id': [id], 'message_id': [message_id], 'chosen_email': [chosen_email]})
        data = pd.concat([data, new_row], ignore_index=True)
    
    # Write the updated data back to the file
    data.to_csv(filepath, index=False)

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

def check_responses(filepath=EMAIL_CHOICES_CSV, data_csv=DATA_CSV):
    try:
        responses = pd.read_csv(filepath)
        total_data = pd.read_csv(data_csv)
    except FileNotFoundError:
        # if no responses file, all ids are missing
        return ["All Rows Missing, Please Start Responding!"]

    missing_ids = [str(row_id) for row_id in total_data['id'] if row_id not in responses['id'].unique()]
    return missing_ids
