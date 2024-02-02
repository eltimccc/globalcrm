$(document).ready(function() {
    $('#id_start_date, #id_end_date, #id_rental_days').change(function() {
      var start_date_str = $('#id_start_date').val();
      var end_date_str = $('#id_end_date').val();
      var rentalDays = $('#id_rental_days').val();
  
      if (start_date_str && end_date_str && rentalDays) {
        var start_date = new Date(start_date_str);
        var end_date = new Date(end_date_str);
        var calculated_rental_days = Math.round((end_date - start_date) / (24 * 60 * 60 * 1000));
  
        if (calculated_rental_days !== parseInt(rentalDays)) {
          end_date = new Date(start_date.getTime() + (parseInt(rentalDays) * 24 * 60 * 60 * 1000));
          $('#id_end_date').val(end_date.toISOString().slice(0, 19).replace('T', ' '));
        }
      }
    });
  });
  