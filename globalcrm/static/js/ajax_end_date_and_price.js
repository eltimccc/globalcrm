$(document).ready(function() {
    $('#id_rental_days').change(function() {
      var rentalDays = $(this).val();
      var contractId = $('#id_contract').val();
      var start_date_str = $('#id_start_date').val();
  
      $.ajax({
        url: '/contracts/get_end_date/',
        data: {'rental_days': rentalDays, 'start_date': start_date_str},
        type: 'GET',
        success: function(response) {
          $('#id_end_date').val(response.end_date);
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(xhr.responseText);
          alert('Произошла ошибка при получении end_date. Подробности в консоли браузера.');
        }
      });
  
      $.ajax({
        url: '/contracts/calculate_price/',
        data: {'tariff_id': $('#id_tariff').val(), 'rental_days': rentalDays},
        type: 'GET',
        success: function(response) {
          $('#id_amount').val(response.amount);
        },
        error: function() {
          alert('Произошла ошибка при расчете стоимости.');
        }
      });
    });
  });
  