function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    m = checkTime(m);
    $('#current_day').text(today.toLocaleString('en-us', { month: 'short' }) + ' ' + today.getDate())
    $('#currentTime').text( h + ":" + m)
    setTimeout(startTime, 1000);
}

function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}

function conectivity_status() {
    $.get( "/general-status").done(function( data ) {
        if(data['conn'] == 'wlan') {
            $("#connectivity").attr("src", "/icons/icon-wifi-01.svg");
        } else if(data['conn'] == 'eth'){
            $("#connectivity").attr("src", "/icons/icon_ethernet-on.svg");
        } else {
            $("#connectivity").attr("src", "/icons/icon_ethernet-off.svg");
        }
        if(data['door'] == "1") {
            $("#door").attr("src", "/icons/icon_lock-on.svg");
        } else {
            $("#door").attr("src", "/icons/icon_lock-off.svg");
        }
    })
    setTimeout(conectivity_status, 2000)
}

conectivity_status()

startTime()