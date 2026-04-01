"""Email sending logic."""

from __future__ import annotations

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Matches "Display Name <addr>" or bare "addr"
_ANGLE_RE = re.compile(r"<([^>]+)>")
_BARE_RE = re.compile(r"[^\s,<>]+@[^\s,<>]+")


def parse_recipients(text: str) -> list[str]:
    """Extract email addresses from comma-or-newline-separated text.

    Handles both bare addresses and "Name <addr>" format.
    Returns a deduplicated list preserving order.
    """
    seen: set[str] = set()
    result: list[str] = []

    for entry in re.split(r"[,\n]+", text):
        entry = entry.strip()
        if not entry:
            continue
        # Try "Name <addr>" first
        m = _ANGLE_RE.search(entry)
        if m:
            addr = m.group(1).strip().lower()
        else:
            # Bare address
            m = _BARE_RE.search(entry)
            if not m:
                continue
            addr = m.group(0).strip().lower()
        if addr not in seen:
            seen.add(addr)
            result.append(addr)
    return result


def send_email(
    gmail_user: str,
    gmail_app_pass: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    from_name: str | None = None,
) -> str:
    """Send one email BCC'd to all recipients. Returns a status string."""
    display_name = from_name or gmail_user
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_pass)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{display_name} <{gmail_user}>"
            msg["To"] = gmail_user  # sender appears as To
            msg.attach(MIMEText(html_body, "html"))

            # Single sendmail call — all recipients receive via BCC
            all_recipients = [gmail_user] + [r for r in recipients if r != gmail_user]
            server.sendmail(gmail_user, all_recipients, msg.as_string())

    except smtplib.SMTPAuthenticationError:
        return "Error: Authentication failed. Check your Gmail address and App Password."
    except Exception as e:
        return f"Error: {e}"

    lines = [f"  BCC -> {r}" for r in recipients]
    return f"Sent 1 email to {len(recipients)} recipient(s):\n" + "\n".join(lines)


def send_email_from_file(
    gmail_user: str,
    gmail_app_pass: str,
    recipients: list[str],
    subject: str,
    html_path: str | Path,
    from_name: str | None = None,
) -> str:
    """Convenience wrapper that reads the HTML from a file path."""
    html_body = Path(html_path).read_text(encoding="utf-8")
    return send_email(
        gmail_user, gmail_app_pass, recipients, subject, html_body, from_name
    )
