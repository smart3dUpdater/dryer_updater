$('#wifi_connections').click(function(){
    $('#listed_wifi').toggleClass('l-overlay--visible');
    $.get("/get-wifi-connection").done(function (data) {
        var select = $("#wifi_list");
        select.empty();
        var selected = data.selected;
        var wifi_list = data.wifi_list;
        for (var i = 0; i < wifi_list.length; i++) {
            if(wifi_list[i] == selected) {
                var d = '<a class="l-overlay-form-list--item wifi_item" data-wifiname="' + wifi_list[i] + '">' + wifi_list[i] + '</a>'
            } else {
                var d = '<a class="l-overlay-form-list--item wifi_item" data-wifiname="' + wifi_list[i] + '">' + wifi_list[i] + '</a>'
            }
            select.append(d);
        }
        $('.wifi_item').click(function(){
            var wifiname = $(this).data('wifiname');
            $("#network_name").val(wifiname);
            $("#network_name_title").text(wifiname);
            $('#listed_wifi').toggleClass('l-overlay--visible');
            $('#password_popup').toggleClass('l-overlay--visible');
        })
    })
})

$('.e-btn-yes').click(function(){
    $('#password_popup').toggleClass('l-overlay--visible');
    $("#wait_fetching_modal").toggleClass("l-overlay--visible");
    var network_name = $("#network_name").val();
    var password = $("#keyboard").val();
    $.ajax({
        url: "/wifi-connection",
        method: "POST",
        data: {network_name: network_name, password: password},
        success: function (result) {
            if(network_name == result){
                $("#wait_fetching_modal").toggleClass("l-overlay--visible");
                $("#connection_ok_modal").toggleClass("l-overlay--visible");
            } else {
                $("#wait_fetching_modal").toggleClass("l-overlay--visible");
                $("#connection_no_ok_modal").toggleClass("l-overlay--visible");
            }
        }
    });
})

$('#disconnect').click(function(){
    $("#wait_fetching_modal").toggleClass("l-overlay--visible");
    $.get('/disconnect-wifi').done(function () {
        window.location.href = '/network'
    })
})

$('.e-btn-no').click(function(){
    $('#password_popup').toggleClass('l-overlay--visible');
})

$('#close_listed_wifi_popup').click(function(){
    $('#listed_wifi').toggleClass('l-overlay--visible');
})

$('#close_ok_popup').click(function(){
    window.location.href = '/network'
})

$('#close_no_ok_popup').click(function(){
    window.location.href = '/network'
})