
"""
sheets.py — Google Sheets helpers
Handles loading, action_taken writes, and the "Assigned To" column.
"""

import json
import streamlit as st
import pandas as pd
from datetime import datetime


# ── Secrets / credentials ─────────────────────────────────────────────────────

def get_secrets():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    try:
        sheet_url      = "https://docs.google.com/spreadsheets/d/1oQOLJpniw1sfXG9Yo2M43YunsXMYuVaMIpB2x35swmU/edit?gid=1141007023#gid=1141007023"
        worksheet_name = "Response"
        sa_info        = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
        return sheet_url, worksheet_name, sa_info
    except KeyError as e:
        st.error(f"Missing env variable: {e}. Check your .env file.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: {e}")
        st.stop()


def get_usertool_token():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return os.environ.get("USERTOOL_ADMIN_TOKEN", "")


# ── Sheet connection ──────────────────────────────────────────────────────────

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


# ── Column-index lookup (cached per load) ─────────────────────────────────────

def _get_col_index(ws, col_name_lower: str):
    """Return 1-based column index for a header matching col_name_lower, or None."""
    headers = ws.row_values(1)
    for i, h in enumerate(headers):
        if h.strip().lower() == col_name_lower:
            return i + 1
    return None


# ── Write helpers ─────────────────────────────────────────────────────────────

def write_action_to_sheet(row_idx: int, action_value: str):
    if st.session_state.get("edd_source") != "gsheet":
        return
    ws = st.session_state.get("gs_worksheet_obj")
    if ws is None:
        return
    try:
        col_idx = _get_col_index(ws, "action_taken")
        if col_idx is None:
            st.warning("Column 'action_taken' not found in the sheet.")
            return
        ws.update_cell(int(row_idx) + 2, col_idx, action_value)
    except Exception as e:
        st.warning(f"Could not write to Google Sheet: {e}")


def write_assigned_to_sheet(row_idx: int, username: str):
    """
    Write username into the 'Assigned To' column for the given row.
    Passing empty string clears the assignment.
    """
    if st.session_state.get("edd_source") != "gsheet":
        return
    ws = st.session_state.get("gs_worksheet_obj")
    if ws is None:
        return
    try:
        col_idx = _get_col_index(ws, "assigned to")
        if col_idx is None:
            st.warning("Column 'Assigned To' not found in the sheet. Please add it first.")
            return
        ws.update_cell(int(row_idx) + 2, col_idx, username)
    except Exception as e:
        st.warning(f"Could not write assignment to Google Sheet: {e}")


def bulk_assign_rows(row_indices: list, username: str):
    """
    Batch-write username into 'Assigned To' for multiple rows at once.
    Uses batch_update for efficiency.
    """
    if st.session_state.get("edd_source") != "gsheet":
        return False, "Not connected to Google Sheets"
    ws = st.session_state.get("gs_worksheet_obj")
    if ws is None:
        return False, "Worksheet not connected"
    try:
        col_idx = _get_col_index(ws, "assigned to")
        if col_idx is None:
            return False, "Column 'Assigned To' not found in sheet"

        # Build batch update data
        updates = []
        for ridx in row_indices:
            sheet_row = int(ridx) + 2  # +1 for header, +1 for 1-based index
            col_letter = _col_letter(col_idx)
            updates.append({
                "range": f"{col_letter}{sheet_row}",
                "values": [[username]],
            })

        if updates:
            ws.batch_update(updates)

        return True, f"Assigned {len(row_indices)} rows to {username}"
    except Exception as e:
        return False, str(e)


def _col_letter(n: int) -> str:
    """Convert 1-based column number to letter (1→A, 26→Z, 27→AA)."""
    result = ""
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def get_assigned_to_col(df: pd.DataFrame):
    """Return the name of the 'Assigned To' column, case-insensitive."""
    for c in df.columns:
        if c.strip().lower() == "assigned to":
            return c
    return None


def is_row_assigned_to_other(row: pd.Series, assigned_col: str, current_user: str) -> bool:
    """True if the row is assigned to someone else (locked)."""
    if assigned_col is None:
        return False
    val = str(row.get(assigned_col, "")).strip()
    return bool(val) and val.lower() != current_user.lower()


def is_row_assigned_to_me(row: pd.Series, assigned_col: str, current_user: str) -> bool:
    """True if the row is assigned to the current user."""
    if assigned_col is None:
        return False
    val = str(row.get(assigned_col, "")).strip()
    return val.lower() == current_user.lower()