# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Móvil Responsive",
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Cambia el formato Web de SICPRO ERP para adaptarla a la '
               'aplicación móvil',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        "base",
        "web",
        "mail"],
    "data": [
        "views/assets.xml",
        "views/res_users.xml",
        "views/web.xml"],
    "qweb": [
        "static/src/xml/apps.xml",
        "static/src/xml/form_view.xml",
        "static/src/xml/navbar.xml",
        "static/src/xml/document_viewer.xml",
        "static/src/xml/discuss.xml",
    ],
}
