$(document).ready(function () {
    $('.dropdown-menu a').click(function () {
        var value = $(this).data('value');
        if(value != 'price' && value != 'score'){
          $('#search_concept').text($(this).text());
          $('#search_type').val(value);
        }else if(value == 'price'){
          if($('.row2').css('display') == 'flex')
            $('.row2').css('display', 'none');
          else if($('.row2').css('display') == 'none')
            $('.row2').css('display', 'flex');
            $('.review').css('display', 'none');
          $('#search_concept').text('Todos');
          $('#search_type').val('all');
        }else{
          if($('.review').css('display') == 'flex')
            $('.review').css('display', 'none');
          else{
            $('.review').css('display', 'flex');
            $('.row2').css('display', 'none');
          }
          $('#search_concept').text('Todos');
          $('#search_type').val('all');
        }
    });
});
function validateQuantity(input) {
  var currentVal = parseInt(input.value);
  if (currentVal < 0) {
      input.value = 0;
  }
}

const baseStarsContainer = document.querySelector('.base-stars');
const baseStars = baseStarsContainer.querySelectorAll('i');
const baseRatingInput = document.getElementById('rating');

baseStars.forEach((star) => {
  star.addEventListener("click", () => {
      const baseValue = parseInt(star.getAttribute('data-value'));
      baseStarsContainer.setAttribute('data-rating', baseValue);
      updateStars(baseValue);
      baseRatingInput.value = baseValue;
  });
});

function updateStars(value) {
  baseStars.forEach((star) => {
      const baseStarValue = parseInt(star.getAttribute('data-value'));
      star.classList.toggle("active", baseStarValue <= value);
  });
}