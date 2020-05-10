$(document).ready(function () {
    _initChat();
});

function _initChat() {
    setHeader();
    addMessages();
    $('textarea').select();
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
    user_sio.emit('read_messages', Number(getRecipientId()));
    replaceStateInHistory({
        'title': document.title,
        id: Number(getRecipientId())
    }, window.location.href);
}

// - JS --------------------------------------------------------------------------------------------

function addMessage(message) {
    if (message.sender.id == me.id) {
        angular.element(document.getElementById('chatController')).scope().addMessageVisualFromYou(message);
    } else {
        angular.element(document.getElementById('chatController')).scope().addMessageVisualFromOther(message);
    }
}

function formatTime(time) {
    let offset = new Date().getTimezoneOffset();
    let seconds = new Date(time).setMinutes(new Date(time).getMinutes() - offset);
    let date = new Date(seconds).toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });
    return date.replace("AM", "am").replace("PM", "pm");
}

function setHeader() {
    if (isDialog()) {
        let recipient = postAjaxInformation('/api/user/get', {'user_id': Number(getRecipientId())}).text;
        let element = '<div class="img_cont">\n' +
            '                <img src="' + recipient.photo + '" class="rounded-circle user_img" ng-click="resizeObjectsWithInformation(' + recipient.id.toString() + ')" />\n' +
            '                <span class="online_icon ' + (recipient.status ? 'online' : 'offline') + '"></span>\n' +
            '            </div>\n' +
            '            <div class="user_info">\n' +
            '                <span>' + recipient.name + ' ' + recipient.surname + '</span>\n' +
            '                <p class="username"> Username: ' + recipient.username + '</p>\n' +
            '            </div>';
        angular.element(document.getElementById('chatController')).scope().setHeader(element);
    } else {
        // TODO: CHAT
    }
}

function addMessages() {
    let data = {'profile_id': Number(getRecipientId())};
    let messages = postAjaxInformation('/api/messages/getDialogHistory', data).text;

    if (messages.length > 0) {
        room_id = messages[0].room_id;
    } else {
        room_id = -1;
    }

    for (let i = 0; i < messages.length; i++) {
        addMessage(messages[i]);
    }
}

function isDialog() {
    return location.search.substr(0, 5) == '?sel=' && location.search[5] != 'c';
}

function getRecipientId() {
    return location.search.split('=')[1];
}

function getNumOfRoom() {
    return room_id;
}

// Send message ----------------------------------------------------------------------------------------

function sendMessage(text) {
    if (text.trim() == '') return false;
    user_sio.emit('send_message', Number(getRecipientId()), text);
    return true;
}

$(window).on('keydown', function (e) {
    if (e.which == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
        if (sendMessage($('textarea').val())) {
            $('textarea').val('');  // clear textarea
        }
    }
});

$('.additional_page').on('click', '.send_btn', function (event) {
    if (sendMessage($('textarea').val())) {
        $('textarea').val('');  // clear textarea
    }
});

$('.additional_page').on('keypress', 'textarea', function (event) {   // Delete new line after sending message
    if (event.keyCode == 13 && !event.shiftKey) {
        event.preventDefault();
    }
});
