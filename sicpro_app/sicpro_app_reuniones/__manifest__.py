# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Gestor de Reuniones',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Herramientas',
    'summary': "Gestor de Reuniones",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encarga de la gestión de reuniones"
                   " y el cumplimiento de los acuerdos realizados "
                   "en las reuniones de la DVPE",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'base',
        'mail',
        'nucleo_sicpro_erp',
        'sicpro_app_trabajadores',
        # 'sicpro_modulo_audio_video',
        'sicpro_modulo_dashboard_extendido',
    ],
    'data': [
        'security/reuniones.xml',
        'security/ir.model.access.csv',
        'views/reuniones_acuerdos_views.xml',
        'views/reuniones_decisiones_views.xml',
        'views/reuniones_participantes_views.xml',
        'views/reuniones_views.xml',
        'views/reuniones_despachos_views.xml',
        'views/reuniones_estados_views.xml',
        'views/reuniones_lugares_views.xml',
        'views/reuniones_etiquetas_views.xml',
        'data/acuerdos_estados_reuniones_data.xml',
        'data/acuerdos_lugares_data.xml',
        'data/acuerdos_categorias_etiquetas.xml',
        'data/plantillas_correo_data.xml',
        'data/cron_automatizacion.xml',
        'informes/informe_modelo_despachos_views.xml',
        'views/reuniones_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_reuniones/static/src/scss/event.scss'
        ],
        'web.assets_common': [
            'sicpro_app_reuniones/static/src/js/tours/event_tour.js'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
