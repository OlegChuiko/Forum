const categoryInput = document.getElementById("category-input");
const categoryError = document.getElementById("category-error");
const submitButton = document.getElementById("submit-button");

categoryInput.addEventListener("input", function() {
    const inputCategory = this.value;

    fetch('/check-category/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ category: inputCategory })
    })
    .then(response => response.json())
    .then(data => {
        if (data.exists) {
            categoryError.style.display = "none";
            submitButton.disabled = false; 
        } else {
            categoryError.style.display = "inline";
            submitButton.disabled = true; 
        }
    })
    .catch(error => {
        console.error('Error:', error);
        submitButton.disabled = true;
    });
});