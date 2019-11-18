$('.validate-form').on('submit',function() {
    const email = $('.email-input').val();
    const data = JSON.stringify({'email': email});

    var response = postAjaxInformation('http://' + getServerName() + '/api/reset', data);
    if (response != true) {
        const error_text = JSON.parse(JSON.parse(response).message);
        $('.email-input-div').attr('data-validate', error_text);
        showValidate($('.email-input'));
        return false;
    } else {
        window.location.assign("http://" + getServerName() + "/");  // TODO: redirect back
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