import streamlit as st
from utils import get_first_row, log_choice, display_email

DATA_CSV = 'data/data.csv'

def main():
    st.title('Email Style Selector')

    # Load data
    first_email_data = get_first_row(DATA_CSV)

    # Displaying fixed information for context, sender, and receiver
    context = first_email_data['email_context']
    sender = first_email_data['from']
    receiver = first_email_data['to']
    gt_email = first_email_data['content']
    
    st.markdown("### Email Sender")
    st.text(sender)
    
    st.markdown("### Email Receiver")
    st.text(receiver)

    st.markdown("### Email Context")
    st.text(context)
    
    st.markdown("### Ground Truth Email")
    st.text(gt_email)

    # Use columns to layout Email A and Email B side by side
    col_a, col_b = st.columns(2)
    email_a_content = "Placeholder"
    email_b_content = "Placeholder"
    
    with col_a:
        st.markdown("#### Email A")
        if display_email(email_a_content, 'A'):
            log_choice(context, sender, receiver, 'A', email_a_content)
            st.success("You selected Email A")
    
    with col_b:
        st.markdown("#### Email B")
        if display_email(email_b_content, 'B'):
            log_choice(context, sender, receiver, 'B', email_b_content)
            st.success("You selected Email B")

if __name__ == "__main__":
    main()