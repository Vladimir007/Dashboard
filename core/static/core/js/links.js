function LinksTree(container, error_not_selected, error_too_many) {
    this.container = container;
    this.errors = {not_selected: error_not_selected, too_many: error_too_many};
    this.activate_children(this.container);
    return this;
}

LinksTree.prototype.get_selected = function() {
    let checkbox_selector = this.container.find('input[type="checkbox"]:checked');
    switch (checkbox_selector.length) {
        case 0:
            return err_notify(this.errors.not_selected);
        case 1:
            break;
        default:
            return err_notify(this.errors.too_many);
    }
    return checkbox_selector.val();
};

LinksTree.prototype.activate_children = function(container) {
    let instance = this;

    container.find('.ui.checkbox').checkbox();

    container.find('.show-children').click(function () {
        let icon_obj = $(this),
            list_container = icon_obj.closest('.item').find('.list').first();
        if (icon_obj.hasClass('right')) {
            console.log('Open!')
            $.get(icon_obj.data('url'), {}, function (resp) {
                icon_obj.toggleClass("right down");
                list_container.html(resp);
                instance.activate_children(list_container);
                list_container.show();
            })
        }
        else {
            console.log('Close!')
            icon_obj.toggleClass("right down");
            list_container.empty();
            list_container.hide();
        }
    });
};

jQuery(function () {
    let actions_processor = new LinksTree(
        $('#actions_tree'), PAGE_ERRORS.action_not_selected, PAGE_ERRORS.action_too_many
    );
    let units_processor = new LinksTree(
        $('#units_tree'), PAGE_ERRORS.unit_not_selected, PAGE_ERRORS.unit_too_many
    );
    let categories_processor = new LinksTree(
        $('#categories_tree'), PAGE_ERRORS.category_not_selected, PAGE_ERRORS.category_too_many
    );

    function get_triple_value() {
        let data = {
            action: actions_processor.get_selected(),
            unit: units_processor.get_selected(),
            category: categories_processor.get_selected(),
        };
        if (!data.action || !data.unit || ! data.category) return false;
        return data;
    }

    $('#create_link_button').click(function () {
        let data = get_triple_value();
        if (data) {
            $.post($(this).data('url'), data, function () {
                success_notify('Saved!')
            })
        }
    });

    $('#remove_link_button').click(function () {
        let data = get_triple_value();
        if (data) {
            $.ajax({
                url: $(this).data('url'),
                method: 'DELETE',
                data: data,
                success: function () {
                    success_notify('Link was deleted!')
                }
            });
        }
    });

    $('#check_link_button').click(function () {
        let data = get_triple_value();
        if (data) {
            $.get($(this).data('url'), data, function (resp) {
                resp.exists ? success_notify('The link exists!') : err_notify('The link was not found!')
            })
        }
    });

});