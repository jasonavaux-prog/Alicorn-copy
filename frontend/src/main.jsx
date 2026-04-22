// Author: Jennifer Behm
// Filename: main.jsx
// Purpose: Run the Alicorn app

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext.jsx";
import './index.css'
import 'leaflet/dist/leaflet.css'
import App from "./App.jsx";

// App entry point
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);