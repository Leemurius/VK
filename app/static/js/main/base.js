// Libs variables
var myApp = angular.module('myApp', []);  // ANGULAR FOR ALL TEMPLATES
var rooms_sio = io.connect(getPrefixUrl() + "/rooms");

// Profile information
var me = getAjaxInformation(getPrefixUrl() + '/api/self/information');
var rooms = getRoomList({'request': ''});

$(document).ready(function() {  // FOR ALL TEMPLATES
    $('#preloader').delay(450).fadeOut('slow');

    $('#action_menu_btn').click(function() {
        $('.action_menu').toggle();
    });
    $('.profile-box').hide();
    angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
    rooms_sio.emit('join');  // Connect with all rooms for giving message
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

rooms_sio.on('get_updated_room', function (room) {
    for (let i = 0; i < rooms.length; i++) {
        if (rooms[i]['id'] == room['id']) {
            rooms[i] = room;
            rooms[0] = [rooms[i], rooms[i] = rooms[0]][0]; // swap first and i-th
            angular.element(document.getElementById('searchRoom')).scope().updateListOfRooms(rooms);
            return;
        }
    }
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

function saveStateInHistory(title, url) {
    window.history.pushState({'title':title}, title, url);
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
                                '<p class="preview">' + room['last_message']['text'] + '</p>' +
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

window.onpopstate = function(e) {
    if(e.state) {
        switch (e.state.title) {
            case 'Messages':
                loadChatPage();
                break;
            case 'Settings':
                loadSettingsPage();
                break;
            case 'Search':
                loadSearchPage();
                break;
        }
    }
};

async function loadSettingsPage() {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/settings.html'};
    $('head').append(getHTMLBlock(data));
    $(document).attr('title', 'Settings');

    // Timeout for loading css
    await new Promise(r => setTimeout(r, 100));

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));

    // JS files
    let js_files = getListOfJSFromHTML(data);
    for (let i = 0; i < js_files.length; i++) {
        loadJS(js_files[i]);
    }

    // Change URL
    saveStateInHistory('Settings', '/my_profile/settings');
}

async function loadSearchPage() {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/search.html'};
    $('head').append(getHTMLBlock(data));
    $(document).attr('title', 'Search');

    // Timeout for loading css
    await new Promise(r => setTimeout(r, 100));

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));

    // JS files
    let js_files = getListOfJSFromHTML(data);
    for (let i = 0; i < js_files.length; i++) {
        loadJS(js_files[i]);
    }

    // Change URL
    saveStateInHistory('Search', '/search');
}

async function loadChatPage(id) {
    // CLear
    $('.additional_page').empty();

    // Head
    let data = {'blockname': 'head', 'filename': '/templates/main/chat.html'};
    $('head').append(getHTMLBlock(data));
    $(document).attr('title', 'Messages');

    // Timeout for loading css
    await new Promise(r => setTimeout(r, 100));

    // Main
    data['blockname'] = 'main';
    $('.additional_page').append(getHTMLBlock(data));


    // JS files
    let js_files = getListOfJSFromHTML(data);
    for (let i = 0; i < js_files.length; i++) {
        loadJS(js_files[i]);
    }

    // Change URL
    saveStateInHistory('Messages', '/messages?sel='+id);
}

// Clicks on buttons ------------------------------------------------------------------------------------------

$('.search_link').click(function () {
    saveStateInHistory(document.title, window.location.href);
    loadSearchPage();
});

$('.settings_link').click(function () {
    saveStateInHistory(document.title, window.location.href);
    loadSettingsPage();
});

$(".write_message button").click(function () {
    saveStateInHistory(document.title, window.location.href);
    loadChatPage(LastClickOn);
});

$('.contacts').on('click', 'li', function () {
    saveStateInHistory(document.title, window.location.href);
    loadChatPage($(this).attr('room_id'));
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
