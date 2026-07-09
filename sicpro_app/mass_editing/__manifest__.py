# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Edición Multiple",
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    "author": 'Daniel Barrero Reyes',
    "category": "Herramientas",
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "summary": "Edición Multiple de datos",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/ir_actions_server.xml",
        "wizard/mass_editing_wizard.xml",
    ],
    "demo": ["demo/mass_editing.xml"],
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
