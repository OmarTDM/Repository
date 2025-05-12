document.addEventListener('DOMContentLoaded', function() {
    const postButton = document.getElementById('postButton');
    const postModal = document.getElementById('postModal');
    const closeButton = document.querySelector('.close-button');
    const postForm = document.getElementById('postForm');
    const postTitle = document.getElementById('postTitle');
    const postContent = document.getElementById('postContent');
    const postImage = document.getElementById('postImage');
    const recentPosts = document.querySelector('.recent-posts');

    // Open the modal
    postButton.addEventListener('click', function(event) {
        event.preventDefault();
        postModal.style.display = 'flex';
    });

    // Close the modal
    closeButton.addEventListener('click', function() {
        postModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === postModal) {
            postModal.style.display = 'none';
        }
    });

    // Handle the post submission
    postForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = postTitle.value.trim();
        const content = postContent.value.trim();
        const image = postImage.files[0];

        if (title && (content || image)) {
            const post = document.createElement('div');
            post.className = 'post';

            let postImageHTML = '';
            if (image) {
                const imageURL = URL.createObjectURL(image);
                postImageHTML = `<img src="${imageURL}" alt="Post Image">`;
            }

            const timestamp = new Date().toLocaleString();

            // Example profile information (this would normally come from the user's profile data)
            const profileHTML = `
                <div class="profile-section">
                    <img src="profile-placeholder.png" alt="Profile Image">
                    <div>
                        <h4>Profile Name</h4>
                        <div class="star-rating">
                            <span class="star">&#9733;</span>
                            <span class="star">&#9733;</span>
                            <span class="star">&#9733;</span>
                            <span class="star">&#9733;</span>
                            <span class="star">&#9733;</span>
                            <span class="numeric-rating">4.5</span>
                        </div>
                    </div>
                </div>
            `;

            post.innerHTML = `
                ${profileHTML}
                <div class="post-title">${title}</div>
                ${postImageHTML}
                <p>${content} <a href="#read-more">Read more...</a></p>
                <div class="timestamp">Posted on ${timestamp}</div>
                <div class="post-actions">
                    <div class="like-dislike-ratio">
                        <button class="like-button">Like</button>
                        <span class="like-count">0</span>
                        <button class="dislike-button">Dislike</button>
                        <span class="dislike-count">0</span>
                    </div>
                </div>
            `;

            // recente post prependen naar de recent posts sectie
            recentPosts.prepend(post);

            // event listener dislike
            const likeButton = post.querySelector('.like-button');
            const dislikeButton = post.querySelector('.dislike-button');
            const likeCount = post.querySelector('.like-count');
            const dislikeCount = post.querySelector('.dislike-count');

            likeButton.addEventListener('click', function() {
                likeCount.textContent = parseInt(likeCount.textContent) + 1;
            });

            dislikeButton.addEventListener('click', function() {
                dislikeCount.textContent = parseInt(dislikeCount.textContent) + 1;
            });

            postTitle.value = '';
            postContent.value = '';
            postImage.value = '';
            postModal.style.display = 'none';
        }
    });

    // ster rating systeem
    const stars = document.querySelectorAll('.star-rating .star');
    stars.forEach(star => {
        star.addEventListener('click', function() {
            let rating = 0;
            const stars = this.parentElement.querySelectorAll('.star');
            stars.forEach((s, index) => {
                if (index <= Array.from(stars).indexOf(this)) {
                    s.classList.add('selected');
                    rating = index + 1;
                } else {
                    s.classList.remove('selected');
                }
            });
            console.log(`Rated: ${rating} stars`);
            this.parentElement.nextElementSibling.textContent = rating.toFixed(1); // Update numeries rating
        });
    });
});
