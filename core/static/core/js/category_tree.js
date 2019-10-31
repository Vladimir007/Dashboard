jQuery(function () {
    let form_modal = $('#category_form_modal'),
        name_input = form_modal.find('#name_input');

    function serialize_data() {
        let name = name_input.val().trim();
        if (!name.length) return err_notify(PAGE_ERRORS.name);
        return {name: name};
    }

    function set_data(data) {
        name_input.val((data && data['name']) ? data['name'] : '');
    }

    let tree_obj = new MpttTree(
        $('#api_list_url').text(), serialize_data, set_data, form_modal, $('#remove_category_modal')
    );
    tree_obj.initialize($('#tree_container'));

    // Uploading file
    let upload_modal = $('#upload_categories_modal');
    activate_modal(upload_modal, false, 'fly up', '#upload_modal_show', function () {
        let data = get_file_data($('#categories_file_input'), PAGE_ERRORS.no_file),
            columns_value = $('#columns_value').val();
        if (!data) return false;

        if (!columns_value.length) return err_notify(PAGE_ERRORS.columns);
        data.append('columns', columns_value);

        upload_modal.modal('hide');
        upload_file($(this).data('url'), data, function () {
            window.location.replace('')
        });
    });
});
