
function format_pressure(pressure) {
    return parseInt(pressure.slice(0, -2))
}

function set_functionality(div_parent) {    
    $(div_parent).click(function() {
        $('.e-info-message__text').text('')
        $(div_parent + "_popup").toggleClass('l-overlay--visible');
    })
    $(div_parent + "_no").click(function() {
        $(div_parent + "_popup").toggleClass('l-overlay--visible');
    })
    $(div_parent + "_confirm").click(function() {
        var name = div_parent.split('#')[1]
        if(name == "material"){
            var data = $('#keyboard').val()
        } else {
            var data = $(div_parent + '_keyboard').val()
        }
        if (validations(name, data)) {
            $(div_parent).children('.l-form-element__text__custom').text(format_data(name, data))
            $(div_parent + "_popup").toggleClass('l-overlay--visible');
        }
    })
}

function validations(name, data) {
    if (name == 'material') {
        if (data.length > 20) {
            $('.e-info-message__text').text(name + ' must be lower of 20 characters')
            return false
        } else {
            return true
        }
    } else if (name == 'pressure') {
        if (!isNaN(data) && parseInt(data) > 300 && data.toString().indexOf('.') == -1) {
            return true
        } else {
            $('.e-info-message__text').text(name + ' must be up to 300 and without decimals')
            return false
        }
    } else if (name == 'temperature') {
        if (!isNaN(data) && (parseInt(data) <= 80 && parseInt(data) > 30) && data.toString().indexOf('.') == -1) {
            return true
        } else {
            $('.e-info-message__text').text(name + ' must be between 30 and 80 and without decimals')
            return false
        }
    } else {
        if (!isNaN(data) && parseInt(data) > 0 && data.toString().indexOf('.') == -1) {
            return true
        } else {
            $('.e-info-message__text').text(name + ' must be a number and without decimals')
            return false
        }
    }
}

function format_data(name, data) {
    if (name == 'pressure') {
        return data + 'mb'
    } else if (name == 'duration') {
        return data + "'"
    } else if (name == 'temperature') {
        return data + '°C'
    } else if (name == 'preheating') {
        return data + "'"
    } else {
        return data
    }
}

set_functionality('#material')
set_functionality('#pressure')
set_functionality('#duration')
set_functionality('#temperature')
set_functionality('#preheating')
set_functionality('#subcicles')

$('#save').click(function () {
    var url = '/save-custom-program';
    if(program == 'edit') {
        url = '/edit-program/' + id_edit;
    }
    $.post(url, JSON.stringify({ 
        name: $('#material').children('.l-form-element__text__custom').text(), 
        pressure: format_pressure($('#pressure').children('.l-form-element__text__custom').text()), 
        duration: parseInt($('#duration').children('.l-form-element__text__custom').text()), 
        temperature: parseInt($('#temperature').children('.l-form-element__text__custom').text()), 
        preheating: parseInt($('#preheating').children('.l-form-element__text__custom').text()), 
        subcicles: parseInt($('#subcicles').children('.l-form-element__text__custom').text())
    }))
    window.location.href = '/drying-programs'
})

$('#activate').click(function () {
    var url = '/activate';
    if(program == 'edit') {
        url = '/activate/' + id_edit;
    }
    $.post(url, JSON.stringify({ 
        name: $('#material').children('.l-form-element__text__custom').text(), 
        pressure: format_pressure($('#pressure').children('.l-form-element__text__custom').text()), 
        duration: parseInt($('#duration').children('.l-form-element__text__custom').text()), 
        temperature: parseInt($('#temperature').children('.l-form-element__text__custom').text()), 
        preheating: parseInt($('#preheating').children('.l-form-element__text__custom').text()), 
        subcicles: parseInt($('#subcicles').children('.l-form-element__text__custom').text())
    }))
    window.location.href = '/drying-programs'
})

$('.e-btn-no').click(function () {
    $('#custom_popup').toggleClass('l-overlay--visible');
})

$('#close_custom_popup').click(function () {
    $('#custom_popup').toggleClass('l-overlay--visible');
})