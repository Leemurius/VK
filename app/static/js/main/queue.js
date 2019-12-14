$(document).ready(function (e) {
    updateQueue();
    updateReady();
});

setInterval(function() {
    updateQueue();
    printNextUser();
}, 2000);

function updateReady() {
    var status = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/self/get/status');
    if (status.substring(0, 5) == 'READY' || status.substring(0, 3) == 'NOT') {
        $("#checkbox").prop("checked", true);
    }
}

function updateQueue() {
    $('tbody tr').remove();
    var cur_username = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/self/username');

    var queue = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/get');
    for (let i = 0; i < queue.length; i++) {
        const row = queue[i];
        var block = $(
            '<tr className="row100 body">' +
            '<td class="cell100 column1">' + (i + 1).toString() + '</td>' +
            '<td class="cell100 column2">' + row['name_surname'] + '</td>' +
            '<td class="cell100 column3">' + row['lab_number'] + '</td>' +
            '<td class="cell100 column4"' +
                (row['is_next'] ? ' style="color: red;  font-weight: 700;"' : '') + '>'
                + row['status'] + '</td>' +
            '</tr>'
        );

        if (cur_username == row['username']) {
            block.css('background-color', '#aae9e8');
        }

        block.appendTo($('tbody'));
    }
}

$('.switch #checkbox').click(function (e) {
    const value = $('.switch input').is(":checked");
    const data = JSON.stringify({'status': value ? 'Ready' : 'Not ready'});
    postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/change/status', data);
});

$('.leave').click(function (e) {
    postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/delete/self/user')
});

function printNextUser() {
    var username = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/next');
    var cur_username = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/self/username');

    if (username == cur_username) {

        var status = getAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/self/get/status');
        if (status.substring(0, 10) == 'PROCESSING') {
            let result = confirm('Ты сдал?');
            if (result) {
                data = JSON.stringify({'status': 'Passed'});
                postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/change/status', data);
            } else {
                data = JSON.stringify({'status': 'Not passed'});
                postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/change/status', data);
            }
            $("#checkbox").prop("checked", false);
        }

        if (status.substring(0, 5) == 'READY') {
            let result = confirm('Ты готов идти сдавать?');
            if (result) {
                var data = JSON.stringify({'status': 'Processing'});
                postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/change/status', data);
            } else {
                var data = JSON.stringify({'status': 'Not ready'});
                postAjaxInformation(getProtocol() + '://' + getServerName() + '/api/queue/change/status', data);
            }
            $("#checkbox").prop("checked", false);
        }
    }
}