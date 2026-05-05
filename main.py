
"""
main.py — Application entry point.

Run with:  streamlit run main.py

Flow:
  1. If not authenticated → show login screen
  2. If role == "admin"  → show admin dashboard
  3. If role == "member" → run the EDD tracker (member_app.py)
"""

import streamlit as st

# ── Page config (must be FIRST Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="EDD Tracking",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth check ─────────────────────────────────────────────────────────────────
current_user = st.session_state.get("current_user")
current_role = st.session_state.get("current_role")

if not current_user:
    # ── Not logged in → login screen ──────────────────────────────────────────
    from edd_app.login import render_login
    render_login()
    st.stop()

# ── Logged in → route by role ──────────────────────────────────────────────────
if current_role == "admin":
    from edd_app.views.admin_view import render_admin_view
    render_admin_view()

else:
    # Member view: exec member_app.py in this process so all Streamlit state
    # (session_state, reruns, widgets) works exactly as if it were the entry point.
    import importlib.util, sys, os

    # Ensure project root is on sys.path so member_app can import its own helpers
    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    # Expose current user info to member_app's sidebar
    from edd_app.auth import get_user
    info = get_user(current_user) or {}
    st.session_state["_current_display"] = info.get("display_name", current_user)
    st.session_state["_current_avatar"]  = info.get("avatar", current_user[:2].upper())

    spec = importlib.util.spec_from_file_location(
        "member_app",
        os.path.join(root, "edd_app", "member_app.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)