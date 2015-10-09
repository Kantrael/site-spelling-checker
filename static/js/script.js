$(document).ready(function() {
    $('#buttonCheck').click(function(e) {
        e.preventDefault();
        $('#loading-indicator').show();
        $.ajax({
            type: 'POST',
            url: '/check',
            data: {inputUrl: $('#inputUrl').val()},
            success: function(response) {
                $('#loading-indicator').hide();
                var responseJson = JSON.parse(response);
                if (responseJson.error == true) {
                    alert("URL is incorrect or website is unavailable.");
                } else if (responseJson.length == 0) {
                    console.log("No errors found");
                    $('#contentContainer').empty();
                    var resultHeaderTemplate = document.querySelector('#misspells-search-results-template').innerHTML;
                    var goodResultTemplate = document.querySelector('#good-result-template').innerHTML;
                    $('#contentContainer').append(resultHeaderTemplate);
                    $('#contentContainer').append(goodResultTemplate);
                } else {
                    // TODO: Show pages with misspells
                    $('#contentContainer').empty();

                    var resultHeaderTemplate = document.querySelector('#misspells-search-results-template').innerHTML;
                    var pageTemplate = document.querySelector('#page-template').innerHTML;
                    var misspellTemplate = document.querySelector('#misspell-template').innerHTML;

                    var html = "";

                    for (var i = 0; i < responseJson.length; i++) {
                        var page = responseJson[i];
                        var misspells = page["misspells"];

                        var pageHtml = pageTemplate;
                        pageHtml = pageHtml.replace(/\{PAGE_TITLE\}/, page["title"]);
                        pageHtml = pageHtml.replace(/\{PAGE_URL\}/g, page["url"]);

                        var misspellsCount = 0;
                        var misspellsHtml = "";
                        for (var word in misspells) {
                            if (misspells.hasOwnProperty(word)) {
                                var wordHtml = misspellTemplate.replace(/\{WORD\}/, word);
                                wordHtml = wordHtml.replace(/\{COUNT\}/, misspells[word]);
                                misspellsHtml += wordHtml + "\n";
                                misspellsCount++;
                            }
                        }

                        pageHtml = pageHtml.replace(/\{MISSPELLS\}/, "" + misspellsHtml);
                        pageHtml = pageHtml.replace(/\{MISSPELLS_COUNT\}/, "" + misspellsCount);
                        html += pageHtml + "\n\n";
                    }

                    $('#contentContainer').append(resultHeaderTemplate);
                    $('#contentContainer').append(html);
                }
            },
            error: function(error) {
                $('#loading-indicator').hide();
                alert("Can not make request to this URL.");
            }
        });
    });
});

$(document).on('click', '.panel-heading.clickable', function(e){
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