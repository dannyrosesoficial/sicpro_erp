# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Instrucciones Laborales',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargara de todo el control de las "
               "instrucciones que se le realizan a los trabajadores",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'mail',
                'sicpro_app_trabajadores',
                'sicpro_app_encuestas',
                'survey',
                ],
    'data': [
        'security/instrucciones.xml',
        'security/ir.model.access.csv',
        'views/instrucciones_etiquetas_views.xml',
        'views/instrucciones_instruccion_views.xml',
        'views/instrucciones_trabajador_views.xml',
        'views/instrucciones_dashboard_views.xml',
        'data/cron_automatizacion.xml',
        'data/plantillas_correo_data.xml',
        'informes/informe_modelo_instrucciones_views.xml',
        'views/instrucciones_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_instrucciones/static/src/scss/instrucciones.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
