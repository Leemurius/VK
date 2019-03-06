$(document).ready(function(){
    $('.messages').scrollTop(100000000000);

    document.getElementById('message').onkeypress = function(e){
        if (e.keyCode == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
            document.getElementById('send').click();
        }
    }
});