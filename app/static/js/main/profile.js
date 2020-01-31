$(document).ready(function () {
    addInformationInProfileBox(me.id);
    $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
    $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
    setTimeout(function () { $('.profile-box').show(); }, 500);  // For normal animation
    LastClickOn = me.id;
});