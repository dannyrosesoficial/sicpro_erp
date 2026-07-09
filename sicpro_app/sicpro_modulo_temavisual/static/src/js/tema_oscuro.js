odoo.define('sicpro_modulo_temavisual.tema_oscuro', function (require) {
    'use strict';


    if(typeof(localStorage.darkMode) == 'undefined')
    {
        localStorage.darkMode = false;
    }

    if(localStorage.darkMode === "true")
    {
        document.documentElement.setAttribute("dark-mode","");
    }

    $(document).on("click", ".o_modo_oscuro_menu .fa-moon-o, .o_modo_oscuro_menu .fa-sun-o",  function (event) {
        $('.oh_dashboards').removeClass('observed');
        waitElementRecursive();
        let valor = true;
        if(localStorage.darkMode !== 'false')
        {
            valor = false;
        }
        localStorage.setItem("darkMode",valor);
        document.documentElement.toggleAttribute("dark-mode");
        $('.o_modo_oscuro_menu .fa-moon-o, .o_modo_oscuro_menu .fa-sun-o').toggle();
    });

    var intervaloEspera;

    function checkLoaded() {
        if (0 != $('.o_modo_oscuro_menu .fa-moon-o').length) {
            clearInterval(intervaloEspera);
            if(localStorage.darkMode === "true")
            {
                document.documentElement.setAttribute("dark-mode","");
                $('.o_modo_oscuro_menu .fa-moon-o').show();
                $('.o_modo_oscuro_menu .fa-sun-o').hide();
            }
            else{
                $('.o_modo_oscuro_menu .fa-moon-o').hide();
                $('.o_modo_oscuro_menu .fa-sun-o').show();
            }
        }
        return;
    }


    intervaloEspera = setInterval(checkLoaded,100);

    function waitElement(selector){
        return new Promise(resolve => {
            if(document.querySelector(selector)){
                return resolve(document.querySelector(selector));
            }

            const observer = new MutationObserver(mutations => {
                if(document.querySelector(selector)){
                    resolve(document.querySelector(selector));
                }
            });

            let lol = {
                childList: true,
                subtree: true
            };

            observer.observe(document,lol);
        });
    }

    function waitElementRecursive(){
        waitElement('.oh_dashboards:not(.oh_dashboards.observed)').then(function(elemento) {
            elemento.classList.add('observed');
            if($('html[dark-mode]')[0])
            {
                $('.o_content')[0].style.cssText = 'background-color: ' + $('.oh_dashboards').css('background-color') +' !important;';
            }
            waitElementRecursive();
        });
    }

    waitElementRecursive();

});
