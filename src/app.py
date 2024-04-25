import streamlit as st
from utils import *

def main():
    st.title('Email Style Selector')
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
    manage_email_response(col_a, col_b, email_data)
    
    manage_navigation()

    # Submit button to check all responses
    if st.button('Submit'):
        missing_ids = check_responses()
        if missing_ids:
            st.error(f"Missing responses for ({len(missing_ids)}) row IDs: {', '.join(missing_ids)}")
        else:
            st.success("All responses complete!")

def display_email_information(email_data):
    st.markdown(f"##### Row_ID: {email_data['id']}")
    st.markdown("### Email Sender")
    st.text(email_data['from'])
    st.markdown("### Email Receiver")
    st.text(email_data['to'])
    st.markdown("### Email Context")
    st.text(email_data['email_context'])
    height = calculate_text_area_height(email_data['content'])
    st.text_area("Ground Truth Email", value=email_data['content'], height=height, disabled=True, label_visibility="collapsed")

def manage_email_response(col_a, col_b, email_data):
    email_a_content = "Placeholder"
    email_b_content = "Placeholder"
    
    with col_a:
        st.markdown("#### Email A")
        if display_email(email_a_content, 'A'):
            log_choice(email_data['id'], email_data['message_id'], 'A')
            st.success("You selected Email A")

    with col_b:
        st.markdown("#### Email B")
        if display_email(email_b_content, 'B'):
            log_choice(email_data['id'], email_data['message_id'], 'B')
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

if __name__ == "__main__":
    main()
