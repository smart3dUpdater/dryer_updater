var materials = []
var colours = []
var densities = []
var diameters = []

function select_functionality(div_father, class_item, popup) {
    $(div_father).click(function() {
        $(popup).toggleClass('l-overlay--visible');
    })
    
    $(class_item).click(function() {
        var text = $(this).text()
        $(div_father + ' .l-form-element__text').text(text)
        $(popup).toggleClass('l-overlay--visible')
    })
}

select_functionality('#material', '.material_item', "#material_popup");
select_functionality('#colour', '.colour_item', "#colour_popup");
select_functionality('#density', '.density_item', "#density_popup");
select_functionality('#diameter', '.diameter_item', "#diameter_popup");

$('.custom_item').click(function() {    
    var id = $(this).parent().parent().parent().attr('id')
    $('#' + id).toggleClass('l-overlay--visible')
    $('#custom_popup').toggleClass('l-overlay--visible')
    $('#keyboard').attr('data-id', id.split('_')[0]);
})

$('.e-btn-yes').click(function() {
    var id = $('#keyboard').data( "id" )
    var data = $('#keyboard').val()
    $('#' + id + '_popup .l-overlay-form-list').append( '<a class="l-overlay-form-list--item density_item">' + data + '</a>' )
    $('#custom_popup').toggleClass('l-overlay--visible')
    
    if(id == "material") {
        materials.push(data)
    } else if (id == "colour") {
        colours.push(data)
    } else if (id == "density") {
        densities.push(data)
    } else if (id == "diameter") {
        diameters.push(data)
    }
})

$('.e-btn-no').click(function() {
    $('#custom_popup').toggleClass('l-overlay--visible')
})

$('#close_custom_popup').click(function() {
    $('#custom_popup').toggleClass('l-overlay--visible')
})

$('#save').click(function() {
    $.post('/save-data', JSON.stringify({ materials: materials, colours: colours, densities: densities, diameters: diameters }))
    window.location.href = '/load'
})