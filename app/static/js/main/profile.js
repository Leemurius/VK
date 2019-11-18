$(document).ready(function () {
   addSelfInformationInProfileBox(); // Default for profile box
   $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
   $('.profile-box').show();
   $('.card-header .big-window').remove();
});

LastTrClick = true;