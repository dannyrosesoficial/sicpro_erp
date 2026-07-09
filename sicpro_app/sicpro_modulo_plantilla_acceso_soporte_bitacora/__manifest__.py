# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Planilla Acceso Soporte',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'El módulo se encarga de actualizar los tickets de soporte y la bitácora del usuario',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_modulo_roles',
        'sicpro_modulo_plantilla_acceso',
        'sicpro_app_soporte',
    ],
    "data": [
        'view/solicitud_bitacora_views.xml',
        'view/solicitud_roles_views.xml',
        'view/solicitud_soporte_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.plantilla': [],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
}
