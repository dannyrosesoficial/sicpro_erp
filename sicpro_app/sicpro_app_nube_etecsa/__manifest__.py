# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Nube ETECSA',
    'version': '1.0',
    'summary': "Aplicación para la interrelación de SICPRO con la Nube ETECSA",
    'description': "Aplicación para la interrelación de SICPRO "
                   "con la Nube ETECSA",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'base',
        'nucleo_sicpro_erp',
    ],
    'data': [
        # 'security/administracion.xml',
        # 'security/ir.model.access.csv',
        # 'views/res_users_view.xml',
        'views/web_nube_etecsa.xml',
    ],
    'qweb': ['static/src/xml/web_boton_nube_etecsa.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
