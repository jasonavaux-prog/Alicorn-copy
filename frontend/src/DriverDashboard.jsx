// Author: Jennifer Behm
// Edited by: Miriam Rodas. Edited 04/21/2026
// Edited by: Jennifer Behm. Edited 04/22/2026
// File Name: DriverDashboard.jsx
// Purpose: Driver dashboard for Alicorn. Tracks 
// location of driver and displays action buttons for driver.

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { useAuth } from "../context/AuthContext";
import { BACKEND } from "../App";

export default function DriverDashboard({ socketRef, onLogout }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [driverStatus, setDriverStatus] = useState("Waiting for GPS...");

  useEffect(() => {
    const socket = io(BACKEND, { transports: ["websocket"] });
    socketRef.current = socket;

    if (!navigator.geolocation) {
      setDriverStatus("Geolocation is not supported by this browser :c");
      return () => socket.disconnect();
    }

    const watchId = navigator.geolocation.watchPosition(
      ({ coords }) => {
        const { latitude, longitude, accuracy } = coords;

        setDriverStatus(
          `Transmitting — lat: ${latitude.toFixed(5)}, lng: ${longitude.toFixed(5)} (±${Math.round(accuracy)}m)`
        );

        socket.emit("send_location", {
          username: user?.username,
          lat: latitude,
          lng: longitude,
        });
      },
      (err) => setDriverStatus(`GPS error: ${err.message}`),
      {
        enableHighAccuracy: true,
        maximumAge: 5000,
        timeout: 10000,
      }
    );

    return () => {
      navigator.geolocation.clearWatch(watchId);
      socket.disconnect();
    };
  }, []);

  return (
    <div style={styles.container}>
      {/* Title */}
      <h1 style={styles.title}>Driver Dashboard</h1>

      {/* Welcome */}
      <p style={styles.subtitle}>
        Welcome, <strong>{user?.username}</strong>
      </p>

      {/* GPS Status Box */}
      <div style={styles.statusBox}>
        {driverStatus}
      </div>

      {/* Info text */}
      <p style={styles.infoText}>
        Your location is being transmitted to parents and school staff.
        <br />
        Press "End Route" when you finish your route.
      </p>

      {/* Buttons */}
      <div>
        <button
          onClick={() => navigate("/driver/documents")}
          style={styles.button}
        >
          Documents
        </button>

        <button
          onClick={onLogout}
          style={styles.logoutButton}
        >
          End Route & Logout
        </button>
      </div>
    </div>
  );
}

// Styles 
const styles = {
  container: {
    textAlign: "center",
    marginTop: "80px",
    padding: "20px",
  },

  title: {
    marginBottom: "10px",
  },

  subtitle: {
    color: "#666",
    marginBottom: "20px",
  },

  statusBox: {
    display: "inline-block",
    margin: "20px auto",
    padding: "16px 24px",
    background: "#e7e7e7",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontFamily: "monospace",
    fontSize: "14px",
    width: "100%",
    boxSizing: "border-box",
  },

  infoText: {
    color: "#666",
    fontSize: "14px",
    marginBottom: "20px",
  },

  button: {
    padding: "10px 20px",
    margin: "10px",
    borderRadius: "8px",
    border: "none",
    background: "#448fd6",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },

  logoutButton: {
    padding: "10px 20px",
    margin: "10px",
    borderRadius: "8px",
    border: "1px solid #f88",
    background: "#fee",
    color: "#900",
    fontWeight: "bold",
    cursor: "pointer",
  },
};