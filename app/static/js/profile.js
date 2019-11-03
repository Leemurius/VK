$(document).ready(function () {
   editVisualProfileBox($('.action_menu .my_profile').attr("data-href")); // Default for profile box
   $('.box-for-all').removeClass('col-xl-9').addClass('col-xl-6');
   $('.profile-box').show();
});

LastTrClick = true;