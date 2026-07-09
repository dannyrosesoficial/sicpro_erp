# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Encuestas',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargará de todo el control de las"
               " encuestas y pruebas creadas por los usuarios.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'survey',
                'sicpro_app_trabajadores',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_templates.xml',
        'views/survey_question_views.xml',
        'views/survey_input_print_templates.xml',
        'views/survey_user_views.xml',
        'views/stats_inherit.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'survey/static/src/js/survey_result.js',
        ],
        'web.assets_frontend': [
            'sicpro_app_encuestas/static/src/js/survey_form.js',
            'sicpro_app_encuestas/static/src/js/survey_submit.js',
            'sicpro_app_encuestas/static/src/js/survey_statistics_inherit.js',
        ],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
