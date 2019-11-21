$(document).ready(function (e) {
    updateQueue();
});

setInterval(function() {
    updateQueue();
    printNextUser();
}, 5000);

function updateQueue() {
    $('tbody tr').remove();

    var queue = getAjaxInformation('http://' + getServerName() + '/api/queue/get');
    for (let i = 0; i < queue.length; i++) {
        const row = queue[i];
        $(  '<tr>' +
                '<th class="number" scope="row">' + row['number'] + '</th> ' +
                '<td class="name_surname">' + row['name_surname'] + '</td>' +
                '<td class="lab_number">' + row['lab_number'] + '</td>' +
                '<td class="status">' + row['status'] + '</td>' +
            '</tr>'
        ).appendTo($('tbody'))
    }
}

$('.switch input').click(function (e) {
    const value = $('.switch input').is(":checked");
    const data = JSON.stringify({'status': value ? 'Ready' : 'Not ready'});
    postAjaxInformation('http://' + getServerName() + '/api/queue/change/status', data);
});

function printNextUser() {
    var username = getAjaxInformation('http://' + getServerName() + '/api/queue/next');
    var cur_username = getAjaxInformation('http://' + getServerName() + '/api/self/username');
    if (username == cur_username) {
        //let result = confirm('Are you ready?');
        if (result) {

        } else {

        }
    }
}