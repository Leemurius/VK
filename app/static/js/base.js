$(window).on('load', function() {
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");
});

$(".messages").animate({ scrollTop: 1000000000 }, "fast");