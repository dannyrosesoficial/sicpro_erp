# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Repositorio Institucional',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Documentos',
    'summary': "Esta aplicación se encargará de la gestión de la información"
               " institucional de la DVPE.",
    'description': "Esta aplicación se encargará de la gestión de la"
                   " información institucional de la división",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'sicpro_app_administracion',
        'sicpro_app_trabajadores',
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_repo_tipo.xml',
        'data/sicpro_app_repo_estados.xml',
        'data/sicpro_app_repo_licencia.xml',
        'data/sicpro_app_repo_facultad.xml',
        'views/repositorio_estado_views.xml',
        'views/repositorio_etiquetas_views.xml',
        'views/repositorio_facultad_views.xml',
        'views/repositorio_licencia_views.xml',
        'views/repositorio_tipo_views.xml',
        'views/repositorio_views.xml',
        'views/repositorio_menu_views.xml',
         ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_repositorio_institucional/static/src/css/repositorio_institucional.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',

 }
