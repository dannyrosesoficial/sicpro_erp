# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Registros de Usuario',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Detalles del usuario de inicio de sesión y dirección IP",
    'description': "Este módulo registra la información de inicio de sesión del usuario",
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
        'base',
        'web',
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/plantillas_correo_data.xml',
        'wizard/pass_user_backup_wizard_views.xml',
        'views/registro_usuarios_reporte.xml',
        'views/registro_usuarios_reporte_template.xml',
        'views/registro_usuarios_reporte_wizard.xml',
        'views/registro_usuarios_views.xml',
        'views/registro_ips_view.xml',
        'views/res_user_views.xml',
        ],
    'assets':
        {
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
