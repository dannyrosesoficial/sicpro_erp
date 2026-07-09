# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Desactivar Usuarios",
    "summary": "Aplicación para la desactivación del usuario del sistema, "
               "mediante reglas de controles de accesos y LDAP empresarial",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Aplicación para simulación de sesión de los usuarios",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_modulo_ldap_query',
        'sicpro_app_soporte',
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/desactivar_usuario_data.xml",
        "data/ir_cron_data.xml",
        "data/plantillas_correo.xml",
        "views/usuario_desactivar_views.xml",
        "views/roles_views.xml",
        "views/usuario_desactivar_menu_views.xml"
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}

