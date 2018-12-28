$(".export-button").click(function (e) {
    let platform = $(this).data("platform");
    let lang = $(this).data("lang");

    $("#export-modal .modal-title").text(platform + " export");
    $("#export-text-area").val("Loading ...");

    let url = "/export?lang=" + lang + "&platform=" + platform;
    $.ajax({
        method: "GET",
        url: url
    }).done(function (msg) {
        $("#export-text-area").val(msg);
    });
});

$("#copy-translation-button").click(function (e) {
    //https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
    let textArea = $("#export-text-area");

    /* Select the text field */
    textArea.select();

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    showDefaultAlert("alert-success", "Translation copied.");
});
