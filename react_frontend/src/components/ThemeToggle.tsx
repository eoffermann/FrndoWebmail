import { useEffect, useState } from "react";

function getInitialTheme(): "dark" | "light" {
  const saved = localStorage.getItem("theme");
  if (saved === "light" || saved === "dark") return saved;
  return "dark";
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<"dark" | "light">(getInitialTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === "dark" ? "light" : "dark"));

  return (
    <button className="icon-btn" onClick={toggle} title="Toggle theme">
      {theme === "dark" ? "☀" : "🌙"}
    </button>
  );
}
