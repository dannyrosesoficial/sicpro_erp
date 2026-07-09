# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Roles',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Gestiona los roles de accesos de los usuarios del sistema',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', "base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/ir_module_category.xml",
        "views/role.xml",
        "views/user.xml",
    ],

    "installable": True,
    'application': True,
    "auto_install": False,
}