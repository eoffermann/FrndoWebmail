import { useState } from "react";
import ThemeToggle from "./components/ThemeToggle";
import SendPanel from "./components/SendPanel";
import SettingsPanel from "./components/SettingsPanel";
import "./App.css";

export default function App() {
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <div className="app">
      <header className="top-bar">
        <h1 className="app-title">Frndo Webmail</h1>
        <div className="top-bar-actions">
          <ThemeToggle />
          <button
            className="icon-btn"
            onClick={() => setSettingsOpen((o) => !o)}
            title="Settings"
          >
            ⚙
          </button>
        </div>
      </header>

      <main className="main-content">
        <SendPanel />
      </main>

      <SettingsPanel open={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </div>
  );
}
