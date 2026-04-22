// Author: Jennifer Behm
// Edited by: Miriam Rodas. Edited 04/21/2026
// Edited by: Jennifer Behm. Edited 04/22/2026
// File Name: ParentDashboard.jsx
// Purpose: Dashboard for parents. Displays live GPS status of their child's bus on a map.

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { io } from "socket.io-client";
import L from "leaflet";
import { useAuth } from "../context/AuthContext";
import { BACKEND } from "../App";
import "leaflet/dist/leaflet.css" // Fix for map breaking. 
// Fix Leaflet's default marker icons, which break under Vite's asset pipeline
import markerIconPng from "leaflet/dist/images/marker-icon.png"
import markerShadowPng from "leaflet/dist/images/marker-shadow.png"
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconUrl: markerIconPng, shadowUrl: markerShadowPng, })


// Uses Kutztown as default map center before any GPS data arrives
const DEFAULT_CENTER = [40.5163, -75.7774];

// Shared map container style — defined outside component so the reference is stable
const MAP_STYLE = { width: "80%", height: "450px", margin: "0 auto 20px" };

// MapUpdater: Re-centers the map when the first driver position arrives.
// Without this, the map stays on DEFAULT_CENTER even after GPS data comes in.
function MapUpdater({ positions }) {
  const map = useMap();
  useEffect(() => {
    const entries = Object.values(positions);
    // Pan to the first known bus position
    if (entries.length > 0) { map.setView([entries[0].lat, entries[0].lng], map.getZoom()); }
  }, [positions, map]);
  return null;
}

export default function ParentDashboard({ socketRef, onLogout }) {
  const { user } = useAuth();
  // Live GPS positions: { driverUsername: { lat, lng } }
  const [busPositions, setBusPositions] = useState({});

  // WebSocket setup: connect, listen for live updates, fetch any positions already broadcasting
  useEffect(() => {
    const socket = io(BACKEND, { transports: ["websocket"] });
    socketRef.current = socket;

    // Listens for position updates broadcast by the server
    socket.on("location_update", ({ driver, lat, lng }) => {
      setBusPositions(prev => ({ ...prev, [driver]: { lat, lng } }));
    });

    // Removes a driver's marker when they go offline
    socket.on("driver_removed", ({ driver }) => {
      setBusPositions(prev => {
        const updated = { ...prev };
        delete updated[driver];
        return updated;
      });
    });

    // Fetch any positions that were already broadcasting before this client connected
    fetch(`${BACKEND}/positions`)
      .then(res => res.json())
      .then(data => { setBusPositions(data); })
      .catch(() => {});

    // Cleanup: disconnect socket when navigating away
    return () => socket.disconnect();
  }, []);

  // Converts positions object to array for rendering markers
  const positionEntries = Object.entries(busPositions);

  // Picks a center: first known bus, or fall back to default
  const mapCenter = positionEntries.length > 0
    ? [positionEntries[0][1].lat, positionEntries[0][1].lng]
    : DEFAULT_CENTER;

  return (
    <div>
      <h1 style={{ textAlign: "center" }}>Parent Dashboard</h1>
      <p style={{ textAlign: "center" }}>
        {positionEntries.length === 0
          ? "Waiting for buses to come online..."
          : `${positionEntries.length} bus(es) currently active`}
      </p>

      {/* Leaflet map, OpenStreetMap tiles, no API key needed */}
      {/* key="parent-map" so tiles don't fragment (happen to a buddy of mine (me)).  */}
      {/* whenReady calls invalidateSize so Leaflet recalculates tile layout */}
      {/* after the container finishes rendering inside the React tree.      */}
      <MapContainer
        key="parent-map"
        center={mapCenter}
        zoom={13}
        style={MAP_STYLE}
        whenReady={({ target }) => { setTimeout(() => target.invalidateSize(), 0); }}
      >
        {/* Free OpenStreetMap tile layer */}
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Auto-pan to first bus position when it arrives */}
        <MapUpdater positions={busPositions} />

        {/* One marker per active driver */}
        {positionEntries.map(([driver, pos]) => (
          <Marker key={driver} position={[pos.lat, pos.lng]}>
            <Popup>
              <strong>{driver}</strong><br />
              {pos.lat.toFixed(5)}, {pos.lng.toFixed(5)}
            </Popup>
          </Marker>
        ))}
      </MapContainer>

    </div>
  );
}