

"""
login.py — Auth screen shown before any view.
Renders a user-select dropdown and a "Continue" button.
Sets st.session_state.current_user on success.
"""

import streamlit as st
from edd_app.auth import all_usernames, get_user

# ── CSS for the login screen ───────────────────────────────────────────────────
LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f7f5; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.login-wrap {
    max-width: 420px;
    margin: 80px auto 0 auto;
    background: #fff;
    border: 1px solid #e8e8e4;
    border-radius: 16px;
    padding: 44px 40px 36px 40px;
    box-shadow: 0 2px 24px rgba(0,0,0,0.07);
}
.login-logo {
    font-size: 22px; font-weight: 600;
    color: #1a1a1a; letter-spacing: -0.02em;
    margin-bottom: 6px;
}
.login-sub {
    font-size: 13px; color: #999;
    margin-bottom: 32px; letter-spacing: 0.01em;
}
.login-avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: #1a1a1a; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 600;
    margin: 0 auto 12px auto;
}
.login-confirm-name {
    text-align: center; font-size: 16px; font-weight: 600;
    color: #1a1a1a; margin-bottom: 2px;
}
.login-confirm-role {
    text-align: center; font-size: 12px; color: #999;
    margin-bottom: 24px; letter-spacing: 0.04em; text-transform: uppercase;
}
</style>
"""

def render_login():
    """Render the login screen. Returns True if authenticated, False otherwise."""

    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    # Centre-column layout
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="login-wrap">
            <div class="login-logo">📋 EDD Tracker</div>
            <div class="login-sub">Select your profile to continue</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Dropdown ──────────────────────────────────────────────────────────
        names = all_usernames()
        selected = st.selectbox(
            "Who are you?",
            options=["— select —"] + names,
            index=0,
            key="login_selected_user",
            label_visibility="collapsed",
        )

        if selected != "— select —":
            user = get_user(selected)
            role_label = "Administrator" if user["role"] == "admin" else "Team Member"

            # ── Confirm card ─────────────────────────────────────────────────
            st.markdown(f"""
            <div style="text-align:center;margin:20px 0 8px 0;">
                <div class="login-avatar">{user['avatar']}</div>
                <div class="login-confirm-name">{user['display_name']}</div>
                <div class="login-confirm-role">{role_label}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Continue as {user['display_name']} →",
                use_container_width=True,
                key="login_continue_btn",
            ):
                st.session_state.current_user = selected
                st.session_state.current_role = user["role"]
                st.rerun()

    return False  # Not yet authenticated — caller should st.stop()