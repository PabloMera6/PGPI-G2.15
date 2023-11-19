$(document).ready(function () {
    $(".qtyplus").click(function () {
        var quantityInput = $(this).siblings(".qty");
        var currentVal = parseInt(quantityInput.val());
        quantityInput.val(currentVal + 1);
    });

    $(".qtyminus").click(function () {
        var quantityInput = $(this).siblings(".qty");
        var currentVal = parseInt(quantityInput.val());

        if (currentVal > 1) {
            quantityInput.val(currentVal - 1);
        }
    });

});