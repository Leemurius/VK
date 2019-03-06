$(".messages").animate({ scrollTop: 1000000000 }, "fast");

$("#profile-img").click(function() {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

function newMessage() {
	message = $(".message-input textarea").val();
	if($.trim(message) == '') {
		return false;
	}
	// $('<li class="sent">' +
    //     '<img src="http://emilcarlsson.se/assets/mikeross.png" alt="">' +
    //     '<p>' + message + '</p>' +
    //     '</li>').appendTo($('.messages ul'));
	// $('.message-input textarea').val(null);
	// $('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: 100000000000 }, "fast");
};

$('.submit').click(function() {
    newMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
      $('.submit').click()
    newMessage();
    return false;
  }
});