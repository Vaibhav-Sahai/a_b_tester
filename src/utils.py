import csv
import pandas as pd
import streamlit as st
import os
import pickle
from passlib.hash import pbkdf2_sha256 as sha256

DATA_CSV = 'data/data.csv'
EMAIL_CHOICES_CSV = 'email_choices.csv'
CREDENTIALS_PKL = 'credentials/hashed_passwords.pkl'

# @st.cache_data
def log_choice(id, message_id, chosen_email, user, filepath=EMAIL_CHOICES_CSV):
    """Logs or updates the user's choice in a CSV file, specific to the user."""
    user_filepath = f"data/{user}/{filepath}"  
    try:
        data = pd.read_csv(user_filepath)
        # print("Read data from file")
    except FileNotFoundError:
        os.makedirs(f"data/{user}", exist_ok=True)  # Ensure user directory exists
        data = pd.DataFrame(columns=['id', 'message_id', 'chosen_email'])
    
    mask = (data['id'] == id) & (data['message_id'] == message_id)
    if mask.any():
        data.loc[mask, 'chosen_email'] = chosen_email
        # print("Updated existing row")
    else:
        new_row = pd.DataFrame({'id': [id], 'message_id': [message_id], 'chosen_email': [chosen_email]})
        data = pd.concat([data, new_row], ignore_index=True)
        # print("Added new row")
    
    data.to_csv(user_filepath, index=False)  # Write back to the user-specific file

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
        /* Targeting disabled text areas and setting the background to white and text to black */
        .stTextArea [data-baseweb=base-input] [disabled] {
            background-color: white !important; /* Ensure the background is white */
            -webkit-text-fill-color: black !important; /* Ensure the text color is black */
        }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)



def calculate_text_area_height(text, max_chars_per_line=100):
    """Calculate the height needed to display the text without scrolling."""
    if not text:
        return 350
    # Account for long lines that wrap
    try:
        lines = text.count('\n') + 1  # Basic line count based on line breaks
        for line in text.split('\n'):
            lines += len(line) // max_chars_per_line
        return max(3, lines) * 30  # Approx. 30 pixels per line
    except:
        return 350

def check_responses(filepath=EMAIL_CHOICES_CSV, data_csv=DATA_CSV):
    filepath = f"data/{st.session_state.username}/{filepath}"
    try:
        responses = pd.read_csv(filepath)
        total_data = pd.read_csv(data_csv)
    except FileNotFoundError:
        # if no responses file, all ids are missing
        return ["All Rows Missing, Please Start Responding!"]

    missing_ids = [str(row_id) for row_id in total_data['id'] if row_id not in responses['id'].unique()]
    return missing_ids

#-------------------------#
# Streamlit Auth Code
def load_credentials(path=CREDENTIALS_PKL):
    """Load hashed passwords and display names from a file."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    else:
        raise FileNotFoundError("Credential file not found. Is it missing?")

def authenticate_user(username, password, credentials):
    """Authenticate the user against hashed passwords and return display name if authenticated."""
    user_credentials = credentials.get(username)
    if user_credentials:
        stored_hash = user_credentials['password_hash']
        if sha256.verify(password, stored_hash):
            return user_credentials['display_name'] 
    return False


def authenticate_user(username, password, credentials):
    """Authenticate the user against hashed passwords and return display name if authenticated."""
    stored_hash = credentials
    if sha256.verify(password, stored_hash):
        return True
    return False