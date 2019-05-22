// language=JQuery-CSS
$('#init-submit-button').click(function (e) {
    e.preventDefault();

    let projectName = $('#project-name').val();
    let absDBPath = $('#database-path').val();

    let langCode = $('#lang-code').val();
    let langName = $('#lang-name').val();
    let langImg = $('#lang-img').val();


    if(projectName === "") {
        $('#project-name').addClass('is-invalid');
        return
    }
    else $('#project-name').removeClass('is-invalid');

    if(absDBPath.length < 3 || absDBPath.charAt(0) !== "/" || absDBPath.slice(-1) !== "/") {
        $('#database-path').addClass('is-invalid');
        return
    }
    else $('#database-path').removeClass('is-invalid');

    $.ajax({
        method: 'POST',
        url: '/init',
        data: {
            projectName: projectName,
            absDBPath: absDBPath,
            langCode: langCode,
            langName: langName,
            langImg: langImg
        }
    }).done(function (data, statusText, xhr) {
        if(xhr.status == 204){
            window.location.href = "/";
        }
    });
});