import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os

# Path to the config.yaml file
CONFIG_FILE = "config.yaml"

# Function to load the existing config file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return yaml.load(file, Loader=SafeLoader)
    return {"credentials": {"usernames": {}}, "cookie": {"name": "some_cookie_name", "key": "some_signature_key", "expiry_days": 30}}

# Function to save the updated config file
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file)
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Function to register a new user (no hashing)
def register_user(username, email, password):
    config = load_config()
    
    # Check if the username already exists
    if username in config["credentials"]["usernames"]:
        st.error(body ='Username already exists. Please choose a different username.', icon="🚨",)
        return False
    
    # Add the new user to the config with plain-text password
    config["credentials"]["usernames"][username] = {
        "email": email,
        "name": username,  # You can customize this field
        "password": password  # Store the plain-text password
    }
    
    # Save the updated config
    save_config(config)
    st.success("Registration successful! You can now log in.")
    return True

# Registration Form
def registration_form():
    st.title("User Registration")

    with st.form("registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Register")

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            elif username and email and password:
                if register_user(username, email, password):
                    # Redirect to the login page
                    st.session_state["show_login"] = True
                    st.switch_page("pages/Login.py")

    # Button to redirect to the login page
    if st.button("Back to Login"):
        st.switch_page("pages/Login.py")

# Main function for the registration page
def main():
    registration_form()

if __name__ == "__main__":
    main()