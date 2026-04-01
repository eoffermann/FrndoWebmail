import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";

// Apply saved theme before first render to avoid flash
const saved = localStorage.getItem("theme");
document.documentElement.setAttribute("data-theme", saved === "light" ? "light" : "dark");

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
