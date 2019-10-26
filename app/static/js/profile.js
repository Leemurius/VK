function getIP() {
    return "127.0.0.1:5000";
}

$(document).ready(function() {

});

function GetAjaxInformation(url) {
    var response = undefined;
    $.ajax({ type: "GET",
             url: url,
             async: false,
             success : function(text) {
                 response = text;
             }
    });
    return response;
}

function GetProfileId() {
    var split_url = (window.location.href).split('/'); // current link
    var nick = split_url[split_url.length - 1];
    return GetAjaxInformation('http://' + getIP() + '/api/profile_id/' + nick);
}

$(".write_message a").click(function() {
    var room_id = GetAjaxInformation('http://' + getIP() + '/api/rooms/' + GetProfileId());
   $(".write_message a").attr('href', 'chat/' + room_id);
});
