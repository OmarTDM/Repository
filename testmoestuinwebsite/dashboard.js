document.getElementById("add-notification-btn").addEventListener("click", function () {
    const titleInput = document.getElementById("notification-title-input");
    const descriptionInput = document.getElementById("notification-description-input");

    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (title && description) {
        // Create a new notification
        const newNotif = document.createElement("div");
        newNotif.className = "notif-item";
        newNotif.textContent = title;

        // Add click event to open the notification in full view
        newNotif.addEventListener("click", function () {
            openModal(title, description);
        });

        // Prepend the new notification to the top of the list
        const notificaties = document.getElementById("notificaties");
        notificaties.insertBefore(newNotif, notificaties.firstChild);

        // Clear input fields after adding a notification
        //titleInput.value = "";
        //descriptionInput.value = "";
    } else {
        alert("Voer aub een titel en een descriptie in!");
    }
});

// Modal functionality
const modal = document.getElementById("modal");
const modalText = document.getElementById("modal-text");
const modalTitle = document.createElement("h2");
modalText.prepend(modalTitle); // Add a title element to the modal

const closeBtn = document.getElementById("close-btn");

// Function to open modal
function openModal(title, description) {
    modal.style.display = "flex";
    modalTitle.textContent = title; // Update title
    modalText.innerHTML = description; // Update description
}

// Function to close modal
closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
});

// Close modal when clicking outside of it
window.addEventListener("click", function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});
