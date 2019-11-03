var LastTrClick = undefined;
$('tr[data-href]').on("click", function() {
    const nick = $(this).attr("data-href");

    if (LastTrClick == nick) {
        $('.box-for-all').removeClass('col-xl-6').addClass('col-xl-9');
        $('.profile-box').hide();
        LastTrClick = undefined;
    } else {
        editVisualProfileBox(nick);
        $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
        $('.profile-box').show();
        LastTrClick = nick;
    }
});



$(".write_message a").click(function() {
    var nick = $(this).attr("href");
    var room_id = getAjaxInformation('http://' + getIP() + '/api/rooms/' + getProfileId(nick));
   $(".write_message a").attr('href', 'chat/' + room_id);
});
