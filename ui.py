"""Gradio web UI – Config and Send tabs."""

from pathlib import Path

import gradio as gr

import config
import mailer


def build_ui() -> gr.Blocks:
    saved_user, saved_pass = config.load_credentials()

    with gr.Blocks(title="Frndo Webmail") as app:
        gr.Markdown("# Frndo Webmail")

        with gr.Tabs():
            # ── Send tab ─────────────────────────────────────────────────
            with gr.Tab("Send"):
                with gr.Row():
                    with gr.Column(scale=1):
                        subject = gr.Textbox(
                            label="Subject",
                            placeholder="Your email subject line",
                        )
                        list_dropdown = gr.Dropdown(
                            label="Email List",
                            choices=["(None)"] + config.list_names(),
                            value="(None)",
                            interactive=True,
                        )
                        to_addresses = gr.Textbox(
                            label="Recipients (comma or newline separated)",
                            lines=4,
                            placeholder="alice@example.com, bob@example.com",
                        )
                        html_file = gr.File(
                            label="Upload HTML Email",
                            file_types=[".html", ".htm"],
                            type="filepath",
                        )
                        send_btn = gr.Button("Send Email", variant="primary")
                        output = gr.Textbox(
                            label="Result", lines=6, interactive=False
                        )

                    with gr.Column(scale=2):
                        preview = gr.HTML(label="Email Preview", value="")

                # ── Send-tab callbacks ────────────────────────────────────

                def on_list_selected(list_name: str, current_text: str) -> str:
                    if list_name == "(None)":
                        return current_text
                    addresses = config.get_list(list_name)
                    return ", ".join(addresses)

                list_dropdown.change(
                    fn=on_list_selected,
                    inputs=[list_dropdown, to_addresses],
                    outputs=to_addresses,
                )

                def on_html_uploaded(filepath) -> str:
                    if filepath is None:
                        return ""
                    return Path(filepath).read_text(encoding="utf-8")

                html_file.change(
                    fn=on_html_uploaded,
                    inputs=html_file,
                    outputs=preview,
                )

                def on_send(to_text: str, subj: str, filepath):
                    user, pw = config.load_credentials()
                    if not user or not pw:
                        return "Error: Configure Gmail credentials on the Config tab first."
                    if not to_text.strip():
                        return "Error: At least one recipient is required."
                    if not subj.strip():
                        return "Error: Subject is required."
                    if filepath is None:
                        return "Error: Please upload an HTML email file."

                    recipients = mailer.parse_recipients(to_text)
                    return mailer.send_email_from_file(
                        user, pw, recipients, subj, filepath
                    )

                send_btn.click(
                    fn=on_send,
                    inputs=[to_addresses, subject, html_file],
                    outputs=output,
                )

            # ── Config tab ───────────────────────────────────────────────
            with gr.Tab("Config"):
                gr.Markdown("## Gmail Credentials")
                with gr.Row():
                    gmail_user = gr.Textbox(
                        label="Gmail Address",
                        value=saved_user,
                        placeholder="you@gmail.com",
                    )
                    gmail_app_pass = gr.Textbox(
                        label="Gmail App Password",
                        value=saved_pass,
                        type="password",
                        placeholder="xxxx xxxx xxxx xxxx",
                    )
                save_creds_btn = gr.Button("Save Credentials")
                creds_status = gr.Textbox(
                    label="Status", interactive=False, lines=1
                )

                def on_save_creds(user: str, pw: str) -> str:
                    if not user or not pw:
                        return "Please fill in both fields."
                    config.save_credentials(user, pw)
                    return "Credentials saved."

                save_creds_btn.click(
                    fn=on_save_creds,
                    inputs=[gmail_user, gmail_app_pass],
                    outputs=creds_status,
                )

                # ── Email lists ───────────────────────────────────────────
                gr.Markdown("---")
                gr.Markdown("## Email Lists")

                with gr.Row():
                    with gr.Column(scale=1):
                        list_selector = gr.Dropdown(
                            label="Select a List",
                            choices=config.list_names(),
                            interactive=True,
                        )
                        refresh_btn = gr.Button("Refresh Lists")

                    with gr.Column(scale=2):
                        list_name_input = gr.Textbox(
                            label="List Name",
                            placeholder="e.g. Beta Testers",
                        )
                        list_addresses_input = gr.Textbox(
                            label="Addresses (comma or newline separated)",
                            lines=5,
                            placeholder="alice@example.com\nbob@example.com",
                        )

                with gr.Row():
                    save_list_btn = gr.Button("Save List", variant="primary")
                    delete_list_btn = gr.Button("Delete List", variant="stop")

                lists_status = gr.Textbox(
                    label="Status", interactive=False, lines=1
                )

                def refresh_lists():
                    names = config.list_names()
                    send_choices = ["(None)"] + names
                    return (
                        gr.update(choices=names, value=None),
                        gr.update(choices=send_choices, value="(None)"),
                    )

                refresh_btn.click(
                    fn=refresh_lists,
                    outputs=[list_selector, list_dropdown],
                )

                def on_list_selector_change(name: str):
                    if not name:
                        return "", ""
                    addresses = config.get_list(name)
                    return name, "\n".join(addresses)

                list_selector.change(
                    fn=on_list_selector_change,
                    inputs=list_selector,
                    outputs=[list_name_input, list_addresses_input],
                )

                def on_save_list(name: str, addrs_text: str):
                    if not name.strip():
                        return (
                            "Error: List name is required.",
                            gr.update(),
                            gr.update(),
                        )
                    addresses = mailer.parse_recipients(addrs_text)
                    config.save_list(name.strip(), addresses)
                    names = config.list_names()
                    send_choices = ["(None)"] + names
                    return (
                        f"List '{name.strip()}' saved with {len(addresses)} address(es).",
                        gr.update(choices=names, value=name.strip()),
                        gr.update(choices=send_choices),
                    )

                save_list_btn.click(
                    fn=on_save_list,
                    inputs=[list_name_input, list_addresses_input],
                    outputs=[lists_status, list_selector, list_dropdown],
                )

                def on_delete_list(name: str):
                    if not name or not name.strip():
                        return (
                            "Error: Select a list to delete.",
                            gr.update(),
                            gr.update(),
                            "",
                            "",
                        )
                    deleted = config.delete_list(name.strip())
                    if not deleted:
                        return (
                            f"Error: List '{name}' not found.",
                            gr.update(),
                            gr.update(),
                            name,
                            "",
                        )
                    names = config.list_names()
                    send_choices = ["(None)"] + names
                    return (
                        f"List '{name}' deleted.",
                        gr.update(choices=names, value=None),
                        gr.update(choices=send_choices, value="(None)"),
                        "",
                        "",
                    )

                delete_list_btn.click(
                    fn=on_delete_list,
                    inputs=list_selector,
                    outputs=[
                        lists_status,
                        list_selector,
                        list_dropdown,
                        list_name_input,
                        list_addresses_input,
                    ],
                )

    return app
