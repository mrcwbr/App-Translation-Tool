//ADD
$("#identifier-add-button").click(function (e) {
    let newIdentNameTF = $("#new-identifier-name");
    let newIdentCompSelect = $("#new-identifier-component");
    let newIdentDesTF = $("#new-identifier-description");

    let name = newIdentNameTF.val();
    let componentID = newIdentCompSelect.val();
    let description = newIdentDesTF.val();

    $.ajax({
        method: "POST",
        url: "/identifier",
        data: {name: name, componentID: componentID, description: description}
    }).done(function (data) {
        if (data.success === true) {
            newIdentNameTF.val("");
            newIdentCompSelect.val("");
            newIdentDesTF.val("");

            let generatedID = data.newIdent.id;
            let generatedName = data.newIdent.name;
            let generatedCompName = data.newIdent.componentName === null ? '' : data.newIdent.componentName;
            let generatedDec = data.newIdent.description === null ? '' : data.newIdent.description;

            let inputID = '<input class="form-control" type="text" value="' + generatedName + '" disabled="disabled">';
            let select = '<select class="form-control" disabled="disabled">\n' +
                '           <option selected>' + generatedCompName + '</option>' +
                '         </select>';
            let inputDesc = '<input class="form-control" type="text" value="' + generatedDec + '" disabled="disabled">';

            $("#identifier-table-body tr:first").after('<tr>' +
                '<td>' + generatedID + '</td>' +
                '<td>' + inputID + '</td>' +
                '<td>' + select + '</td>' +
                '<td>' + inputDesc + '</td>' +
                '<td></td>' +
                '</tr>');

            //TODO: Remove identifier from add-new-identifier-select
        } else alert(data.msg);
    });
});

//DELETE
$(".del-button").click(function (e) {
    let id = $(this).data("id");

    let check = confirm("Do you really want to delete the identifier with the ID: " + id);
    if (check === true) {
        $.ajax({
            method: "DELETE",
            url: "/identifier",
            data: {id: id}
        }).done(function (msg) {
            $("#identifier-row-" + id).remove();
        });
    }
});

//EDIT (= Update Preparation)
$(".edit-button").click(function (e) {
    let id = $(this).data("id");

    $("#del-button-" + id).toggle();
    $("#com-button-" + id).toggle();

    let nameTF = $("#name-input-" + id);
    if (nameTF.attr("disabled") === 'disabled') nameTF.prop("disabled", false);
    else nameTF.prop("disabled", 'disabled');

    let componentSelect = $("#component-select-" + id);
    if (componentSelect.attr("disabled") === 'disabled') componentSelect.prop("disabled", false);
    else componentSelect.prop("disabled", 'disabled');

    let descriptionTF = $("#description-input-" + id);
    if (descriptionTF.attr("disabled") === 'disabled') descriptionTF.prop("disabled", false);
    else descriptionTF.prop("disabled", 'disabled');
});

//Update
$(".com-button").click(function (e) {
    let id = $(this).data("id");

    let nameTF = $("#name-input-" + id);
    let componentSelect = $("#component-select-" + id);
    let descriptionTF = $("#description-input-" + id);

    let name = nameTF.val();
    let componentID = componentSelect.val();
    let description = descriptionTF.val();

    $.ajax({
        method: "PUT",
        url: "/identifier",
        data: {id: id, name: name, componentID: componentID, description: description}
    }).done(function (data) {
        if (data.success === true) {
            nameTF.val(data.updatedIdentifier.name);
            nameTF.prop("disabled", 'disabled');

            componentSelect.val(data.updatedIdentifier.componentID);
            componentSelect.prop("disabled", 'disabled');

            descriptionTF.val(data.updatedIdentifier.description);
            descriptionTF.prop("disabled", 'disabled');

            $("#del-button-" + id).toggle();
            $("#com-button-" + id).toggle();

            showDefaultAlert("alert-success", "Identifier successfully updated.");

        } else alert(data.msg);
    });
});