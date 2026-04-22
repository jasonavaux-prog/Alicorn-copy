// Author: Jennifer Behm
// File Name: DriverDocuments.jsx
// Purpose: Displays various document types to be 
// added and viewed. The buttons are to be implemented.

import { useNavigate } from "react-router-dom";

export default function DriverDocuments() {
  const navigate = useNavigate();

  // Document list
  const documents = [
    { name: "Driver License", action: "Upload" },
    { name: "Bus Inspection Report", action: "Upload" },
    { name: "Route Sheet", action: "View" },
  ];

  
  return (
    <div style={styles.container}>

      {/** Title */}
      <h1 style={{ textAlign: "center", marginTop: "60px" }}>
        Driver Documents 
      </h1>

      {/** Subtitle */}
      <p style={styles.subtitle}>
        View and manage your required documents
      </p>

      {/** Action buttons */}
      <div style={styles.grid}>
        {documents.map((doc, index) => (
          <div key={index}>
            <p style={styles.docName}>{doc.name}</p>

            <button style={styles.button}>
              {doc.action}
            </button>
          </div>
        ))}
      </div>

      {/** Back button */}
      <button
        onClick={() => navigate("/driver")}
        style={styles.backButton}
      >
        ← Back to Dashboard
      </button>
    </div>
  );
}


{/** Styles */}
const styles = {
  container: {
    textAlign: "center",
    marginTop: "60px",
    padding: "20px",
  },

  title: {
    marginBottom: "10px",
  },

  subtitle: {
    color: "#666",
    marginBottom: "30px",
  },

  grid: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: "20px",
  },


  docName: {
    marginBottom: "15px",
    fontWeight: "bold",
  },

  button: {
    padding: "8px 16px",
    borderRadius: "8px",
    border: "none",
    background: "#448fd6",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },

  backButton: {
    marginTop: "30px",
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#448fd6",
    color: "white",
    cursor: "pointer",
  },
};
