function getIP() {
    return "127.0.0.1:5000";
}

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

function GetProfileId(nick) {
    return GetAjaxInformation('http://' + getIP() + '/api/profile_id/' + nick);
}

$(".write_message a").click(function() {
    var nick = $(this).attr("href");
    var room_id = GetAjaxInformation('http://' + getIP() + '/api/rooms/' + GetProfileId(nick));
   $(".write_message a").attr('href', 'chat/' + room_id);
});
