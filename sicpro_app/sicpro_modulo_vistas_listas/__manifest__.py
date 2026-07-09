# -*- encoding: utf-8 -*-
{
    'name': 'SICPRO: Modificación vistas de Lista',
    'version': '1.0',
    'summary': "Modifica las vistas listas",
    'description': "Este módulo se encarga de todas las modificaciones a las "
                   "vistas de de árbol o lista",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp',
                'base',
                'web'],
    'data': [
        'views/autonumeracion_listas.xml',

             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
