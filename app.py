import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDD Tracking",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
STATUS_OPTIONS = ["Pending", "Form Sent", "Under Review", "Done"]
BADGE_MAP = {
    "Pending": "badge-pending", "Form Sent": "badge-form_sent",
    "Under Review": "badge-under_review", "Done": "badge-done",
}
PAGE_SIZE = 20

DUMMY_PROFILES = {
    "USR-001": {"Full Name":"Ahmed Karim",   "Email":"ahmed.k@email.com",   "Phone":"+20 111 234 5678","KYC Level":"Level 2","Account Age":"3 years",  "Risk Score":"Low",   "Country":"Egypt"},
    "USR-002": {"Full Name":"Sara Nour",     "Email":"sara.n@email.com",    "Phone":"+20 100 876 5432","KYC Level":"Level 1","Account Age":"8 months", "Risk Score":"Medium","Country":"Egypt"},
    "USR-003": {"Full Name":"Omar Sayed",    "Email":"omar.s@email.com",    "Phone":"+20 122 345 6789","KYC Level":"Level 3","Account Age":"5 years",  "Risk Score":"Low",   "Country":"Egypt"},
    "USR-004": {"Full Name":"Lina Hassan",   "Email":"lina.h@email.com",    "Phone":"+20 115 987 6543","KYC Level":"Level 2","Account Age":"2 years",  "Risk Score":"Medium","Country":"Egypt"},
    "USR-005": {"Full Name":"Youssef Adel",  "Email":"youssef.a@email.com", "Phone":"+20 109 111 2222","KYC Level":"Level 3","Account Age":"7 years",  "Risk Score":"High",  "Country":"Egypt"},
    "USR-006": {"Full Name":"Mona Ibrahim",  "Email":"mona.i@email.com",    "Phone":"+20 128 333 4444","KYC Level":"Level 1","Account Age":"4 months", "Risk Score":"Medium","Country":"Egypt"},
    "USR-007": {"Full Name":"Khaled Farouk", "Email":"khaled.f@email.com",  "Phone":"+20 101 555 6666","KYC Level":"Level 2","Account Age":"1.5 years","Risk Score":"Low",  "Country":"Egypt"},
    "USR-008": {"Full Name":"Dina Mostafa",  "Email":"dina.m@email.com",    "Phone":"+20 106 777 8888","KYC Level":"Level 2","Account Age":"2.5 years","Risk Score":"Medium","Country":"Egypt"},
}

def get_profile(uid):
    return DUMMY_PROFILES.get(str(uid), {
        "Full Name":"Unknown","Email":"—","Phone":"—",
        "KYC Level":"—","Account Age":"—","Risk Score":"—","Country":"—",
    })

def badge_html(status, extra=""):
    cls = BADGE_MAP.get(status, "badge-pending")
    return f'<span class="badge {cls}" style="{extra}">{status}</span>'

def risk_badge(risk):
    cls = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(risk,"badge-pending")
    return f'<span class="badge {cls}">{risk}</span>'

# ── Secrets helpers ────────────────────────────────────────────────────────────
def get_secrets():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    try:
        sheet_url      = os.environ["GOOGLE_SHEET_URL"]
        worksheet_name = os.environ.get("GOOGLE_WORKSHEET_NAME", "").strip() or None
        raw_sa         = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
        sa_info        = json.loads(raw_sa)
        return sheet_url, worksheet_name, sa_info
    except KeyError as e:
        st.error(f"Missing env variable: {e}. Check your .env file.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error reading credentials: {e}")
        st.stop()

def get_usertool_token():
    """Read the UserTool admin token from .env (USERTOOL_ADMIN_TOKEN)."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return os.environ.get("USERTOOL_ADMIN_TOKEN", "")

# ── Google Sheets loader ───────────────────────────────────────────────────────
def _dedupe_headers(raw_headers):
    seen = {}; result = []
    for i, h in enumerate(raw_headers):
        h = h.strip() if h.strip() else f"__col_{i}__"
        if h in seen:
            seen[h] += 1; result.append(f"{h} _{seen[h]}")
        else:
            seen[h] = 1; result.append(h)
    return result

def load_from_google_sheets():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        st.error("Missing dependencies. Run:  pip install gspread google-auth")
        st.stop()

    sheet_url, worksheet_name, sa_info = get_secrets()
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
        gc    = gspread.authorize(creds)
        sh    = gc.open_by_url(sheet_url)
        ws    = sh.worksheet(worksheet_name) if worksheet_name else sh.sheet1
        st.session_state["gs_worksheet_obj"] = ws
        all_values = ws.get_all_values()
        if not all_values:
            return pd.DataFrame()
        headers = _dedupe_headers(all_values[0])
        rows    = all_values[1:]
        n       = len(headers)
        rows    = [r + [""] * (n - len(r)) if len(r) < n else r[:n] for r in rows]
        return pd.DataFrame(rows, columns=headers)
    except Exception as e:
        st.error(f"Google Sheets error: {e}")
        st.stop()

def write_action_to_sheet(row_idx: int, action_value: str):
    if st.session_state.get("edd_source") != "gsheet":
        return
    ws = st.session_state.get("gs_worksheet_obj")
    df = st.session_state.get("df_edd")
    if ws is None or df is None:
        return
    try:
        headers = ws.row_values(1)
        col_idx = next(
            (i + 1 for i, h in enumerate(headers) if h.strip().lower() == "action_taken"),
            None,
        )
        if col_idx is None:
            st.warning("Column 'action_taken' not found in the sheet. Please add it first.")
            return
        sheet_row = int(row_idx) + 2
        ws.update_cell(sheet_row, col_idx, action_value)
    except Exception as e:
        st.warning(f"Could not write to Google Sheet: {e}")

# ── UserTool API ───────────────────────────────────────────────────────────────
USERTOOL_BASE = "https://admin-service.thndr-internal.app/compliance-service/admin/account-forms"

def fetch_usertool(uid: str) -> dict:
    """
    Call the UserTool API for a given user ID.
    Returns {"ok": True, "data": {...}} or {"ok": False, "error": "..."}.
    Token is read from USERTOOL_ADMIN_TOKEN in .env
    """
    token = get_usertool_token()
    if not token:
        return {"ok": False, "error": "USERTOOL_ADMIN_TOKEN not set in .env"}

    url = f"{USERTOOL_BASE}/{uid.strip()}"
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

st.markdown("""
<div class="edd-header">
  <p class="edd-title">EDD Tracking</p>
  <p class="edd-subtitle">Enhanced Due Diligence Portal</p>
</div>
""", unsafe_allow_html=True)

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
    visible_df  = df[~df["_row_idx"].isin(st.session_state.edd_deleted)]
    if not show_hidden:
        visible_df = visible_df[~visible_df["_row_idx"].isin(st.session_state.edd_hidden)]

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

    n_hidden = len(st.session_state.edd_hidden - st.session_state.edd_deleted)
    if n_hidden:
        st.markdown(f'<p style="font-size:11px;color:#bbb;margin:6px 0 0 2px">{n_hidden} row(s) hidden · toggle "Show hidden rows" in the sidebar to restore</p>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    left, right = st.columns([5, 4], gap="large")

    # ── Left: submission list ──────────────────────────────────────────────────
    with left:
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

            uid_totals  = filtered[uid_col].astype(str).value_counts().to_dict()
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
                    f'<span style="font-size:11px;color:#bbb">{total_rows} total · page {page+1} of {total_pages}</span>',
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
                    btn_label = "👁 Show" if is_hidden else "View"
                    if st.button(btn_label, key=f"edd_v_{row_idx}", use_container_width=True):
                        if is_hidden:
                            st.session_state.edd_hidden.discard(row_idx)
                        else:
                            st.session_state.selected_edd_idx = row_idx
                            st.session_state.detail_tab = "submission"  # reset to submission tab on new selection
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

    # ── Right: detail panel with tabs ─────────────────────────────────────────
    with right:
        sel_idx = st.session_state.selected_edd_idx

        if sel_idx is None:
            st.markdown(
                '<div style="background:#fff;border:1px solid #e8e8e4;border-radius:10px;padding:40px;text-align:center;color:#bbb;">'
                '<div style="font-size:32px;margin-bottom:12px">👤</div>'
                '<div style="font-size:13px">Select a submission to view details</div></div>',
                unsafe_allow_html=True,
            )
        else:
            try:
                row = df.loc[int(sel_idx)]
            except (KeyError, ValueError):
                row = None

            if row is None:
                st.warning("Submission not found.")
            else:
                status = get_edd_status(sel_idx)
                uid    = str(row[uid_col]) if uid_col in row.index else sel_idx

                # ── User header (always visible above tabs) ────────────────────
                hc1, hc2 = st.columns([3, 2])
                with hc1:
                    st.markdown(f'<span style="font-size:18px;font-weight:600;color:#1a1a1a;word-break:break-all">{uid}</span>', unsafe_allow_html=True)
                with hc2:
                    st.markdown(badge_html(status, "margin-top:6px;display:block"), unsafe_allow_html=True)

                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

                # ── Tab switcher ───────────────────────────────────────────────
                dt1, dt2 = st.tabs(["📄  Submission Info", "🔍  UserTool Info"])

                # ════════════════════════════════════════════════
                # TAB 1 — Submission Info
                # ════════════════════════════════════════════════
                with dt1:
                    st.markdown("<hr style='border:none;border-top:1px solid #efefec;margin:8px 0'>", unsafe_allow_html=True)

                    priority = [
                        ("Submitted At",    date_col),
                        ("Country",         country_col),
                        ("Primary Funding", src_col),
                        ("Employer",        emp_col),
                        ("Job Title",       job_col),
                        ("Monthly Income",  inc_col),
                        ("Review Status",   review_col),
                        ("Notes",           notes_col),
                    ]
                    shown_cols = set()
                    for label, cn in priority:
                        if cn and cn in row.index:
                            shown_cols.add(cn)
                            val = row[cn]
                            try:
                                is_empty = pd.isna(val) or str(val).strip() == ""
                            except Exception:
                                is_empty = False
                            if is_empty: continue
                            if label == "Submitted At":
                                try: val = pd.to_datetime(val).strftime("%d %b %Y  %H:%M")
                                except Exception: pass
                            st.markdown(
                                f'<div class="detail-label">{label}</div>'
                                f'<div class="detail-value" style="word-break:break-word">{val}</div>',
                                unsafe_allow_html=True,
                            )

                    skip_cols = {"_row_idx","_status",uid_col} | set(doc_cols)
                    other_cols = [c for c in cols if c not in shown_cols and c not in skip_cols and not c.startswith("_")]
                    if other_cols:
                        with st.expander("All fields", expanded=False):
                            for cn in other_cols:
                                if cn not in row.index: continue
                                val = row[cn]
                                try:
                                    is_empty = pd.isna(val) or str(val).strip() == ""
                                except Exception:
                                    is_empty = False
                                if is_empty: continue
                                short_label = cn[:60] + ("…" if len(cn)>60 else "")
                                st.markdown(
                                    f'<div class="detail-label" style="font-size:10px">{short_label}</div>'
                                    f'<div class="detail-value" style="word-break:break-word;font-size:13px">{val}</div>',
                                    unsafe_allow_html=True,
                                )

                    if doc_cols:
                        st.markdown('<div class="detail-label">Documents</div>', unsafe_allow_html=True)
                        links = [
                            (dc, str(row[dc])) for dc in doc_cols
                            if dc in row.index and pd.notna(row[dc]) and str(row[dc]).strip().startswith("http")
                        ]
                        if links:
                            dcols_ui = st.columns(min(len(links), 3))
                            for i, (dc, link) in enumerate(links):
                                with dcols_ui[i % 3]:
                                    st.link_button(f"📄 Doc {i+1}", url=link, use_container_width=True)
                        else:
                            st.markdown("<small style='color:#bbb'>No document links found</small>", unsafe_allow_html=True)

                    st.markdown("<hr style='border:none;border-top:1px solid #efefec;margin:14px 0'>", unsafe_allow_html=True)
                    st.markdown('<p class="section-title" style="margin-top:0">Update Status</p>', unsafe_allow_html=True)

                    new_s = st.selectbox(
                        "edd_status_sel", STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0,
                        key=f"edd_sel_{sel_idx}", label_visibility="collapsed",
                    )
                    a1, a2, a3 = st.columns(3)
                    with a1:
                        if st.button("Save Status", use_container_width=True, key=f"edd_save_{sel_idx}"):
                            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                            set_edd_status(sel_idx, new_s)
                            write_action_to_sheet(sel_idx, f"{new_s} — {ts}")
                            if new_s == "Form Sent":
                                st.session_state.form_sent_log[sel_idx] = {"uid": uid, "at": ts}
                            st.success("Saved"); st.rerun()
                    with a2:
                        if st.button("📤 Send Form", use_container_width=True, key=f"edd_send_{sel_idx}"):
                            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                            set_edd_status(sel_idx, "Form Sent")
                            write_action_to_sheet(sel_idx, f"Form Sent — {ts}")
                            st.session_state.form_sent_log[sel_idx] = {"uid": uid, "at": ts}
                            st.success("Marked Form Sent"); st.rerun()
                    with a3:
                        if st.button("✔ Mark Done", use_container_width=True, key=f"edd_done_{sel_idx}"):
                            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                            set_edd_status(sel_idx, "Done")
                            write_action_to_sheet(sel_idx, f"Done — {ts}")
                            st.success("Marked Done"); st.rerun()

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    ih1, ih2 = st.columns(2)
                    with ih1:
                        is_hid    = sel_idx in st.session_state.edd_hidden
                        hide_label = "👁 Un-hide row" if is_hid else "🙈 Hide row"
                        if st.button(hide_label, use_container_width=True, key=f"edd_hide_{sel_idx}"):
                            if is_hid: st.session_state.edd_hidden.discard(sel_idx)
                            else:      st.session_state.edd_hidden.add(sel_idx)
                            st.rerun()
                    with ih2:
                        if st.button("🗑 Delete row", use_container_width=True, key=f"edd_del_{sel_idx}"):
                            st.session_state.edd_deleted.add(sel_idx)
                            st.session_state.selected_edd_idx = None
                            st.warning("Row deleted from this session"); st.rerun()

                # ════════════════════════════════════════════════
                # TAB 2 — UserTool Info
                # ════════════════════════════════════════════════
                with dt2:
                    st.markdown("<hr style='border:none;border-top:1px solid #efefec;margin:8px 0'>", unsafe_allow_html=True)
                    render_usertool_panel(uid)

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
        if not show_hidden:
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
        al_left, al_right = st.columns([5, 4], gap="large")

        with al_left:
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
                        btn_label = "👁 Show" if is_hidden else "View"
                        if st.button(btn_label, key=f"alert_v_{idx}", use_container_width=True):
                            if is_hidden: st.session_state.alert_hidden.discard(idx)
                            else:         st.session_state.selected_alert_idx = idx
                            st.rerun()
                    st.markdown("<hr style='border:none;border-top:1px solid #f2f2ef;margin:4px 0'>", unsafe_allow_html=True)

        with al_right:
            st.markdown('<p class="section-title">Alert Detail</p>', unsafe_allow_html=True)
            sel_idx = st.session_state.selected_alert_idx

            if sel_idx is None:
                st.markdown(
                    '<div style="background:#fff;border:1px solid #e8e8e4;border-radius:10px;padding:40px;text-align:center;color:#bbb;">'
                    '<div style="font-size:32px;margin-bottom:12px">🔔</div>'
                    '<div style="font-size:13px">Select an alert to view details</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                match_a = da[da["_idx"] == sel_idx]
                if match_a.empty:
                    st.warning("Alert not found.")
                else:
                    arow     = match_a.iloc[0]
                    a_uid    = str(arow[a_uid_col])
                    a_type   = str(arow.get(a_type_col, "—"))
                    a_ts     = arow.get(a_ts_col, "")
                    a_status = get_alert_status(sel_idx)
                    profile  = get_profile(a_uid)

                    try:
                        a_ts_str = pd.to_datetime(a_ts).strftime("%d %b %Y  %H:%M") if pd.notna(a_ts) else "—"
                    except Exception:
                        a_ts_str = "—"

                    ah1, ah2 = st.columns([3, 2])
                    with ah1:
                        st.markdown(f'<span style="font-size:20px;font-weight:600;color:#1a1a1a">{a_uid}</span>', unsafe_allow_html=True)
                    with ah2:
                        st.markdown(badge_html(a_status, "margin-top:6px;display:block"), unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="detail-label" style="margin-top:10px">Alert Triggered</div>'
                        f'<div style="margin-bottom:12px"><span class="alert-chip">{a_type}</span></div>'
                        f'<div class="detail-label">Timestamp</div>'
                        f'<div class="detail-value">{a_ts_str}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown("<hr style='border:none;border-top:1px solid #efefec;margin:10px 0'>", unsafe_allow_html=True)
                    st.markdown(
                        '<p class="section-title" style="margin-top:0">User Profile '
                        '<span style="color:#ccc;font-size:10px;margin-left:6px;font-weight:400;text-transform:none;letter-spacing:0">via UserTool</span></p>',
                        unsafe_allow_html=True,
                    )

                    p1, p2 = st.columns(2)
                    items = list(profile.items())
                    half  = len(items) // 2 + len(items) % 2
                    for col_obj, chunk in [(p1, items[:half]), (p2, items[half:])]:
                        with col_obj:
                            for label, val in chunk:
                                if label == "Risk Score":
                                    st.markdown(f'<div class="detail-label">{label}</div>{risk_badge(val)}<div style="height:14px"></div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="detail-label">{label}</div><div class="detail-value">{val}</div>', unsafe_allow_html=True)

                    st.markdown("<hr style='border:none;border-top:1px solid #efefec;margin:14px 0'>", unsafe_allow_html=True)
                    st.markdown('<p class="section-title" style="margin-top:0">Update Status</p>', unsafe_allow_html=True)

                    new_as = st.selectbox(
                        "alert_status_sel", STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(a_status) if a_status in STATUS_OPTIONS else 0,
                        key=f"alert_sel_{sel_idx}", label_visibility="collapsed",
                    )
                    aa1, aa2, aa3 = st.columns(3)
                    with aa1:
                        if st.button("Save Status", use_container_width=True, key=f"alert_save_{sel_idx}"):
                            set_alert_status(sel_idx, new_as)
                            if new_as == "Form Sent":
                                st.session_state.alert_form_log[sel_idx] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.success("Saved"); st.rerun()
                    with aa2:
                        if st.button("📤 Send Form", use_container_width=True, key=f"alert_send_{sel_idx}"):
                            set_alert_status(sel_idx, "Form Sent")
                            st.session_state.alert_form_log[sel_idx] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.success("Marked Form Sent"); st.rerun()
                    with aa3:
                        if st.button("✔ Mark Done", use_container_width=True, key=f"alert_done_{sel_idx}"):
                            set_alert_status(sel_idx, "Done"); st.success("Marked Done"); st.rerun()

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    dh1, dh2 = st.columns(2)
                    with dh1:
                        is_hid   = sel_idx in st.session_state.alert_hidden
                        hide_lbl = "👁 Un-hide" if is_hid else "🙈 Hide"
                        if st.button(hide_lbl, use_container_width=True, key=f"alert_hide_{sel_idx}"):
                            if is_hid: st.session_state.alert_hidden.discard(sel_idx)
                            else:      st.session_state.alert_hidden.add(sel_idx)
                            st.rerun()
                    with dh2:
                        if st.button("🗑 Delete", use_container_width=True, key=f"alert_del_{sel_idx}"):
                            st.session_state.alert_deleted.add(sel_idx)
                            st.session_state.selected_alert_idx = None
                            st.warning("Alert deleted from this session"); st.rerun()

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