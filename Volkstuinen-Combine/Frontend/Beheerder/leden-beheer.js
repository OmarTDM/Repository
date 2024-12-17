let memberCount = 1; // Keeps track of the number of members

// Modal functionality
const modal = document.getElementById("modal");
const closeBtn = document.getElementById("close-btn");

// Function to open the modal
function openModal() {
  modal.style.display = "flex";
}

// Function to close the modal
function closeModal() {
  modal.style.display = "none";
}

// Close modal on close button click
closeBtn.addEventListener("click", closeModal);

// Close modal when clicking outside the modal content
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

// Function to add a new member
function addMember() {
  memberCount++;
  const table = document.getElementById("ledenTable").getElementsByTagName("tbody")[0];

  // Create a new row
  const newRow = document.createElement("tr");
  newRow.id = `member${memberCount}`;
  newRow.innerHTML = `
    <td id="naam${memberCount}">Nieuw Lid</td>
    <td id="complex${memberCount}">Complex ${memberCount}</td>
    <td id="grootte${memberCount}">?m²</td>
    <td id="datum${memberCount}">Datum</td>
    <td id="email${memberCount}">sjaakie@gmail.com</td>
    <td id="telefoon${memberCount}">123-456-7890</td>
    <td>
      <button class="info-button" onclick="showInfo(${memberCount})">Meer Info</button>
    </td>
  `;

  // Append the row to the table
  table.appendChild(newRow);
}

// Add member button functionality
document.getElementById("addMember").addEventListener("click", addMember);

// Function to show member info in the modal
function showInfo(memberId) {
  const name = document.getElementById(`naam${memberId}`).textContent;
  const complex = document.getElementById(`complex${memberId}`).textContent;
  const size = document.getElementById(`grootte${memberId}`).textContent;
  const email = document.getElementById(`email${memberId}`).textContent;
  const telefoon = document.getElementById(`telefoon${memberId}`).textContent;

  // Split name into first and last names (if applicable)
  const nameParts = name.split(" ");
  const firstName = nameParts[0] || "";
  const lastName = nameParts.slice(1).join(" ") || "";

  // Populate modal fields
  document.getElementById("voornaam").value = firstName;
  document.getElementById("achternaam").value = lastName;
  document.getElementById("email").value = email;
  document.getElementById("telefoon").value = telefoon;
  document.getElementById("complex-naam").value = complex;
  document.getElementById("complex-size").value = size;

  // Open the modal
  openModal();
}

// Functionality for edit button
const editButton = document.querySelector(".edit-button");
editButton.addEventListener("click", () => {
  alert("Bewerk functie nog niet geïmplementeerd.");
});

// Functionality for send message button
const sendMessageButton = document.querySelector(".send-message");
sendMessageButton.addEventListener("click", () => {
  alert("Bericht verzonden naar het lid!");
});

