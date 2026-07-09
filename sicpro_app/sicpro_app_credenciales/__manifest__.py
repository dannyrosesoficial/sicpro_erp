# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Credenciales',
    'version': '19.0.0.0.1',
    'category': 'Trabajadores',
    'sequence': 2,
    'summary': "Esta aplicación se encargará del control de las credenciales "
               "de accesos de los trabajadores a la entidad",
'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
 'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'sicpro_app_trabajadores',
        # 'sicpro_modulo_dashboard_extendido',
        'base',
        'mail',
        'web',
        # 'web_editor',
        #'website',
'sicpro_app_administracion',
    ],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'informes/credencial_personal.xml',
             'informes/credencial_pvc.xml',
             'informes/credencial_laptop.xml',
             'informes/credencial_personal_laptop.xml',
             'views/credenciales_tipo_views.xml',
             'views/credenciales_accesos_views.xml',
             'views/credenciales_siglas_views.xml',
             'views/credenciales_alcance.xml',
             'views/credenciales_cancelacion_views.xml',
             'views/credenciales_views.xml',
             'data/sicpro_app_credenciales_tipo.xml',
             'data/sicpro_app_credenciales_siglas.xml',
             'data/sicpro_app_credenciales_accesos.xml',
             'data/sicpro_app_credenciales_alcance.xml',
             'data/ir_cron.xml',
             'data/mail_template.xml',
             'views/credenciales_menu_views.xml',
             'wizards/recortador_de_imagenes.xml',
             ],
    'assets':
        {'web.assets_backend': [
            'sicpro_app_credenciales/static/lib/cropper/cropper.min.css',
            'sicpro_app_credenciales/static/lib/cropper/cropper.min.js',
            # --- JavaScript (Orden Crítico de Dependencias) ---
            'sicpro_app_credenciales/static/src/js/image_processing.js',
            # 3. Componentes que heredan o usan los anteriores
            'sicpro_app_credenciales/static/src/js/widget_recortar_imagen.js',
            'sicpro_app_credenciales/static/src/js/imagen_con_recortar.js',
            'sicpro_app_credenciales/static/src/xml/templates_recortador.xml',
         'sicpro_app_credenciales/static/src/scss/imagen_con_recortar.scss',
            'sicpro_app_credenciales/static/src/scss/recortador.scss',
            'sicpro_app_credenciales/static/src/scss/sicpro_app_credenciales.backend.scss',
    ],
        'web.report_assets_common': [
            'sicpro_app_credenciales/static/src/css/credencial_pvc.css',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
