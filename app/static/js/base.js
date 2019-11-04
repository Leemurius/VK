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
             }
    });
    return response;
}

function getIP() {
    return "192.168.43.86:5000";
}

function getProfileInformation(username) {
    return getAjaxInformation('http://' + getIP() + '/api/self/profile_information/' + username)
}

function editVisualProfileBox(username) {
    var dict = getProfileInformation(username);
    $('.profile-box .name_surname p').text(dict['Name'] + ' ' + dict['Surname']);
    $('.profile-box .photo-preview img').attr('src', dict['Photo']);
    $('.profile-box .list .age .value').text(dict['Age'] ? dict['Age'] : 'No information');
    $('.profile-box .list .username .value').text(dict['username'] ? dict['username'] : 'No information');
    $('.profile-box .list .Email .value').text(dict['Email'] ? dict['Email'] : 'No information');
    $('.profile-box .list .Address .value').text(dict['Address'] ? dict['Address'] : 'No information');
}

var LastLiClick = false;
$('li[data-href]').on("click", function() {
    const username = $(this).attr("data-href");

    if (LastLiClick) {
        $('.box-for-all').removeClass('col-xl-6').addClass('col-xl-9');
        $('.profile-box').hide();
        LastLiClick = false;
    } else {
        editVisualProfileBox(username);
        $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
        $('.profile-box').show();
        LastLiClick = true;
    }
});

function getProfileId(username) {
    return getAjaxInformation('http://' + getIP() + '/api/profile_id/' + username);
}

$(".write_message button").click(function () {
    var room_id = getAjaxInformation('http://' + getIP() + '/api/rooms/' + getProfileId(LastTrClick));
    window.location.assign("http://" + getIP() + "/chat/" + room_id);
});