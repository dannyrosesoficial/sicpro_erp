# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Servicios Internos',
    'version': '19.0.0.0.1',
    'category': 'Trabajadores',
    'sequence': 2,
    'summary': "Esta aplicación se encargará del control de los servicios "
               "mobiles y de datos asignados a los trabajadores",
    'description': "Esta aplicación se encargará del control de los servicios "
               "mobiles y de datos asignados a los trabajadores",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'depends': [
        'sicpro_app_administracion',
        'sicpro_app_trabajadores',
        'base',
    ],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'data/mail_template.xml',
             'data/ir_cron.xml',
             'informes/informe_anexo1_views.xml',
             'informes/informe_anexo2_views.xml',
             'informes/informe_compromiso_nauta_views.xml',
             'informes/informe_planilla_unica_views.xml',
             'views/interno_lineas_views.xml',
             'views/interno_fijos_views.xml',
             'views/interno_nauta_views.xml',
             'views/interno_correos_views.xml',
             'views/interno_trabajadores_views.xml',
             'views/interno_solicitudes_observaciones_views.xml',
             'views/interno_solicitudes_views.xml',
             'views/interno_menu_views.xml',
             ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
