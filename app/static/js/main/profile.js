$(document).ready(function () {
   addInformationInProfileBox(getSelfUsername());
   $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
   $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
   $('.profile-box').show();
   LastClickOn = getSelfUsername();
});