# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Gestor Documental',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Documentos',
    'summary': "Documentos",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encargará de todo el control de "
                "la documentación de la división",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        'mail',
    ],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/gestor_documental_views.xml',
         ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_gestor_documental/static/src/css/document_management_system.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',",

 }