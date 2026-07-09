# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Login Screen',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Crear una nueva configuración del login para SICPRO ERP',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', "base", "sicpro_app_administracion",],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/attachment.xml",
        "views/login_version_views.xml",
        "views/login_sociales_views.xml",
        "data/ir_config_parameter.xml",
        "data/imagen.xml",
        "data/login_data.xml",
        "views/webclient_templates.xml",
    ],

    "installable": True,
    'application': True,
    "auto_install": False,
}
