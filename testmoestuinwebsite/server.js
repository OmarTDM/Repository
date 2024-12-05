const express = require("express");
const bodyParser = require("body-parser");
const app = express();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Simple user database simulation
const users = [
  { username: "testuser", email: "test@example.com", password: "password123" }
];

// Serve the static HTML file
app.use(express.static("public"));

// Login endpoint
app.post("/login", (req, res) => {
    const { username } = req.body; // The input field named 'username' in the form
    const password = req.body.password;
  
    // Check if the input matches either username or email
    const user = users.find(
      (u) => (u.username === username || u.email === username) && u.password === password
    );
  
    if (user) {
      return res.json({ success: true, message: "Login successful!" });
    } else {
      return res.status(401).json({ success: false, message: "Invalid credentials" });
    }
  });
  

// Start the server
app.listen(3000, () => console.log("Server running on http://localhost:3000"));
