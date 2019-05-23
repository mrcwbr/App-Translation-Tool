$("#add-language-button").click(function (e) {

    let langCode = $("#lang-code").val();
    let langName = $("#lang-name").val();
    let langImg = $("#lang-img").val();

    $.ajax({
        method: 'POST',
        url: '/language',
        data: {
            langCode: langCode,
            langName: langName,
            langImg: langImg
        }
    }).done(function () {
        window.location.href = "/";
    }).fail(function (data) {
        showDefaultAlert("alert-danger", data.responseJSON.msg);
    });
});