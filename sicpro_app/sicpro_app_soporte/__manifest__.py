# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Soporte',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Soporte',
    'summary': "Esta aplicación se encargara de la gestión del "
               "soporte técnico de la administración del sistema.",
    'description': "Esta aplicación se encargara de la gestión del "
               "soporte técnico de la administración del sistema.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'sicpro_app_trabajadores',
        'sicpro_modulo_roles',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_soporte_equipos.xml',
        'data/mail_template.xml',
        'data/ir_sequence.xml',
        'data/sicpro_app_soporte_etiquetas.xml',
        'data/sicpro_app_soporte_estados.xml',
        'data/sicpro_app_soporte_canales.xml',
        'data/sicpro_app_soporte_estados_versiones.xml',
        'data/sicpro_app_soporte_estados_aplicaciones.xml',
        'data/sicpro_app_soporte_estados_paquetes.xml',
        'views/trabajadores_view.xml',
        'views/soporte_equipos_view.xml',
        'views/soporte_estados_view.xml',
        'views/soporte_estados_versiones_view.xml',
        'views/soporte_estados_paquetes_view.xml',
        'views/soporte_estados_aplicaciones_view.xml',
        'views/soporte_etiquetas_view.xml',
        'views/soporte_canales_view.xml',
        'views/soporte_ticket_view.xml',
        'views/soporte_ticket_todos_view.xml',
        'views/soporte_dashboard_view.xml',
        'views/soporte_versiones_view.xml',
        'views/soporte_aplicaciones_view.xml',
        'views/soporte_paquetes_view.xml',
        'views/soporte_bitacora_view.xml',
        'views/soporte_fragmentos_codigos_view.xml',
        'views/soporte_ticket_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
