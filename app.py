"""Frndo Webmail – launcher and CLI interface.

Usage examples:
    # Launch the web UI (default)
    python app.py

    # Save credentials
    python app.py creds --user you@gmail.com --pass "xxxx xxxx xxxx xxxx"

    # Manage email lists
    python app.py list-show                          # show all lists
    python app.py list-show --name "Beta Testers"    # show one list
    python app.py list-save --name "Beta Testers" --addresses a@x.com b@x.com
    python app.py list-delete --name "Beta Testers"

    # Send an email
    python app.py send --subject "Hello" --html email.html --to a@x.com b@x.com
    python app.py send --subject "Hello" --html email.html --list "Beta Testers"
"""

import argparse
import sys

import config
import mailer


def cmd_ui(args: argparse.Namespace) -> None:
    import ui

    ui.build_ui().launch(
        inbrowser=not args.no_browser,
        server_port=args.port,
    )


def cmd_creds(args: argparse.Namespace) -> None:
    if args.user and args.app_pass:
        config.save_credentials(args.user, args.app_pass)
        print("Credentials saved.")
    else:
        user, _ = config.load_credentials()
        if user:
            print(f"Stored user: {user}")
        else:
            print("No credentials stored.")


def cmd_list_show(args: argparse.Namespace) -> None:
    if args.name:
        addresses = config.get_list(args.name)
        if not addresses:
            print(f"List '{args.name}' not found or empty.")
            return
        print(f"List '{args.name}' ({len(addresses)} addresses):")
        for addr in addresses:
            print(f"  {addr}")
    else:
        names = config.list_names()
        if not names:
            print("No email lists configured.")
            return
        for name in names:
            count = len(config.get_list(name))
            print(f"  {name} ({count})")


def cmd_list_save(args: argparse.Namespace) -> None:
    config.save_list(args.name, args.addresses)
    print(f"List '{args.name}' saved with {len(args.addresses)} address(es).")


def cmd_list_delete(args: argparse.Namespace) -> None:
    if config.delete_list(args.name):
        print(f"List '{args.name}' deleted.")
    else:
        print(f"List '{args.name}' not found.")
        sys.exit(1)


def cmd_send(args: argparse.Namespace) -> None:
    user, pw = config.load_credentials()
    if args.user:
        user = args.user
    if args.app_pass:
        pw = args.app_pass
    if not user or not pw:
        print("Error: Gmail credentials required. Use 'creds' command or --user/--pass.")
        sys.exit(1)

    recipients: list[str] = []
    if args.to:
        recipients.extend(args.to)
    if args.list:
        addresses = config.get_list(args.list)
        if not addresses:
            print(f"Error: List '{args.list}' not found or empty.")
            sys.exit(1)
        recipients.extend(addresses)

    if not recipients:
        print("Error: Specify recipients with --to and/or --list.")
        sys.exit(1)

    result = mailer.send_email_from_file(
        user, pw, recipients, args.subject, args.html, args.from_name
    )
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Frndo Webmail – send HTML emails via Gmail"
    )
    sub = parser.add_subparsers(dest="command")

    # ── ui (default) ──────────────────────────────────────────────────────
    p_ui = sub.add_parser("ui", help="Launch the web UI")
    p_ui.add_argument("--port", type=int, default=7860)
    p_ui.add_argument("--no-browser", action="store_true")

    # ── creds ─────────────────────────────────────────────────────────────
    p_creds = sub.add_parser("creds", help="View or save Gmail credentials")
    p_creds.add_argument("--user", help="Gmail address")
    p_creds.add_argument("--pass", dest="app_pass", help="Gmail App Password")

    # ── list-show ─────────────────────────────────────────────────────────
    p_ls = sub.add_parser("list-show", help="Show email lists")
    p_ls.add_argument("--name", help="Show a specific list")

    # ── list-save ─────────────────────────────────────────────────────────
    p_lsave = sub.add_parser("list-save", help="Create or update an email list")
    p_lsave.add_argument("--name", required=True)
    p_lsave.add_argument("--addresses", nargs="+", required=True)

    # ── list-delete ───────────────────────────────────────────────────────
    p_ldel = sub.add_parser("list-delete", help="Delete an email list")
    p_ldel.add_argument("--name", required=True)

    # ── send ──────────────────────────────────────────────────────────────
    p_send = sub.add_parser("send", help="Send an HTML email")
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--html", required=True, help="Path to HTML file")
    p_send.add_argument("--to", nargs="+", help="Recipient addresses")
    p_send.add_argument("--list", help="Name of a saved email list")
    p_send.add_argument("--user", help="Override stored Gmail address")
    p_send.add_argument("--pass", dest="app_pass", help="Override stored App Password")
    p_send.add_argument("--from-name", dest="from_name", help="Display name for From header")

    args = parser.parse_args()

    dispatch = {
        "ui": cmd_ui,
        "creds": cmd_creds,
        "list-show": cmd_list_show,
        "list-save": cmd_list_save,
        "list-delete": cmd_list_delete,
        "send": cmd_send,
    }

    if args.command is None:
        # Default: launch the UI
        args.port = 7860
        args.no_browser = False
        cmd_ui(args)
    else:
        dispatch[args.command](args)


if __name__ == "__main__":
    main()
