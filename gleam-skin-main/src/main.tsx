import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// Diagnostic error handler
window.onerror = (message, source, lineno, colno, error) => {
    const display = document.createElement('div');
    display.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:white;color:red;padding:20px;z-index:9999;font-family:monospace;white-space:pre-wrap;overflow:auto;';
    display.innerHTML = `<h1>Application Crash</h1><p>${message}</p><p>at ${source}:${lineno}:${colno}</p><pre>${error?.stack || ''}</pre>`;
    document.body.appendChild(display);
};

try {
    const rootElement = document.getElementById("root");
    if (!rootElement) throw new Error("Root element not found");
    createRoot(rootElement).render(<App />);
} catch (e: any) {
    console.error("Mounting error:", e);
    alert("Mounting error: " + e.message);
}
