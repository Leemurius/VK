$(document).ready(function() {
	$('#action_menu_btn').click(function() {
		$('.action_menu').toggle();
	});
});

function getProfileId(nick) {
    return getAjaxInformation('http://' + getIP() + '/api/profile_id/' + nick);
}

$(".write_message a").click(function() {
    var nick = $(this).attr("href");
    var room_id = getAjaxInformation('http://' + getIP() + '/api/rooms/' + getProfileId(nick));
   $(".write_message a").attr('href', 'chat/' + room_id);
});
