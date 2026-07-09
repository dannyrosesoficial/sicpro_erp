# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Solicitudes de Trabajo',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Producción',
    'summary': "Esta aplicación se encargara de la recepción de "
               "solicitudes de trabajo y da inicio al proceso de ejecución.",
    'description': "Esta aplicación se encargara de la recepción de "
               "solicitudes de trabajo y da inicio al proceso de ejecución.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'calendar',
        'sicpro_app_clientes',
        'sicpro_app_trabajadores',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/solicitudes_estados_views.xml',
        'views/solicitudes_rechazo_views.xml',
        'views/solicitudes_etiquetas_views.xml',
        'views/res_company.xml',
        'data/sicpro_app_solicitudes_rechazadas.xml',
        'data/mail_template.xml',
        'data/sicpro_app_solicitudes_etiquetas.xml',
        'data/sicpro_app_solicitudes_estados.xml',
        'views/solicitudes_inversionistas_views.xml',
        'views/solicitudes_negociacion_views.xml',
        'views/solicitudes_negociacion_pg_views.xml',
        'views/solicitudes_ejecutor_views.xml',
        'views/solicitudes_grupos_views.xml',
        'views/solicitudes_tablasreportes_views.xml',
        'informes/informe_modelo_solicitud_views.xml',
        'views/solicitudes_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
