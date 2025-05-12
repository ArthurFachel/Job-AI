import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")


# Custom CSS to hide the sidebar navigation
st.markdown(
       """
    <style>
    /* Hide the sidebar navigation items */
    .st-emotion-cache-bjn8vh {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Check if the user is authenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Redirect to login if not authenticated
if not st.session_state["authenticated"]:
    st.switch_page("pages/Login.py")
else:
    st.switch_page("pages/Job_AI.py")
