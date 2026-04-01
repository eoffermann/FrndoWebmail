# Frndo Webmail

A lightweight tool for sending HTML emails via Gmail, built with [Gradio](https://gradio.app). Supports managed email lists, BCC group sends, and both a web UI and full CLI.

## Setup

```bash
pip install -r requirements.txt
```

You'll need a [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your regular Gmail password).

## Web UI

```bash
python app.py
```

Opens a browser with two tabs:

- **Send** — Upload an HTML email, pick recipients (from a saved list or manually), preview, and send.
- **Config** — Save Gmail credentials and manage email lists.

## CLI

Every operation available in the UI is also available from the command line.

```bash
# Credentials
python app.py creds --user you@gmail.com --pass "xxxx xxxx xxxx xxxx"

# Email lists
python app.py list-show
python app.py list-show --name "Beta Testers"
python app.py list-save --name "Beta Testers" --addresses a@x.com b@x.com c@x.com
python app.py list-delete --name "Beta Testers"

# Send
python app.py send --subject "Hello" --html email.html --list "Beta Testers"
python app.py send --subject "Hello" --html email.html --to a@x.com b@x.com
python app.py send --subject "Hello" --html email.html --list "Beta Testers" --to extra@x.com
```

Emails are sent as a single message with all recipients BCC'd.

## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Entry point — argparse CLI and web UI launcher |
| `config.py` | Credentials and email list management |
| `mailer.py` | Email parsing and SMTP sending |
| `ui.py` | Gradio web interface |

## Recipient Format

The recipient parser accepts both bare addresses and named formats:

```
alice@example.com
Bob Smith <bob@example.com>
```

Comma-separated, newline-separated, or mixed.
