odoo.define('sicpro_modulo_temavisual.tema_clic', function (require) {
    'use strict';

    $(document).on("click", "#selector_imagen",  function (event) {
        if(event.delegateTarget.activeElement.localName != "a") {
            event.stopPropagation();
        }
        else
        {
            $('#barra_superior').removeClass("o_main_navbar_custom");
            $('.o_menu_systray').removeClass("o_menu_systray_custom");
            $('a.o_menu_brand').removeClass('o_hidden');
            $('div.o_menu_sections').removeClass('o_hidden');
            sessionStorage.setItem('abandonadoUnaVez','true');
        }
        
    });

    $(document).on("click", ".o_content",  function (event) {
        // console.log('o_content');
        if(event.delegateTarget.activeElement.localName == "body")
        {
            event.stopPropagation();
        }
    });

    // Probando
    // $(document).on("click", "#barra_superior.o_main_navbar_custom .o_menu_systray .dropdown-item",  function (event) {
    //     $('#barra_superior').removeClass("o_main_navbar_custom");
    //     $('.o_menu_systray').removeClass("o_menu_systray_custom");
    //     $('a.o_menu_brand').removeClass('o_hidden');
    //     $('div.o_menu_sections').removeClass('o_hidden');
    //     $('a.o_menu_toggle svg, a.o_menu_toggle .sicpro-return-icon').toggle();
    // });

    // $(document).on("click", "#barra_superior.o_main_navbar_custom .o_menu_systray .dropdown",  function (event) {
    //     if(event.delegateTarget.activeElement.localName != "body")
    //     {
    //         event.stopPropagation();
    //     }
    //     else{
    //         $('a.o_menu_brand').toggleClass('o_hidden');
    //         $('div.o_menu_sections').toggleClass('o_hidden');
    //         $('#barra_superior').toggleClass('o_main_navbar_custom'); 
    //         $('.o_menu_systray').toggleClass('o_menu_systray_custom');
    //         $('a.o_menu_toggle svg, a.o_menu_toggle .sicpro-return-icon').toggle();
    //     }
    // });

    $(document).on("click", "#barra_superior.o_main_navbar_custom",  function (event) {
        if(event.target === this)
        {
            event.stopPropagation();
        }
        else
        {
            $('#barra_superior').removeClass("o_main_navbar_custom");
            $('.o_menu_systray').removeClass("o_menu_systray_custom");
            $('a.o_menu_brand').removeClass('o_hidden');
            $('div.o_menu_sections').removeClass('o_hidden');
            $('a.o_menu_toggle svg, a.o_menu_toggle .sicpro-return-icon').toggle();
            sessionStorage.setItem('abandonadoUnaVez','true');
        }
    });

    $(document).on("click", ".dropdown-toggle.o-no-caret.o-dropdown--narrow[title=Actividades]",  function (event) {
        $('#barra_superior').removeClass("o_main_navbar_custom");
        $('.o_menu_systray').removeClass("o_menu_systray_custom");
        $('a.o_menu_brand').removeClass('o_hidden');
        $('div.o_menu_sections').removeClass('o_hidden');
        $('a.o_menu_toggle svg, a.o_menu_toggle .sicpro-return-icon').toggle();
        sessionStorage.setItem('abandonadoUnaVez','true');
    });

    // dropdown-toggle o-no-caret o-dropdown--narrow 

    // o_menu_systray o_menu_systray_custom

    $(document).on("click", "#barra_superior .o_app.o_menuitem",  function (event) {
        $('#barra_superior').removeClass("o_main_navbar_custom");
        $('.o_menu_systray').removeClass("o_menu_systray_custom");
        $('a.o_menu_brand').removeClass('o_hidden');
        $('div.o_menu_sections').removeClass('o_hidden');
        sessionStorage.setItem('abandonadoUnaVez','true');
    });

});
