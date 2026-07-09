# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Solicitudes de Trabajo',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Solicitudes',
    'summary': "Esta aplicación se encargara de la recepción de "
               "solicitudes de trabajo y da inicio al proceso de ejecución.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'calendar',
        'sicpro_app_clientes',
        'sicpro_app_trabajadores',
        'sicpro_modulo_dashboard_extendido',
    ],
    'data': [
        'security/solicitudes.xml',
        'security/ir.model.access.csv',
        'views/solicitudes_estados_views.xml',
        'views/solicitudes_rechazo_views.xml',
        'views/solicitudes_etiquetas_views.xml',
        'views/res_company.xml',
        'data/rechazadas_data.xml',
        'data/plantillas_correo_data.xml',
        'data/etiquetas_data.xml',
        'data/estados_data.xml',
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
        'web.assets_backend': [
            'sicpro_app_solicitudes/static/src/css/crm.css'
        ],
        'web.assets_qweb': [], },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
