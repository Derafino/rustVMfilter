$(document).ready(function() {
  var searchItemInput = $('#item_name');
  var searchCurrencyInput = $('#currency_name');
  var searchResults = $('#search_results');

  searchItemInput.on('input', function() { // fix variable name
    var searchItem = searchItemInput.val();
    var searchCurrency = searchCurrencyInput.val();
    search(searchItem, searchCurrency);
  });

  searchCurrencyInput.on('input', function() { // fix variable name
    var searchItem = searchItemInput.val();
    var searchCurrency = searchCurrencyInput.val();
    search(searchItem, searchCurrency);
  });

  function search(item_name, currency_name) {
    $.ajax({
      url: '/search',
      data: { item_name: item_name, currency_name: currency_name },
      success: function(response) {
        searchResults.html(response);
      }
    });
  }
});
