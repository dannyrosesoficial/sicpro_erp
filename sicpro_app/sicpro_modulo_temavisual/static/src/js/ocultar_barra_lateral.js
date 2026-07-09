odoo.define('sicpro_modulo_temavisual.ocultar_barra_lateral', function (require) {
    'use strict';

    if(typeof(localStorage.barra_lateral) == 'undefined')
    {
        localStorage.barra_lateral = true;
    }

    var intervaloEsperaBarra;

    function checkLoaded() {
        if(localStorage.barra_lateral === "true")
        {
            $('.sidebar_panel').show();
            $('.o_action_manager').css({'margin-left': '50px'});
        }
        else{
            $('.sidebar_panel').hide();
            $('.o_action_manager').css({'margin-left': '0px'});
        }

        return;
    }

    intervaloEsperaBarra = setInterval(checkLoaded,100);

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


});
