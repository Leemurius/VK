var sio = io.connect(getPrefixUrl() + "/chat");

$(document).ready(function() {
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
});

// - SIO ------------------------------------------------------------------------------------------

sio.on('get_message', function (message, photo) {
    angular.element(document.getElementById('chatController')).scope().addMessageVisualFromOther(message, photo);
    setBeginState();
});

// - API ------------------------------------------------------------------------------------------

function getSelfPhoto() {
    return getAjaxInformation(getPrefixUrl() + '/api/self/photo');
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
    sio.emit('send_message', Number(getRoomId()), text);
    return true;
}

// - JS --------------------------------------------------------------------------------------------


myApp.controller('chatController',['$scope', '$compile',function($scope, $compile) {
    $scope.addMessageVisualFromYou = function(message) {
        const cur_date = new Date();
        let date = cur_date.toLocaleString('en-US', {hour: 'numeric', minute: 'numeric', hour12: true});
        date = date.replace("AM", "am").replace("PM", "pm");

        var element = '<div class="d-flex justify-content-end mb-4">' +
                '<div class="msg_cotainer_send">' +
                    '<p class="text">' + message + '</p>' +
                    '<span class="msg_time_send">' + date + '</span>' +
                '</div>' +

                '<div class="img_cont_msg">' +
                   '<img src="' + getSelfPhoto() + '" class="rounded-circle user_img_msg" ng-click="resizeObjectsWithInformation(' +'\'' + getSelfUsername() + '\''+ ')">' +
                '</div>' +
            '</div>';

        var compiledElement = $compile(element)($scope);
        (compiledElement).appendTo($('.msg_card_body'));
    };

    $scope.addMessageVisualFromOther = function(message, photo) {
        const cur_date = new Date();
        let date = cur_date.toLocaleString('en-US', {hour: 'numeric', minute: 'numeric', hour12: true});
        date = date.replace("AM", "am").replace("PM", "pm");

        var element = '<div class="d-flex justify-content-start mb-4">' +
                '<div class="img_cont_msg">' +
                   '<img src="' + photo + '" ' +
            '           class="rounded-circle user_img_msg" ' +
            '           ng-click="resizeObjectsWithInformation(' +'\'' + "LOL" + '\''+ ')"' +
            '       >' +
                '</div>' +

                '<div class="msg_cotainer">' +
                    '<p class="text">' + message + '</p>' +
                    '<span class="msg_time">' + date + '</span>' +
                '</div>' +
            '</div>';

        var compiledElement = $compile(element)($scope);
        (compiledElement).appendTo($('.msg_card_body'));
    };
}]);

// Send message ----------------------------------------------------------------------------------------

function sendMessage() {
    var message = getMessageFromArea();
    if (addMessage(message)) {
        angular.element(document.getElementById('chatController')).scope().addMessageVisualFromYou(message);
        setBeginState();
    }
}

function setBeginState() {
    $('textarea').val('');
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);
}

function getMessageFromArea() {
    var message = $('textarea').val();
    return message;
}

$(window).on('keydown', function(e) {
    if (e.which == 13 && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
        sendMessage()
    }
});

$(".send_btn").click(function() {
    sendMessage();
});

$('textarea').keypress(function(event) {   // Delete new line after sending message
    if (event.keyCode == 13 && !event.shiftKey) {
        event.preventDefault();
    }
});


