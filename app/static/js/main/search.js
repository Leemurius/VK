// Search user ------------------------------------------------------------------------------------------------

function getUserList(data) {
    const response = postAjaxInformation(getPrefixUrl() + '/api/self/find/user', data);
    return response;
}

function searchUser() {
    const data = JSON.stringify({
       'request': $('.search-person-input').val()
    });

    // Use angular, because if add ng-click through Jquery - it doesn't work
    angular.element(document.getElementById('searchController')).scope().updateListOfUsers(data);
}

myApp.controller('searchController',['$scope', '$compile',function($scope, $compile) {
    $scope.updateListOfUsers = function (data) {
        $('.user-links').remove();  // delete all links on user
        var users = getUserList(data);
        for (let i = 0; i < users.length; i++) {
            var user = users[i];
            var element = '<tr class="user-links" ng-click="resizeObjectsWithInformation(' + '\'' + user.username +  '\'' + ')">' +
                    '<td>' +
                        '<img src="' + user['photo'] + '" alt="" class="rounded-circle user_img">' +
                        '<span class="name_surname">' + user['name'] + ' ' + user['surname'] + '</span>' +
                    '</td>' +
                    '<td>' + (user['age'] ? user['age'] : 'No information') + '</td>' +
                    '<td class="text-center">' +
                        (user['status'] ? '<span class="label label-success">Online</span>' : '<span class="label label-default">Offline</span>') +
                    '</td>' +
                    '<td>' +
                        '<span>' + user['email'] + '</span>' +
                    '</td>' +
                '</tr>';
            var compiledElement = $compile(element)($scope);
            $(compiledElement).appendTo($('.list-for-users'));
        }
    }
}]);

$('.search-person').click(function (e) {
    searchUser()
});

$(".search-person-input").on('keyup', function (e) {
    if (e.keyCode == 13) {
        searchUser();
    }
});