$(document).ready(function () {
    _initSettings();
});

function _initSettings() {
    addGeneralInformationInFields();
    replaceStateInHistory({'title': document.title}, window.location.href);
}

$('.additional_page').on('click', '.choose-photo-link', function (event) {
    $('.choose-photo input').click();
});

$('.choose-photo input').change(function (e) {
    let photo_path = this.files[0].name;
    if (photo_path.length > 40) {
        photo_path = photo_path.substring(0, 20) + '...' +
            photo_path.substring(photo_path.length - 10, photo_path.length);
    }
    $("#upload-file-info").html(photo_path);
});

function addGeneralInformationInFields() {
    $('.name-field').val(me['name']);
    $('.surname').val(me['surname']);
    $('.username').val(me['username']);
    $('.age').val((me['age'] == 0 ? '' : me['age']));
    $('.email').val(me['email']);
    $('.address').val(me['address']);
}


// PROFILE INFORMATION SETTINGS ------------------------------------------------


$('.left-form').on('submit', function () {
    let name = $('.name-field').val();
    let surname = $('.surname').val();
    let username = $('.username').val();
    let age = $('.age').val();
    let email = $('.email').val();
    let address = $('.address').val();
    let infData = {
        'user_id': me['id'],
        'name': name,
        'surname': surname,
        'username': username,
        'age': Number.parseInt(age),
        'email': email,
        'address': address,
    };
    let photoData = {
        'user_id': me['id'],
        'photo': $('.choose-photo input').prop('files')[0],
    };

    let responseData = postAjaxInformation('/api/user/setInformation', infData);

    // Not required field
    let responsePhoto = {'status_code': 200};
    if (photoData.photo !== undefined && responseData.status_code == 200) {
        responsePhoto = postAjaxPhoto('/api/user/setPhoto', photoData);
    }

    if (responseData.status_code != 200 || responsePhoto.status_code != 200) {
        if (responseData.status_code != 200) {
            let errors_list = JSON.parse(JSON.parse(responseData.text).message);
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

        if (responsePhoto.status_code != 200) {
            let errors_list = JSON.parse(JSON.parse(responsePhoto.text).message);
            for (let i = 0; i < errors_list.length; i++) {
                if (errors_list[i] == null) {
                    continue;
                }

                if (errors_list[i][0] == 'photo') {
                    addValidateMessage('.photo-path', errors_list[i][1]);
                }

                if (errors_list[i][0] == 'user_id') {
                    alert('Oooops. Something went wrong.');
                }
            }
        }
        return false;
    } else {
        return true;
    }
});


// PASSWORD SETTINGS -----------------------------------------------------------


$('.right-form').on('submit', function () {
    let old_password = $('.old-password').val();
    let new_password = $('.new-password').val();
    let confirm_password = $('.confirm-password').val();
    let data = {
        'old_password': old_password,
        'new_password': new_password,
        'confirm_password': confirm_password
    };

    let response = postAjaxInformation('/api/user/setPassword', data);
    if (response.status_code != 200) {
        let errors_list = JSON.parse(JSON.parse(response.text).message);
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