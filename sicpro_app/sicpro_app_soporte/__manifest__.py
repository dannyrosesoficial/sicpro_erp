# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Soporte',
    'version': '1.0',
    'sequence': 2,
    'category': 'Soporte/Soporte',
    'summary': "Esta aplicación se encargara de la gestión del "
               "soporte técnico de la administración del sistema.",
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'portal',
    ],
    'data': [
        'security/soporte_security.xml',
        'security/ir.model.access.csv',
        'data/soporte_data.xml',
        'views/res_partner_view.xml',
        'views/soporte_ticket_menu.xml',
        'views/soporte_equipos_view.xml',
        'views/soport_estados_view.xml',
        'views/soporte_categoria_view.xml',
        'views/soporte_canales_view.xml',
        'views/soporte_etiquetas_view.xml',
        'views/soporte_ticket_view.xml',
        'views/soporte_dashboard_view.xml',
    ],

    'application': True,
    'installable': True,
}
