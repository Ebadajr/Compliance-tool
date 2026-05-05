# ── Auth config ────────────────────────────────────────────────────────────────
# Hardcoded users.
# role: "admin" → Admin view  |  "user" → Member (EDD tracker) view

ADMIN_ROLE = "admin"
USER_ROLE  = "user"

USERS = {
    "Admin": {
        "display":      "Admin",
        "display_name": "Admin",   # kept for login.py compatibility
        "role":   ADMIN_ROLE,
        "avatar": "AD",
    },
    "Sara": {
        "display":      "Sara Nour",
        "display_name": "Sara Nour",
        "role":   USER_ROLE,
        "avatar": "SN",
    },
    "Khaled": {
        "display":      "Khaled Farouk",
        "display_name": "Khaled Farouk",
        "role":   USER_ROLE,
        "avatar": "KF",
    },
}

# ── Lookup helpers ─────────────────────────────────────────────────────────────

def get_user(username: str) -> dict | None:
    return USERS.get(username)

def all_usernames() -> list[str]:
    return list(USERS.keys())

def is_admin(username: str) -> bool:
    u = get_user(username)
    return u is not None and u["role"] == ADMIN_ROLE

def get_display_name(username: str) -> str:
    u = get_user(username)
    return u["display"] if u else username

def get_non_admin_users() -> list[str]:
    """Return list of usernames whose role is not admin."""
    return [k for k, v in USERS.items() if v["role"] != ADMIN_ROLE]