document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const username = document.getElementById("Username").value;
    const password = document.getElementById("password").value;
  
    if (!username || !password) {
      alert("Vul aub beide velden in");
      return;
    }
  
    // Optional: Check if username is an email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailRegex.test(username)) {
      console.log("Login with email detected.");
    } else {
      console.log("Login with username detected.");
    }
  
    // Simulated login request
    if ((username === "testuser" || username === "test@example.com") && password === "password123") {
      alert("Login successful!");
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid username or password.");
    }
  });
  
  