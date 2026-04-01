"""UI framework dispatcher."""


def launch(framework: str, port: int = 7860, no_browser: bool = False) -> None:
    if framework == "gradio":
        from ui.gradio_ui import build_ui

        build_ui().launch(inbrowser=not no_browser, server_port=port)
    elif framework == "react":
        from ui.react_api import run_server

        run_server(port=port, open_browser=not no_browser)
    elif framework == "pyqt6":
        from ui.pyqt6_ui import run_app

        run_app()
    else:
        raise ValueError(f"Unknown UI framework: {framework}")
