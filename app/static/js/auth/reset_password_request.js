$('.validate-form').on('submit',function() {
    const email = $('.email-input').val();
    const data = JSON.stringify({'email': email});

    var response = postAjaxInformation(getServerName' + getServerName() + '/api/reset', data);
    if (response != true) {
        const error_text = JSON.parse(JSON.parse(response).message);
        $('.email-input-div').attr('data-validate', error_text);
        showValidate($('.email-input'));
        return false;
    } else {
        $('.toast').stop().fadeIn(400).delay(3000).fadeOut(500);
        setTimeout(
            function () {
                window.location.assign("http://" + getServerName() + "/")
            },
            3000
        );
        return false;
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