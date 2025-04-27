function loadPostCounters(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) {
        console.warn('Section not found:', sectionId);
        return;
    }

    const commentSpans = section.querySelectorAll('span[id^="comments-"]');
    const viewSpans = section.querySelectorAll('span[id^="views-"]');

    const ids = new Set();

    commentSpans.forEach(span => ids.add(span.id.replace('comments-', '')));
    viewSpans.forEach(span => ids.add(span.id.replace('views-', '')));

    if (ids.size === 0) {
        return;
    }

    const params = new URLSearchParams();
    ids.forEach(id => params.append('ids[]', id));

    fetch(`/post-counters/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            ids.forEach(id => {
                const localCommentSpans = section.querySelectorAll(`#comments-${id}`);
                const localViewSpans = section.querySelectorAll(`#views-${id}`);

                if (data[id]) {
                    localCommentSpans.forEach(span => {
                        if (span) {
                            const commentWord = data[id].comments === 1 ? 'answer' : 'answers';
                            span.innerText = `${data[id].comments} ${commentWord}`;
                        }
                    });
                    localViewSpans.forEach(span => {
                        if (span) {
                            const viewWord = data[id].views === 1 ? 'view' : 'views';
                            span.innerText = `${data[id].views} ${viewWord}`;
                        }
                    });
                }
            });
        })
    .catch(error => console.error('Failed to load counters:', error));
}
document.addEventListener('DOMContentLoaded', function() {
    loadPostCounters('main');
});