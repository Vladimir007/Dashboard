function MpttTree(list_url, serialize_data, set_data, form_modal, destroy_modal) {
    this.list_url = list_url;
    this.serialize_data = serialize_data;
    this.set_data = set_data;
    this.form_modal = form_modal;
    this.destroy_modal = destroy_modal;

    this.api_parent = null;
    this.api_url = null;
    this.api_method = null;

    return this;
}

MpttTree.prototype.initialize = function(container) {
    let instance = this;

    // Activate form modal
    activate_modal(instance.form_modal, false, 'fade', null, function () {
        let data = instance.serialize_data();
        if (!data) return false;
        data['parent'] = instance.api_parent;
        send_json(instance.api_url, instance.api_method, data, function () {
            window.location.replace('')
        });
    });

    // Activate destroy modal
    activate_modal(instance.destroy_modal, false, 'fly up', null, function () {
        instance.destroy_modal.modal('hide');
        $('#dimmer_of_page').addClass('active');
        $.ajax({
            url: instance.api_url, method: 'DELETE',
            success: function () {
                window.location.replace('')
            },
            error: function () {
                $('#dimmer_of_page').removeClass('active')
            }
        });
    });

    // Activate root items
    instance.activate_children(container);
};

MpttTree.prototype.activate_children = function(container) {
    let instance = this;

    container.find('.note-popup').popup();

    container.find('.remove-item').click(function () {
        instance.api_url = $(this).data('url');
        instance.destroy_modal.modal('show');
    });

    container.find('.add-item').click(function () {
        instance.api_parent = $(this).data('parent');
        instance.api_url = instance.list_url;
        instance.api_method = 'POST';
        instance.set_data(null);
        instance.form_modal.modal('show');
    });

    container.find('.edit-item').click(function () {
        instance.api_parent = null;
        instance.api_url = $(this).data('url');
        instance.api_method = 'PUT';
        $.get(instance.api_url, {}, function (resp) {
            instance.set_data(resp);

            instance.form_modal.modal('show');
        });
    });

    container.find('.show-children').click(function () {
        let icon_obj = $(this),
            list_container = icon_obj.closest('.item').find('.list').first();
        if (icon_obj.hasClass('right')) {
            $.get(icon_obj.data('url'), {}, function (resp) {
                icon_obj.toggleClass("right down");
                list_container.html(resp);
                instance.activate_children(list_container);
                list_container.show();
            })
        }
        else {
            icon_obj.toggleClass("right down");
            list_container.empty();
            list_container.hide();
        }
    });
};
