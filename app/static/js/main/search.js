var LastTrClick = undefined;
$('tr[data-href]').on("click", function() {
    const username = $(this).attr("data-href");

    if (LastTrClick == username) {
        $('.box-for-all').removeClass('col-xl-6').addClass('col-xl-9');
        $('.profile-box').hide();
        LastTrClick = undefined;
    } else {
        addInformationInProfileBox(username);
        $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
        $('.profile-box').show();
        LastTrClick = username;
    }
});

$(".write_message a").click(function() {
    var username = $(this).attr("href");
    var room_id = getAjaxInformation('http://' + getIP() + '/api/rooms/' + getProfileId(username));
   $(".write_message a").attr('href', 'chat/' + room_id);
});


$(".search-person").click(function (e) {
    // TODO: realize this:(
});