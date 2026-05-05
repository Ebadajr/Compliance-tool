"""
admin_view.py — Admin dashboard
Shows: user list, who reviewed what, performance stats, user management, row assignment.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from ..auth import USERS, get_non_admin_users, get_display_name, ADMIN_ROLE
from sheets import (
    get_assigned_to_col,
    write_assigned_to_sheet,
    bulk_assign_rows,
    load_from_google_sheets,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_df():
    if not st.session_state.get("gs_loaded"):
        with st.spinner("Connecting to Google Sheets…"):
            df_gs = load_from_google_sheets()
            st.session_state.df_edd     = df_gs
            st.session_state.gs_loaded  = True
            st.session_state.edd_source = "gsheet"
    return st.session_state.get("df_edd")


def _get_ws():
    return st.session_state.get("gs_worksheet_obj")


def badge(text, color="#f0f0ec", fg="#1a1a1a"):
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:4px;'
        f'font-size:11px;font-weight:500;background:{color};color:{fg};'
        f'font-family:monospace;letter-spacing:0.04em">{text}</span>'
    )


def metric(num, label, accent="#1a1a1a"):
    return (
        f'<div style="background:#fff;border:1px solid #e8e8e4;border-radius:10px;'
        f'padding:20px 24px;text-align:center">'
        f'<div style="font-size:32px;font-weight:600;color:{accent};letter-spacing:-0.02em">{num}</div>'
        f'<div style="font-size:11px;color:#999;letter-spacing:0.08em;text-transform:uppercase;margin-top:4px">{label}</div>'
        f'</div>'
    )


# ── Main render ───────────────────────────────────────────────────────────────

def render_admin_view():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
* { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f7f5; }
section[data-testid="stSidebar"] { background-color: #1a1a1a; border-right: none; }
section[data-testid="stSidebar"] * { color: #e8e8e4 !important; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.edd-header {
    background: #1a1a1a; color: #f7f7f5;
    padding: 28px 36px; border-radius: 12px; margin-bottom: 24px;
    display: flex; align-items: baseline; gap: 16px;
}
.edd-title    { font-size: 26px; font-weight: 600; letter-spacing: -0.02em; margin: 0; }
.edd-subtitle { font-size: 13px; color: #888; letter-spacing: 0.04em; margin: 0; }
.metric-box { background: #fff; border: 1px solid #e8e8e4; border-radius: 10px; padding: 20px 24px; text-align: center; }
.metric-num { font-size: 32px; font-weight: 600; color: #1a1a1a; letter-spacing: -0.02em; }
.metric-lbl { font-size: 11px; color: #999; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }
.section-title { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-bottom: 14px; margin-top: 8px; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 500; letter-spacing: 0.04em; font-family: 'DM Mono', monospace; }
.badge-pending      { background: #f0ede8; color: #8a7560; }
.badge-form_sent    { background: #e8edf5; color: #3a5a8a; }
.badge-under_review { background: #fef3e2; color: #9a6820; }
.badge-done         { background: #e8f4ee; color: #2d7a4f; }
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stButton > button {
    border-radius: 7px; font-family: 'DM Sans', sans-serif;
    font-weight: 500; font-size: 13px;
    border: 1px solid #1a1a1a !important;
    background: #fff !important; color: #1a1a1a !important;
    padding: 6px 16px; transition: all 0.15s;
}
.stButton > button:hover { background: #1a1a1a !important; color: #fff !important; }
div[data-testid="stCheckbox"] { margin-bottom: 0 !important; padding: 0 !important; }
div[data-testid="stCheckbox"] label { font-size: 13px !important; color: #1a1a1a !important; }
div[data-testid="stCheckbox"] label p { color: #1a1a1a !important; }
div[data-testid="stCheckbox"] span { color: #1a1a1a !important; }

/* Force all main content text to dark */
.main .block-container { color: #1a1a1a !important; }
.main p, .main label, .main span, .main div { color: #1a1a1a !important; }

/* Selectbox / radio / text inputs */
div[data-testid="stSelectbox"] label { color: #1a1a1a !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] { background: #fff !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #1a1a1a !important; }
div[data-baseweb="popover"] * { color: #1a1a1a !important; background: #fff !important; }
div[data-testid="stRadio"] label { color: #1a1a1a !important; }
div[data-testid="stRadio"] span { color: #1a1a1a !important; }

/* Tab labels */
button[data-baseweb="tab"] { color: #1a1a1a !important; }
button[data-baseweb="tab"] p { color: #1a1a1a !important; }

/* Markdown text */
div[data-testid="stMarkdownContainer"] p { color: #1a1a1a !important; }
div[data-testid="stMarkdownContainer"] li { color: #1a1a1a !important; }

/* Info / warning / success boxes */
div[data-testid="stAlert"] p { color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

    hdr_col, btn_col = st.columns([6, 1])
    with hdr_col:
        st.markdown("""
    <div style="background:#1a1a1a;color:#f7f7f5;padding:24px 32px;border-radius:12px;margin-bottom:24px;display:flex;align-items:baseline;gap:14px">
      <span style="font-size:24px;font-weight:600;letter-spacing:-0.02em">Admin Dashboard</span>
      <span style="font-size:12px;color:#666;letter-spacing:0.06em">EDD Tracking · Internal</span>
    </div>
    """, unsafe_allow_html=True)
    with btn_col:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True, key="admin_refresh"):
            with st.spinner("Refreshing…"):
                df_gs = load_from_google_sheets()
                st.session_state.df_edd    = df_gs
                st.session_state.gs_loaded = True
            st.rerun()

    tab_overview, tab_users, tab_assign = st.tabs([
        "📊  Overview & Performance",
        "👥  User Management",
        "🗂  Assign Rows",
    ])

    df = _get_df()

    # ── TAB 1: Overview ───────────────────────────────────────────────────────
    with tab_overview:
        if df is None:
            st.info("No EDD data loaded yet. Refresh from the sidebar.")
            return

        assigned_col = get_assigned_to_col(df)

        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:14px">Overall Stats</p>', unsafe_allow_html=True)

        total = len(df)
        assigned = df[assigned_col].astype(str).str.strip().ne("").sum() if assigned_col else 0
        unassigned = total - assigned

        # Status column
        action_col = next((c for c in df.columns if c.strip().lower() == "action_taken"), None)
        done_count = 0
        review_count = 0
        if action_col:
            done_count   = df[action_col].astype(str).str.lower().str.startswith("done").sum()
            review_count = df[action_col].astype(str).str.lower().str.startswith("under review").sum()

        m1, m2, m3, m4, m5 = st.columns(5)
        for col_obj, num, lbl, clr in [
            (m1, total,       "Total Rows",   "#1a1a1a"),
            (m2, assigned,    "Assigned",     "#2d7a4f"),
            (m3, unassigned,  "Unassigned",   "#9a6820"),
            (m4, review_count,"Under Review", "#3a5a8a"),
            (m5, done_count,  "Done",         "#2d7a4f"),
        ]:
            with col_obj:
                st.markdown(metric(num, lbl, clr), unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        # ── Per-user performance ──────────────────────────────────────────────
        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:14px">User Performance</p>', unsafe_allow_html=True)

        non_admin = get_non_admin_users()
        perf_rows = []
        for uname in non_admin:
            display = get_display_name(uname)
            if assigned_col:
                user_df = df[df[assigned_col].astype(str).str.strip().str.lower() == uname.lower()]
            else:
                user_df = pd.DataFrame()

            n_assigned = len(user_df)
            n_done     = 0
            n_review   = 0
            n_form     = 0
            if action_col and not user_df.empty:
                acts = user_df[action_col].astype(str).str.lower()
                n_done   = acts.str.startswith("done").sum()
                n_review = acts.str.startswith("under review").sum()
                n_form   = acts.str.startswith("form sent").sum()

            perf_rows.append({
                "User":         display,
                "Assigned":     n_assigned,
                "Done":         n_done,
                "Under Review": n_review,
                "Form Sent":    n_form,
                "Pending":      max(0, n_assigned - n_done - n_review - n_form),
                "Completion %": f"{int(n_done / n_assigned * 100)}%" if n_assigned else "—",
            })

        if perf_rows:
            perf_df = pd.DataFrame(perf_rows)
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
        else:
            st.info("No non-admin users found.")

        # ── Action log: who did what ──────────────────────────────────────────
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:14px">Row-level Assignments</p>', unsafe_allow_html=True)

        if assigned_col and action_col:
            log_df = df[[assigned_col, action_col]].copy()
            uid_col = next((c for c in df.columns if c.strip().lower() == "user_id"
                            or "user" in c.lower() or "uid" in c.lower()), None)
            if uid_col:
                log_df.insert(0, "User ID", df[uid_col])
            log_df = log_df[log_df[assigned_col].astype(str).str.strip() != ""]
            log_df.columns = [c.replace(assigned_col, "Assigned To").replace(action_col, "Action Taken") for c in log_df.columns]
            st.dataframe(log_df, use_container_width=True, hide_index=True)
        else:
            st.info("Need both 'Assigned To' and 'action_taken' columns in the sheet for the log.")

    # ── TAB 2: User Management ────────────────────────────────────────────────
    with tab_users:
        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:14px">Current Users</p>', unsafe_allow_html=True)

        for uname, meta in USERS.items():
            role_badge = badge("ADMIN", "#1a1a1a", "#f7f7f5") if meta["role"] == ADMIN_ROLE else badge("USER", "#e8edf5", "#3a5a8a")
            st.markdown(
                f'<div style="background:#fff;border:1px solid #e8e8e4;border-radius:8px;padding:12px 18px;'
                f'margin-bottom:8px;display:flex;align-items:center;justify-content:space-between">'
                f'<span style="font-size:14px;font-weight:500;color:#1a1a1a">{meta["display"]}</span>'
                f'{role_badge}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.info(
            "👨‍💻  To add or remove users, edit the `USERS` dictionary in **auth.py**. "
            "Each entry needs a `display` name and a `role` (`admin` or `user`). "
            "Restart the app after saving."
        )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:8px">Quick Guide</p>', unsafe_allow_html=True)
        st.code(
            '# auth.py — USERS dict\n'
            'USERS = {\n'
            '    "Sarah (Admin)": {"display": "Sarah", "role": "admin"},\n'
            '    "Ahmed":         {"display": "Ahmed", "role": "user"},\n'
            '    "Lina":          {"display": "Lina",  "role": "user"},\n'
            '    # Add more here:\n'
            '    # "NewUser": {"display": "New User", "role": "user"},\n'
            '}',
            language="python",
        )

    # ── TAB 3: Assign Rows ────────────────────────────────────────────────────
    with tab_assign:
        if df is None:
            st.info("No EDD data loaded.")
            return

        assigned_col = get_assigned_to_col(df)
        uid_col = next((c for c in df.columns if c.strip().lower() == "user_id"
                        or "user" in c.lower() or "uid" in c.lower()), df.columns[0])

        st.markdown('<p style="font-size:11px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#999;margin-bottom:14px">Assign Rows to Users</p>', unsafe_allow_html=True)

        non_admin = get_non_admin_users()
        if not non_admin:
            st.warning("No non-admin users found.")
            return

        target_user = st.selectbox("Assign to user", non_admin, key="admin_assign_target")

        # Show unassigned rows (or all rows if no assigned_col)
        filter_mode = st.radio("Show", ["Unassigned rows only", "All rows"], horizontal=True, key="admin_assign_filter")

        display_df = df.copy()
        if assigned_col and filter_mode == "Unassigned rows only":
            display_df = display_df[display_df[assigned_col].astype(str).str.strip() == ""]

        if display_df.empty:
            st.success("All rows are already assigned.")
            return

        st.markdown(f"**{len(display_df)} rows shown**")

        # Checkboxes for selection
        if "admin_selected_rows" not in st.session_state:
            st.session_state.admin_selected_rows = set()

        sel_all = st.checkbox(f"Select all ({len(display_df)})", key="admin_sel_all")
        if sel_all:
            st.session_state.admin_selected_rows = set(display_df.index.astype(str).tolist())

        st.markdown("<hr style='border:none;border-top:1px solid #e8e8e4;margin:6px 0 10px 0'>", unsafe_allow_html=True)

        # Render rows
        for ridx, row in display_df.iterrows():
            row_idx_str = str(ridx)
            uid_val     = str(row.get(uid_col, ridx))
            assigned_val = str(row.get(assigned_col, "")).strip() if assigned_col else ""
            assigned_tag = f' → <em style="color:#999;font-size:11px">{assigned_val}</em>' if assigned_val else ""

            cb_col, info_col = st.columns([0.5, 7])
            with cb_col:
                checked = st.checkbox(
                    "sel", value=(row_idx_str in st.session_state.admin_selected_rows),
                    key=f"admin_chk_{row_idx_str}", label_visibility="collapsed",
                )
                if checked: st.session_state.admin_selected_rows.add(row_idx_str)
                else:       st.session_state.admin_selected_rows.discard(row_idx_str)
            with info_col:
                st.markdown(
                    f'<div style="padding-top:4px"><span style="font-size:13px;font-weight:600;color:#1a1a1a">{uid_val}</span>'
                    f'<span style="font-size:11px;color:#bbb"> · row {ridx}</span>{assigned_tag}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("<hr style='border:none;border-top:1px solid #f2f2ef;margin:4px 0'>", unsafe_allow_html=True)

        n_sel = len(st.session_state.admin_selected_rows)
        if n_sel:
            st.markdown(f"**{n_sel} rows selected**")
            if st.button(f"✅ Assign {n_sel} rows to {get_display_name(target_user)}", use_container_width=False, key="admin_assign_btn"):
                row_indices = [int(r) for r in st.session_state.admin_selected_rows]
                ok, msg = bulk_assign_rows(row_indices, target_user)
                if ok:
                    # Update local state
                    if assigned_col:
                        for ridx in row_indices:
                            st.session_state.df_edd.at[ridx, assigned_col] = target_user
                    st.success(msg)
                    st.session_state.admin_selected_rows = set()
                    st.rerun()
                else:
                    st.error(f"Assignment failed: {msg}")