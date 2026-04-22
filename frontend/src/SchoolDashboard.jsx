// Author: Jennifer Behm
// Edited by: Miriam Rodas. Edited 04/21/2026
// Edited by: Jennifer Behm. Edited 04/22/2026
// File Name: SchoolDashboard.jsx
// Purpose: School Dashboard. Administrative actions
// such as edit buses, roster, driver status.

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { io } from "socket.io-client";
import L from "leaflet";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { BACKEND } from "../App";
import "leaflet/dist/leaflet.css";

// Fix Leaflet marker icons
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import markerShadowPng from "leaflet/dist/images/marker-shadow.png";
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIconPng,
  shadowUrl: markerShadowPng,
});

const DEFAULT_CENTER = [40.5163, -75.7774];

// Keeps map centered when data updates
function MapUpdater({ positions }) {
  const map = useMap();
  useEffect(() => {
    const entries = Object.values(positions);
    if (entries.length > 0) {
      map.setView([entries[0].lat, entries[0].lng], map.getZoom());
    }
  }, [positions, map]);
  return null;
}

export default function SchoolDashboard({ socketRef, onLogout }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [busPositions, setBusPositions] = useState({});

  useEffect(() => {
    const socket = io(BACKEND, { transports: ["websocket"] });
    socketRef.current = socket;

    socket.on("location_update", ({ driver, lat, lng }) => {
      setBusPositions(prev => ({ ...prev, [driver]: { lat, lng } }));
    });

    socket.on("driver_removed", ({ driver }) => {
      setBusPositions(prev => {
        const updated = { ...prev };
        delete updated[driver];
        return updated;
      });
    });

    fetch(`${BACKEND}/positions`)
      .then(res => res.json())
      .then(data => setBusPositions(data))
      .catch(() => {});

    return () => socket.disconnect();
  }, []);

  const positionEntries = Object.entries(busPositions);

  const mapCenter =
    positionEntries.length > 0
      ? [positionEntries[0][1].lat, positionEntries[0][1].lng]
      : DEFAULT_CENTER;

  return (
    <div style={styles.page}>
      {/* Title */}
      <h1 style={styles.title}>School Dashboard</h1>

      {/* Subtitle */}
      <p style={styles.subtitle}>
        Logged in as <strong>{user?.username}</strong>
      </p>

      {/* Map */}
      <MapContainer
        center={mapCenter}
        zoom={13}
        style={styles.map}
        whenReady={({ target }) =>
          setTimeout(() => target.invalidateSize(), 0)
        }
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        <MapUpdater positions={busPositions} />

        {positionEntries.map(([driver, pos]) => (
          <Marker key={driver} position={[pos.lat, pos.lng]}>
            <Popup>
              <strong>{driver}</strong>
              <br />
              {pos.lat.toFixed(5)}, {pos.lng.toFixed(5)}
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Buttons */}
      <div style={styles.grid}>
        <button style={styles.button} onClick={() => navigate("/school/add-bus")}>
          Add Bus
        </button>

        <button style={styles.button} onClick={() => navigate("/school/routes")}>
          View Routes
        </button>

        <button style={styles.button} onClick={() => navigate("/school/drivers")}>
          Driver Status
        </button>
      </div>

      {/* Active drivers */}
      <div style={styles.driverSection}>
        <h3>Active Drivers ({positionEntries.length})</h3>

        {positionEntries.length === 0 ? (
          <p>No drivers currently online.</p>
        ) : (
          <ul style={styles.driverList}>
            {positionEntries.map(([driver, pos]) => (
              <li key={driver}>
                {driver} — {pos.lat.toFixed(5)}, {pos.lng.toFixed(5)}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Logout */}
      <button onClick={onLogout} style={styles.logoutButton}>
        Logout
      </button>
    </div>
  );
}

// Styles 
const styles = {
  page: {
    textAlign: "center",
    paddingTop: "50px",
  },

  title: {
    marginBottom: "5px",
  },

  subtitle: {
    color: "#666",
    marginBottom: "20px",
  },

  map: {
    width: "80%",
    height: "450px",
    margin: "0 auto 30px",
    borderRadius: "12px",
    overflow: "hidden",
  },

  grid: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: "15px",
    marginBottom: "30px",
  },

  button: {
    padding: "12px 18px",
    borderRadius: "10px",
    border: "none",
    background: "#448fd6",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    minWidth: "140px",
  },

  driverSection: {
    marginTop: "20px",
  },

  driverList: {
    listStyle: "none",
    padding: 0,
  },

  logoutButton: {
    marginTop: "20px",
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#eee",
    cursor: "pointer",
  },
};