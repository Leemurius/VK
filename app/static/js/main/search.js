// Search user ------------------------------------------------------------------------------------------------

$(document).ready(function () {
    _initSearch();
});

function _initSearch() {
    searchUser("");
    replaceStateInHistory({'title': document.title}, window.location.href);
}

function getUserList(data) {
    return postAjaxInformation('/api/search/user', data).text;
}

function searchUser(request) {
    let data = {'request': request};
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