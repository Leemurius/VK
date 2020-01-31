var messages_sio = io.connect(getPrefixUrl() + "/messages");

$(document).ready(function() {
    joinToChatOrDialog();
    $('textarea').select();
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
});

// - SIO ------------------------------------------------------------------------------------------

messages_sio.on('get_message', function (message) {
    addMessage(message);
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);  // scroll chat to down
});

// - JS --------------------------------------------------------------------------------------------

function addMessage(message) {
    if (message.sender.id == me.id) {
        angular.element(document.getElementById('chatController')).scope().addMessageVisualFromYou(message);
    } else {
        angular.element(document.getElementById('chatController')).scope().addMessageVisualFromOther(message);
    }
}

function formatTime(time) {
    let date = new Date(time + ' UTC').toLocaleString('en-US', {hour: 'numeric', minute: 'numeric', hour12: true});
    return date.replace("AM", "am").replace("PM", "pm");
}

function setHeader() {
    if (isDialog()) {
        let recipient = postAjaxInformation(getPrefixUrl() + '/api/user/information', {'id': Number(getRecipientId())});
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
    const messages = postAjaxInformation(
        getPrefixUrl() + '/api/dialog/get/messages',
        {'profile_id': Number(getRecipientId())}
    );
    for (let i = 0; i < messages.length; i++) {
        addMessage(messages[i]);
    }
}

function isDialog() {
    return location.search[5] != 'c';
}

function getRecipientId() {
    return location.search.split('=')[1];
}

function joinToChatOrDialog() {
    if (isDialog()) {
        messages_sio.emit('join', getRecipientId());
    } else {
        // TODO: CHAT
    }
    setHeader();
    addMessages();
}

// Send message ----------------------------------------------------------------------------------------

function sendMessage(text) {
    if (text == '') {
        return null;
    }
    messages_sio.emit('send_message', Number(getRecipientId()), text);
    return true;
}

$(window).on('keydown', function(e) {
    if (e.which == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
        sendMessage($('textarea').val());
        $('textarea').val('');  // clear textarea
    }
});

$(".send_btn").click(function() {
    sendMessage($('textarea').val());
    $('textarea').val('');  // clear textarea
});

$('textarea').keypress(function(event) {   // Delete new line after sending message
    if (event.keyCode == 13 && !event.shiftKey) {
        event.preventDefault();
    }
});
