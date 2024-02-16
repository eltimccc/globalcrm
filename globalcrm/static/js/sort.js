document.addEventListener('DOMContentLoaded', function() {
    var sortForm = document.getElementById('sortForm');
    var selectElement = document.getElementById('sort_by');

    selectElement.addEventListener('change', function() {
        sortForm.submit();
    });
});