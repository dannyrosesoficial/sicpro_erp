# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Timeout',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'El modulo se encarga de cerrar la session después del tiempo '
               'predeterminado por la configuración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', "base"],
    "data": ["data/ir_config_parameter_data.xml"],

    "installable": True,
    'application': True,
    "auto_install": False,
}