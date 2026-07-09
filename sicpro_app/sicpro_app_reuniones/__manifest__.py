# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
{
    'name': 'SICPRO: Gestor de Reuniones',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Gestor de Reuniones, actividades e indicaciones",
    'description': "Esta aplicación se encarga de la gestión de reuniones"
                   " y el cumplimiento de los acuerdos realizados "
                   "en las reuniones de la DVPE",
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
        'mail',
        'sicpro_app_trabajadores',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_reuniones_estados.xml',
        'data/sicpro_app_reuniones_lugares.xml',
        'data/sicpro_app_reuniones_categorias.xml',
        'data/mail_template.xml',
        'data/ir_cron.xml',
        'informes/informe_modelo_despachos_views.xml',
        'views/reuniones_acuerdos_views.xml',
        'views/reuniones_decisiones_views.xml',
        'views/reuniones_participantes_views.xml',
        'views/reuniones_views.xml',
        'views/reuniones_despachos_views.xml',
        'views/reuniones_estados_views.xml',
        'views/reuniones_lugares_views.xml',
        'views/reuniones_etiquetas_views.xml',
        'views/reuniones_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_reuniones/static/src/scss/event.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
