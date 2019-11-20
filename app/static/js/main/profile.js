$(document).ready(function () {
   addSelfInformationInProfileBox(); // Default for profile box
   $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
   $('.profile-box').removeClass('col-xl-1').addClass('col-xl-3');
   $('.profile-box').show();
   $('.card-header .big-window').remove();
   LastLiClick = true;
});