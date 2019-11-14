$('.btn').click(function (e) {
    var lab = $('select').find(':selected').data('id');
    var data = JSON.stringify({'lab_number': lab});
    postAjaxInformation("http://" + getIP() + "/api/self/queue/add", data);
    window.location.assign("http://" + getIP() + "/queue");
});