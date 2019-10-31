jQuery(function () {
    let form_modal = $('#unit_form_modal'),
        names_list = form_modal.find('#names_list');

    function serialize_data() {
        let names = [];
        $.each(names_list.val().split(/\n/), function (i, value) {
            value = value.trim();
            if (value) names.push(value)
        });
        if (!names.length) return err_notify(PAGE_ERRORS.names);

        return {names: names};
    }

    function set_data(data) {
        let names_str = '';
        if (data && data['names']) names_str = data['names'].join('\n');
        names_list.val(names_str);
    }

    let tree_obj = new MpttTree(
        $('#api_list_url').text(), serialize_data, set_data, form_modal, $('#remove_unit_modal')
    );
    tree_obj.initialize($('#tree_container'));

    // Uploading file
    let upload_modal = $('#upload_units_modal');
    activate_modal(upload_modal, false, 'fly up', '#upload_modal_show', function () {
        let data = get_file_data($('#units_file_input'), PAGE_ERRORS.no_file);
        if (!data) return false;

        upload_modal.modal('hide');
        upload_file($(this).data('url'), data, function () {
            window.location.replace('')
        });
    });
});
