$(document).ready(function() {  // FOR ALL TEMPLATES
	$('#action_menu_btn').click(function() {
		$('.action_menu').toggle();
	});
    $('.profile-box').hide();
});

$(window).on('load', function() {
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");
});

function getAjaxInformation(url) {
    let response = '';
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
    let response = '';
    $.ajax({ type: "POST",
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

function getIP() {
    return "192.168.43.86:5000";
}

function getProfileInformation(username) {
    return getAjaxInformation('http://' + getIP() + '/api/user/information/' + username)
}

function getSelfProfileInformation() {
    return getAjaxInformation('http://' + getIP() + '/api/self/information')
}

function addInformationInProfileBox(username) {
    editVisualProfileBox(getProfileInformation(username));
}

function addSelfInformationInProfileBox() {
    editVisualProfileBox(getSelfProfileInformation());
}

function editVisualProfileBox(dict) {
    $('.profile-box .name_surname p').text(dict['name'] + ' ' + dict['surname']);
    $('.profile-box .photo-preview img').attr('src', dict['photo']);
    $('.profile-box .list .age .value').text(dict['age'] ? dict['age'] : 'No information');
    $('.profile-box .list .username .value').text(dict['username']);
    $('.profile-box .list .email .value').text(dict['email']);
    $('.profile-box .list .address .value').text(dict['address'] ? dict['address'] : 'No information');
}

var LastLiClick = false; // Action menu
$('.my_profile').on("click", function() {
    if (LastLiClick) {
        $('.box-for-all').removeClass('col-xl-6').addClass('col-xl-9');
        $('.profile-box').hide();
        LastLiClick = false;
    } else {
        addSelfInformationInProfileBox();
        $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
        $('.profile-box').show();
        LastLiClick = true;
    }
});

function getProfileId(username) {
    return getAjaxInformation('http://' + getIP() + '/api/user/id/' + username);
}

$(".write_message button").click(function () {
    var room_id = getAjaxInformation('http://' + getIP() + '/api/rooms/' + getProfileId(LastTrClick));
    window.location.assign("http://" + getIP() + "/chat/" + room_id);
});