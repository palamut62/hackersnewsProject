document.addEventListener('DOMContentLoaded', function () {
    const isAuthenticated = window.isAuthenticated;
    const loginUrl = window.loginUrl;
    const csrfToken = window.csrfToken;

    const ratingIcons = document.querySelectorAll('.rating-icon');
    const commentIcons = document.querySelectorAll('.comment-icon');
    const likeIcons = document.querySelectorAll('.like-icon');
    const ratingModal = document.getElementById('ratingModal');
    const ratingForm = document.getElementById('ratingForm');
    const stars = document.querySelectorAll('.star');
    let ratingValue = 0;

    // Yıldız tıklama olaylarını işleme
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            ratingValue = star.getAttribute('data-value');
            document.getElementById('ratingValue').value = ratingValue;
            stars.forEach(s => s.classList.remove('selected'));
            for (let i = 0; i <= index; i++) {
                stars[i].classList.add('selected');
            }
        });
    });

    // Rating Icons Click Event
    ratingIcons.forEach(icon => {
        icon.addEventListener('click', (e) => {
            if (!isAuthenticated) {
                window.location.href = loginUrl;
                return;
            }
            ratingModal.style.display = 'block';
            const newsId = icon.getAttribute('data-news-id');
            ratingForm.setAttribute('data-rating-id', newsId);
        });
    });

    // Like Icons Click Event
    likeIcons.forEach(icon => {
        icon.addEventListener('click', (e) => {
            if (!isAuthenticated) {
                window.location.href = loginUrl;
                return;
            }
            e.preventDefault();
            const newsId = icon.getAttribute('data-news-id');
            fetch(`/like/${newsId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const likeCountElement = document.querySelector(`#likes_count_${newsId}`);
                        likeCountElement.textContent = data.likes_count;
                        icon.classList.toggle('liked', data.user_liked);
                    } else {
                        alert('Beğenme işlemi yapılırken bir hata oluştu.');
                    }
                });
        });
    });

    // Rating Form Submit Event
    ratingForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(ratingForm);
        const ratingId = ratingForm.getAttribute('data-rating-id');
        fetch(`/rate/${ratingId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            credentials: 'same-origin'
        }).then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const scoreElement = document.querySelector(`#score_${ratingId}`);
                    scoreElement.textContent = data.rating;
                    ratingModal.style.display = 'none';
                } else {
                    alert('Puanlama yapılırken bir hata oluştu.');
                }
            });
    });

    // Close Modal Event
    document.querySelector('.close').onclick = function () {
        ratingModal.style.display = 'none';
    };

    // Comment Icons Click Event
    commentIcons.forEach(icon => {
        icon.addEventListener('click', (e) => {
            if (!isAuthenticated) {
                window.location.href = loginUrl;
                return;
            }
            e.preventDefault();
            const newsId = icon.getAttribute('data-news-id');
            fetch(`/comment/${newsId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }).then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const comments = JSON.parse(data.comments);
                        const commentList = document.querySelector('#commentModal ul');
                        commentList.innerHTML = '';
                        comments.forEach(comment => {
                            const li = document.createElement('li');
                            li.textContent = comment.fields.comment;
                            commentList.appendChild(li);
                        });
                        document.querySelector('#commentForm').setAttribute('data-news-id', newsId);
                        document.getElementById('commentModal').style.display = 'block';
                    }
                });
        });
    });

    // Comment Form Submit Event
    const commentForm = document.getElementById('commentForm');
    commentForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(commentForm);
        const newsId = commentForm.getAttribute('data-news-id');
        fetch(`/comment/${newsId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const comments = JSON.parse(data.comments);
                    const commentList = document.getElementById('commentList');
                    commentList.innerHTML = '';
                    comments.forEach(comment => {
                        const li = document.createElement('li');
                        li.textContent = comment.fields.comment;
                        commentList.appendChild(li);
                    });
                    document.querySelector(`#comment_count_${newsId}`).textContent = data.comments_count;
                } else {
                    alert('Yorum yapılırken bir hata oluştu.');
                }
            });
    });

    // Search Input Keyup Event
    const searchInput = document.querySelector('input[name="q"]');
    searchInput.addEventListener('keyup', function () {
        const query = searchInput.value;
        fetch(`/search-news/?q=${query}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
            .then(data => {
                const newsTableBody = document.querySelector('.news-item');
                newsTableBody.innerHTML = '';
                data.results.forEach((news, index) => {
                    const newsRow = `
                        <tr class="news-row">
                            <td>
                                <table class="news-item">
                                    <tr class="athing" id="news_${news.id}">
                                        <td class="rank-cell">${index + 1}.</td>
                                        <td class="vote-cell">
                                            <center><a id="up_${news.id}" href="vote?id=${news.id}&how=up&goto=news">
                                                <div class="votearrow" title="upvote"></div>
                                            </a></center>
                                        </td>
                                        <td class="title-cell">
                                            <a href="${news.link}">${news.short_description}</a>
                                            <span class="sitebit comhead">(<a href="${news.link}">${news.category}</a>)</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2"></td>
                                        <td class="subtext-cell">
                                            <a href="#" class="rating-icon" data-news-id="${news.id}">
                                                <i class="fas fa-star"></i>
                                            </a>
                                            <span class="score" id="score_${news.id}">
                                                ${news.average_rating || 0}
                                            </span>
                                            |
                                            by ${news.user}
                                            <span class="age">${news.time_ago}</span> |
                                            <a href="#" class="comment-icon" data-news-id="${news.id}">
                                                <i class="fas fa-comment"></i>
                                            </a>
                                            <a href="item?id=${news.id}" id="comment_count_${news.id}">${news.comments_count}</a>|
                                            <a href="#" class="like-icon ${news.user_liked ? 'liked' : ''}" data-news-id="${news.id}">
                                                <i class="fas fa-heart"></i>
                                            </a>
                                            <span class="likes-count" id="likes_count_${news.id}">
                                                ${news.likes_count}
                                            </span>
                                            |
                                            ${isAuthenticated && news.is_superuser ? `<a href="/edit_news/${news.id}/"><i class="fas fa-pencil-alt edit-icon"></i></a>` : ''}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    `;
                    newsTableBody.insertAdjacentHTML('beforeend', newsRow);
                });
            });
    });
});
