$(document).ready(function () {
  $('form.cart-add').ajaxForm(function (responseText) {
    $('#cart-order-list').append(responseText);
    $('.cart').removeClass('cart-empty');
  });

  $('form.cart-remove').ajaxForm(function (responseText, statusText, xhr, element) {
    $(element).closest('.cart-item').remove();
    if (!$('#cart-order-list').has('li'))
      $(element).closest('.cart').addClass('cart-empty');
  });

  $.getJSON('/api/drinks/')
    .done(function (data) {
      let drinks = JSON.parse(data);
      for (let drink of drinks) {
        let drinkHTML = `
  <div class="drink">
    <div class="drink-picture">${drink.product.image}</div>
    <drink class="description">${drink.product.name}</drink>
    <button>Add to cart</button>
  </div>
`;
        $('.products').append(drinkHTML);
      }
    })
    .fail(function (error) {});
});
