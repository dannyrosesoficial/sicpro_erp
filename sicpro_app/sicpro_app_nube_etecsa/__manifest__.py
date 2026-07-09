# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Nube ETECSA',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Aplicación para la interrelación de SICPRO con la Nube ETECSA",
    'description': "Aplicación para la interrelación de SICPRO "
                   "con la Nube ETECSA",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 2,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'base',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
    ],
    'data': ['security/ir.model.access.csv',
             'views/res_users_token_views.xml',
             'views/res_users_views.xml',
             ],
    'assets': {
        'web.assets_qweb': [
            'sicpro_app_nube_etecsa/static/src/xml/web_boton_nube_etecsa.xml',
        ],
        'web.assets_backend': [
            # se desactivo el botón de la barra superior para optimizar el espacio
            # 'sicpro_app_nube_etecsa/static/src/js/web_nube_etecsa.js',
            'sicpro_app_nube_etecsa/static/src/js/user_menu.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
