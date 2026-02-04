import streamlit as st
import pandas as pd

from github import GithubException
from .clients import create_supabase_client, create_github_repo
from .config import get_env
from .utils import current_ist_date
from .logger import get_logger

logger = get_logger(__name__)

# setup clients
def setup_clients():
    supabase = create_supabase_client()
    gh, repo = create_github_repo()
    admin_user = get_env("ADMIN_USERNAME")
    admin_pass = get_env("ADMIN_PASSWORD")
    return supabase, repo, admin_user, admin_pass


# ---------------------- Admin Login -------------------------
def admin_login(admin_user, admin_pass):
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        with st.form("Admin Login"):
            username = st.text_input('Username')
            password = st.text_input('Password',type="password")

            if st.form_submit_button("Login"):
                if username == admin_user and password == admin_pass:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        st.stop()


# --------------------- Sidebar Controls ---------------------
def sidebar_controls(supabase):
    try:
        with st.sidebar:
            st.markdown("Create Class")
            class_input = st.text_input("New Class Name")
            if st.button("Add Class"):
                if class_input.strip():
                    exists = supabase.table("classroom_settings").select("*").eq("class_name",class_input).execute().data
                    if exists:
                        st.warning("Class already exists")
                    else:
                        supabase.table("classroom_settings").insert({
                            "class_name":class_input,
                            "code": "1234",
                            "daily_limit": 10,
                            "is_open":False
                        }).execute()
                        st.success(f"Class '{class_input}' created")
                        st.rerun()
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
            
            if st.markdown("Delete Class"):
                delete_target = st.text_input("Enter class to delete")
            if st.button("Delete this class"):
                if delete_target.strip():
                    st.warning("This will permanently delete the class and all data.")
                    if st.text_input("Type DELETE to confirm") == "DELETE":
                        supabase.table("attendance").delete().eq("class_name",delete_target).execute()
                        supabase.table("roll_map").delete().eq("class_name",delete_target).execute()
                        supabase.table("classroom_settings").delete().eq("class_name",delete_target).execute()
                        st.success("Class deleted")
                        st.rerun()
    except Exception as e:
        logger.exception("Error in sidebar_controls")
        st.error(f'Sidebar error: {e}')

