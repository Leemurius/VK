$('.btn').click(function (e) {
    var lab = $('select').find(':selected').data('id');
    var data = JSON.stringify({'lab_number': lab});
    var response = postAjaxInformation(getProtocol() + '://' + getServerName() + "/api/self/queue/add", data);

    if (response == true) {
        alert(response);
    } else {
        alert("Error: " + JSON.parse(JSON.parse(response).message))
    }
    window.location.assign(getProtocol() + '://' + getServerName() + "/queue");
});