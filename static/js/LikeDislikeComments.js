function updateLikeDislike(slug, action) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/like/${slug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `csrfmiddlewaretoken=${csrfToken}&action=${action}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.likes !== undefined && data.dislikes !== undefined) {
            const likesElement = document.getElementById(`likes-${slug}`);
            const dislikesElement = document.getElementById(`dislikes-${slug}`);

            if (likesElement) likesElement.textContent = data.likes;
            if (dislikesElement) dislikesElement.textContent = data.dislikes;

            const likeButton = document.getElementById(`like-btn-${slug}`);
            const dislikeButton = document.getElementById(`dislike-btn-${slug}`);

            if (action === 'like') {
                likeButton.disabled = true;
                dislikeButton.disabled = false;
            } else if (action === 'dislike') {
                dislikeButton.disabled = true;
                likeButton.disabled = false;
            }
        } else {
            console.log('Error:', data);
        }
    })
    .catch(error => console.log('Error:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.thumbs-up2');
    const dislikeButtons = document.querySelectorAll('.thumbs-down2');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const slug = button.getAttribute('data-slug'); 
            updateLikeDislike(slug, 'like');
        });
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const slug = button.getAttribute('data-slug'); 
            updateLikeDislike(slug, 'dislike');
        });
    });
});
