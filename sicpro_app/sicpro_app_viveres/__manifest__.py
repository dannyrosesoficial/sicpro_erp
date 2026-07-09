# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Víveres',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Trabajadores',
    'summary': "Esta aplicación se encarga del control de la entrega de víveres a los trabajadores.",
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
        'sicpro_app_administracion',
        'sicpro_modulo_nomencladores',
        'sicpro_app_trabajadores',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/sicpro_app_viveres_productos.xml',
        'wizard/viveres_trabajadores_entrega_wizard_views.xml',
        'views/viveres_views.xml',
        'views/viveres_productos_views.xml',
        'views/viveres_productos_comprados_views.xml',
        'views/viveres_cierre_views.xml',
        'views/viveres_areas_entregas_resumenes_views.xml',
        'views/viveres_areas_fondo_views.xml',
        'views/viveres_areas_entregas_views.xml',
        'views/viveres_trabajadores_entregas_views.xml',
        'views/viveres_areas_altas_bajas_views.xml',
        'views/viveres_areas_efectivo_views.xml',
        'views/viveres_areas_views.xml',
        'views/viveres_trabajador_views.xml',
        'views/viveres_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_viveres/static/src/xml/viveres_distribuir_productos.xml',
            'sicpro_app_viveres/static/src/js/viveres_distribuir_productos.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    "pre_init_hook": "pre_init_check",
}