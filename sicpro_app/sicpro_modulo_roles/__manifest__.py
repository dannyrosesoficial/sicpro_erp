# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Roles',
    'version': '19.0.0.0.1',
    'category': 'Administration',
    'summary': 'Gestiona los roles de accesos de los usuarios del sistema',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/ir_module_category.xml",
        "views/role.xml",
        "views/user.xml",
        "views/group.xml",
        "wizards/create_from_user.xml",
        "wizards/wizard_groups_into_role.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "pre_init_hook": "pre_init_check",
}
