$(document).ready(function() {
    $('#buttonCheck').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/check',
            data: {inputUrl: $('#inputUrl').val()},
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.panel-heading.clickable').on("click", function (e) {
        if (!$(e.target).is("a")) {
            // change panel state if clicked element not a link
            if ($(this).hasClass('panel-collapsed')) {
                // expand the panel
                $(this).parents('.panel').find('.panel-body').slideDown();
                $(this).removeClass('panel-collapsed');
                $(this).find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
            }
            else {
                // collapse the panel
                $(this).parents('.panel').find('.panel-body').slideUp();
                $(this).addClass('panel-collapsed');
                $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
            }
        }

    });
});
