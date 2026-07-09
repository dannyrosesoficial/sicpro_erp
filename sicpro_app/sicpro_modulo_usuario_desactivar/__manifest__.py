# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    "name": "SICPRO: Desactivar Usuarios",
    "summary": "Aplicación para la desactivación del usuario del sistema, "
               "mediante reglas de controles de accesos y LDAP empresarial",
    "description": "Aplicación para la desactivación del usuario del sistema, "
               "mediante reglas de controles de accesos y LDAP empresarial",
    'version': '19.0.0.0.1',
    "category": "Técnico",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        'sicpro_app_administracion',
        'sicpro_modulo_ldap_query',
        'sicpro_app_soporte',
        'sicpro_modulo_roles',
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sicpro_app_modulo_usuario_desactivar.xml",
        "data/ir_cron.xml",
        "data/mail_template.xml",
        "views/usuario_desactivar_views.xml",
        "views/roles_views.xml",
        "views/solicitud_bitacora_views.xml",
        "views/usuario_desactivar_menu_views.xml"
    ],
    "assets": {
        "web.assets_backend": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}

