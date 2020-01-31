// Search user ------------------------------------------------------------------------------------------------

$(document).ready(function() {
    searchUser("");
});

function getUserList(data) {
    return postAjaxInformation(getPrefixUrl() + '/api/self/find/user', data);
}

function searchUser(request) {
    const data = {'request': request};
    // Use angular, because if add ng-click through Jquery - it doesn't work
    angular.element(
        document.getElementById('searchController')
    ).scope().updateListOfUsers(getUserList(data));
}

$('.search-person').click(function (e) {
    searchUser($('.search-person-input').val())
});

$(".search-person-input").on('keyup', function (e) {
    if (e.keyCode == 13) {
        searchUser($('.search-person-input').val());
    }
});