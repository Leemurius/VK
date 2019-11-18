$('.validate-form').on('submit',function() {
    const name = $('.name-input').val();
    const surname = $('.surname-input').val();
    const username = $('.username-input').val();
    const email = $('.email-input').val();
    const password = $('.password-input').val();
    const confirm_password = $('.confirm_password-input').val();

    const data = JSON.stringify({
        'name': name,
        'surname': surname,
        'username': username,
        'email': email,
        'password' : password,
        'confirm_password': confirm_password
    });
    var response = postAjaxInformation('http://' + getServerName() + '/api/user/create', data);
    if (response != true) {
        const errors_list = JSON.parse(JSON.parse(response).message);
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

            if (errors_list[i][0] == 'password') {
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
                window.location.assign("http://" + getServerName() + "/")
            },
            3000
        );
        return false;
    }
});

$('.validate-form .input100').each(function() {
    $(this).focus(function(){
       hideValidate(this);
    });
});

function addValidateMessage(attr, message) {
    $(attr + '-div').attr('data-validate', message);
    showValidate($(attr));
}

function showValidate(input) {
    var thisAlert = $(input).parent();
    $(thisAlert).addClass('alert-validate');
}

function hideValidate(input) {
    var thisAlert = $(input).parent();
    $(thisAlert).removeClass('alert-validate');
}