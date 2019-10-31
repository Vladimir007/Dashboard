jQuery(function () {
    let form_modal = $('#action_form_modal'),
        phrases_input = form_modal.find('#phrases_list');

    function serialize_data() {
        let phrases = [];
        $.each(phrases_input.val().split(/\n/), function (i, value) {
            value = value.trim();
            if (value) phrases.push(value)
        });
        if (!phrases.length) return err_notify(PAGE_ERRORS.phrases);

        return {phrases: phrases};
    }

    function set_data(data) {
        let phrases_str = '';
        if (data && data['phrases']) phrases_str = data['phrases'].join('\n');
        phrases_input.val(phrases_str);
    }

    let tree_obj = new MpttTree(
        $('#api_list_url').text(), serialize_data, set_data, form_modal, $('#remove_action_modal')
    );
    tree_obj.initialize($('#tree_container'));

    // Uploading file
    let upload_modal = $('#upload_actions_modal');
    activate_modal(upload_modal, false, 'fly up', '#upload_modal_show', function () {
        let data = get_file_data($('#actions_file_input'), PAGE_ERRORS.no_file);
        if (!data) return false;

        upload_modal.modal('hide');
        upload_file($(this).data('url'), data, function () {
            window.location.replace('')
        });
    });
});
