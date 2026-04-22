// Author: Jennifer Behm
// Edited by: Miriam Rodas. Edited 04/21/2026
// Edited by: Jennifer Behm. Editied 04/22/2026
// File Name: App.jsx
// Purpose: App navigation and backend connectivity.

import { useRef } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "./context/AuthContext";

// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import ParentDashboard from "./pages/ParentDashboard";
import SchoolDashboard from "./pages/SchoolDashboard";
import DriverDashboard from "./pages/DriverDashboard";
import DriverDocuments from "./pages/DriverDocuments";
import Header from "./components/Header";

// Backend URL
const BACKEND =
  import.meta.env.VITE_BACKEND_URL ||
  "https://alicorn-backend.onrender.com";

export { BACKEND };

export default function App() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Hide header on login page
  const isLoginPage = location.pathname === "/login";

  // Shared socket reference across dashboards
  const socketRef = useRef(null);

  // Logout handler
  const handleLogout = () => {
    if (user?.role === "driver" && socketRef.current) {
      socketRef.current.emit("driver_offline", {
        username: user.username,
      });
    }

    socketRef.current?.disconnect();
    socketRef.current = null;

    logout();
    navigate("/");
  };

  return (
    <>
      {/* Header (hidden on login page) */}
      {!isLoginPage && (
        <Header
          onLoginClick={() => navigate("/login")}
          onContactClick={() => navigate("/contact")}
        />
      )}

      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route
          path="/parent"
          element={
            <ParentDashboard
              socketRef={socketRef}
              onLogout={handleLogout}
            />
          }
        />

        <Route
          path="/school"
          element={
            <SchoolDashboard
              socketRef={socketRef}
              onLogout={handleLogout}
            />
          }
        />

        <Route
          path="/driver"
          element={
            <DriverDashboard
              socketRef={socketRef}
              onLogout={handleLogout}
            />
          }
        />

        <Route
          path="/driver/documents"
          element={<DriverDocuments />}
        />
      </Routes>
    </>
  );
}