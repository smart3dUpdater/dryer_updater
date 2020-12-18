$("#update_btn").click(function() {
    $("#update_popup").toggleClass('l-overlay--visible');
    $.get( "/update").done(function( data ) {
        alert(data)
        $("#update_popup").toggleClass('l-overlay--visible');
    }).fail(function() {
        alert( "error" );
    })
})