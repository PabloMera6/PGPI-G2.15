$(document).ready(function () {
    $(".qtyplus").click(function () {
        var quantityInput = $(this).siblings(".qty");
        var currentVal = parseInt(quantityInput.val());
        var maxStock = parseInt(quantityInput.attr('max'));
        
        if (currentVal < maxStock) {
            quantityInput.val(currentVal + 1);
        }else{
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
});

function validateQuantity(input) {
    var currentVal = parseInt(input.value);
    var maxStock = parseInt(input.getAttribute('max'));

    if (currentVal < 1) {
        input.value = 1;
    }else if (currentVal > maxStock) {
        input.value = maxStock;
    }
}
