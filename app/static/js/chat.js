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
	$(".messages").animate({ scrollTop: undefined }, "fast");
};

$('.submit').click(function() {

});

var check = false;
$(window).on('keydown', function(e) {
  if (e.which == 13 && !check && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
    check = true;
      $('.submit').click()
      $('.message-input textarea').val(null);
  }

    message = $(".message-input textarea").val();
	if((message.match(/\n/g)||[]).length) {
        $(".message-input textarea").css({"height" : "5em"});
        $("#frame .content .messages ul li:nth-last-child(1)").css({"margin-bottom" : "5em"});
        $(".messages").animate({ scrollTop: 10000000000 }, "fast");
        $("#frame .content .message-input .wrap .attachment").css({"margin-top" : "1.5em"});
        $("#frame .content .message-input .wrap button").css({"margin-top" : "1.5em"});
	}

	if(!(message.match(/\n/g)||[]).length) {
        $(".message-input textarea").css({"height" : "2.2em"});
        $("#frame .content .messages ul li:nth-last-child(1)").css({"margin-bottom" : "1em"});
        $(".messages").animate({ scrollTop: 10000000000 }, "fast");
        $("#frame .content .message-input .wrap .attachment").css({"margin-top" : "17px"});
        $("#frame .content .message-input .wrap button").css({"margin-top" : "0em"});
	}
});

$(document).ready(function() {
    $('.message-input textarea').focus()
});