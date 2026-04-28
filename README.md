# EDD Tracking Portal

> A unified compliance operations tool for reviewing Enhanced Due Diligence (EDD) submissions, cross-referencing UserTool profiles, managing alerts, and tracking case statuses — all in one place.

---

## Overview

The EDD Tracking Portal is an internal Streamlit application built for the compliance team. It replaces a fragmented workflow spread across Google Sheets, Superset, Slack, and UserTool by providing a single interface where analysts can:

- Load EDD form submissions directly from a live Google Sheet
- Browse, filter, paginate, and search submissions
- View full submission details alongside live UserTool profile data
- Take and record case actions (Form Sent, Under Review, Done)
- Manage compliance alerts from a CSV feed
- Perform bulk actions across multiple cases at once

---

## Screenshots

> _Add screenshots here after deployment_

---

## Features

| Feature | Description |
|---|---|
| **Google Sheets integration** | Connects to a live Google Sheet via a service account — no manual exports needed |
| **CSV fallback** | Toggle to CSV upload mode for offline use or testing |
| **Live UserTool lookup** | Fetches user profile data from the internal admin API on demand, cached per session |
| **Paginated submission list** | 20 rows per page with prev/next controls and a jump-to-page input |
| **Per-row checkboxes + bulk actions** | Select individual rows or all on page; apply Form Sent / Under Review / Done / Hide / Delete in one click |
| **Duplicate submission handling** | Same user ID appearing multiple times is labeled `uid (1)`, `uid (2)`, etc. |
| **Duplicate column headers** | Google Sheet duplicate headers are automatically de-duplicated (`col`, `col _2`, `col _3`) |
| **Status persistence** | Statuses set this session are reflected across the list and metrics instantly |
| **Write-back to Google Sheet** | Saves action + timestamp to an `action_taken` column in the source sheet |
| **Alerts tab** | Load a CSV of triggered alerts, view details, and manage status independently |
| **Hide / Delete rows** | Soft-hide rows from view or remove them from the session entirely |
| **Form Sent log** | Running log of all cases marked Form Sent, with timestamps |

---

## Project Structure

```
edd-tracking/
├── app.py              # Main Streamlit application
├── .env                # Local secrets (not committed — see setup below)
├── .env.example        # Template for required environment variables
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Requirements

- Python 3.9+
- A Google Cloud service account with access to the Google Sheet
- A UserTool admin bearer token

Install dependencies:

```bash
pip install streamlit pandas gspread google-auth python-dotenv requests
```

Or with a requirements file:

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit
pandas
gspread
google-auth
python-dotenv
requests
```

---

## Environment Setup

Create a `.env` file in the project root. Use `.env.example` as a template.

```bash
cp .env.example .env
```

Then fill in the values:

```env
# ── Google Sheets ──────────────────────────────────────────────────────────────
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
GOOGLE_WORKSHEET_NAME=          # Leave blank to use the first sheet

# ── Service Account (paste entire JSON as a single line) ───────────────────────
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}

# ── UserTool API ───────────────────────────────────────────────────────────────
USERTOOL_ADMIN_TOKEN=your-bearer-token-here
```

> ⚠️ Never commit `.env` to version control. Add it to `.gitignore`.

---

## Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → enable **Google Sheets API** and **Google Drive API**
2. Create a **Service Account** → go to **Keys** → **Add Key** → **JSON** → download
3. Open your Google Sheet → **Share** → paste the service account email (ends in `@...iam.gserviceaccount.com`) → grant **Viewer** access (or **Editor** if you want write-back to work)
4. Paste the full contents of the downloaded JSON file into `GOOGLE_SERVICE_ACCOUNT_JSON` in `.env` as a single line

### Write-back support

To enable the app to write action statuses back to the sheet, add a column named exactly `action_taken` to your Google Sheet and grant the service account **Editor** access.

---

## Google Sheet Column Reference

The app auto-detects columns by keyword matching. The following column names (or partial matches) are recognised:

| Field | Matched by |
|---|---|
| Submission date | `submitted`, `date`, `time` |
| User ID | `user_id` (exact), or `user`, `uid`, `id` |
| Primary funding source | `funding`, `source of income`, `primary` |
| Employer | `employer` |
| Job title | `job titl`, `occupation` |
| Monthly income | `monthly income` (excluding `business`) |
| Country | `country of resid`, `residency` |
| Notes | `added to notes`, `notes`, `note` |
| Review status | `response`, `duplication check`, `status` |
| Documents | `upload document`, columns starting with `upload` |
| Action taken | `action_taken` (exact, for write-back) |

Any columns not matched by the above are surfaced in an **"All fields"** expander inside the submission detail panel.

---

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. On first load it automatically connects to Google Sheets using your `.env` credentials.

---

## Deployment

### Streamlit Community Cloud

1. Push the repo to GitHub (ensure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → connect your repo
3. In **Advanced settings → Secrets**, add each environment variable from `.env` in TOML format:

```toml
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/..."
GOOGLE_SERVICE_ACCOUNT_JSON = '{"type":"service_account",...}'
USERTOOL_ADMIN_TOKEN = "your-token"
```

### Self-hosted (Docker)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t edd-tracking .
docker run -p 8501:8501 --env-file .env edd-tracking
```

---

## Usage Guide

### EDD Cases tab

- **List panel (left):** Browse paginated submissions. Use the sidebar filters (status, date range, user ID search) to narrow down results.
- **Checkboxes:** Select individual rows. Use **This page** or **All** checkboxes to select in bulk. The toolbar above the list exposes bulk actions: Form Sent, Under Review, Done, Hide, Delete.
- **View button:** Opens the detail panel on the right.
- **Detail panel (right):** Two tabs —
  - **📄 Submission Info** — all form fields, document links, status controls, hide/delete
  - **🔍 UserTool Info** — live profile fetched from the internal admin API, cached for the session. Hit 🔄 Refresh to re-fetch.

### Alerts tab

- Upload an alerts CSV using the sidebar uploader
- Browse alerts with the same checkbox + bulk action pattern as EDD cases
- Click View to open alert details with status controls

### Sidebar

| Control | Purpose |
|---|---|
| **Use Google Sheets toggle** | Switch between live Google Sheet and CSV file upload |
| **🔄 Refresh from Sheet** | Re-fetch the latest data from Google Sheets |
| **Alerts Sheet (CSV)** | Upload an alerts CSV |
| **Status filter** | Show only rows with selected statuses |
| **Date Range** | Filter submissions by date |
| **Search User ID** | Live text filter on the user ID column |
| **Show hidden rows** | Toggle visibility of soft-hidden rows |

---

## Notes & Limitations

- **Session only:** Statuses set in the app (except write-back) reset on page refresh. The source of truth for persistence is the `action_taken` column in Google Sheets.
- **Write-back requires Editor access:** The service account must have Editor permission on the sheet for status write-back to work.
- **UserTool cache is per-session:** Closing the browser tab clears the cache. Use the Refresh button to get updated data within a session.
- **Alerts are CSV only:** Alert data is not yet connected to a live source.
- **Deletion is session-only:** Deleted rows return on refresh. True deletion from the sheet is not yet supported.

---

## Proposed Enhancements

See the technical scoping document for a full breakdown. In brief:

1. **Real-time alert ingestion** via webhook or scheduled n8n workflow into a database
2. **Persistent status storage** in a lightweight database (Supabase / PostgreSQL) so statuses survive refresh
3. **Role-based access** so senior analysts can approve actions taken by junior analysts
4. **Audit log** with full history of every action taken on every case, by whom and when
5. **Notification system** that pings a Slack channel when a case is marked Done or escalated

---

## Contributing

This is an internal tool. To propose changes, open a pull request against `main` with a description of what you changed and why. Tag the compliance team lead for review.

---

## License

Internal use only.
