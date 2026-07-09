# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Consultas Dinámicas al LDAP',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Este módulo permite la realización de consultas al "
               "ldap empresarial",
    'description': "Este módulo permite la realización de consultas al "
                   "ldap empresarial",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'sicpro_app_administracion',
        'base',
        "auth_ldap",
        "sicpro_modulo_ldap_ssl",
        'sicpro_app_contactos',
        "sicpro_modulo_nomencladores",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/mail_template.xml",
        "views/ldap_registros_views.xml",
        "views/ldap_historial_views.xml",
        "views/ldap_query_menu_views.xml",
             ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
