// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var modalImg = document.getElementById("modalImg");

// Get all elements with class="modal-link"
var modalLinks = document.getElementsByClassName("modal-link");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// Loop through the modal links and add onClick listeners
for (var i = 0; i < modalLinks.length; i++) {
    modalLinks[i].onclick = function() {
        modal.style.display = "block";
        modalImg.src = this.href;
        return false; // Prevent default link behavior
    }
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
