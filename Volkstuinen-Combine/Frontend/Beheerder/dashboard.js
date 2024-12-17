document.addEventListener("DOMContentLoaded", function () {
    const notificaties = document.getElementById("notificaties");


    fetch("../../Backend/FetchMessages.php")
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to fetch messages.");
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                renderNotifications(data.messages); // Fix key name from `data.message` to `data.messages`
            } else {
                console.error(data.error);
            }
        })
        .catch((error) => {
            console.error("Error fetching messages:", error);
        });


    // Render notifications
    function renderNotifications(messages) {
        notificaties.innerHTML = "";

        if (messages.length === 0) {
            notificaties.textContent = "Geen berichten beschikbaar.";
        }

        messages.forEach((message) => {
            const notifItem = document.createElement("div");
            notifItem.className = "notif-item";
            notifItem.textContent = message.Subject;

            notifItem.addEventListener("click", function () {
                openModal(message.Subject, message.Message);
            });

            notificaties.appendChild(notifItem);
        });
    }

    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const closeBtn = document.getElementById("close-btn");

    function openModal(title, description) {
        modal.style.display = "flex";
        modalTitle.textContent = title;
        modalDescription.textContent = description;
    }

    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    fetchMessages();
});
