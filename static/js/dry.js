var finish_setted = false;

function set_temperature(temp) {
    $("#temp").text(temp + "°C")
}

function set_preasure(preassure) {
    $("#preassure").text(preassure)
}

function set_elapsed(time) {
    $("#elapsed").text(time)
}
function set_remaining(time) {
    $("#remaining").text(time)
}

function set_action(txt) {
    $("#action").text('elapsed time ' + txt)
}

$('#stop_dry').click( function() {
    $("#stop_dry_popup").toggleClass('l-overlay--visible');
})

$('#stop_no').click( function() {
    $("#stop_dry_popup").toggleClass('l-overlay--visible');
})

$("#stop_yes").click(function() {
    $.get( "/stop");
    window.location.href = '/'
})

$('#close_finished_popup').click(function() {
    window.location.href = '/'
})

function call_temp() {
    $.get( "/status").done(function( data ) {
        set_temperature(data['temp'])
        set_preasure(data['preassure'])
        set_elapsed(data['time_formated'])
        set_action(data['action'])
        set_remaining(data['remaining_time'])
        if(drying && !data['cycling'] && !finish_setted) {
            $("#dry_finished_popup").toggleClass('l-overlay--visible');
            finish_setted = true;
        }
    }).fail(function() {
        set_temperature('26')
    })
    setTimeout(call_temp, 2000)
}

call_temp()