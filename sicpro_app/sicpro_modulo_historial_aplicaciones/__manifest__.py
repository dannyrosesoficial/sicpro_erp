# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Historial de Aplicaciones',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Visualización del historial de instalación desinstalación / actualización de los módulos",
    'description': "Visualización del historial de instalación desinstalación / actualización de los módulos",
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
        'sicpro_app_administracion'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/historial_aplicaciones_view.xml',
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
