// file_upload.js
$(document).ready(function() {
    var fileIndex = 1;
    $("#addFileInput").click(function() {
      var newInput = $("<input type='file' name='xfiles' id='id_xfiles_" + fileIndex + "' multiple/>");
      $("#fileInputs").append(newInput);
      fileIndex++;
    });
  });