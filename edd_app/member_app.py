
import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f7f5; }

section[data-testid="stSidebar"] { background-color: #1a1a1a; border-right: none; }
section[data-testid="stSidebar"] * { color: #e8e8e4 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stDateInput label {
    color: #999 !important; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aaa !important; }

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.edd-header {
    background: #1a1a1a; color: #f7f7f5;
    padding: 28px 36px; border-radius: 12px; margin-bottom: 24px;
    display: flex; align-items: baseline; gap: 16px;
}
.edd-title    { font-size: 26px; font-weight: 600; letter-spacing: -0.02em; margin: 0; }
.edd-subtitle { font-size: 13px; color: #888; letter-spacing: 0.04em; margin: 0; }

.source-banner {
    display: flex; align-items: center; gap: 10px;
    background: #fff; border: 1px solid #e8e8e4; border-radius: 8px;
    padding: 10px 16px; margin-bottom: 18px; font-size: 12px; color: #666;
}
.source-dot-sheet { width:8px; height:8px; border-radius:50%; background:#34a853; display:inline-block; }
.source-dot-csv   { width:8px; height:8px; border-radius:50%; background:#4285f4; display:inline-block; }

.bulk-count {
    font-size: 12px; font-weight: 600; color: #1a1a1a;
    background: #f0f0ec; border-radius: 4px; padding: 2px 8px;
    font-family: 'DM Mono', monospace;
}
.bulk-hint { font-size: 11px; color: #999; }

.badge {
    display: inline-block; padding: 3px 10px; border-radius: 4px;
    font-size: 11px; font-weight: 500; letter-spacing: 0.04em;
    font-family: 'DM Mono', monospace;
}
.badge-pending      { background: #f0ede8; color: #8a7560; }
.badge-form_sent    { background: #e8edf5; color: #3a5a8a; }
.badge-under_review { background: #fef3e2; color: #9a6820; }
.badge-done         { background: #e8f4ee; color: #2d7a4f; }
.badge-high         { background: #fdecea; color: #c0392b; }
.badge-medium       { background: #fef3e2; color: #9a6820; }
.badge-low          { background: #e8edf5; color: #3a5a8a; }

.metric-box { background: #fff; border: 1px solid #e8e8e4; border-radius: 10px; padding: 20px 24px; text-align: center; }
.metric-num { font-size: 32px; font-weight: 600; color: #1a1a1a; letter-spacing: -0.02em; }
.metric-lbl { font-size: 11px; color: #999; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }

.section-title { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-bottom: 14px; margin-top: 8px; }
.detail-label  { font-size: 11px; color: #999; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px; }
.detail-value  { font-size: 14px; color: #1a1a1a; font-weight: 500; margin-bottom: 16px; }

.alert-chip {
    display: inline-block; padding: 2px 9px; border-radius: 3px;
    font-size: 11px; font-family: 'DM Mono', monospace;
    background: #1a1a1a; color: #f7f7f5; letter-spacing: 0.03em;
}

/* UserTool panel styles */
.ut-section { font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #bbb; margin: 14px 0 8px 0; }
.ut-card { background: #fafaf8; border: 1px solid #ebebea; border-radius: 8px; padding: 14px 16px; margin-bottom: 10px; }
.ut-key { font-size: 10px; color: #aaa; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 1px; }
.ut-val { font-size: 13px; color: #1a1a1a; font-weight: 500; word-break: break-all; }
.ut-badge-active   { display:inline-block; padding:2px 8px; border-radius:3px; font-size:11px; background:#e8f4ee; color:#2d7a4f; font-family:'DM Mono',monospace; }
.ut-badge-inactive { display:inline-block; padding:2px 8px; border-radius:3px; font-size:11px; background:#fdecea; color:#c0392b; font-family:'DM Mono',monospace; }
.ut-badge-neutral  { display:inline-block; padding:2px 8px; border-radius:3px; font-size:11px; background:#f0ede8; color:#8a7560; font-family:'DM Mono',monospace; }
.ut-loading { color:#bbb; font-size:13px; padding: 20px 0; text-align:center; }
.ut-error   { color:#c0392b; font-size:12px; background:#fdecea; border-radius:6px; padding:10px 14px; }

div[data-testid="stCheckbox"] { margin-bottom: 0 !important; padding: 0 !important; }
div[data-testid="stCheckbox"] label { font-size: 13px !important; color: #1a1a1a !important; }
div[data-testid="stCheckbox"] label p { color: #1a1a1a !important; }
div[data-testid="stCheckbox"] span { color: #1a1a1a !important; }

.stButton > button {
    border-radius: 7px; font-family: 'DM Sans', sans-serif;
    font-weight: 500; font-size: 13px;
    border: 1px solid #1a1a1a !important;
    background: #fff !important; color: #1a1a1a !important;
    padding: 6px 16px; transition: all 0.15s;
}
.stButton > button:hover { background: #1a1a1a !important; color: #fff !important; }
.stButton > button p { color: #1a1a1a !important; }
.stButton > button:hover p { color: #fff !important; }

.stLinkButton > a {
    border: 1px solid #1a1a1a !important;
    background: #fff !important; color: #1a1a1a !important;
    border-radius: 7px; font-size: 13px; font-weight: 500;
}
.stLinkButton > a:hover { background: #1a1a1a !important; color: #fff !important; }

.uid-text { font-size: 13px; font-weight: 600; color: #1a1a1a !important; }
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── All-fields expander ─────────────────────────────────────────────────── */
div[data-testid="stExpander"] > details > summary {
    background-color: #1a1a1a !important; color: #f7f7f5 !important;
    border-radius: 7px !important; padding: 8px 14px !important;
    font-size: 13px !important; font-weight: 500 !important;
}
div[data-testid="stExpander"] > details > summary:hover { background-color: #333 !important; }
div[data-testid="stExpander"] > details > summary svg { fill: #f7f7f5 !important; }

/* ── Modal card ──────────────────────────────────────────────────────────── */
.edd-modal {
    background: #fff; border-radius: 16px; border: 1px solid #e0e0dc;
    width: 100%; overflow: hidden; margin-bottom: 24px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
}
.edd-modal-header {
    padding: 20px 26px 16px; border-bottom: 1px solid #f0f0ec;
    display: flex; align-items: center; justify-content: space-between;
}
.edd-modal-avatar {
    width: 44px; height: 44px; border-radius: 50%;
    background: #f0f0ec; border: 1px solid #e8e8e4;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600; color: #555; flex-shrink: 0;
}
.edd-modal-uid { font-size: 16px; font-weight: 600; color: #1a1a1a; margin: 0; }
.edd-modal-sub { font-size: 12px; color: #999; margin: 2px 0 0 0; }
.edd-modal-nav {
    display: flex; border-bottom: 1px solid #f0f0ec; padding: 0 26px;
    overflow-x: auto; background: #fafaf8;
}
.edd-modal-nav-tab {
    font-size: 12px; font-weight: 500; padding: 11px 16px;
    color: #999; border-bottom: 2px solid transparent;
    white-space: nowrap;
}
.edd-modal-nav-tab.active { color: #1a1a1a; border-bottom-color: #1a1a1a; }
.edd-modal-body { padding: 22px 26px; }
.edd-modal-section {
    font-size: 10px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #bbb; margin: 18px 0 10px 0;
}
.edd-modal-section:first-child { margin-top: 0; }
.edd-modal-field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 28px; }
.edd-modal-field { margin-bottom: 14px; }
.edd-modal-field-label { font-size: 10px; color: #bbb; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 3px; }
.edd-modal-field-value { font-size: 13px; color: #1a1a1a; font-weight: 500; word-break: break-word; }
.edd-modal-divider { border: none; border-top: 1px solid #f0f0ec; margin: 16px 0; }
.edd-modal-footer {
    padding: 14px 26px; border-top: 1px solid #f0f0ec;
    background: #fafaf8; display: flex; align-items: center; gap: 8px;
}
.edd-doc-chip {
    display: inline-block; padding: 4px 12px; border-radius: 5px;
    font-size: 11px; background: #f0f0ec; color: #1a1a1a;
    border: 1px solid #e8e8e4; margin: 2px 4px 2px 0; text-decoration: none;
}
.edd-doc-chip:hover { background: #1a1a1a; color: #fff; }
.edd-modal-close-btn {
    width: 28px; height: 28px; border-radius: 50%;
    background: #f0f0ec; border: 1px solid #e0e0dc;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; color: #666; cursor: default; flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
STATUS_OPTIONS = ["Pending", "Form Sent", "Under Review", "Done"]
BADGE_MAP = {
    "Pending": "badge-pending", "Form Sent": "badge-form_sent",
    "Under Review": "badge-under_review", "Done": "badge-done",
}
PAGE_SIZE = 20



def badge_html(status, extra=""):
    cls = BADGE_MAP.get(status, "badge-pending")
    return f'<span class="badge {cls}" style="{extra}">{status}</span>'

def risk_badge(risk):
    cls = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(risk,"badge-pending")
    return f'<span class="badge {cls}">{risk}</span>'

# ── Sheet helpers (imported from sheets.py) ────────────────────────────────────
from sheets import (
    load_from_google_sheets,
    write_action_to_sheet,
    write_assigned_to_sheet,
    bulk_assign_rows,
    get_assigned_to_col,
    is_row_assigned_to_other,
    is_row_assigned_to_me,
    get_usertool_token,
)

# ── UserTool API ───────────────────────────────────────────────────────────────
USERTOOL_BASE = "google"

def fetch_usertool(uid: str) -> dict:
    """
    Call the UserTool API for a given user ID.
    Returns {"ok": True, "data": {...}} or {"ok": False, "error": "..."}.
    Token is read from USERTOOL_ADMIN_TOKEN in .env
    """
    token = get_usertool_token()
    if not token:
        return {"ok": False, "error": "USERTOOL_ADMIN_TOKEN not set in .env"}

    url = f"https://admin-service.thndr-internal.app/compliance-service/admin/account-forms/VMsGQAe1eabXWcI4DOTs6A7rMiB2"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://usertool.thndr-internal.app",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {token}",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return {"ok": True, "data": resp.json()}
        else:
            return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _ut_badge(val):
    """Return a coloured badge for boolean-ish values."""
    s = str(val).lower()
    if s in ("true", "yes", "active", "verified", "approved", "1"):
        return f'<span class="ut-badge-active">{val}</span>'
    if s in ("false", "no", "inactive", "rejected", "blocked", "0"):
        return f'<span class="ut-badge-inactive">{val}</span>'
    return f'<span class="ut-badge-neutral">{val}</span>'


def render_usertool_panel(uid: str):
    """
    Render the UserTool info panel for a given uid.
    Uses st.session_state to cache per-uid so we don't re-fetch on every rerun.
    """
    cache_key = f"ut_cache_{uid}"

    # ── Fetch / cache ──────────────────────────────────────────────────────────
    if cache_key not in st.session_state:
        with st.spinner(f"Fetching UserTool data for {uid}…"):
            result = fetch_usertool(uid)
        st.session_state[cache_key] = result
    else:
        result = st.session_state[cache_key]

    # Refresh button
    if st.button("🔄 Refresh UserTool", key=f"ut_refresh_{uid}", use_container_width=False):
        with st.spinner("Refreshing…"):
            result = fetch_usertool(uid)
        st.session_state[cache_key] = result
        st.rerun()

    if not result["ok"]:
        st.markdown(f'<div class="ut-error">⚠ {result["error"]}</div>', unsafe_allow_html=True)
        return

    data = result["data"]

    # ── Render: walk the JSON and display every field nicely ──────────────────
    def render_value(key, val, indent=0):
        """Recursively render a JSON value."""
        if isinstance(val, dict):
            st.markdown(f'<div class="ut-section" style="margin-left:{indent*12}px">{key}</div>', unsafe_allow_html=True)
            for k, v in val.items():
                render_value(k, v, indent + 1)
        elif isinstance(val, list):
            st.markdown(f'<div class="ut-section" style="margin-left:{indent*12}px">{key} ({len(val)})</div>', unsafe_allow_html=True)
            for i, item in enumerate(val):
                render_value(f"[{i}]", item, indent + 1)
        elif isinstance(val, bool):
            st.markdown(
                f'<div style="margin-left:{indent*12}px;margin-bottom:10px">'
                f'<div class="ut-key">{key}</div>'
                f'<div>{_ut_badge(val)}</div></div>',
                unsafe_allow_html=True,
            )
        elif val is None or str(val).strip() in ("", "None", "null"):
            pass  # skip empty fields silently
        else:
            # Check if it's a URL → make it a link
            sval = str(val)
            display = f'<a href="{sval}" target="_blank" style="color:#3a5a8a;font-size:13px">{sval[:60]}{"…" if len(sval)>60 else ""}</a>' \
                      if sval.startswith("http") else \
                      f'<span class="ut-val">{sval}</span>'
            st.markdown(
                f'<div style="margin-left:{indent*12}px;margin-bottom:10px">'
                f'<div class="ut-key">{key}</div>'
                f'<div>{display}</div></div>',
                unsafe_allow_html=True,
            )

    if isinstance(data, dict):
        for k, v in data.items():
            render_value(k, v)
    else:
        # API returned a list or scalar at root
        st.json(data)


# ── Session state ──────────────────────────────────────────────────────────────
DEFAULTS = {
    "edd_statuses": {}, "alert_statuses": {},
    "form_sent_log": {}, "alert_form_log": {},
    "df_edd": None, "df_alerts": None,
    "selected_edd_idx": None,
    "edd_page": 0,
    "selected_alert_idx": None,
    "edd_source": "gsheet",
    "gs_loaded": False,
    "edd_checked": set(),
    "alert_checked": set(),
    "edd_hidden": set(),
    "edd_deleted": set(),
    "alert_hidden": set(),
    "alert_deleted": set(),
    "show_hidden_edd": False,
    # detail panel tab: "submission" | "usertool"
    "detail_tab": "submission",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get_edd_status(row_idx):
    row_idx = str(row_idx)
    if row_idx in st.session_state.edd_statuses:
        return st.session_state.edd_statuses[row_idx]
    df = st.session_state.get("df_edd")
    if df is not None:
        try:
            action_col = next(
                (c for c in df.columns if c.strip().lower() == "action_taken"), None,
            )
            if action_col:
                raw = str(df.loc[int(row_idx), action_col]).strip()
                if raw and raw.lower() not in ("", "nan", "none"):
                    label = raw.split(" — ")[0].strip()
                    if label in STATUS_OPTIONS:
                        return label
                    return raw[:40]
        except Exception:
            pass
    return "Pending"

def set_edd_status(row_idx, s): st.session_state.edd_statuses[str(row_idx)] = s
def get_alert_status(idx):      return st.session_state.alert_statuses.get(str(idx), "Pending")
def set_alert_status(idx, s):   st.session_state.alert_statuses[str(idx)] = s

# ── Auto-connect ───────────────────────────────────────────────────────────────
if not st.session_state.gs_loaded:
    with st.spinner("Connecting to Google Sheets…"):
        df_gs = load_from_google_sheets()
        st.session_state.df_edd    = df_gs
        st.session_state.gs_loaded = True
        st.session_state.edd_source = "gsheet"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### EDD Tracking")
    st.markdown("---")

    st.markdown("**EDD Data Source**")
    use_gsheet = st.toggle(
        "Use Google Sheets",
        value=(st.session_state.edd_source == "gsheet"),
        key="toggle_gsheet",
    )
    new_source = "gsheet" if use_gsheet else "csv"
    if new_source != st.session_state.edd_source:
        st.session_state.edd_source  = new_source
        st.session_state.df_edd      = None
        st.session_state.gs_loaded   = False
        st.session_state.edd_checked = set()
        st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if not use_gsheet:
        st.markdown("**EDD Sheet (CSV)**")
        up_edd = st.file_uploader("EDD CSV", type=["csv"], key="up_edd", label_visibility="collapsed")
        if up_edd:
            df_raw = pd.read_csv(up_edd)
            df_raw.columns = [c.strip() for c in df_raw.columns]
            st.session_state.df_edd      = df_raw
            st.session_state.gs_loaded   = False
            st.session_state.edd_checked = set()
            st.success(f"{len(df_raw)} EDD records loaded")
    else:
        if st.session_state.gs_loaded and st.session_state.df_edd is not None:
            n_rows = len(st.session_state.df_edd)
            st.markdown(
                f'<div style="background:#2a2a2a;border-radius:8px;padding:12px 14px;margin-bottom:10px">'
                f'<span style="color:#34a853;font-size:12px">● Connected</span>'
                f'<span style="color:#888;font-size:12px"> · {n_rows} rows loaded</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if st.button("🔄 Refresh from Sheet", use_container_width=True, key="gs_refresh_btn"):
            with st.spinner("Refreshing…"):
                df_gs = load_from_google_sheets()
                st.session_state.df_edd      = df_gs
                st.session_state.gs_loaded   = True
                st.session_state.edd_checked = set()
            st.success(f"Refreshed — {len(df_gs)} rows")
            st.rerun()

    st.markdown("---")
    st.markdown("**Alerts Sheet (CSV)**")
    up_alerts = st.file_uploader("Alerts CSV", type=["csv"], key="up_alerts", label_visibility="collapsed")
    if up_alerts:
        df_a = pd.read_csv(up_alerts)
        df_a.columns = [c.strip() for c in df_a.columns]
        st.session_state.df_alerts = df_a
        st.success(f"{len(df_a)} alerts loaded")

    st.markdown("---")
    st.markdown("**Filters**")
    status_filter = st.multiselect("Status", STATUS_OPTIONS, default=STATUS_OPTIONS, key="sb_status")

    date_range = None
    uid_search = ""
    if st.session_state.df_edd is not None:
        cols_edd    = list(st.session_state.df_edd.columns)
        date_col_sb = next(
            (c for c in cols_edd if "submitted" in c.lower() or "date" in c.lower() or "time" in c.lower()),
            cols_edd[0],
        )
        try:
            st.session_state.df_edd[date_col_sb] = pd.to_datetime(
                st.session_state.df_edd[date_col_sb], errors="coerce"
            )
            valid = st.session_state.df_edd[date_col_sb].dropna()
            if not valid.empty:
                date_range = st.date_input(
                    "Date Range",
                    value=(valid.min().date(), valid.max().date()),
                    min_value=valid.min().date(),
                    max_value=valid.max().date(),
                )
        except Exception:
            pass
        uid_search = st.text_input("Search User ID", placeholder="Type to filter…")

    st.markdown("---")
    show_hidden = st.toggle(
        "Show hidden rows",
        value=st.session_state.show_hidden_edd,
        key="show_hidden_toggle",
    )
    st.session_state.show_hidden_edd = show_hidden
    st.markdown("---")
    st.caption("Session only — statuses reset on refresh")

# ── Page header ────────────────────────────────────────────────────────────────
src_label = "Google Sheets" if st.session_state.edd_source == "gsheet" else "CSV Upload"
src_dot   = "source-dot-sheet" if st.session_state.edd_source == "gsheet" else "source-dot-csv"
_cur_user = st.session_state.get("current_user", "")

hdr_col, btn_col = st.columns([6, 1])
with hdr_col:
    st.markdown(f"""
<div class="edd-header">
  <p class="edd-title">EDD Tracking</p>
  <p class="edd-subtitle">Enhanced Due Diligence Portal &nbsp;·&nbsp; Welcome, <strong>{_cur_user}</strong></p>
</div>
""", unsafe_allow_html=True)
with btn_col:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True, key="member_signout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown(
    f'<div class="source-banner"><span class="{src_dot}"></span>'
    f'EDD source: <strong>{src_label}</strong>'
    + (' &nbsp;·&nbsp; connected via secrets.toml' if st.session_state.gs_loaded else '')
    + '</div>',
    unsafe_allow_html=True,
)

tab_edd, tab_alerts = st.tabs(["📋  EDD Cases", "🔔  Alerts"])

# ══════════════════════════════════════════════════════════════════════════════
# BULK TOOLBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_bulk_toolbar(checked: set, page_ids: list, all_ids: list, prefix: str):
    n_checked   = len(checked)
    n_page      = len(page_ids)
    n_all       = len(all_ids)
    all_page_on = bool(page_ids) and all(i in checked for i in page_ids)
    all_on      = bool(all_ids)  and all(i in checked for i in all_ids)
    current_user = st.session_state.get("current_user", "")

    sc1, sc2, sc3, sc4 = st.columns([2, 2, 2, 4])
    with sc1:
        if st.checkbox(f"This page ({n_page})", value=all_page_on, key=f"{prefix}_sel_page"):
            for i in page_ids: checked.add(i)
        else:
            if all_page_on:
                for i in page_ids: checked.discard(i)
    with sc2:
        if st.checkbox(f"All ({n_all})", value=all_on, key=f"{prefix}_sel_all"):
            for i in all_ids: checked.add(i)
        else:
            if all_on: checked.clear()
    with sc3:
        if n_checked and st.button("Clear selection", key=f"{prefix}_clear_sel", use_container_width=True):
            checked.clear(); st.rerun()
    with sc4:
        if n_checked:
            st.markdown(
                f'<div style="padding:6px 0"><span class="bulk-count">{n_checked} selected</span>'
                f' <span class="bulk-hint">— choose an action below</span></div>',
                unsafe_allow_html=True,
            )

    if n_checked:
        # ── Bulk self-assign (EDD tab only) ───────────────────────────────────
        if prefix == "edd" and current_user:
            df_live = st.session_state.get("df_edd")
            assigned_col = get_assigned_to_col(df_live) if df_live is not None else None
            if assigned_col:
                assignable = [
                    r for r in checked
                    if str(df_live.at[int(r), assigned_col]).strip() in ("", "nan")
                    or str(df_live.at[int(r), assigned_col]).strip().lower() == current_user.lower()
                ]
                locked_count = n_checked - len(assignable)
                lbl = f"🙋 Assign {len(assignable)} to me" + (f" ({locked_count} locked)" if locked_count else "")
                if st.button(lbl, key="edd_bulk_self_assign"):
                    if assignable:
                        ok, msg = bulk_assign_rows([int(r) for r in assignable], current_user)
                        if ok:
                            for r in assignable:
                                st.session_state.df_edd.at[int(r), assigned_col] = current_user
                            st.success(f"Assigned {len(assignable)} rows to you")
                            checked.clear(); st.rerun()
                        else:
                            st.error(f"Failed: {msg}")
                    else:
                        st.warning("All selected rows are locked by other users.")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        ab1, ab2, ab3, ab4, ab5 = st.columns(5)
        with ab1:
            if st.button("📤 Form Sent", use_container_width=True, key=f"{prefix}_bulk_formsent"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                for ridx in list(checked):
                    if prefix == "edd":
                        set_edd_status(ridx, "Form Sent")
                        st.session_state.form_sent_log[ridx] = {"uid": ridx, "at": ts}
                        write_action_to_sheet(ridx, f"Form Sent — {ts}")
                    else:
                        set_alert_status(ridx, "Form Sent")
                        st.session_state.alert_form_log[ridx] = ts
                st.success(f"Marked {n_checked} as Form Sent")
                checked.clear(); st.rerun()
        with ab2:
            if st.button("🔍 Under Review", use_container_width=True, key=f"{prefix}_bulk_review"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                for ridx in list(checked):
                    if prefix == "edd":
                        set_edd_status(ridx, "Under Review")
                        write_action_to_sheet(ridx, f"Under Review — {ts}")
                    else:
                        set_alert_status(ridx, "Under Review")
                st.success(f"Marked {n_checked} as Under Review")
                checked.clear(); st.rerun()
        with ab3:
            if st.button("✔ Mark Done", use_container_width=True, key=f"{prefix}_bulk_done"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                for ridx in list(checked):
                    if prefix == "edd":
                        set_edd_status(ridx, "Done")
                        write_action_to_sheet(ridx, f"Done — {ts}")
                    else:
                        set_alert_status(ridx, "Done")
                st.success(f"Marked {n_checked} as Done")
                checked.clear(); st.rerun()
        with ab4:
            if st.button("🙈 Hide", use_container_width=True, key=f"{prefix}_bulk_hide"):
                for ridx in list(checked):
                    st.session_state[f"{prefix}_hidden"].add(ridx)
                st.success(f"Hidden {n_checked} row(s)")
                checked.clear(); st.rerun()
        with ab5:
            if st.button("🗑 Delete", use_container_width=True, key=f"{prefix}_bulk_delete"):
                for ridx in list(checked):
                    st.session_state[f"{prefix}_deleted"].add(ridx)
                st.warning(f"Deleted {n_checked} row(s) from this session")
                checked.clear(); st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# EDD TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_edd:
    if st.session_state.df_edd is None:
        st.info("Loading data…" if use_gsheet else "Upload an EDD CSV in the sidebar to get started.")
        st.stop()

    df = st.session_state.df_edd.copy()
    df["_row_idx"] = df.index.astype(str)
    cols = list(df.columns)

    date_col    = next((c for c in cols if "submitted" in c.lower()), None) \
                  or next((c for c in cols if "date" in c.lower() or "time" in c.lower()), cols[0])
    uid_col     = next((c for c in cols if c.strip().lower() == "user_id"), None) \
                  or next((c for c in cols if "user" in c.lower() or "uid" in c.lower()), cols[1])
    src_col     = next((c for c in cols if "funding" in c.lower() or "source of income" in c.lower() or "primary" in c.lower()), None)
    emp_col     = next((c for c in cols if "employer" in c.lower()), None)
    job_col     = next((c for c in cols if "job titl" in c.lower() or "occupation" in c.lower()), None)
    inc_col     = next((c for c in cols if "monthly income" in c.lower() and "business" not in c.lower()), None)
    country_col = next((c for c in cols if "country of resid" in c.lower() or "residency" in c.lower()), None)
    notes_col   = next((c for c in cols if c.strip().lower() in ("added to notes","notes","note")), None)
    review_col  = next((c for c in cols if c.strip().lower() in ("response","duplication check","status")), None)
    doc_cols    = [c for c in cols if "upload document" in c.lower() or c.strip().lower().startswith("upload")]

    try:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    except Exception:
        pass

    df["_status"] = df["_row_idx"].apply(get_edd_status)

    show_hidden = st.session_state.show_hidden_edd
    assigned_col = get_assigned_to_col(df)
    visible_df  = df[~df["_row_idx"].isin(st.session_state.edd_deleted)]
    if not show_hidden:
        visible_df = visible_df[~visible_df["_row_idx"].isin(st.session_state.edd_hidden)]
    # Members only see rows assigned to them
    if assigned_col:
        visible_df = visible_df[
            visible_df[assigned_col].astype(str).str.strip().str.lower() == _cur_user.lower()
        ]

    filtered = visible_df.copy()
    if date_range and len(date_range) == 2:
        try:
            filtered = filtered[
                (filtered[date_col].dt.date >= date_range[0]) &
                (filtered[date_col].dt.date <= date_range[1])
            ]
        except Exception:
            pass
    if uid_search:
        filtered = filtered[filtered[uid_col].astype(str).str.contains(uid_search, case=False, na=False)]
    if status_filter:
        filtered = filtered[filtered["_status"].isin(status_filter)]

    # Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    for col_obj, num, lbl in [
        (m1, len(visible_df), "Total"),
        (m2, (visible_df["_status"]=="Pending").sum(), "Pending"),
        (m3, (visible_df["_status"]=="Form Sent").sum(), "Form Sent"),
        (m4, (visible_df["_status"]=="Under Review").sum(), "Under Review"),
        (m5, (visible_df["_status"]=="Done").sum(), "Done"),
    ]:
        with col_obj:
            st.markdown(f'<div class="metric-box"><div class="metric-num">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ── Modal card: shown above the list when a row is selected ───────────────
    sel_idx = st.session_state.selected_edd_idx
    if sel_idx is not None:
        try:
            row = df.loc[int(sel_idx)]
        except (KeyError, ValueError):
            row = None

        if row is not None:
            status  = get_edd_status(sel_idx)
            uid     = str(row[uid_col]) if uid_col in row.index else sel_idx
            initials = (uid.replace("-","")[:2]).upper()
            badge_cls = BADGE_MAP.get(status, "badge-pending")

            def fld(label, val, wide=False):
                try:
                    empty = pd.isna(val) or str(val).strip() == ""
                except Exception:
                    empty = False
                if empty:
                    return ""
                span = "grid-column:1/-1;" if wide else ""
                return (
                    f'<div class="edd-modal-field" style="{span}">' 
                    f'<div class="edd-modal-field-label">{label}</div>'
                    f'<div class="edd-modal-field-value">{val}</div>'
                    f'</div>'
                )

            date_val = row.get(date_col, "") if date_col else ""
            try: date_val = pd.to_datetime(date_val).strftime("%d %b %Y  %H:%M")
            except Exception: pass

            shown_cols = set()
            pfields = ""
            for label, cn in [
                ("Submitted At", date_col), ("Country", country_col),
                ("Primary Funding", src_col), ("Employer", emp_col),
                ("Job Title", job_col), ("Monthly Income", inc_col),
                ("Review Status", review_col), ("Notes", notes_col),
            ]:
                if cn and cn in row.index:
                    shown_cols.add(cn)
                    v = date_val if label == "Submitted At" else row[cn]
                    pfields += fld(label, v, wide=(label in ("Notes","Primary Funding")))

            skip_cols = {"_row_idx","_status", uid_col} | set(doc_cols)
            ofields = ""
            for cn in cols:
                if cn in shown_cols or cn in skip_cols or cn.startswith("_"): continue
                if cn not in row.index: continue
                short = cn[:50] + ("…" if len(cn)>50 else "")
                ofields += fld(short, row[cn])

            links = [
                (dc, str(row[dc])) for dc in doc_cols
                if dc in row.index and pd.notna(row[dc]) and str(row[dc]).strip().startswith("http")
            ]
            docs_html = ""
            if links:
                docs_html = '<div class="edd-modal-section">Documents</div>'
                for i, (dc, link) in enumerate(links):
                    docs_html += f'<a class="edd-doc-chip" href="{link}" target="_blank">Doc {i+1}</a>'
            elif doc_cols:
                docs_html = '<div class="edd-modal-section">Documents</div><small style="color:#bbb">No document links found</small>'

            other_sec = f'<div class="edd-modal-section">All fields</div><div class="edd-modal-field-grid">{ofields}</div>' if ofields else ""

            # Render modal as in-page card HTML
            st.markdown(f"""
<div class="edd-modal">
  <div class="edd-modal-header">
    <div style="display:flex;align-items:center;gap:14px;">
      <div class="edd-modal-avatar">{initials}</div>
      <div>
        <p class="edd-modal-uid">{uid}</p>
        <p class="edd-modal-sub">EDD Submission &middot; Row {sel_idx}</p>
      </div>
    </div>
    <span class="badge {badge_cls}">{status}</span>
  </div>
  <div class="edd-modal-nav">
    <span class="edd-modal-nav-tab active">Submission Info</span>
    <span class="edd-modal-nav-tab">UserTool Info</span>
  </div>
  <div class="edd-modal-body">
    <div class="edd-modal-field-grid">{pfields}</div>
    {other_sec}
    {docs_html}
    <hr class="edd-modal-divider">
    <div class="edd-modal-section">Update Status</div>
  </div>
</div>
""", unsafe_allow_html=True)

            # Action row — Streamlit widgets rendered right below the card
            _cur_user = st.session_state.get("current_user", "")
            ac1, ac2, ac3, ac4, ac5 = st.columns([3, 2, 2, 2, 1])
            with ac1:
                new_s = st.selectbox(
                    "status", STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0,
                    key=f"edd_sel_{sel_idx}", label_visibility="collapsed",
                )
            with ac2:
                if st.button("Save Status", use_container_width=True, key=f"edd_save_{sel_idx}"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    set_edd_status(sel_idx, new_s)
                    write_action_to_sheet(sel_idx, f"{new_s} — {ts}")
                    if _cur_user:
                        write_assigned_to_sheet(int(sel_idx), _cur_user)
                        assigned_col_name = get_assigned_to_col(st.session_state.df_edd)
                        if assigned_col_name:
                            st.session_state.df_edd.at[int(sel_idx), assigned_col_name] = _cur_user
                    if new_s == "Form Sent":
                        st.session_state.form_sent_log[sel_idx] = {"uid": uid, "at": ts}
                    st.success("Saved"); st.rerun()
            with ac3:
                if st.button("Send Form", use_container_width=True, key=f"edd_send_{sel_idx}"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    set_edd_status(sel_idx, "Form Sent")
                    write_action_to_sheet(sel_idx, f"Form Sent — {ts}")
                    if _cur_user:
                        write_assigned_to_sheet(int(sel_idx), _cur_user)
                        assigned_col_name = get_assigned_to_col(st.session_state.df_edd)
                        if assigned_col_name:
                            st.session_state.df_edd.at[int(sel_idx), assigned_col_name] = _cur_user
                    st.session_state.form_sent_log[sel_idx] = {"uid": uid, "at": ts}
                    st.success("Marked Form Sent"); st.rerun()
            with ac4:
                if st.button("Mark Done", use_container_width=True, key=f"edd_done_{sel_idx}"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    set_edd_status(sel_idx, "Done")
                    write_action_to_sheet(sel_idx, f"Done — {ts}")
                    if _cur_user:
                        write_assigned_to_sheet(int(sel_idx), _cur_user)
                        assigned_col_name = get_assigned_to_col(st.session_state.df_edd)
                        if assigned_col_name:
                            st.session_state.df_edd.at[int(sel_idx), assigned_col_name] = _cur_user
                    st.success("Marked Done"); st.rerun()
            with ac5:
                if st.button("Close", use_container_width=True, key="edd_close"):
                    st.session_state.selected_edd_idx = None; st.rerun()

            # Delete + UserTool expander
            dx, _ = st.columns([2, 6])
            with dx:
                if st.button("Delete row", use_container_width=True, key=f"edd_del_{sel_idx}"):
                    st.session_state.edd_deleted.add(sel_idx)
                    st.session_state.selected_edd_idx = None
                    st.warning("Row deleted from this session"); st.rerun()

            with st.expander("UserTool Info", expanded=False):
                render_usertool_panel(uid)

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Submission list (full width) ──────────────────────────────────────────
    if filtered.empty:
        st.markdown('<p class="section-title">Submissions</p>', unsafe_allow_html=True)
        st.info("No submissions match the current filters.")
    else:
        total_rows  = len(filtered)
        total_pages = max(1, -(-total_rows // PAGE_SIZE))
        if st.session_state.edd_page >= total_pages:
            st.session_state.edd_page = 0
        page    = st.session_state.edd_page
        page_df = filtered.iloc[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]

        uid_totals: dict  = filtered[uid_col].astype(str).value_counts().to_dict()
        uid_running: dict = {}
        uid_label_map: dict = {}
        for ridx, brow in filtered.iterrows():
            bu = str(brow[uid_col])
            uid_running[bu] = uid_running.get(bu, 0) + 1
            uid_label_map[str(ridx)] = bu if uid_totals.get(bu, 1) == 1 else f"{bu} ({uid_running[bu]})"

        page_ids = [str(ridx) for ridx, _ in page_df.iterrows()]
        all_ids  = [str(ridx) for ridx, _ in filtered.iterrows()]

        th1, th2 = st.columns([3, 2])
        with th1:
            st.markdown(
                f'<p class="section-title" style="margin-bottom:4px">Submissions</p>'
                f'<span style="font-size:11px;color:#bbb">{total_rows} total &middot; page {page+1} of {total_pages}</span>',
                unsafe_allow_html=True,
            )
        with th2:
            pb1, pb2 = st.columns(2)
            with pb1:
                if st.button("← Prev", use_container_width=True, key="edd_prev", disabled=(page==0)):
                    st.session_state.edd_page -= 1; st.rerun()
            with pb2:
                if st.button("Next →", use_container_width=True, key="edd_next", disabled=(page>=total_pages-1)):
                    st.session_state.edd_page += 1; st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        render_bulk_toolbar(st.session_state.edd_checked, page_ids, all_ids, "edd")
        st.markdown("<hr style='border:none;border-top:1px solid #e8e8e4;margin:6px 0 10px 0'>", unsafe_allow_html=True)

        for ridx, row in page_df.iterrows():
            row_idx     = str(ridx)
            uid         = str(row[uid_col])
            status      = get_edd_status(row_idx)
            uid_display = uid_label_map.get(row_idx, uid)
            is_hidden   = row_idx in st.session_state.edd_hidden

            try:
                ts_str = pd.to_datetime(row[date_col]).strftime("%d %b %Y") if pd.notna(row[date_col]) else "—"
            except Exception:
                ts_str = "—"

            funding_tag = ""
            if src_col and src_col in row.index and pd.notna(row.get(src_col)):
                raw   = str(row[src_col])
                short = raw.split(",")[0].split("-")[0].strip()[:32]
                funding_tag = f'<small style="color:#bbb"> · {short}{"…" if len(raw)>32 else ""}</small>'

            row_opacity = "opacity:0.45;" if is_hidden else ""

            cb_col, info_col, badge_col, btn_col = st.columns([0.5, 3.5, 2, 1])
            with cb_col:
                checked_val = st.checkbox(
                    "sel", value=(row_idx in st.session_state.edd_checked),
                    key=f"chk_edd_{row_idx}", label_visibility="collapsed",
                )
                if checked_val: st.session_state.edd_checked.add(row_idx)
                else:           st.session_state.edd_checked.discard(row_idx)
            with info_col:
                hidden_tag = ' <small style="color:#bbb;font-size:10px">[hidden]</small>' if is_hidden else ""
                st.markdown(
                    f'<div style="{row_opacity}padding-top:4px">'
                    f'<span class="uid-text">{uid_display}</span>{hidden_tag}{funding_tag}'
                    f'<br><small style="color:#999">{ts_str}</small></div>',
                    unsafe_allow_html=True,
                )
            with badge_col:
                st.markdown(f'<div style="{row_opacity}padding-top:8px">{badge_html(status)}</div>', unsafe_allow_html=True)
            with btn_col:
                btn_label = "Show" if is_hidden else "View"
                if st.button(btn_label, key=f"edd_v_{row_idx}", use_container_width=True):
                    if is_hidden: st.session_state.edd_hidden.discard(row_idx)
                    else:
                        st.session_state.selected_edd_idx = row_idx
                        st.session_state.detail_tab = "submission"
                    st.rerun()
            st.markdown("<hr style='border:none;border-top:1px solid #f2f2ef;margin:4px 0'>", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        bp1, bp2, bp3 = st.columns([1, 2, 1])
        with bp1:
            if st.button("← Prev ", use_container_width=True, key="edd_prev2", disabled=(page==0)):
                st.session_state.edd_page -= 1; st.rerun()
        with bp2:
            jump = st.number_input("Go to page", min_value=1, max_value=total_pages,
                value=page+1, step=1, key="edd_jump", label_visibility="collapsed")
            if int(jump)-1 != page:
                st.session_state.edd_page = int(jump)-1; st.rerun()
        with bp3:
            if st.button(" Next →", use_container_width=True, key="edd_next2", disabled=(page>=total_pages-1)):
                st.session_state.edd_page += 1; st.rerun()

    # Form sent log
    if st.session_state.form_sent_log:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown('<p class="section-title">Form Sent Log</p>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {
                "Row #": ridx,
                "User ID": v["uid"] if isinstance(v, dict) else ridx,
                "Form Sent At": v["at"] if isinstance(v, dict) else v,
                "Current Status": get_edd_status(ridx),
            }
            for ridx, v in st.session_state.form_sent_log.items()
        ]), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# ALERTS TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_alerts:
    if st.session_state.df_alerts is None:
        st.info("Upload an Alerts CSV in the sidebar to load alerts.")
        st.markdown("**Expected columns:** Timestamp · User ID · Triggered Alert")
    else:
        da    = st.session_state.df_alerts.copy()
        acols = list(da.columns)

        a_uid_col  = next((c for c in acols if "user" in c.lower() or "uid" in c.lower() or "id" in c.lower()), acols[0])
        a_ts_col   = next((c for c in acols if "time" in c.lower() or "date" in c.lower()), acols[0])
        a_type_col = next((c for c in acols if "alert" in c.lower() or "trigger" in c.lower() or "type" in c.lower()), acols[min(2, len(acols)-1)])

        try:
            da[a_ts_col] = pd.to_datetime(da[a_ts_col], errors="coerce")
        except Exception:
            pass

        da["_idx"]    = da.index.astype(str)
        da["_status"] = da["_idx"].apply(get_alert_status)

        visible_a = da[~da["_idx"].isin(st.session_state.alert_deleted)]
        if not st.session_state.show_hidden_edd:
            visible_a = visible_a[~visible_a["_idx"].isin(st.session_state.alert_hidden)]

        filtered_a = visible_a[visible_a["_status"].isin(status_filter)] if status_filter else visible_a.copy()

        am1, am2, am3, am4, am5 = st.columns(5)
        for col_obj, num, lbl in [
            (am1, len(visible_a), "Total Alerts"),
            (am2, (visible_a["_status"]=="Pending").sum(), "Pending"),
            (am3, (visible_a["_status"]=="Form Sent").sum(), "Form Sent"),
            (am4, (visible_a["_status"]=="Under Review").sum(), "Under Review"),
            (am5, (visible_a["_status"]=="Done").sum(), "Done"),
        ]:
            with col_obj:
                st.markdown(f'<div class="metric-box"><div class="metric-num">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

        # ── Alert modal card ──────────────────────────────────────────────────
        sel_idx = st.session_state.selected_alert_idx
        if sel_idx is not None:
            match_a = da[da["_idx"] == sel_idx]
            if not match_a.empty:
                arow     = match_a.iloc[0]
                a_uid    = str(arow[a_uid_col])
                a_type   = str(arow.get(a_type_col, "—"))
                a_ts     = arow.get(a_ts_col, "")
                a_status = get_alert_status(sel_idx)
                profile  = get_profile(a_uid)
                initials_a = a_uid[:2].upper()
                badge_cls_a = BADGE_MAP.get(a_status, "badge-pending")

                try:
                    a_ts_str = pd.to_datetime(a_ts).strftime("%d %b %Y  %H:%M") if pd.notna(a_ts) else "—"
                except Exception:
                    a_ts_str = "—"

                phtml = ""
                for label, val in profile.items():
                    if label == "Risk Score":
                        r_cls = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(val,"badge-pending")
                        phtml += (
                            f'<div class="edd-modal-field">'
                            f'<div class="edd-modal-field-label">{label}</div>'
                            f'<div><span class="badge {r_cls}">{val}</span></div>'
                            f'</div>'
                        )
                    else:
                        phtml += (
                            f'<div class="edd-modal-field">'
                            f'<div class="edd-modal-field-label">{label}</div>'
                            f'<div class="edd-modal-field-value">{val}</div>'
                            f'</div>'
                        )

                st.markdown(f"""
<div class="edd-modal">
  <div class="edd-modal-header">
    <div style="display:flex;align-items:center;gap:14px;">
      <div class="edd-modal-avatar">{initials_a}</div>
      <div>
        <p class="edd-modal-uid">{a_uid}</p>
        <p class="edd-modal-sub">Alert &middot; <span style="font-family:monospace;font-size:11px;background:#f0f0ec;padding:1px 6px;border-radius:3px">{a_type}</span></p>
      </div>
    </div>
    <span class="badge {badge_cls_a}">{a_status}</span>
  </div>
  <div class="edd-modal-body">
    <div class="edd-modal-section">Alert details</div>
    <div class="edd-modal-field-grid">
      <div class="edd-modal-field">
        <div class="edd-modal-field-label">Triggered</div>
        <div class="edd-modal-field-value"><span class="alert-chip">{a_type}</span></div>
      </div>
      <div class="edd-modal-field">
        <div class="edd-modal-field-label">Timestamp</div>
        <div class="edd-modal-field-value">{a_ts_str}</div>
      </div>
    </div>
    <hr class="edd-modal-divider">
    <div class="edd-modal-section">User profile <span style="color:#ccc;font-weight:400;text-transform:none;letter-spacing:0;margin-left:4px">via UserTool</span></div>
    <div class="edd-modal-field-grid">{phtml}</div>
    <hr class="edd-modal-divider">
    <div class="edd-modal-section">Update Status</div>
  </div>
</div>
""", unsafe_allow_html=True)

                bc1, bc2, bc3, bc4, bc5 = st.columns([3, 2, 2, 2, 1])
                with bc1:
                    new_as = st.selectbox(
                        "alert_status", STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(a_status) if a_status in STATUS_OPTIONS else 0,
                        key=f"alert_sel_{sel_idx}", label_visibility="collapsed",
                    )
                with bc2:
                    if st.button("Save Status", use_container_width=True, key=f"alert_save_{sel_idx}"):
                        set_alert_status(sel_idx, new_as)
                        if new_as == "Form Sent":
                            st.session_state.alert_form_log[sel_idx] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.success("Saved"); st.rerun()
                with bc3:
                    if st.button("Send Form", use_container_width=True, key=f"alert_send_{sel_idx}"):
                        set_alert_status(sel_idx, "Form Sent")
                        st.session_state.alert_form_log[sel_idx] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.success("Marked Form Sent"); st.rerun()
                with bc4:
                    if st.button("Mark Done", use_container_width=True, key=f"alert_done_{sel_idx}"):
                        set_alert_status(sel_idx, "Done"); st.success("Marked Done"); st.rerun()
                with bc5:
                    if st.button("Close", use_container_width=True, key="alert_close"):
                        st.session_state.selected_alert_idx = None; st.rerun()

                dx2, _ = st.columns([2, 6])
                with dx2:
                    if st.button("Delete alert", use_container_width=True, key=f"alert_del_{sel_idx}"):
                        st.session_state.alert_deleted.add(sel_idx)
                        st.session_state.selected_alert_idx = None
                        st.warning("Alert deleted from this session"); st.rerun()

                st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ── Alerts list (full width) ──────────────────────────────────────────
        st.markdown('<p class="section-title">Alerts</p>', unsafe_allow_html=True)
        if filtered_a.empty:
            st.info("No alerts match the current filters.")
        else:
            a_page_ids = filtered_a["_idx"].tolist()
            a_all_ids  = visible_a["_idx"].tolist()
            render_bulk_toolbar(st.session_state.alert_checked, a_page_ids, a_all_ids, "alert")
            st.markdown("<hr style='border:none;border-top:1px solid #e8e8e4;margin:6px 0 10px 0'>", unsafe_allow_html=True)

            for _, row in filtered_a.iterrows():
                idx        = str(row["_idx"])
                uid        = str(row[a_uid_col])
                alert_type = str(row.get(a_type_col, "—"))
                a_status   = get_alert_status(idx)
                ts         = row.get(a_ts_col, "")
                is_hidden  = idx in st.session_state.alert_hidden
                row_opacity = "opacity:0.45;" if is_hidden else ""

                try:
                    ts_str = pd.to_datetime(ts).strftime("%d %b %Y  %H:%M") if pd.notna(ts) else "—"
                except Exception:
                    ts_str = "—"

                cb_a, info_a, badge_a, btn_a = st.columns([0.5, 4, 2, 1])
                with cb_a:
                    a_checked_val = st.checkbox(
                        "sel", value=(idx in st.session_state.alert_checked),
                        key=f"chk_alert_{idx}", label_visibility="collapsed",
                    )
                    if a_checked_val: st.session_state.alert_checked.add(idx)
                    else:             st.session_state.alert_checked.discard(idx)
                with info_a:
                    hidden_tag = ' <small style="color:#bbb;font-size:10px">[hidden]</small>' if is_hidden else ""
                    st.markdown(
                        f'<div style="{row_opacity}padding-top:4px">'
                        f'<span class="uid-text">{uid}</span>&nbsp;&nbsp;'
                        f'<span class="alert-chip">{alert_type}</span>{hidden_tag}'
                        f'<br><small style="color:#999">{ts_str}</small></div>',
                        unsafe_allow_html=True,
                    )
                with badge_a:
                    st.markdown(f'<div style="{row_opacity}padding-top:8px">{badge_html(a_status)}</div>', unsafe_allow_html=True)
                with btn_a:
                    btn_lbl = "Show" if is_hidden else "View"
                    if st.button(btn_lbl, key=f"alert_v_{idx}", use_container_width=True):
                        if is_hidden: st.session_state.alert_hidden.discard(idx)
                        else:         st.session_state.selected_alert_idx = idx
                        st.rerun()
                st.markdown("<hr style='border:none;border-top:1px solid #f2f2ef;margin:4px 0'>", unsafe_allow_html=True)

        if st.session_state.alert_form_log:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            st.markdown('<p class="section-title">Alert Form Sent Log</p>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([
                {
                    "Alert #": idx,
                    "User ID": da.loc[int(idx), a_uid_col] if int(idx) in da.index else "—",
                    "Form Sent At": ts,
                    "Current Status": get_alert_status(idx),
                }
                for idx, ts in st.session_state.alert_form_log.items()
            ]), use_container_width=True, hide_index=True)