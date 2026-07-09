# -*- encoding: utf-8 -*-

{
    'name': 'SICPRO: Mostrar Contraseña Login',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Permite visualizar la contraseña del login de SICPRO ERP',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp',
                'sicpro_modulo_web_login'
                ],
    "data": [
        'views/login_pass_template.xml'
         ],
    'assets': {
        'web.assets_frontend': [
          'sicpro_modulo_web_login_show_pass/static/src/js/show_password.js',
      ],
    },
    "pre_init_hook": "pre_init_check",
    "installable": True,
    'application': True,
    "auto_install": False,
}