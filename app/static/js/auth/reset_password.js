$('.validate-form').on('submit', function () {
    let new_password = $('.new-password').val();
    let confirm_password = $('.confirm-password').val();

    let data = {
        'new_password': new_password,
        'confirm_password': confirm_password
    };
    let token = window.location.pathname.split('/')[2];
    let response = postAjaxInformation('/api/user/setPassword/' + token, data);
    if (response.status_code != 200) {
        let errors_list = JSON.parse(JSON.parse(response.text).message);
        for (let i = 0; i < errors_list.length; i++) {
            if (errors_list[i] == null) {
                continue;
            }

            if (errors_list[i][0] == 'new_password') {
                addValidateMessage('.new-password', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'confirm_password') {
                addValidateMessage('.confirm-password', errors_list[i][1]);
            }
        }
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

$('.input100').each(function () {
    $(this).focus(function () {
        hideValidate(this);
    });
});

function addValidateMessage(attr, message) {
    $(attr).parent().attr('data-validate', message);
    showValidate($(attr));
}

function showValidate(input) {
    let thisAlert = $(input).parent();
    $(thisAlert).addClass('alert-validate');
}

function hideValidate(input) {
    let thisAlert = $(input).parent();
    $(thisAlert).removeClass('alert-validate');
}