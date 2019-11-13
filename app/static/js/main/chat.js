// - Requests --------------------------------------------------------------------------------------

function getSelfPhoto() {
    return getAjaxInformation('http://' + getIP() + '/api/self/photo');
}

function getRoomId() {
    const split_url = (window.location.href).split('/'); // current link
    const room_id = split_url[split_url.length - 1];
    return room_id;
}

function addMessage(text) {
    if (text == '') {
        return null;
    }
    var data = JSON.stringify({'room_id' : Number(getRoomId()), 'message' : text});
    var response = JSON.parse(postAjaxInformation('http://' + getIP() + '/api/messages', data));
    return response;
}

// - JS --------------------------------------------------------------------------------------------

$(document).ready(function() {
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
});

$(window).on('keydown', function(e) {
    if (e.which == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
        var message = getMessageFromArea();
        if (addMessage(message)) {
            addMessageVisualFromYou(message);
            beginState();
        }
    }
});

$('textarea').keypress(function(event) {   // Delete new line after sending message
    if (event.keyCode == 13 && !event.shiftKey) {
        event.preventDefault();
    }
});

function beginState() {
    $('textarea').val('');
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
}

function getMessageFromArea() {
    var message = $('textarea').val();
    return message;
}

function addMessageVisualFromYou(message) {
    const cur_date = new Date();
    let date = cur_date.toLocaleString('en-US', {hour: 'numeric', minute: 'numeric', hour12: true});
    date = date.replace("AM", "am").replace("PM", "pm");

    $('<div class="d-flex justify-content-end mb-4">' +
            '<div class="msg_cotainer_send">' +
                '<p class="text">' + message + '</p>' +
                '<span class="msg_time_send">' + date + '</span>' +
            '</div>' +

            '<div class="img_cont_msg">' +
               '<img src="' + getSelfPhoto() + '" class="rounded-circle user_img_msg" >' +
            '</div>' +
        '</div>'
    ).appendTo($('.msg_card_body'));
}

$(".send_btn").click(function() {
    var message = getMessageFromArea();
    if (addMessage(message)) {
        addMessageVisualFromYou(message);
        beginState();
    }
});