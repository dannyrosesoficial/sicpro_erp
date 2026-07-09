# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Edición Multiple",
    "version": "14.0.1.0.1",
    "author": 'Daniel Barrero Reyes',
    "category": "Herramientas",
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
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
}
