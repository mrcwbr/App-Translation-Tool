//ADD
$("#component-add-button").click(function (e) {
    let name = $("#new-component-name").val();

    $.ajax({
        method: "POST",
        url: "/component",
        data: {name: name}
    }).done(function (msg) {
        if (msg.success === true) {
            $("#new-component-name").val("");
            let generated_id = msg.newComp.id;
            let generated_name = msg.newComp.name;

            let input = '<input class="form-control" type="text" value="' + generated_name + '" disabled="disabled">';

            $("#component-table-body tr:first").after('<tr><td>' + generated_id + '</td><td>' + input + '</td><td></td></tr>');

        } else alert("Component's name is shorter than 3 characters or already in usage.");
    });
});

//DELETE
$(".del-button").click(function (e) {
    let id = $(this).data("value");

    let check = confirm("Do you really want to delete the Component with the ID: " + id);
    if (check === true) {
        $.ajax({
            method: "DELETE",
            url: "/component",
            data: {id: id}
        }).done(function (msg) {
            $("#component-row-" + id).remove();
        });
    }
});

//EDIT (= Update Preparation)
$(".edit-button").click(function (e) {
    let id = $(this).data("value");

    $("#del-button-" + id).toggle();
    $("#com-button-" + id).toggle();

    let nameTF = $("#component-input-name-" + id);
    if (nameTF.attr("disabled") === 'disabled') nameTF.prop("disabled", false);
    else nameTF.prop("disabled", 'disabled');
});

//Update
$(".com-button").click(function (e) {
    let id = $(this).data("value");
    let nameTextField = $("#component-input-name-" + id);
    let name = nameTextField.val();

    $.ajax({
        method: "PUT",
        url: "/component",
        data: {name: name, id: id}
    }).done(function (msg) {
        if (msg.success === true) {
            nameTextField.val(msg.updateComp.name);
            nameTextField.prop("disabled", 'disabled');
            $("#del-button-" + id).toggle();
            $("#com-button-" + id).toggle();

            showDefaultAlert("alert-success", "Component successfully updated.");

        } else alert("Component's name is shorter than 3 characters or already in usage.");
    });
});