# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Integración con Mapas',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Permite la integración con la vista de mapas para todas las aplicaciones",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        "views/plantillas_mapas_views.xml",
        "views/res_partner_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_mapas/static/src/js/solmap_common.js',
            'sicpro_modulo_mapas/static/src/js/main_view.js',
            'sicpro_modulo_mapas/static/src/js/map_form.js',
            'sicpro_modulo_mapas/static/src/scss/main_view.scss',
            'sicpro_modulo_mapas/static/src/scss/map_form.scss',
            ],
        'web.assets_qweb': [
            'sicpro_modulo_mapas/static/src/xml/solmaptemplate.xml',
            'sicpro_modulo_mapas/static/src/xml/solmapform.xml',
            ],
        },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}

