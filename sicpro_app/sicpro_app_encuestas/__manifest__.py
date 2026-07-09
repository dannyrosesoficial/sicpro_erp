# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Encuestas',
    'version': '1.0',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargara de todo el control de las"
               " encuestas y pruebas creadas por los usuarios.",
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'depends': ['nucleo_sicpro_erp',
                'base',
                'survey',
                'sicpro_app_trabajadores',
                ],
    'data': [
        'views/survey_survey.xml',
    ],
    'installable': True,
    'application': True,
}
