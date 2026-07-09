# -*- coding: utf-8 -*-

{
'name': 'SICPRO: Gestor Documental',
'version': '1.0',
'sequence': 2,
 'category': 'Documentos',
'summary': "Documentos",
 'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
 'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
 'license': 'AGPL-3',
 'description': "Esta aplicación se encargará de todo el control de "
                "la documentación de la división",
 'depends': ['nucleo_sicpro_erp',
             'base',
             'mail',
             'sicpro_app_administracion',
             ],
 'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/webclient_templates.xml', 'views/gestor_documental_views.xml',
    ],
 'installable': True,
 'application': True,
 'auto_install': False,

 }