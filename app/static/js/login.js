$('.login_button').click(function () {
    const login = $('.username-input').val();
    const password = $('.password-input').val();
    const data = JSON.stringify({'login' : login, 'password' : password});
    var response = postAjaxInformation('http://' + getIP() + '/api/login_user', data)
});