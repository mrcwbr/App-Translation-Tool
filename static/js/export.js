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