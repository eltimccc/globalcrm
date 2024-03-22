$(document).ready(function() {
    $('.price-detail-link').click(function(event) {
        event.preventDefault();
        var tariffPK = $(this).data('price-pk');
        var modal = $('#tariffModal');
        $.ajax({
            url: '/prices/price_modal/' + tariffPK + '/',
            success: function(data) {
                modal.find('.modal-body').html(data.html_modal_content);
                modal.modal('show');
            }
        });
    });
});