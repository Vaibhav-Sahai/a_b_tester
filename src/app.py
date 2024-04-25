import streamlit as st
from utils import get_first_row, log_choice, display_email, set_button_style, calculate_text_area_height

DATA_CSV = 'data/data.csv'

def main():
    st.title('Email Style Selector')
    set_button_style()

    # set session state
    if 'index' not in st.session_state:
        st.session_state.index = 0
    
    # Load data
    email_data = get_first_row(DATA_CSV, st.session_state.index)
    
    if email_data is None:
        st.error("No more emails to display.")
        return

    # Displaying fixed information for context, sender, and receiver
    context = email_data['email_context']
    sender = email_data['from']
    receiver = email_data['to']
    gt_email = email_data['content']
    
    # these are just variables we need while writing to the file
    id = email_data['id']
    message_id = email_data['message_id']
    
    st.markdown("### Email Sender")
    st.text(sender)
    
    st.markdown("### Email Receiver")
    st.text(receiver)

    st.markdown("### Email Context")
    st.text(context)
    
    st.markdown("### Ground Truth Email")
    height = calculate_text_area_height(gt_email)
    st.text_area("a", value=gt_email, height=height, key="gt_email_area", disabled=True, label_visibility="collapsed")
    
    # Use columns to layout Email A and Email B side by side
    col_a, col_b = st.columns(2)
    email_a_content = "Placeholder"
    email_b_content = "Placeholder"
    
    with col_a:
        st.markdown("#### Email A")
        if display_email(email_a_content, 'A'):
            log_choice(id, message_id, 'A')
            st.success("You selected Email A")

    with col_b:
        st.markdown("#### Email B")
        if display_email(email_b_content, 'B'):
            log_choice(id, message_id, 'B')
            st.success("You selected Email B")
    
    # Navigation buttons
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
            st.session_state.index += 1
            st.rerun()


if __name__ == "__main__":
    main()