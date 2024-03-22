$(document).ready(function() {
    $('.task-detail-link').click(function(event) {
      event.preventDefault();
      var taskPK = $(this).data('task-pk');
      var modal = $('#taskModal');

      $.ajax({
        url: '/task_modal/' + taskPK + '/', 
        success: function(data) {
          modal.find('.modal-body').html(data.html_modal_content);
          modal.modal('show');
        }
      });
    });
});
