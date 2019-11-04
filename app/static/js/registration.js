$('.registration-btn').on('submit',function(){
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
        'password' : password,
        'confirm_password': confirm_password
    });

    var response = postAjaxInformation('http://' + getIP() + '/api/user/create', data)
    if (response != true) {
        const error_text = JSON.parse(response).message;
        return false;
    } else {
        return true;
    }
});

$('.validate-form .input100').each(function(){
    $(this).focus(function(){
       hideValidate(this);
    });
});

function showValidate(input) {
    var thisAlert = $(input).parent();
    $(thisAlert).addClass('alert-validate');
}

function hideValidate(input) {
    var thisAlert = $(input).parent();
    $(thisAlert).removeClass('alert-validate');
}