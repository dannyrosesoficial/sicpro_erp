# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Registro Certificado LDAPS',
    'version': '1.0',
    'category': 'Administración',
    'summary': "Este módulo permite la autentificación via ldap ssl, "
               "permitiendo la validación del certificado de seguridad",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp',
                'base',
                "auth_ldap"],
    "data": [
        "views/res_company_ldap_views.xml",
        "data/ldap_data.xml"
    ],
    "external_dependencies": {"python": ["python-ldap"]},

    'installable': True,
    'application': True,
}