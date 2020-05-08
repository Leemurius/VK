$(document).ready(function () {
    // Add information and show box with profile information
    addInformationInProfileBox(me.id);
    $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
    $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
    setTimeout(function () {
        $('.profile-box').show();
    }, 500);

    // Save state on yourself
    LastClickOn = me.id;

    // For upload without refreshing
    replaceStateInHistory({'title': document.title}, window.location.href);
});