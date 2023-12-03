// static/js/file_input_script.js
$(document).ready(function() {
    var fileIndex = 1;
    $("#addFileInput").click(function() {
        var newInput = $("<input type='file' name='uploaded_file' id='id_uploaded_file_" + fileIndex + "'/>");
        $("#fileInputs").append(newInput);
        fileIndex++;
    });
});