function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie.length) {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$(document).on('change', '.btn-file :file', function () {
    let input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            let csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ajaxError(function (xhr, err) {
    $('#dimmer_of_page').removeClass('active');
    if (err['responseJSON']) {
        if (err['responseJSON'].error) err_notify(err['responseJSON'].error);
        else if (err['responseJSON'].detail) err_notify(err['responseJSON'].detail);
        else {
            if (Array.isArray(err['responseJSON'])) {
                let is_empty = true;
                $.each(err['responseJSON'], function (i, value) {
                    err_notify(value + '');
                    is_empty = false;
                });
                if (is_empty) err_notify($('#error__ajax_error').text());
            }
            else err_notify(err['responseJSON'] + '');
        }
    }
    else err_notify($('#error__ajax_error').text());
});

window.err_notify = function (message, duration) {
    let notify_opts = {autoHide: false, style: 'bootstrap', className: 'error'};
    if (!isNaN(duration)) {
        notify_opts['autoHide'] = true;
        notify_opts['autoHideDelay'] = duration;
    }
    $.notify(message, notify_opts);
    return false;
};

window.success_notify = function (message, duration) {
    if (isNaN(duration)) {
        duration = 2500;
    }
    $.notify(message, {
        autoHide: true,
        autoHideDelay: duration,
        style: 'bootstrap',
        className: 'success'
    });
};

window.activate_modal = function (modal_div, closable, transition, activator, on_confirm) {
    if (!modal_div.length) return false;

    let confirm_btn = modal_div.find('.modal-confirm'),
        cancel_btn = modal_div.find('.modal-cancel');
    modal_div.modal({closable: closable, transition: transition, autofocus: false});
    cancel_btn.click(function () {
        modal_div.modal('hide')
    });
    if (activator) {
        $(activator).click(function () {
            modal_div.modal('show')
        });
    }
    if (on_confirm) confirm_btn.click(on_confirm);
};

window.send_json = function(url, method, data, on_success, on_error) {
    $.ajax({
        url: url, method: method,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        crossDomain: false,
        success: on_success,
        error: on_error
    });
};

window.upload_file = function(url, data, on_success) {
    $('#dimmer_of_page').addClass('active');
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        contentType: false,
        processData: false,
        mimeType: 'multipart/form-data',
        xhr: function() {
            return $.ajaxSettings.xhr();
        },
        success: on_success
    });
};

window.get_file_data = function(input_obj, error_msg, key_name='file') {
    let files = input_obj[0].files;
    if (!files.length) return err_notify(error_msg);

    let data = new FormData();
    data.append(key_name, files[0]);
    return data;
};

$(document).ready(function () {
    $('.btn-file').each(function () {
        $(this).find("input[type='file']").on('fileselect', function () {
            if($(this)[0].files.length)
                $(this).parent().find('span.btn-file-name').text($(this)[0].files[0].name);
        });
    });
    $('.note-popup').popup();
});
