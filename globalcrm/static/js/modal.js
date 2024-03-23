$(document).ready(function() {
    $('.modal-link').click(function(event) {
        event.preventDefault();
        var url = $(this).data('url'); // URL для AJAX-запроса
        var modalSelector = $(this).data('target'); // Селектор модального окна
        var modal = $(modalSelector);

        $.ajax({
            url: url,
            success: function(data) {
                modal.find('.modal-body').html(data.html_modal_content);
                modal.modal('show');
            }
        });
    });
});