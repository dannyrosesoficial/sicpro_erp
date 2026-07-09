# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Órdenes de Trabajo',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Producción',
    'summary': "Esta aplicación se encarga de la creación y control de las"
               " órdenes de trabajo de inversiones y mantenimiento.",
    'description': "Esta aplicación se encarga de la creación y control de las"
                   " órdenes de trabajo de inversiones y mantenimiento.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'sicpro_app_administracion',
        'base',
        'calendar',
        'sicpro_app_clientes',
        'sicpro_app_trabajadores',
        'sicpro_app_transporte',
        'sicpro_app_solicitudes',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_ordenes_clases_proyecto.xml',
        'data/sicpro_app_ordenes_etiquetas.xml',
        'data/sicpro_app_ordenes_problemas.xml',
        'data/sicpro_app_ordenes_estados.xml',
        'data/sicpro_app_ordenes_consecutivos.xml',
        'data/sicpro_app_ordenes_programa_inversiones.xml',
        'data/mail_template.xml',
        'data/sicpro_app_ordenes_paralizacion.xml',
        'views/ordenes_estados_views.xml',
        'views/ordenes_consecutivos_views.xml',
        'views/ordenes_etiquetas_views.xml',
        'views/ordenes_clases_proyectos_views.xml',
        'views/ordenes_paralizacion_views.xml',
        'views/ordenes_problemas_views.xml',
        'views/ordenes_programa_inversiones_views.xml',
        'views/ordenes_trabajo_views.xml',
        'views/ordenes_estado_ordenes_views.xml',
        'informes/informe_ordenes_anexo_3_views.xml',
        'wizard/ordenes_modelo_anexo3_views.xml',
        'views/ordenes_estados_trabajador_views.xml',
        'views/ordenes_estados_transporte_equipos_views.xml',
        'views/ordenes_grupos_transporte_equipos_views.xml',
        'views/ordenes_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
},
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
