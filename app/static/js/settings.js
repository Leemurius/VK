$(document).ready(function() {
    addGeneralInformationInFields();

    // $('.input-file').click(function() {
    //     input = document.getElementById('photo');
    //     input.addEventListener('change', readSingleFile, false);
    //     input.click();
    // });
    //
    // function readSingleFile(evt) {
    //     var f = evt.target.files[0];
    //
    //     if (f) {
    //         $('.input-file__info').text(f.name);
    //
    //     } else {
    //         alert("Failed to load file");
    //     }
    // }
});

function addGeneralInformationInFields() {
    const data = getAjaxInformation('http://' + getIP() + '/api/self/information');
    $('.name').val(data['name']);
    $('.surname').val(data['surname']);
    $('.username').val(data['username']);
    $('.age').val(data['age']);
    $('.email').val(data['email']);
    $('.address').val(data['address']);
}

$('.save-information').click(function() {
    const name = $('.name').val();
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
        'address' : address,
        'photo' : 'none'
    });
    var response = postAjaxInformation('http://' + getIP() + '/api/self/update/information', data);
});


$('.save-password').click(function() {
    const old_password = $('.old-password').val();
    const new_password = $('.new-password').val();
    const confirm_password = $('.confirm-password').val();
    const data = JSON.stringify({
        'password' : new_password
    });
    var response = postAjaxInformation('http://' + getIP() + '/api/self/update/password', data);
});
