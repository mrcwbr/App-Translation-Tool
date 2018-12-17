function showDefaultAlert(className, msg) {
    $("#main-alert").addClass(className);
    $("#main-alert-text").text(msg);

    //TODO: wird nicht automatsich ausgeblendet
    $("#main-alert").fadeTo(2000, 500).slideUp(500, function () {
        $("#main-alert").slideUp(500);
    });
}