# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Consultas Dinámicas al LDAP',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': "Este módulo permite la realización de consultas al ldap "
               "empresarial",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        "auth_ldap",
        'sicpro_app_contactos',
        "sicpro_modulo_nomencladores",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "data/plantillas_correo.xml",
        "views/ldap_registros_views.xml",
        "views/ldap_historial_views.xml",
             ],
    'assets': {
        'web.assets_backend': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}