# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Historial de Aplicaciones',
    'version': '1.0',
    'summary': """Visualización del historial de instalación / 
    desinstalación / actualización de los módulos""",
    'description': """Visualización del historial de instalación / 
    desinstalación / actualización de los módulos""",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'sicpro_app_administracion'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/historial_aplicaciones_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
