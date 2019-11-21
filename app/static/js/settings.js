$(document).ready(function() {
    addGeneralInformationInFields();
});

$('.choose-photo-link').on('click', function (e) {
    $('.choose-photo input').click();
});

$('.choose-photo input').bind('input',function (e) {
    var photo_path = $(this).val();
    if (photo_path.length > 40) {
        photo_path = photo_path.substring(0, 20) + '...' +
            photo_path.substring(photo_path.length - 10, photo_path.length);
    }
    $("#upload-file-info").html(photo_path);
});

function addGeneralInformationInFields() {
    const data = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/self/information');
    $('.name-field').val(data['name']);
    $('.surname').val(data['surname']);
    $('.username').val(data['username']);
    $('.age').val((data['age'] == 0 ? '' : data['age']));
    $('.email').val(data['email']);
    $('.address').val(data['address']);
}

$('.left-form').on('submit',function() {
    const name = $('.name-field').val();
    const surname = $('.surname').val();
    const username = $('.username').val();
    const age = $('.age').val();
    const email = $('.email').val();
    const address = $('.address').val();
    const data = JSON.stringify({
        'name': name,
        'surname': surname,
        'username': username,
        'age': Number.parseInt(age),
        'email': email,
        'address': address,
    });
    const file = $('.choose-photo input').prop('files')[0];

    var responseData = postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/self/update/information', data);
    var responsePhoto = postAjaxPhoto(getProtocol() + '://' + getServerName() + '/api/self/update/photo', file);
    if (responseData != true || responsePhoto != true) {
        if (responseData != true) {
            const errors_list = JSON.parse(JSON.parse(responseData).message);
            for (let i = 0; i < errors_list.length; i++) {
                if (errors_list[i] == null) {
                    continue;
                }

                if (errors_list[i][0] == 'name') {
                    addValidateMessage('.name-field', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'surname') {
                    addValidateMessage('.surname', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'username') {
                    addValidateMessage('.username', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'age') {
                    addValidateMessage('.age', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'email') {
                    addValidateMessage('.email', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'address') {
                    addValidateMessage('.address', errors_list[i][1]);
                }
            }
        }

        if (responsePhoto != true) {
            var error = JSON.parse(JSON.parse(responsePhoto).message);
            addValidateMessage('.photo-path', error);
        }
        return false;
    } else {
        return true;
    }
});

$('.right-form').on('submit',function() {
    const old_password = $('.old-password').val();
    const new_password = $('.new-password').val();
    const confirm_password = $('.confirm-password').val();
    const data = JSON.stringify({
        'old_password' : old_password,
        'new_password' : new_password,
        'confirm_password' : confirm_password
    });

    var response = postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/self/update/password', data);
    if (response != true) {
        const errors_list = JSON.parse(JSON.parse(response).message);
        for (let i = 0; i < errors_list.length; i++) {
            if (errors_list[i] == null) {
                continue;
            }

            if (errors_list[i][0] == 'old_password') {
                addValidateMessage('.old-password', errors_list[i][1]);
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
        return true;
    }
});

$('.input100').each(function() {
    $(this).focus(function(){
       hideValidate(this);
    });
});

function addValidateMessage(attr, message) {
    $(attr).parent().attr('data-validate', message);
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