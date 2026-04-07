const express = require("express");
const app = express();

const cors = require("cors");

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("Alicorn backend is running.");
});

app.get("/bus-location", (req, res) => {
  res.json({
    busId: "12",
    latitude: 38.8816,
    longitude: -77.0910,
    status: "On Route"
  });
});

app.get("/attendance", (req, res) => {
  res.json([
    { studentId: "1001", name: "Jordan Lee", status: "On Bus" },
    { studentId: "1002", name: "Taylor Smith", status: "Absent" }
  ]);
});

app.get("/students", (req, res) => {
  res.json([
    { studentId: "1001", name: "Jordan Lee", route: "Route A" },
    { studentId: "1002", name: "Taylor Smith", route: "Route B" }
  ]);
});

// ✅ ADD THIS BLOCK HERE
app.post("/gps", (req, res) => {
  console.log("Received GPS:", req.body);
  res.json({ success: true });
});

app.listen(PORT, () => {
