$(document).ready(function () {
    $(".qtyplus").click(function () {
        var quantityInput = $(this).siblings(".qty");
        var currentVal = parseInt(quantityInput.val());
        var maxStock = parseInt(quantityInput.attr('max'));

        if (currentVal < maxStock) {
            quantityInput.val(currentVal + 1);
        } else {
            quantityInput.val(maxStock);
        }
    });

    $(".qtyminus").click(function () {
        var quantityInput = $(this).siblings(".qty");
        var currentVal = parseInt(quantityInput.val());

        if (currentVal > 1) {
            quantityInput.val(currentVal - 1);
        }
    });

    function validateOpinion() {
        var selectedRating = parseInt($('#selectedRating').val());

        if (selectedRating === 0) {
            alert('Por favor, selecciona una puntuación antes de enviar la opinión.');
            return false;
        }

        return true;
    }

    $(".round-black-btn").click(function () {
        return validateOpinion();
    });

});

function validateQuantity(input) {
    var currentVal = parseInt(input.value);
    var maxStock = parseInt(input.getAttribute('max'));

    if (currentVal < 1) {
        input.value = 1;
    } else if (currentVal > maxStock) {
        input.value = maxStock;
    }
}

const starsContainer = document.querySelector('.stars');
const stars = starsContainer.querySelectorAll('i');
const ratingInput = document.getElementById('selectedRating');

stars.forEach((star) => {
    star.addEventListener("click", () => {
        const value = parseInt(star.getAttribute('data-value'));
        starsContainer.setAttribute('data-rating', value);
        updateStars(value);
        ratingInput.value = value;
    });
});

function updateStars(value) {
    stars.forEach((star) => {
        const starValue = parseInt(star.getAttribute('data-value'));
        star.classList.toggle("active", starValue <= value);
    });
}