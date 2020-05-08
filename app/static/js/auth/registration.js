$('.validate-form').on('submit', function () {
    let name = $('.name-input').val();
    let surname = $('.surname-input').val();
    let username = $('.username-input').val();
    let email = $('.email-input').val();
    let password = $('.password-input').val();
    let confirm_password = $('.confirm_password-input').val();

    let data = {
        'name': name,
        'surname': surname,
        'username': username,
        'email': email,
        'new_password': password,
        'confirm_password': confirm_password
    };
    let response = postAjaxInformation('/api/user/create', data);
    if (response.status_code != 200) {
        let errors_list = JSON.parse(JSON.parse(response.text).message);
        for (let i = 0; i < errors_list.length; i++) {
            if (errors_list[i] == null) {
                continue;
            }

            if (errors_list[i][0] == 'name') {
                addValidateMessage('.name-input', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'surname') {
                addValidateMessage('.surname-input', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'username') {
                addValidateMessage('.username-input', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'email') {
                addValidateMessage('.email-input', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'new_password') {
                addValidateMessage('.password-input', errors_list[i][1]);
            }

            if (errors_list[i][0] == 'confirm_password') {
                addValidateMessage('.confirm_password-input', errors_list[i][1]);
            }
        }
        return false;
    } else {
        $('.toast').stop().fadeIn(400).delay(3000).fadeOut(500);
        setTimeout(
            function () {
                window.location.assign("/")
            },
            2000
        );
        return false;
    }
});

$('.validate-form .input100').each(function () {
    $(this).focus(function () {
        hideValidate(this);
    });
});

function addValidateMessage(attr, message) {
    $(attr + '-div').attr('data-validate', message);
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