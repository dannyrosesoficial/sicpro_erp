# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Transporte',
    'version': '1.0',
    'sequence': 2,
    'category': 'Human Resources/Transporte',
    'summary': "Esta aplicación se encargará de todo el control del parqué "
               "automotor de la división.",
    'depends': [
        'nucleo_sicpro_erp',
        'base',
                'mail',
                'sicpro_modulo_nomencladores',
                'sicpro_app_trabajadores',
                ],
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'data': [
        'security/transporte.xml',
        'security/ir.model.access.csv',
        'views/transporte_modelo_views.xml',
        'views/config_rest_api_views.xml',
        'views/transporte_views.xml',
        'views/transporte_trabajadores.xml',
        'data/cron_automatizacion.xml',
        'data/Transporte_fabricantes_data.xml',
        'data/transporte_api_data.xml',
        'data/estados_data.xml',
        'data/plantillas_correo_data.xml',
        'views/transporte_menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
