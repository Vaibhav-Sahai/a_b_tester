import streamlit as st
import csv

def main():
    st.title('Email Style Selector')

    # User inputs for the context, sender, and receiver
    context = st.text_area("Email Context", "Describe the context...")
    sender = st.text_input("Email Sender", "Sender's email address")
    receiver = st.text_input("Email Receiver", "Receiver's email address")

    # Displaying two different styled emails for selection
    email_a = st.text_area("Email A", "Content of Email A...")
    email_b = st.text_area("Email B", "Content of Email B...")

    # Button for user to select Email A
    if st.button('Choose Email A'):
        log_choice(context, sender, receiver, 'A', email_a)
        st.success("You selected Email A")

    # Button for user to select Email B
    elif st.button('Choose Email B'):
        log_choice(context, sender, receiver, 'B', email_b)
        st.success("You selected Email B")

def log_choice(context, sender, receiver, choice, content):
    """Logs the user's choice to a CSV file."""
    with open('email_choices.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([context, sender, receiver, choice, content])

if __name__ == "__main__":
    main()
