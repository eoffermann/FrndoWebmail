import { useEffect, useState } from "react";
import {
  getCredentials,
  saveCredentials,
  getLists,
  getList,
  saveList,
  deleteList,
  type ListSummary,
} from "../api";

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function SettingsPanel({ open, onClose }: Props) {
  // Credentials
  const [gmailUser, setGmailUser] = useState("");
  const [gmailPass, setGmailPass] = useState("");
  const [credStatus, setCredStatus] = useState("");

  // Lists
  const [lists, setLists] = useState<ListSummary[]>([]);
  const [selectedList, setSelectedList] = useState("");
  const [listName, setListName] = useState("");
  const [listAddresses, setListAddresses] = useState("");
  const [listStatus, setListStatus] = useState("");

  useEffect(() => {
    if (!open) return;
    getCredentials()
      .then((c) => setGmailUser(c.user))
      .catch(() => {});
    refreshLists();
  }, [open]);

  const refreshLists = async () => {
    try {
      const l = await getLists();
      setLists(l);
    } catch {
      /* ignore */
    }
  };

  const handleSaveCreds = async () => {
    if (!gmailUser || !gmailPass) return setCredStatus("Please fill in both fields.");
    try {
      await saveCredentials(gmailUser, gmailPass);
      setCredStatus("Credentials saved.");
    } catch {
      setCredStatus("Error saving credentials.");
    }
  };

  const handleSelectList = async (name: string) => {
    setSelectedList(name);
    if (!name) {
      setListName("");
      setListAddresses("");
      return;
    }
    try {
      const detail = await getList(name);
      setListName(detail.name);
      setListAddresses(detail.addresses.join("\n"));
    } catch {
      /* ignore */
    }
  };

  const handleSaveList = async () => {
    if (!listName.trim()) return setListStatus("Error: List name is required.");
    const addrs = listAddresses
      .split(/[,\n]+/)
      .map((a) => a.trim())
      .filter(Boolean);
    try {
      await saveList(listName.trim(), addrs);
      setListStatus(`List "${listName.trim()}" saved with ${addrs.length} address(es).`);
      await refreshLists();
      setSelectedList(listName.trim());
    } catch {
      setListStatus("Error saving list.");
    }
  };

  const handleDeleteList = async () => {
    if (!selectedList) return setListStatus("Error: Select a list to delete.");
    try {
      const ok = await deleteList(selectedList);
      if (ok) {
        setListStatus(`List "${selectedList}" deleted.`);
        setSelectedList("");
        setListName("");
        setListAddresses("");
        await refreshLists();
      } else {
        setListStatus(`List "${selectedList}" not found.`);
      }
    } catch {
      setListStatus("Error deleting list.");
    }
  };

  return (
    <>
      {open && <div className="drawer-backdrop" onClick={onClose} />}
      <div className={`settings-drawer ${open ? "open" : ""}`}>
        <div className="drawer-header">
          <h2>Settings</h2>
          <button className="icon-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="drawer-body">
          {/* Credentials Card */}
          <div className="card">
            <h3>Gmail Credentials</h3>
            <label>Gmail Address</label>
            <input
              type="text"
              value={gmailUser}
              onChange={(e) => setGmailUser(e.target.value)}
              placeholder="you@gmail.com"
            />
            <label>App Password</label>
            <input
              type="password"
              value={gmailPass}
              onChange={(e) => setGmailPass(e.target.value)}
              placeholder="xxxx xxxx xxxx xxxx"
            />
            <button className="btn-primary" onClick={handleSaveCreds}>
              Save Credentials
            </button>
            {credStatus && <div className="status-msg">{credStatus}</div>}
          </div>

          {/* Email Lists Card */}
          <div className="card">
            <h3>Email Lists</h3>
            <label>Select a List</label>
            <select
              value={selectedList}
              onChange={(e) => handleSelectList(e.target.value)}
            >
              <option value="">— New List —</option>
              {lists.map((l) => (
                <option key={l.name} value={l.name}>
                  {l.name} ({l.count})
                </option>
              ))}
            </select>

            <label>List Name</label>
            <input
              type="text"
              value={listName}
              onChange={(e) => setListName(e.target.value)}
              placeholder="e.g. Beta Testers"
            />

            <label>Addresses</label>
            <textarea
              rows={5}
              value={listAddresses}
              onChange={(e) => setListAddresses(e.target.value)}
              placeholder={"alice@example.com\nbob@example.com"}
            />

            <div className="btn-row">
              <button className="btn-primary" onClick={handleSaveList}>
                Save List
              </button>
              <button className="btn-danger" onClick={handleDeleteList}>
                Delete List
              </button>
            </div>
            {listStatus && <div className="status-msg">{listStatus}</div>}
          </div>
        </div>
      </div>
    </>
  );
}
