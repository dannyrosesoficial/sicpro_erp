# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Web Gestor de Base de Datos',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Se encarga de gestionar el proceso de salva y restaura del sistema SICPRO ERP.',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'external_dependencies': {'python': ['gitpython']},
    "depends": [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        'web',
    ],
    "data": [
        'views/web_base_datos.xml'
    ],
    'assets': {
        'web.assets_backend': [],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}
