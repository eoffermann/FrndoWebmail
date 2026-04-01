"""PyQt6 desktop UI for Frndo Webmail."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

# ---------------------------------------------------------------------------
# Resolve backend modules (one directory up from ui/)
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

import config  # noqa: E402
import mailer  # noqa: E402

# ---------------------------------------------------------------------------
# QSS Themes
# ---------------------------------------------------------------------------

DARK_STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #1e1e2e;
    color: #e0e0e0;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}
QToolBar {
    background-color: #181828;
    border-bottom: 1px solid #333350;
    spacing: 6px;
    padding: 4px;
}
QToolBar QPushButton {
    background-color: transparent;
    color: #e0e0e0;
    border: none;
    font-size: 18px;
    padding: 4px 10px;
    border-radius: 6px;
}
QToolBar QPushButton:hover {
    background-color: #2a2a3e;
}
QLabel {
    color: #e0e0e0;
}
QLineEdit, QPlainTextEdit {
    background-color: #2a2a3e;
    color: #e0e0e0;
    border: 1px solid #444466;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #6c8ebf;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #6c8ebf;
}
QComboBox {
    background-color: #2a2a3e;
    color: #e0e0e0;
    border: 1px solid #444466;
    border-radius: 6px;
    padding: 6px 8px;
}
QComboBox QAbstractItemView {
    background-color: #2a2a3e;
    color: #e0e0e0;
    selection-background-color: #6c8ebf;
    border: 1px solid #444466;
}
QComboBox::drop-down {
    border: none;
}
QPushButton {
    background-color: #2a2a3e;
    color: #e0e0e0;
    border: 1px solid #444466;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #353550;
    border-color: #6c8ebf;
}
QPushButton:pressed {
    background-color: #444466;
}
QPushButton#sendBtn {
    background-color: #6c8ebf;
    color: #ffffff;
    font-weight: bold;
    border: none;
}
QPushButton#sendBtn:hover {
    background-color: #5a7dae;
}
QPushButton#sendBtn:pressed {
    background-color: #4a6d9e;
}
QPushButton#saveCredsBtn, QPushButton#saveListBtn {
    background-color: #6c8ebf;
    color: #ffffff;
    font-weight: bold;
    border: none;
}
QPushButton#saveCredsBtn:hover, QPushButton#saveListBtn:hover {
    background-color: #5a7dae;
}
QPushButton#deleteListBtn {
    background-color: #8b3a3a;
    color: #ffffff;
    border: none;
}
QPushButton#deleteListBtn:hover {
    background-color: #a04040;
}
QSplitter::handle {
    background-color: #333350;
    width: 2px;
}
QTabWidget::pane {
    border: 1px solid #444466;
    border-radius: 6px;
    background-color: #1e1e2e;
}
QTabBar::tab {
    background-color: #2a2a3e;
    color: #b0b0b0;
    border: 1px solid #444466;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 18px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #e0e0e0;
    border-bottom: 2px solid #6c8ebf;
}
"""

LIGHT_STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #f5f5f8;
    color: #1e1e2e;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d0d8;
    spacing: 6px;
    padding: 4px;
}
QToolBar QPushButton {
    background-color: transparent;
    color: #1e1e2e;
    border: none;
    font-size: 18px;
    padding: 4px 10px;
    border-radius: 6px;
}
QToolBar QPushButton:hover {
    background-color: #e8e8f0;
}
QLabel {
    color: #1e1e2e;
}
QLineEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #1e1e2e;
    border: 1px solid #c0c0cc;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #6c8ebf;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #6c8ebf;
}
QComboBox {
    background-color: #ffffff;
    color: #1e1e2e;
    border: 1px solid #c0c0cc;
    border-radius: 6px;
    padding: 6px 8px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1e1e2e;
    selection-background-color: #6c8ebf;
    border: 1px solid #c0c0cc;
}
QComboBox::drop-down {
    border: none;
}
QPushButton {
    background-color: #ffffff;
    color: #1e1e2e;
    border: 1px solid #c0c0cc;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #e8e8f0;
    border-color: #6c8ebf;
}
QPushButton:pressed {
    background-color: #d0d0d8;
}
QPushButton#sendBtn {
    background-color: #6c8ebf;
    color: #ffffff;
    font-weight: bold;
    border: none;
}
QPushButton#sendBtn:hover {
    background-color: #5a7dae;
}
QPushButton#sendBtn:pressed {
    background-color: #4a6d9e;
}
QPushButton#saveCredsBtn, QPushButton#saveListBtn {
    background-color: #6c8ebf;
    color: #ffffff;
    font-weight: bold;
    border: none;
}
QPushButton#saveCredsBtn:hover, QPushButton#saveListBtn:hover {
    background-color: #5a7dae;
}
QPushButton#deleteListBtn {
    background-color: #c04040;
    color: #ffffff;
    border: none;
}
QPushButton#deleteListBtn:hover {
    background-color: #d05050;
}
QSplitter::handle {
    background-color: #d0d0d8;
    width: 2px;
}
QTabWidget::pane {
    border: 1px solid #c0c0cc;
    border-radius: 6px;
    background-color: #f5f5f8;
}
QTabBar::tab {
    background-color: #e8e8f0;
    color: #606070;
    border: 1px solid #c0c0cc;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 18px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #f5f5f8;
    color: #1e1e2e;
    border-bottom: 2px solid #6c8ebf;
}
"""


# ---------------------------------------------------------------------------
# Settings Dialog
# ---------------------------------------------------------------------------

class SettingsDialog(QDialog):
    """Modal settings dialog with Credentials and Email Lists tabs."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 420)
        self._build_ui()
        self._load_credentials()
        self._refresh_list_selector()

    # ---- build ----

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        tabs = QTabWidget()
        tabs.addTab(self._build_credentials_tab(), "Credentials")
        tabs.addTab(self._build_lists_tab(), "Email Lists")
        layout.addWidget(tabs)

    def _build_credentials_tab(self) -> QWidget:
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(16, 16, 16, 16)
        vbox.setSpacing(10)

        vbox.addWidget(QLabel("Gmail Address"))
        self.creds_email = QLineEdit()
        self.creds_email.setPlaceholderText("you@gmail.com")
        vbox.addWidget(self.creds_email)

        vbox.addWidget(QLabel("App Password"))
        self.creds_password = QLineEdit()
        self.creds_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.creds_password.setPlaceholderText("xxxx xxxx xxxx xxxx")
        vbox.addWidget(self.creds_password)

        save_btn = QPushButton("Save Credentials")
        save_btn.setObjectName("saveCredsBtn")
        save_btn.clicked.connect(self._save_credentials)
        vbox.addWidget(save_btn)

        self.creds_status = QLabel("")
        self.creds_status.setWordWrap(True)
        vbox.addWidget(self.creds_status)

        vbox.addStretch()
        return tab

    def _build_lists_tab(self) -> QWidget:
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(16, 16, 16, 16)
        vbox.setSpacing(10)

        vbox.addWidget(QLabel("Select List"))
        self.list_selector = QComboBox()
        self.list_selector.currentTextChanged.connect(self._on_list_selected)
        vbox.addWidget(self.list_selector)

        vbox.addWidget(QLabel("List Name"))
        self.list_name = QLineEdit()
        self.list_name.setPlaceholderText("e.g. Beta Testers")
        vbox.addWidget(self.list_name)

        vbox.addWidget(QLabel("Addresses (one per line or comma-separated)"))
        self.list_addresses = QPlainTextEdit()
        self.list_addresses.setMaximumHeight(120)
        vbox.addWidget(self.list_addresses)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save List")
        save_btn.setObjectName("saveListBtn")
        save_btn.clicked.connect(self._save_list)
        btn_row.addWidget(save_btn)

        del_btn = QPushButton("Delete List")
        del_btn.setObjectName("deleteListBtn")
        del_btn.clicked.connect(self._delete_list)
        btn_row.addWidget(del_btn)
        vbox.addLayout(btn_row)

        self.list_status = QLabel("")
        self.list_status.setWordWrap(True)
        vbox.addWidget(self.list_status)

        vbox.addStretch()
        return tab

    # ---- credentials helpers ----

    def _load_credentials(self) -> None:
        user, pw = config.load_credentials()
        self.creds_email.setText(user)
        self.creds_password.setText(pw)

    def _save_credentials(self) -> None:
        user = self.creds_email.text().strip()
        pw = self.creds_password.text().strip()
        if not user or not pw:
            self.creds_status.setText("Both fields are required.")
            return
        config.save_credentials(user, pw)
        self.creds_status.setText("Credentials saved.")

    # ---- list helpers ----

    def _refresh_list_selector(self) -> None:
        self.list_selector.blockSignals(True)
        self.list_selector.clear()
        self.list_selector.addItem("(New List)")
        for name in config.list_names():
            self.list_selector.addItem(name)
        self.list_selector.blockSignals(False)
        self._on_list_selected(self.list_selector.currentText())

    def _on_list_selected(self, name: str) -> None:
        if name == "(New List)" or not name:
            self.list_name.clear()
            self.list_addresses.clear()
            return
        self.list_name.setText(name)
        addresses = config.get_list(name)
        self.list_addresses.setPlainText("\n".join(addresses))

    def _save_list(self) -> None:
        name = self.list_name.text().strip()
        if not name:
            self.list_status.setText("List name is required.")
            return
        raw = self.list_addresses.toPlainText()
        addresses = mailer.parse_recipients(raw)
        if not addresses:
            self.list_status.setText("No valid addresses found.")
            return
        config.save_list(name, addresses)
        self.list_status.setText(f"List \"{name}\" saved with {len(addresses)} address(es).")
        self._refresh_list_selector()

    def _delete_list(self) -> None:
        name = self.list_name.text().strip()
        if not name:
            self.list_status.setText("Enter the list name to delete.")
            return
        if config.delete_list(name):
            self.list_status.setText(f"List \"{name}\" deleted.")
            self.list_name.clear()
            self.list_addresses.clear()
            self._refresh_list_selector()
        else:
            self.list_status.setText(f"List \"{name}\" not found.")


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Frndo Webmail")
        self.setMinimumSize(900, 560)
        self.resize(1060, 640)

        self._dark = True
        self._html_path: str | None = None

        self._build_toolbar()
        self._build_central()
        self._refresh_email_lists()

    # ---- toolbar ----

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        settings_btn = QPushButton("\u2699")
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self._open_settings)
        toolbar.addWidget(settings_btn)

        self._theme_btn = QPushButton("\u2600")
        self._theme_btn.setToolTip("Toggle theme")
        self._theme_btn.clicked.connect(self._toggle_theme)
        toolbar.addWidget(self._theme_btn)

    # ---- central widget ----

    def _build_central(self) -> None:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- left panel (send form) ---
        left = QWidget()
        form = QVBoxLayout(left)
        form.setContentsMargins(16, 16, 16, 16)
        form.setSpacing(10)

        form.addWidget(QLabel("Subject"))
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Email subject line")
        form.addWidget(self.subject_input)

        form.addWidget(QLabel("Email List"))
        self.list_combo = QComboBox()
        self.list_combo.currentTextChanged.connect(self._on_list_changed)
        form.addWidget(self.list_combo)

        form.addWidget(QLabel("Recipients"))
        self.recipients_input = QPlainTextEdit()
        self.recipients_input.setPlaceholderText(
            "Comma or newline separated email addresses..."
        )
        self.recipients_input.setMaximumHeight(100)
        form.addWidget(self.recipients_input)

        upload_row = QHBoxLayout()
        upload_btn = QPushButton("Upload HTML")
        upload_btn.clicked.connect(self._upload_html)
        upload_row.addWidget(upload_btn)
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #888;")
        upload_row.addWidget(self.file_label, 1)
        form.addLayout(upload_row)

        send_btn = QPushButton("Send Email")
        send_btn.setObjectName("sendBtn")
        send_btn.clicked.connect(self._send)
        form.addWidget(send_btn)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        form.addWidget(self.result_label)

        form.addStretch()

        # --- right panel (HTML preview) ---
        self.preview = QWebEngineView()
        self.preview.setHtml(
            "<html><body style='background:#2a2a3e;color:#888;"
            "display:flex;align-items:center;justify-content:center;"
            "height:100vh;margin:0;font-family:sans-serif;'>"
            "<p>Upload an HTML file to preview it here.</p>"
            "</body></html>"
        )

        splitter.addWidget(left)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        self.setCentralWidget(splitter)

    # ---- slots ----

    def _refresh_email_lists(self) -> None:
        self.list_combo.blockSignals(True)
        self.list_combo.clear()
        self.list_combo.addItem("(None)")
        for name in config.list_names():
            self.list_combo.addItem(name)
        self.list_combo.blockSignals(False)

    def _on_list_changed(self, name: str) -> None:
        if name == "(None)" or not name:
            return
        addresses = config.get_list(name)
        self.recipients_input.setPlainText("\n".join(addresses))

    def _upload_html(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select HTML File", "", "HTML Files (*.html *.htm)"
        )
        if not path:
            return
        self._html_path = path
        self.file_label.setText(Path(path).name)
        self.preview.setUrl(QUrl.fromLocalFile(path))

    def _send(self) -> None:
        user, pw = config.load_credentials()
        if not user or not pw:
            self.result_label.setText(
                "No credentials configured. Open Settings to add them."
            )
            return

        subject = self.subject_input.text().strip()
        if not subject:
            self.result_label.setText("Subject is required.")
            return

        recipients = mailer.parse_recipients(self.recipients_input.toPlainText())
        if not recipients:
            self.result_label.setText("At least one valid recipient is required.")
            return

        if not self._html_path:
            self.result_label.setText("Upload an HTML file first.")
            return

        self.result_label.setText("Sending...")
        QApplication.processEvents()

        result = mailer.send_email_from_file(
            gmail_user=user,
            gmail_app_pass=pw,
            recipients=recipients,
            subject=subject,
            html_path=self._html_path,
        )
        self.result_label.setText(result)

    def _open_settings(self) -> None:
        dlg = SettingsDialog(self)
        dlg.exec()
        self._refresh_email_lists()

    def _toggle_theme(self) -> None:
        app = QApplication.instance()
        if app is None:
            return
        self._dark = not self._dark
        if self._dark:
            app.setStyleSheet(DARK_STYLE)
            self._theme_btn.setText("\u2600")
        else:
            app.setStyleSheet(LIGHT_STYLE)
            self._theme_btn.setText("\U0001f319")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_app() -> None:
    """Create and run the PyQt6 application."""
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
