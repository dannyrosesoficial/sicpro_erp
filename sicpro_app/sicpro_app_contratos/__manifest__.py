# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Contratos',
    'version': '1.0',
    'sequence': 2,
    'category': 'Contratos',
    'summary': "Contratos",
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encargará de todo el control de los "
                   "contratos y proveedores de la división, así como del "
                   "proceso de contabilidad.",
    'depends': [
        'base_setup',
        'product',
        'analytic',
        'portal',
        'digest'],
    'data': [
        'security/contratos.xml',
        'security/ir.model.access.csv',
        'views/contratos.xml',
        'views/contratos_proveedores_etiquetas_views.xml',
        'views/contratos_proveedores_tipo_views.xml',
        'views/contratos_proveedores_estados_views.xml',
        'views/contratos_tipo_views.xml',
        'views/contratos_estados_views.xml',
        'views/contratos_dias_views.xml',
        'views/contratos_etiquetas_views.xml',
        'views/contratos_unidades_views.xml',
        'views/contratos_areas_views.xml',
        'views/contratos_proveedores.xml',
        'views/contratos_menu_views.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
