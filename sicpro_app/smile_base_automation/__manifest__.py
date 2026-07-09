# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Automatización Ext.',
    'version': '1.0',
    'category': 'Administración',
    'summary': """Este módulo se encargara de ampliar el acceso a la 
                automatización.""",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'base',
        'base_automation',
        'smile_log',
        'sicpro_app_administracion',
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/ir_actions.xml",
        "views/ir_model_methods_view.xml",
        "views/base_automation_view.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
