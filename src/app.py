import streamlit as st
from utils import *

def main():
    st.set_page_config(layout = "wide")
    ## AUTH
    username = login_page()
    if not username:
        return
    
    set_button_style()

    if 'index' not in st.session_state:
        st.session_state.index = 0
    
    if 'row_count' not in st.session_state:
        st.session_state.row_count = total_rows(DATA_CSV)
    
    email_data = get_first_row(DATA_CSV, st.session_state.index)
    
    if email_data is None:
        st.error("No more emails to display.")
        return

    display_email_information(email_data)
    
    col_a, col_b = st.columns(2)
    manage_email_response(col_a, col_b, email_data, username)
    
    # Progress Bar Logic
    progress_value = (st.session_state.index + 1) / st.session_state.row_count
    st.progress(progress_value)

    st.markdown(f"Viewing email {st.session_state.index + 1} of {st.session_state.row_count}")
    
    manage_navigation()

    _, col_submit, _ = st.columns([1,2,1])  # only way to center submit :(
    # Submit button to check all responses
    with col_submit:
        if st.button('Check Missing Responses'):
            missing_ids = check_responses()
            if missing_ids:
                st.error(f"Missing responses for ({len(missing_ids)}) row IDs: {', '.join(missing_ids)}")
            else:
                st.success("All responses complete!")
    
    with st.sidebar: # putting instructions on sidebar for now
        st.markdown("### Instructions")
        st.markdown("""
        1. Read the email content in the 'Response Email' text area.
        2. Compare the two emails displayed below.
        3. Choose the email that most closely matches the 'Response Email'.
        4. Click 'Next' to move to the next email.
        5. Click 'Check Missing Responses' to see which ids are missing responses.
        \n
        Note: You can always go back to previous emails. Each field is scrollable. \n
        Feel free to use the little triangle on the right side of the text area to expand it (drag using your mouse).
        """)


def display_email_information(email_data):
    st.markdown(f"##### Row_ID: {email_data['id']}")

    # Side by side for sender and receiver
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Email Sender")
        st.text(email_data['from'])

    with col2:
        st.markdown("### Email Receiver")
        st.text(email_data['to'])

    # Side by side for email context and Response Email
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Previous Email")
        height = calculate_text_area_height(email_data['email_context'])
        st.text_area("Email Context", value=email_data['email_context'], height=height, disabled=True, label_visibility="collapsed")

    with col4:
        st.markdown("### Response Email")
        height = calculate_text_area_height(email_data['content'])
        st.text_area("Ground Truth Email", value=email_data['content'], height=height, disabled=True, label_visibility="collapsed")

def manage_email_response(col_a, col_b, email_data, username):
    email_a_content = "Placeholder"
    email_b_content = "Placeholder"
    
    with col_a:
        st.markdown("#### Email A")
        if display_email(email_a_content, 'A'):
            log_choice(email_data['id'], email_data['message_id'], 'A', username)
            # print(email_data['id'], email_data['message_id'], 'A', username)
            st.success("You selected Email A")

    with col_b:
        st.markdown("#### Email B")
        if display_email(email_b_content, 'B'):
            log_choice(email_data['id'], email_data['message_id'], 'B', username)
            # print(email_data['id'], email_data['message_id'], 'B', username)
            st.success("You selected Email B")

def manage_navigation():
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Previous'):
            if st.session_state.index <= 0:
                st.warning("You are at the beginning of the dataset.")
            else:
                st.session_state.index -= 1
                st.rerun()
    with col2:
        if st.button('Next'):
            if st.session_state.index >= st.session_state.row_count - 1:
                st.warning("You have reached the end of the dataset.")
            else:
                st.session_state.index += 1
                st.rerun()

def login_page():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Handle logout logic
    if st.session_state['authenticated']:
        display_name = st.session_state.get('display_name', None)
        st.sidebar.write(f"Welcome, {display_name}!")  # Display welcome message
        if st.sidebar.button("Logout"):
            del st.session_state['authenticated']
            del st.session_state['username']  
            del st.session_state['display_name']
            st.rerun()
        return st.session_state.get('username', None)

    try:
        credentials = load_credentials()
    except FileNotFoundError as e:
        st.error(str(e))
        return None

    # Authentication fields in the sidebar.
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user_info = credentials.get(username, None)
        if user_info and authenticate_user(username, password, user_info['password_hash']):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username  
            st.session_state['display_name'] = user_info['display_name']
            st.sidebar.success("Login successful!")
            st.rerun()
        else:
            st.sidebar.error("Incorrect username or password")
            return None

    st.sidebar.warning("Please log in to continue.")
    return None

if __name__ == "__main__":
    main()
