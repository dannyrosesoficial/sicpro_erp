# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Gestor de Reuniones',
    'version': '1.0',
    'sequence': 2,
    'category': 'Herramientas',
    'summary': "Gestor de Reuniones",
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encarga de la gestión de reuniones"
                   " y el cumplimiento de los acuerdos realizados "
                   "en las reuniones de la DVPE",
    'depends': [
        'base',
        'mail',
        'nucleo_sicpro_erp',
        'sicpro_app_trabajadores',
        'sicpro_modulo_audio_video',
        'sicpro_app_administracion'
    ],
    'data': [
        'security/reuniones.xml',
        'security/ir.model.access.csv',
        'views/reuniones_acuerdos_views.xml',
        'views/reuniones_template.xml',
        'views/reuniones_participantes_views.xml',
        'views/reuniones_views.xml',
        'views/reuniones_estados_views.xml',
        'views/reuniones_lugares_views.xml',
        'views/reuniones_etiquetas_views.xml',
        'data/acuerdos_estados_reuniones_data.xml',
        'data/acuerdos_lugares_data.xml',
        'data/acuerdos_categorias_etiquetas.xml',
        'data/plantillas_correo_data.xml',
        'data/cron_automatizacion.xml',
        'views/reuniones_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
