# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Clientes',
    'version': '1.0',
    'category': 'Clientes',
    'summary': "Esta aplicación le ofrece una vista rápida de su directorio "
               "de clientes, accesible desde su página de inicio.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'sicpro_modulo_nomencladores',
        'mail',
    ],

    'data': [
        'security/clientes_security.xml',
        'security/ir.model.access.csv', 'views/clientes_views.xml',
        'views/clientes_etiquetas_views.xml',
        'views/res_user.xml',
        'data/etiquetas_data.xml',
        'views/clientes_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
