$('.validate-form').on('submit', function () {
    let email = $('.email-input').val();
    let data = {'email': email};

    let response = postAjaxInformation('/api/user/reset', data);
    if (response.status_code != 200) {
        let error_text = JSON.parse(JSON.parse(response.text).message);
        $('.email-input-div').attr('data-validate', error_text);
        showValidate($('.email-input'));
        return false;
    } else {
        $('.toast').stop().fadeIn(400).delay(3000).fadeOut(500);
        setTimeout(
            function () {
                window.location.assign("/")
            },
            3000
        );
        return false;
    }
});

$('.validate-form .input100').each(function () {
    $(this).focus(function () {
        hideValidate(this);
    });
});

function showValidate(input) {
    let thisAlert = $(input).parent();
    $(thisAlert).addClass('alert-validate');
}

function hideValidate(input) {
    let thisAlert = $(input).parent();
    $(thisAlert).removeClass('alert-validate');
}