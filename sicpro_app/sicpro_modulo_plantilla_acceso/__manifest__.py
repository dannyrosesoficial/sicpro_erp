# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Planilla Acceso',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'El módulo se encarga de las peticiones de roles de acceso',
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
        'base',
        'web',
        "http_routing",
        'sicpro_app_trabajadores',
        'sicpro_modulo_web_login',
        'sicpro_modulo_roles',
        'sicpro_modulo_ldap_local',
        'sicpro_app_clientes',
    ],
    "data": [
        'security/ir.model.access.csv',
        'view/sequency.xml',
        'informes/informe_planilla_acceso_views.xml',
        'data/plantillas_correo_data.xml',
        'view/solicitud_roles_views.xml',
        'view/res_users_views.xml',
        'view/solicitud_roles_menu_views.xml',
            ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_plantilla_acceso/static/src/scss/planilla_con_fondo.scss',
        ],
        'web.plantilla': [
            'sicpro_modulo_plantilla_acceso/static/src/js/plantilla_actions.js',
            'sicpro_modulo_plantilla_acceso/static/src/scss/plantilla_acceso.scss',
            'sicpro_modulo_plantilla_acceso/static/lib/html2pdf.bundle.js',
            'sicpro_modulo_plantilla_acceso/static/lib/he.js',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
}
