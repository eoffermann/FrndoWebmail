# B2C Webmail

A lightweight tool for sending HTML emails via Gmail. Supports managed email lists, BCC group sends, and three UI options: PyQt6 (desktop), React (web), and Gradio (web).

## Setup

```bash
pip install -r requirements.txt
```

For the React UI, the frontend is pre-built — no Node.js required. To modify the React frontend, install Node.js and run:

```bash
cd react_frontend && npm install && npm run build
```

You'll need a [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your regular Gmail password).

## UI

```bash
# Launch the default UI (PyQt6 desktop app)
python app.py

# Choose a specific UI framework
python app.py --ui pyqt6    # Native desktop app (default)
python app.py --ui react    # Modern web app on port 7860
python app.py --ui gradio   # Gradio web app on port 7860

# Web UIs accept port and browser options
python app.py --ui react ui --port 8080 --no-browser
```

### PyQt6 (default)
Native desktop application with dark/light theme toggle and a settings modal dialog.

### React
Modern single-page web app with dark/light theme toggle. Settings slides in as a drawer panel from the right.

### Gradio
Two-tab web interface — Send and Config. The original UI.

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

| File / Directory | Purpose |
|------------------|---------|
| `app.py` | Entry point — argparse CLI and UI launcher |
| `config.py` | Credentials and email list management |
| `mailer.py` | Email parsing and SMTP sending |
| `ui/` | UI implementations |
| `ui/gradio_ui.py` | Gradio web interface |
| `ui/pyqt6_ui.py` | PyQt6 desktop interface |
| `ui/react_api.py` | FastAPI backend for React UI |
| `react_frontend/` | React + TypeScript SPA (Vite) |

## Recipient Format

The recipient parser accepts both bare addresses and named formats:

```
alice@example.com
Bob Smith <bob@example.com>
```

Comma-separated, newline-separated, or mixed.
