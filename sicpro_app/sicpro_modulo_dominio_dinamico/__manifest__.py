# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Dominio Dinámico',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Permite crear dominios a campo Many2one de forma dinámica.",
    'description': "Permite crear dominios a campo Many2one de forma dinámica.",
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
        'base',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': ["/sicpro_modulo_dominio_dinamico/static/lib/js/*.js", ],
        'web.assets_frontend': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
