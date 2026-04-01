export interface ListSummary {
  name: string;
  count: number;
}

export interface ListDetail {
  name: string;
  addresses: string[];
}

export async function getCredentials(): Promise<{ user: string }> {
  const res = await fetch("/api/credentials");
  return res.json();
}

export async function saveCredentials(user: string, app_pass: string): Promise<void> {
  await fetch("/api/credentials", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user, app_pass }),
  });
}

export async function getLists(): Promise<ListSummary[]> {
  const res = await fetch("/api/lists");
  const data = await res.json();
  return data.lists;
}

export async function getList(name: string): Promise<ListDetail> {
  const res = await fetch(`/api/lists/${encodeURIComponent(name)}`);
  return res.json();
}

export async function saveList(name: string, addresses: string[]): Promise<void> {
  await fetch(`/api/lists/${encodeURIComponent(name)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ addresses }),
  });
}

export async function deleteList(name: string): Promise<boolean> {
  const res = await fetch(`/api/lists/${encodeURIComponent(name)}`, {
    method: "DELETE",
  });
  return res.ok;
}

export async function sendEmail(
  subject: string,
  to: string,
  html_body: string
): Promise<string> {
  const res = await fetch("/api/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subject, to, html_body }),
  });
  const data = await res.json();
  return data.result;
}

export async function uploadHtml(file: File): Promise<string> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/upload-html", { method: "POST", body: form });
  const data = await res.json();
  return data.html;
}
