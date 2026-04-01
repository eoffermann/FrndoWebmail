"""Credentials and email-list management."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent
CREDENTIALS_FILE = DATA_DIR / ".credentials.json"
EMAIL_LISTS_FILE = DATA_DIR / ".email_lists.json"


# ── credentials ──────────────────────────────────────────────────────────────

def load_credentials() -> tuple[str, str]:
    if CREDENTIALS_FILE.exists():
        data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
        return data.get("gmail_user", ""), data.get("gmail_app_pass", "")
    return "", ""


def save_credentials(gmail_user: str, gmail_app_pass: str) -> None:
    CREDENTIALS_FILE.write_text(
        json.dumps({"gmail_user": gmail_user, "gmail_app_pass": gmail_app_pass}),
        encoding="utf-8",
    )


# ── email lists ──────────────────────────────────────────────────────────────

def _load_all_lists() -> dict[str, list[str]]:
    if EMAIL_LISTS_FILE.exists():
        return json.loads(EMAIL_LISTS_FILE.read_text(encoding="utf-8"))
    return {}


def _save_all_lists(lists: dict[str, list[str]]) -> None:
    EMAIL_LISTS_FILE.write_text(
        json.dumps(lists, indent=2), encoding="utf-8"
    )


def list_names() -> list[str]:
    return sorted(_load_all_lists().keys())


def get_list(name: str) -> list[str]:
    return _load_all_lists().get(name, [])


def save_list(name: str, addresses: list[str]) -> None:
    lists = _load_all_lists()
    lists[name] = addresses
    _save_all_lists(lists)


def delete_list(name: str) -> bool:
    lists = _load_all_lists()
    if name in lists:
        del lists[name]
        _save_all_lists(lists)
        return True
    return False


def rename_list(old_name: str, new_name: str) -> bool:
    lists = _load_all_lists()
    if old_name not in lists or new_name in lists:
        return False
    lists[new_name] = lists.pop(old_name)
    _save_all_lists(lists)
    return True
