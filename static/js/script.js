var LS_KEY_WORDS = "kantrael.sitespellingchecker.allowedwords";
var MIN_PAGES = 1;
var MAX_PAGES = 300;

$(document).ready(function() {
    $('#buttonCheck').click(function(e) {
        e.preventDefault();
        $('#loading-indicator').show();

        var allowedWords = supportsHtml5Storage() ? localStorage.getItem(LS_KEY_WORDS) : null;
        $.ajax({
            type: 'POST',
            url: '/check',
            data: {
                inputUrl: $('#inputUrl').val(),
                maxPages: $('#maxPages').val(),
                allowedWords: allowedWords
            },
            success: function(response) {
                $('#loading-indicator').hide();
                var responseJson = JSON.parse(response);

                if (responseJson.error) {
                    alert("URL is incorrect or website is unavailable.");
                    return;
                }

                if (responseJson.length == 0) {
                    showGoodResult();
                } else {
                    showMisspells(responseJson);
                }
            },
            error: function(error) {
                $('#loading-indicator').hide();
                alert("Can not make request to this URL.");
            }
        });
    });

    $("#maxPages").bind("change paste keyup", function() {
        var value = $(this).val();
        if (value) {
            value =  Math.max(value, MIN_PAGES);
            value =  Math.min(value, MAX_PAGES);
            $(this).val(value);
        }
    });

    $('#btnApplyDictionary').click(function(e) {
        if (supportsHtml5Storage()) {
            localStorage.setItem(LS_KEY_WORDS, $("#allowedWords").val());
        }
    });

    $('#btnClearDictionary').click(function(e) {
        $("#allowedWords").val("");
    });

    $('#btnOpenDictionary').click(function(e) {
        if (supportsHtml5Storage()) {
            var allowedWords = localStorage.getItem(LS_KEY_WORDS);
            if (allowedWords) {
                $("#allowedWords").val(allowedWords);
            }
        }
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
        } else {
            // collapse the panel
            $(this).parents('.panel').find('.panel-body').slideUp();
            $(this).addClass('panel-collapsed');
            $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        }
    }
});

function supportsHtml5Storage() {
    try {
        return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
        return false;
    }
}

function showGoodResult() {
    var contentContainer = $('#contentContainer');
    contentContainer.empty();
    contentContainer.append(document.querySelector('#misspells-search-results-template').innerHTML);
    contentContainer.append(document.querySelector('#good-result-template').innerHTML);
}

function showMisspells(responseJson) {
    var contentContainer = $('#contentContainer');
    contentContainer.empty();
    var html = "";
    for (var i = 0; i < responseJson.length; i++) {
        var page = responseJson[i];
        var misspells = page["misspells"];

        var pageHtml = document.querySelector('#page-template').innerHTML;
        pageHtml = pageHtml.replace(/\{PAGE_TITLE\}/, page["title"]);
        pageHtml = pageHtml.replace(/\{PAGE_URL\}/g, page["url"]);

        var misspellsCount = 0;
        var misspellsHtml = "";
        for (var word in misspells) {
            if (misspells.hasOwnProperty(word)) {
                var wordHtml = document.querySelector('#misspell-template').innerHTML;
                wordHtml = wordHtml.replace(/\{WORD\}/, word);
                wordHtml = wordHtml.replace(/\{COUNT\}/, misspells[word]);

                misspellsHtml += wordHtml + "\n";
                misspellsCount++;
            }
        }
        pageHtml = pageHtml.replace(/\{MISSPELLS\}/, "" + misspellsHtml);
        pageHtml = pageHtml.replace(/\{MISSPELLS_COUNT\}/, "" + misspellsCount);
        html += pageHtml + "\n\n";
    }
    contentContainer.append(document.querySelector('#misspells-search-results-template').innerHTML);
    contentContainer.append(html);
}