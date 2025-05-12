import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os

# Path to the config.yaml file
CONFIG_FILE = "/C-SSD/fachel/Job-AI/config.yaml"

# Function to load the existing config file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return yaml.load(file, Loader=SafeLoader)
    return {"credentials": {"usernames": {}}, "cookie": {"name": "some_cookie_name", "key": "some_signature_key", "expiry_days": 30}}

# Function to authenticate a user
def authenticate_user(username, password):
    config = load_config()
    
    # Check if the username exists
    if username in config["credentials"]["usernames"]:
        # Check if the password matches
        if config["credentials"]["usernames"][username]["password"] == password:
            return True
    return False
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Login Form
def login_form():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # Button to redirect to the registration page
    if st.button("Create a new account"):
        st.session_state["show_login"] = False
        st.switch_page("pages/register.py")

# Main function for the login page
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_form()
    else:
        st.switch_page("pages/Job_AI.py")

if __name__ == "__main__":
    main()