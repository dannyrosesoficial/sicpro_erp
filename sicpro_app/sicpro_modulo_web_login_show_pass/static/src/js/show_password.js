$(document).ready(function() {
    // por defecto al cargar la pagina desactivo la opción de visualizar la contraseña
    document.getElementById("ver_pass_login").checked = "";

    $(ver_pass_login).on('click', function () {
        if (document.getElementById('ver_pass_login').checked)
            {
            document.getElementById("password").type = "text";
        } else {
            document.getElementById("password").type = "password";
        }
    });
});
