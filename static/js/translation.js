//ADD
$("#translation-add-button").click(function (e) {
    let translationStringTF = $("#new-translation-string");
    let identIDSelect = $("#new-ident-id");


    let translationString = translationStringTF.val();
    let identifierID = identIDSelect.val();
    let langCode = $("#lang-code-helper").html();

    $.ajax({
        method: "POST",
        url: "/translation",
        data: {translationString: translationString, identifierID: identifierID, langCode: langCode}
    }).done(function (data) {
        if (data.success === true) {
            console.log(data);
            translationStringTF.val("");
            identIDSelect.val("");

            let generatedID = data.newTrans.id;
            let text = data.newTrans.text;
            let timestamp = data.newTrans.timestamp;
            let identifier = data.newTrans.identifier;

            let select = '<select class="form-control" disabled="disabled">\n' +
                '           <option selected>' + identifier + '</option>' +
                '         </select>';
            let textTF = '<input class="form-control" type="text" value="' + text + '" disabled="disabled">';

            $("#translation-table-body tr:first").after('<tr>' +
                '<td>' + generatedID + '</td>' +
                '<td>' + timestamp + '</td>' +
                '<td>' + select + '</td>' +
                '<td>' + textTF + '</td>' +
                '<td></td>' +
                '</tr>');
        } else alert(data.msg);
    });
});

//DELETE
$(".del-button").click(function (e) {
    let id = $(this).data("value");

    let check = confirm("Do you really want to delete the translation with the ID: " + id);
    if (check === true) {
        $.ajax({
            method: "DELETE",
            url: "/translation",
            data: {id: id}
        }).done(function (msg) {
            $("#translation-row-" + id).remove();
        });
    }
});