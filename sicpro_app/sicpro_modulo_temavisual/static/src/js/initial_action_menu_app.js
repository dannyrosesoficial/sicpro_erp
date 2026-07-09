odoo.define('sicpro_temavisual.action_menuapps', function (require) {
    'use strict';

    // console.log("sicpro_temavisual_menu_apps");

    // Se deshabilita que habrá el menu una sola vez y se cambia para que salga siempre
    // if(typeof(sessionStorage.abandonadoUnaVez) === 'undefined')
    // {
    //     sessionStorage.setItem('abandonadoUnaVez','false');
    // }
    //
    // if(typeof(sessionStorage.abiertoUnaVez) === 'undefined' || sessionStorage.getItem('abandonadoUnaVez') === "false")
    // {
    //     sessionStorage.setItem('abiertoUnaVez','true');
    // }

    var intervaloEsperaAccion;

    function checkLoadedItems() {
        if (sessionStorage.getItem('abiertoUnaVez') === "true") {
            if (0 != $('.o_menu_toggle svg').length && 0 != $('.dropdown-item.o_menu_brand').length) {
                sessionStorage.setItem('abiertoUnaVez','false');
                clearInterval(intervaloEsperaAccion);
                $('.o_menu_toggle svg').click();
                $('input.form-control').focus();
                $('#barra_superior').focus();
            }
        }
        return;
    }

    intervaloEsperaAccion = setInterval(checkLoadedItems,50);

});
