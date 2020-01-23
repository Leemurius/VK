var myApp = angular.module('myApp', []);  // ANGULAR FOR ALL TEMPLATES

$(document).ready(function() {  // FOR ALL TEMPLATES
    $('#preloader').delay(450).fadeOut('slow');

	$('#action_menu_btn').click(function() {
		$('.action_menu').toggle();
	});
    $('.profile-box').hide();
});

// Requests -----------------------------------------------------------------------------------------

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
             data: data,
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

function getProfileId(username) {
    return getAjaxInformation(getPrefixUrl() + '/api/user/id/' + username);
}

function getRoomList(data) {
    return postAjaxInformation(getPrefixUrl() + '/api/self/find/room', data);
}

function getSelfUsername() {
    return getAjaxInformation(getPrefixUrl() + '/api/self/username')
}

function getProfileInformation(username) {
    return getAjaxInformation(getPrefixUrl() + '/api/user/information/' + username)
}

function addInformationInProfileBox(username) {
    if (username == getSelfUsername()) {
        $('.write_message').hide();
    } else {
        $('.write_message').show();
    }
    editVisualProfileBox(getProfileInformation(username));
}

$(".write_message button").click(function () {
    var room_id = getAjaxInformation(getPrefixUrl() + '/api/rooms/' + getProfileId(LastClickOn));
    window.location.assign(getPrefixUrl() + "/chat/" + room_id);
});

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
myApp.controller('baseController',['$scope',function($scope) {
    $scope.name = {};
    $scope.resizeObjectsWithInformation = function (username) {
        if (LastClickOn == username) {
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
            addInformationInProfileBox(username);
            $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');

            setTimeout(
                function () {
                    $('.profile-box').show();
                    $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
                },
                200);

            LastClickOn = username;
        }
    };
}]);

// Search of rooms ------------------------------------------------------------------------------------------------

function searchRooms() {
    const data = JSON.stringify({
       'request': $('.search-room-input').val()
    });

    updateListOfRooms(data);
}

function updateListOfRooms(data) {
    $('.room-links').remove();  // delete all links on rooms

    var rooms = getRoomList(data);
    for (let i = 0; i < rooms.length; i++) {
        var room = rooms[i];
        if (room['is_dialog']) {
            $('<a class="room-links" href="/chat/' + room['room_id'] + '">' +
                    '<li>' +
                        '<div class="d-flex bd-highlight">' +
                            '<div class="img_cont">' +
                                '<img src="' + room['photo'] + '" class="rounded-circle user_img">' +
                                '<span class="online_icon ' + (room['status'] ? 'online' : 'offline') + '"></span>' +
                            '</div>' +
                            '<div class="user_info">' +
                                '<span class="name">' + room['title'] + '</span>' +
                                '<p class="preview">' + room['last_message'] + '</p>' +
                            '</div>' +
                        '</div>' +
                    '</li>' +
                '</a>'
            ).appendTo($('.contacts'))
        } else {
            // TODO: for conversations
        }
    }
}

$(".search-room").click(function (e) {
    searchRooms();
});

$(".search-room-input").on('keyup', function (e) {
    if (e.keyCode == 13) {
        searchRooms();
    }
});