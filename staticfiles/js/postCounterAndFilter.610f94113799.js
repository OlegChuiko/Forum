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
                const commentSpans = document.querySelectorAll(`#comments-${id}`);
                const viewSpans = document.querySelectorAll(`#views-${id}`);
                
                if (data[id]) {
                    commentSpans.forEach(commentSpan => {
                        if (commentSpan) {
                            const commentWord = data[id].comments === 1 ? 'answer' : 'answers';
                            commentSpan.innerText = `${data[id].comments} ${commentWord}`;
                        }
                    });
                    viewSpans.forEach(viewSpan => {
                        if (viewSpan) {
                            const viewWord = data[id].views === 1 ? 'view' : 'views';
                            viewSpan.innerText = `${data[id].views} ${viewWord}`;
                        }
                    });
                }
            });
        })
        .catch(error => console.error('Failed to load counters:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    const filterRadios = document.querySelectorAll('input[name="filter"]');
    const sections = {
        recent_post: 'content1',
        most_response: 'content2',
        no_response: 'content3',
        popular_post: 'content4',
    };

    const categoriesSections = {
        recent_post: 'categories_recent',
        most_response: 'categories_most_response',
        no_response: 'categories_no_response',
        popular_post: 'categories_popular',
    };

    function showSection(selected) {
        Object.keys(sections).forEach(key => {
            const section = document.getElementById(sections[key]);
            if (section) {
                section.style.display = key === selected ? 'block' : 'none';
            }
        });

        Object.keys(categoriesSections).forEach(key => {
            const catSection = document.getElementById(categoriesSections[key]);
            if (catSection) {
                catSection.style.display = key === selected ? 'block' : 'none';
            }
        });

        setTimeout(() => {
            loadPostCounters(sections[selected]);
        }, 100);
    }

    filterRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            showSection(this.value);
            localStorage.setItem('selectedFilter', this.value);
        });
    });

    const savedFilter = localStorage.getItem('selectedFilter') || 'recent_post';
    document.querySelector(`input[value="${savedFilter}"]`).checked = true;
    showSection(savedFilter);
});