"""FastAPI backend serving API endpoints and the React frontend."""

from __future__ import annotations

import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import (
    delete_list,
    get_list,
    list_names,
    load_credentials,
    save_credentials,
    save_list,
)
from mailer import parse_recipients, send_email

# ── Pydantic models ────────────────────────────────────────────────────────────


class CredentialsRequest(BaseModel):
    user: str
    app_pass: str


class CredentialsResponse(BaseModel):
    user: str


class StatusResponse(BaseModel):
    status: str


class ListSummary(BaseModel):
    name: str
    count: int


class ListsResponse(BaseModel):
    lists: list[ListSummary]


class ListDetailResponse(BaseModel):
    name: str
    addresses: list[str]


class SaveListRequest(BaseModel):
    addresses: list[str]


class SaveListResponse(BaseModel):
    status: str
    count: int


class SendRequest(BaseModel):
    subject: str
    to: str
    html_body: str


class SendResponse(BaseModel):
    result: str


class UploadHtmlResponse(BaseModel):
    html: str


# ── FastAPI app ─────────────────────────────────────────────────────────────────

app = FastAPI(title="Frndo Webmail")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API endpoints ───────────────────────────────────────────────────────────────


@app.get("/api/credentials", response_model=CredentialsResponse)
def api_get_credentials():
    user, _ = load_credentials()
    return CredentialsResponse(user=user)


@app.post("/api/credentials", response_model=StatusResponse)
def api_save_credentials(body: CredentialsRequest):
    save_credentials(body.user, body.app_pass)
    return StatusResponse(status="ok")


@app.get("/api/lists", response_model=ListsResponse)
def api_get_lists():
    names = list_names()
    summaries = [
        ListSummary(name=n, count=len(get_list(n))) for n in names
    ]
    return ListsResponse(lists=summaries)


@app.get("/api/lists/{name}", response_model=ListDetailResponse)
def api_get_list(name: str):
    addresses = get_list(name)
    return ListDetailResponse(name=name, addresses=addresses)


@app.post("/api/lists/{name}", response_model=SaveListResponse)
def api_save_list(name: str, body: SaveListRequest):
    save_list(name, body.addresses)
    return SaveListResponse(status="ok", count=len(body.addresses))


@app.delete("/api/lists/{name}", response_model=StatusResponse)
def api_delete_list(name: str):
    if not delete_list(name):
        raise HTTPException(status_code=404, detail="List not found")
    return StatusResponse(status="ok")


@app.post("/api/send", response_model=SendResponse)
def api_send(body: SendRequest):
    user, app_pass = load_credentials()
    if not user or not app_pass:
        raise HTTPException(status_code=400, detail="Credentials not configured")
    recipients = parse_recipients(body.to)
    if not recipients:
        raise HTTPException(status_code=400, detail="No valid recipients")
    result = send_email(user, app_pass, recipients, body.subject, body.html_body)
    return SendResponse(result=result)


@app.post("/api/upload-html", response_model=UploadHtmlResponse)
async def api_upload_html(file: UploadFile = File(...)):
    content = await file.read()
    html = content.decode("utf-8")
    return UploadHtmlResponse(html=html)


# ── Static file serving (React frontend) ───────────────────────────────────────

_dist_dir = Path(__file__).parent.parent / "react_frontend" / "dist"
if _dist_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_dist_dir), html=True), name="spa")


# ── Server runner ───────────────────────────────────────────────────────────────


def run_server(port: int = 8000, open_browser: bool = True) -> None:
    """Start the uvicorn server, optionally opening a browser."""
    if open_browser:
        threading.Timer(
            1.5, webbrowser.open, args=(f"http://localhost:{port}",)
        ).start()
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    run_server()
