# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Tema Visual',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Opciones del tema visual',
    'description': 'Este módulo ofrece un diseño compatible con dispositivos '
                   'móviles para SICPRO ERP. Además, permite al usuario definir'
                   ' algunas preferencias de diseño.',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'sicpro_app_administracion',
        'sicpro_modulo_tema_agrupar',
        'sicpro_modulo_tema_chatter',
        'sicpro_modulo_tema_dialogos',
        'sicpro_modulo_tema_barra',
        'sicpro_modulo_tema_colores',
        'sicpro_modulo_tema_auto_actualizar',
        'sicpro_modulo_tema_favicon',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            (
                'after',
                'web/static/src/scss/primary_variables.scss',
                'sicpro_modulo_tema_visual/static/src/scss/colors.scss'
            ),
            (
                'after',
                'web/static/src/scss/primary_variables.scss',
                'sicpro_modulo_tema_visual/static/src/scss/variables.scss'
            ),
        ],
        'web.assets_backend': [
            'sicpro_modulo_tema_visual/static/src/webclient/**/*.xml',
            'sicpro_modulo_tema_visual/static/src/webclient/**/*.scss',
            'sicpro_modulo_tema_visual/static/src/webclient/**/*.js',
            'sicpro_modulo_tema_visual/static/src/views/**/*.scss',
            'sicpro_modulo_tema_visual/static/src/template/template_circulo_color.xml',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}