$('.registration-btn').click(function () {
    const name = $('.name-input').val();
    const surname = $('.surname-input').val();
    const username = $('.username-input').val();
    const email = $('.email-input').val();
    const password = $('.password-input').val();
    const confirm_password = $('.confirm-input').val();
    const data = JSON.stringify({
        'name': name,
        'surname': surname,
        'username': username,
        'email': email,
        'password' : password
    });

    if (password == confirm_password) {
        var response = postAjaxInformation('http://' + getIP() + '/api/create_user', data)
        if (response) {
            alert('kek')
        }
    }
});