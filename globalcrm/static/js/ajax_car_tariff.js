$(document).ready(function() {
    $('#id_car').change(function() {
      var carId = $(this).val();
  
      $.ajax({
        url: '/contracts/get_car_tariff/',
        data: {'car_id': carId},
        type: 'GET',
        success: function(response) {
          $('#id_tariff').val(response.tariff);
        },
        error: function() {
          alert('Произошла ошибка при получении тарифа машины.');
        }
      });
    });
  });
  