// Libs variables
var myApp = angular.module('myApp', []);  // ANGULAR FOR ALL TEMPLATES
var user_sio = io.connect(getPrefixUrl() + "/user");

// Profile information
var me = getAjaxInformation(getPrefixUrl() + '/api/self/information');
var rooms = getRoomList({'request': ''});
var uploaded_pages = [];

$(document).ready(function() {  // FOR ALL TEMPLATES
    $('#preloader').delay(450).fadeOut('slow');

    $('#action_menu_btn').click(function() {
        $('.action_menu').toggle();
    });
    $('.profile-box').hide();
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
    user_sio.emit('join');  // Connect user to events
    uploaded_pages.push(document.title);
});

// Requests -----------------------------------------------------------------------------------------

function loadJS (url) {
    jQuery.ajax({
        url: url,
        dataType: 'script',
        async: true
    });
}

function getAjaxInformation(url) {
    let response = null;
    $.ajax({ type: "GET",
             url: url,
             async: false,
             success : function(text) {
                 response = text;
             }
    });
    return response;
}

function postAjaxInformation(url, data) {
    let response = null;
    $.ajax({
             type: "POST",
             url: url,
             async: false,
             data: JSON.stringify(data),
             contentType: 'application/json;charset=UTF-8',
             success : function(text) {
                 response = text;
             },
             error: function(xhr, status, error) {
                 response = xhr.responseText;
             }
    });
    return response
}

function postAjaxPhoto(url, photo) {
     var form_data = new FormData();
     form_data.append('photo', photo);

     let response = null;
     $.ajax({
        type: 'POST',
        url: url,
        data: form_data,
        contentType: false,
        async: false,
        cache: false,
        processData: false,
        success : function(text) {
             response = text;
        },
        error: function(xhr, status, error) {
            response = xhr.responseText;
        }
    });

    return response;
}

// SIO ----------------------------------------------------------------------------------------------

user_sio.on('get_message', function (message) {
    addMessage(message);
    for (let i = 0; i < rooms.length; i++) {
        if (rooms[i].is_dialog == message.is_dialog && rooms[i].id == message.room_id) {

            if (document.title == 'Messages' && Number(getRecipientId()) == rooms[i].recipient_id) {
                rooms[i].unread_messages_count = 0;
            } else {
                rooms[i].unread_messages_count += 1;
            }
            rooms[i].last_message = message;
            rooms[0] = [rooms[i], rooms[i] = rooms[0]][0]; // swap first and i-th
            break;
        }
    }

     if (document.title == 'Messages') {
         user_sio.emit('read_messages', Number(getRecipientId()));
     }
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
    $('.msg_card_body').scrollTop($('.msg_card_body')[0].scrollHeight);  // scroll chat to down
});

user_sio.on('update_room', function (room) {
    for (let i = 0; i < rooms.length; i++) {
        if (rooms[i].id == room.id) {
            rooms[i] = room;
            break;
        }
    }
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
});

user_sio.on('get_new_room', function (room) {
    rooms.splice(0, 0, room);
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
});

// API ----------------------------------------------------------------------------------------------

function getProtocol() {
    return location.protocol;
}

function getServerName() {
    return document.domain + ':' + location.port;
}

function getPrefixUrl() {
    return getProtocol() + "//" + getServerName();
}

function getRoomList(data) {
    return postAjaxInformation(getPrefixUrl() + '/api/self/find/room', data);
}

function getProfileInformation(id) {
    return postAjaxInformation(getPrefixUrl() + '/api/user/information', {'id': id});
}

function getHTMLBlock(data) {
    return postAjaxInformation(getPrefixUrl() + '/api/html/get', data);
}

function getListOfJSFromHTML(data) {
    return postAjaxInformation(getPrefixUrl() + '/api/js/list/get', data);
}

function replaceStateInHistory(data, url) {
    window.history.replaceState(data, data['title'], url);
}

function saveStateInHistory(data, url) {
    window.history.pushState(data, data['title'], url);
}

function addInformationInProfileBox(id) {
    if (id == me.id) {
        $('.write_message').hide();
    } else {
        $('.write_message').show();
    }
    editVisualProfileBox(getProfileInformation(id));
}

function editVisualProfileBox(dict) {
    $('.profile-box .name_surname p').text(dict['name'] + ' ' + dict['surname']);
    $('.profile-box .photo-preview img').attr('src', dict['photo']);
    $('.profile-box .list .age-base .value').text(dict['age'] ? dict['age'] : 'No information');
    $('.profile-box .list .username-base .value').text(dict['username']);
    $('.profile-box .list .email-base .value').text(dict['email']);
    $('.profile-box .list .address-base .value').text(dict['address'] ? dict['address'] : 'No information');
}

// Angular for profile box animation ------------------------------------------------------------------------------

var LastClickOn = undefined;  // Search menu
myApp.controller('baseController',['$scope', '$compile',function($scope, $compile) {
    $scope.name = {};
    $scope.resizeObjectsWithInformation = function (id) {
        if (LastClickOn == id) {
            setTimeout(
                function () {
                    $('.profile-box').removeClass('col-xl-3').addClass('col-xl-1');
                    setTimeout(
                        function () {
                            $('.profile-box').hide();
                        },
                        150);
                },
                200);
            setTimeout(
                function () {
                    $('.box-for-all').removeClass('col-xl-6').addClass('col-xl-9');
                },
                400);

            LastClickOn = undefined;
        } else {
            addInformationInProfileBox(id);
            $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');

            setTimeout(
                function () {
                    $('.profile-box').show();
                    $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
                },
                200);

            LastClickOn = id;
        }
    };

    // TODO: Moved from search.js, because it has problems with dynamically upload of ng-controllers
    $scope.updateListOfUsers = function (users) {
        $('.user-links').remove();  // delete all links on user
        for (let i = 0; i < users.length; i++) {
            var user = users[i];
            var element = '<tr class="user-links" ng-click="resizeObjectsWithInformation(' + user.id.toString() + ')">' +
                    '<td>' +
                        '<img src="' + user['photo'] + '" alt="" class="rounded-circle user_img">' +
                        '<span class="name_surname">' + user['name'] + ' ' + user['surname'] + '</span>' +
                    '</td>' +
                    '<td>' + (user['age'] ? user['age'] : 'No information') + '</td>' +
                    '<td class="text-center">' +
                        (user['status'] ? '<span class="label label-success">Online</span>' : '<span class="label label-default">Offline</span>') +
                    '</td>' +
                    '<td>' +
                        '<span>' + user['email'] + '</span>' +
                    '</td>' +
                '</tr>';

            var compiledElement = $compile(element)($scope);
            $(compiledElement).appendTo($('.list-for-users'));
        }
    };

    $scope.updateListOfRooms = function (rooms) {
        $('.room-links').remove();  // delete all links on rooms

        for (let i = 0; i < rooms.length; i++) {
            let room = rooms[i];
            if (room['is_dialog']) {
                let element = '<li class="room-links" room_id="' + (room['is_dialog'] ? room['recipient_id'] : 'c' + room['id']) + '">' +
                        '<div class="d-flex bd-highlight">' +
                            '<div class="img_cont">' +
                                '<img src="' + room['photo'] + '" class="rounded-circle user_img">' +
                                '<span class="online_icon ' + (room['status'] ? 'online' : 'offline') + '"></span>' +
                            '</div>' +
                            '<div class="user_info">' +
                                '<span class="name">' + room['title'] + '</span>' +
                                '<p class="preview">' + (room['last_message']['sender']['username'] == me.username ? 'You' : room['last_message']['sender']['username']) + ':  ' + room['last_message']['text'] + '</p>' +
                            '</div>' +
                            (room['unread_messages_count'] > 0 ?
                            '<div class="message_info">' +
                               '<p>' + room['unread_messages_count'] + '</p>' +
                            '</div>' : '') +
                        '</div>' +
                    '</li>';
                let compiledElement = $compile(element)($scope);
                $(compiledElement).appendTo($('.contacts'));
            } else {
                // TODO: CHAT
            }
        }
    };

    // TODO: Moved from chat.js, because it has problems with dynamically upload of ng-controllers
    $scope.setHeader = function(element) {
        let compiledElement = $compile(element)($scope);
        (compiledElement).appendTo($('.chat_user_header'));
    };

    // TODO: Moved from chat.js, because it has problems with dynamically upload of ng-controllers
    $scope.addMessageVisualFromYou = function(message) {
        let element = '<div class="d-flex justify-content-end mb-4">' +
                '<div class="msg_cotainer_send">' +
                    '<p class="text">' + message.text + '</p>' +
                    '<span class="msg_time_send">' + formatTime(message.time) + '</span>' +
                '</div>' +

                '<div class="img_cont_msg">' +
                   '<img src="' + me.photo + '" class="rounded-circle user_img_msg" ng-click="resizeObjectsWithInformation(' + me.id.toString() + ')">' +
                '</div>' +
            '</div>';
        let compiledElement = $compile(element)($scope);
        (compiledElement).appendTo($('.msg_card_body'));
    };

    // TODO: Moved from chat.js, because it has problems with dynamically upload of ng-controllers
    $scope.addMessageVisualFromOther = function(message) {
        let element = '<div class="d-flex justify-content-start mb-4">' +
                '<div class="img_cont_msg">' +
                   '<img src="' + message.sender.photo + '" ' +
            '           class="rounded-circle user_img_msg" ' +
            '           ng-click="resizeObjectsWithInformation(' + message.sender.id.toString() + ')"' +
            '       >' +
                '</div>' +

                '<div class="msg_cotainer">' +
                    '<p class="text">' + message.text + '</p>' +
                    '<span class="msg_time">' + formatTime(message.time) + '</span>' +
                '</div>' +
            '</div>';

        let compiledElement = $compile(element)($scope);
        (compiledElement).appendTo($('.msg_card_body'));
    };
}]);

// Page loads ------------------------------------------------------------------------------------------

function addUploadedPageInList(title) {
    if (!wasUploadedPage(title)) {
        uploaded_pages.push(title);
    }
}

function wasUploadedPage(title) {
    for (let i = 0; i < uploaded_pages.length; i++) {
        if (uploaded_pages[i] == title) {
            return true;
        }
    }
    return false;
}

window.onpopstate = function(e) {
    if(e.state) {
        switch (e.state.title) {
            case 'Messages':
                loadChatPage(e.state.id, false);
                break;
            case 'Settings':
                loadSettingsPage(false);
                break;
            case 'Search':
                loadSearchPage(false);
                break;
        }
    }
};

async function loadSettingsPage(needSaveState) {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/settings.html'};
    if (!wasUploadedPage('Settings')) {
        $('head').append(getHTMLBlock(data));

        // Timeout for loading css
        await new Promise(r => setTimeout(r, 100));
    }
    $(document).attr('title', 'Settings');

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));

    // JS files
    if (!wasUploadedPage('Settings')) {
        let js_files = getListOfJSFromHTML(data);
        for (let i = 0; i < js_files.length; i++) {
            loadJS(js_files[i]);
        }
    } else {
        _initSettings();
    }

    // Change URL
    if (needSaveState) {
        saveStateInHistory({'title': 'Settings'}, '/my_profile/settings');
    }
    addUploadedPageInList('Settings');
}

async function loadSearchPage(needSaveState) {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/search.html'};
    if (!wasUploadedPage('Search')) {
        $('head').append(getHTMLBlock(data));

        // Timeout for loading css
        await new Promise(r => setTimeout(r, 100));
    }
    $(document).attr('title', 'Search');

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));

    // JS files
    if (!wasUploadedPage('Search')) {
        let js_files = getListOfJSFromHTML(data);
        for (let i = 0; i < js_files.length; i++) {
            loadJS(js_files[i]);
        }
    } else {
        _initSearch();
    }

    // Change URL
    if (needSaveState) {
        saveStateInHistory({'title': 'Search'}, '/search');
    }
    addUploadedPageInList('Search');
}

async function loadChatPage(id, needSaveState) {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/chat.html'};
    if (!wasUploadedPage('Messages')) {
        $('head').append(getHTMLBlock(data));
        // Timeout for loading css
        await new Promise(r => setTimeout(r, 100));
    }
    $(document).attr('title', 'Messages');

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));

    // Change URL
    if (needSaveState) {
        saveStateInHistory({'title': 'Messages', 'id': id}, '/messages?sel=' + id);
    }

    // JS files
    if (!wasUploadedPage('Messages')) {
        let js_files = getListOfJSFromHTML(data);
        for (let i = 0; i < js_files.length; i++) {
            loadJS(js_files[i]);
        }
    } else {
        _initChat();
    }
    addUploadedPageInList('Messages');
}

// Clicks on buttons ------------------------------------------------------------------------------------------

$('.search_link').click(function () {
    replaceStateInHistory({'title': document.title}, window.location.href);
    loadSearchPage(true);
});

$('.settings_link').click(function () {
    replaceStateInHistory({'title': document.title}, window.location.href);
    loadSettingsPage(true);
});

$(".write_message button").click(function () {
    replaceStateInHistory({'title': document.title, 'id': LastClickOn}, window.location.href);
    loadChatPage(LastClickOn, true);
});

$('.contacts').on('click', 'li', function () {
    replaceStateInHistory({'title': document.title, 'id': LastClickOn}, window.location.href);
    loadChatPage($(this).attr('room_id'), true);
});


// Search of rooms ------------------------------------------------------------------------------------------------

function searchRooms() {
    const data = {'request': $('.search-room-input').val()};
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(getRoomList(data));
}

$(".search-room").click(function (e) {
    searchRooms();
});

$(".search-room-input").on('keyup', function (e) {
    if (e.keyCode == 13) {
        searchRooms();
    }
});
