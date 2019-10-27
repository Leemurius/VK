function getIP() {
    return "127.0.0.1:5000";
}

const INF = 100000000000;

function GetAjaxInformation(url) {
    var response = '';
    $.ajax({ type: "GET",
             url: url,
             async: false,
             success : function(text) {
                 response = text;
             }
    });
    return response;
}

function PostAjaxInformation(url, data) {
    var response = '';
    $.ajax({ type: "POST",
             url: url,
             async: false,
             data: data,
             contentType: 'application/json;charset=UTF-8',
             success : function(text) {
                 response = text;
             }
    });
    return response;
}

function GetSelfPhoto() {
    return GetAjaxInformation('http://' + getIP() + '/api/self/user_photo');
}

function GetRoomId() {
    var split_url = (window.location.href).split('/'); // current link
    var room_id = split_url[split_url.length - 1];
    return room_id;
}

function AddMessageInChat(message) {
    var cur_date = new Date();
    var date = cur_date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    date = date.replace("AM", "am").replace("PM", "pm");

    $('<li class="sent">' +
        '<img src=' + GetSelfPhoto() + ' alt="">' +
        '<p>' + message + '</p>' +
        '<span>' + date + '</span>' +
        '</li>'
    ).appendTo($('.messages ul'));
}

function StartState() {
    $('.messages').css({
        'min-height': 'calc(100% - 110px)',
        'max-height': 'calc(100% - 110px)'
    });
    $('.message-input textarea').val('');
    $('.message-input textarea').css({
        'height': '2.3em',
    });

    $(".messages").animate({ scrollTop: INF }, "fast");
}

function AddMessage(text) {
    var data = JSON.stringify({'room_id' : Number(GetRoomId()), 'message' : text});
    var response = JSON.parse(PostAjaxInformation('http://' + getIP() + '/api/messages', data));
    if (response) {
        AddMessageInChat(text);
    }
    StartState();
}

function GetMessageFromArea() {
    var message = $('.message-input textarea').val();
    return message.replace(/^\s+|\s+$/g, ''); // clear text
}

var AREA_HEIGHT = $('textarea').height();
$(window).on('keydown', function(e) {
    if (e.which == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
        if (GetMessageFromArea() == '') return;
        AddMessage(GetMessageFromArea());
        AREA_HEIGHT = $('textarea').height();
    }
});

$(".submit").click(function(e) {
    if (GetMessageFromArea() == '') return;
    AddMessage(GetMessageFromArea());
    AREA_HEIGHT = $('textarea').height();
});

$("textarea").keyup(function(e) {
    function get_height(elt) {
        return elt.scrollHeight +
            parseFloat($(elt).css("borderTopWidth")) +
            parseFloat($(elt).css("borderBottomWidth"));
    }

    if (GetMessageFromArea() == '') { // new line before enter
        StartState();
        return;
    }

    var max_height = +$(this).css('max-height').replace('px', '');
    if ($(this).height() + 50 <= max_height) {
        var found = 0;
        while (!found) {
            $(this).height($(this).height() - 10);
            while($(this).outerHeight() < get_height(this)) {
                $(this).height($(this).height() + 1);
                found = 1;
            }
        }
    }

    var div_heaght = $('.messages').height();
    var area_heaght = $('textarea').height();
    if (AREA_HEIGHT != area_heaght) {
        $('.messages').css({
            'min-height': (div_heaght - (area_heaght - AREA_HEIGHT)).toString() + 'px',
            'max-height': (div_heaght - (area_heaght - AREA_HEIGHT)).toString() + 'px'
        });
        $(".messages").animate({ scrollTop: INF }, "fast");
        AREA_HEIGHT = $('textarea').height();
    }
});
