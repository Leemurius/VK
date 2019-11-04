$('.validate-form').on('submit',function(){
    const login = $('.username-input').val();
    const password = $('.password-input').val();
    const data = JSON.stringify({'login' : login, 'password' : password});

    var response = postAjaxInformation('http://' + getIP() + '/api/user/login', data);
    if (response != true) {
        const error_text = JSON.parse(response).message;
        // This line add text in alert, usual solve doesn't work!
        $('.password-input').append("<style>.alert-validate::before{content:'" + error_text + "'}</style>");
        showValidate($('.password-input'));
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