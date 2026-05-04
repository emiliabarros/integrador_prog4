import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "./context/AuthContext";
import { InsumosProvider } from "./context/InsumosContext";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <InsumosProvider>
        <App />
      </InsumosProvider>
    </AuthProvider>
  </React.StrictMode>
);
