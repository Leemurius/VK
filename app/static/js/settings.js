$(document).ready(function() {
    $('.input-file').click(function() {
        input = document.getElementById('photo');
        input.addEventListener('change', readSingleFile, false);
        input.click();
    });

    function readSingleFile(evt) {
        var f = evt.target.files[0];

        if (f) {
            $('.input-file__info').text(f.name);
        } else {
          alert("Failed to load file");
        }
    }
});







