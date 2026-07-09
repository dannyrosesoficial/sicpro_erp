# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Marketing por Correo',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Gestión del marketing digital mediante correo electrónico",
    'description': "Aquí se realiza la gestión del marketing digital vía correo electrónico",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'contacts',
        'mail',
        'utm',
        'mass_mailing',
        'sicpro_app_trabajadores',
    ],
    'data': [
        # 'views/marketing_views_menus.xml',
        'data/cron_automatizacion.xml',
        'data/plantillas_correo_data.xml',
        'views/mailing_contact_views.xml',
        'views/res_users_view.xml',
    ],
    'assets': {
        'web.assets_qweb': [],
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}

