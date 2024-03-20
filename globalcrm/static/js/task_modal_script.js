// task_modal_script.js
$(document).ready(function() {
    $('.task-detail-link').click(function(event) {
      event.preventDefault(); // Предотвращаем переход по ссылке по умолчанию
      var taskPK = $(this).data('task-pk'); // Получаем идентификатор задачи
      var modal = $('#taskModal');
      // AJAX-запрос для получения HTML-кода модального окна
      $.ajax({
        url: '/task_modal/' + taskPK + '/', // URL для получения информации о задаче
        success: function(data) {
          modal.find('.modal-body').html(data.html_modal_content); // Заполняем модальное окно HTML-кодом
          modal.modal('show'); // Показываем модальное окно
        }
      });
    });
});
