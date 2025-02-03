document.addEventListener('DOMContentLoaded', function() {
    const replyLinks = document.querySelectorAll('.reply-link');
    replyLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.querySelector(`.reply-form[data-comment-id="${commentId}"]`);
            replyForm.style.display = 'block';
        });
    });
});
