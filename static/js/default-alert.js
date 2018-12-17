function showDefaultAlert(className, msg) {
    $("#main-alert").removeClass();
    $("#main-alert").addClass('alert ' + className);
    $("#main-alert-text").text(msg);

    //Hide Alert after 3 sec
    $("#main-alert").fadeIn("fast", function(){
        setTimeout(function(){ $("#main-alert").fadeOut(); }, 3000);
    });
}