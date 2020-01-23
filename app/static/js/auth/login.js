$('.validate-form').on('submit',function(){
    const login = $('.username-input').val();
    const password = $('.password-input').val();
    const data = JSON.stringify({'login' : login, 'password' : password});

    var response = postAjaxInformation(getPrefixUrl() + '/api/login', data);
    if (response != true) {
        const error_text = JSON.parse(JSON.parse(response).message);
        $('.password-input-div').attr('data-validate', error_text);
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