import { useCallback, useEffect, useRef, useState } from "react";
import { getLists, getList, sendEmail, uploadHtml, type ListSummary } from "../api";

export default function SendPanel() {
  const [lists, setLists] = useState<ListSummary[]>([]);
  const [selectedList, setSelectedList] = useState("(None)");
  const [subject, setSubject] = useState("");
  const [recipients, setRecipients] = useState("");
  const [htmlBody, setHtmlBody] = useState("");
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState("");
  const [sending, setSending] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const dropRef = useRef<HTMLDivElement>(null);

  const refreshLists = useCallback(async () => {
    try {
      setLists(await getLists());
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    refreshLists();
  }, [refreshLists]);

  const handleListChange = async (name: string) => {
    setSelectedList(name);
    if (name === "(None)") return;
    try {
      const detail = await getList(name);
      setRecipients(detail.addresses.join(", "));
    } catch {
      /* ignore */
    }
  };

  const handleFile = async (file: File) => {
    setFileName(file.name);
    try {
      const html = await uploadHtml(file);
      setHtmlBody(html);
    } catch {
      setResult("Error uploading file.");
    }
  };

  const onFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    dropRef.current?.classList.remove("drag-over");
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    dropRef.current?.classList.add("drag-over");
  };

  const onDragLeave = () => {
    dropRef.current?.classList.remove("drag-over");
  };

  const handleSend = async () => {
    if (!subject.trim()) return setResult("Error: Subject is required.");
    if (!recipients.trim()) return setResult("Error: At least one recipient is required.");
    if (!htmlBody) return setResult("Error: Please upload an HTML email file.");

    setSending(true);
    setResult("");
    try {
      const r = await sendEmail(subject, recipients, htmlBody);
      setResult(r);
    } catch {
      setResult("Error: Failed to send email.");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="send-panel">
      <div className="send-form">
        <label>Subject</label>
        <input
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Your email subject line"
        />

        <label>Email List</label>
        <select value={selectedList} onChange={(e) => handleListChange(e.target.value)}>
          <option value="(None)">(None)</option>
          {lists.map((l) => (
            <option key={l.name} value={l.name}>
              {l.name} ({l.count})
            </option>
          ))}
        </select>

        <label>Recipients</label>
        <textarea
          rows={4}
          value={recipients}
          onChange={(e) => setRecipients(e.target.value)}
          placeholder="alice@example.com, bob@example.com"
        />

        <label>HTML Email</label>
        <div
          ref={dropRef}
          className="drop-zone"
          onClick={() => fileRef.current?.click()}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
        >
          <input
            ref={fileRef}
            type="file"
            accept=".html,.htm"
            onChange={onFileInput}
            hidden
          />
          {fileName ? (
            <span className="file-name">📄 {fileName}</span>
          ) : (
            <span className="drop-hint">Drop .html file here or click to browse</span>
          )}
        </div>

        <button className="btn-primary" onClick={handleSend} disabled={sending}>
          {sending ? "Sending…" : "Send Email"}
        </button>

        {result && <div className="result-box">{result}</div>}
      </div>

      <div className="preview-pane">
        <label>Email Preview</label>
        {htmlBody ? (
          <iframe
            title="Email Preview"
            srcDoc={htmlBody}
            sandbox=""
            className="preview-iframe"
          />
        ) : (
          <div className="preview-placeholder">Upload an HTML file to preview</div>
        )}
      </div>
    </div>
  );
}
