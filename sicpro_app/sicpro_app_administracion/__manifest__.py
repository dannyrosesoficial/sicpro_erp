# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Administración',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Aplicación para la administración de SICPRO ERP",
    'description': "Aplicación para la administración de SICPRO ERP",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 1,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'base',
        'mail',
        'web',
        'base_automation',
        'nucleo_sicpro_erp',
        'sicpro_modulo_roles',
        'auth_ldap',
        'sicpro_modulo_web_notify',
    ],
    'data': [
        'security/administracion.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/ir_module_view.xml',
        'views/res_company.xml',
        # 'data/res_company_data.xml', ---Se deshabilita para producción
        # 'data/mail_channel_data.xml', ---Se deshabilita para producción
        'data/res_user_data.xml',
        'data/ir_mail_server_data.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_config_parameter.xml',
        'views/webclient_templates.xml',
        'views/sicpro_app_administracion.xml',
        'views/administracion_menus_accesos_view.xml',
        'views/administracion_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_administracion/static/src/js/web_debug.js',
            'sicpro_app_administracion/static/src/css/web_no_bubble.scss',
            'sicpro_app_administracion/static/src/css/web_administracion.scss',
            'sicpro_app_administracion/static/src/models/attachment/attachment.js',
            'sicpro_app_administracion/static/src/models/thread/thread.js',
            'sicpro_app_administracion/static/src/widgets/form_renderer/form_renderer.js',
            'sicpro_app_administracion/static/src/components/attachment_card/attachment_card.js',
            'sicpro_app_administracion/static/src/components/attachment_card/attachment_card.scss',
        ],
        'web.assets_frontend': [
            'sicpro_app_administracion/static/src/css/web_no_bubble.scss'
        ],
        'web.assets_qweb': [
           'sicpro_app_administracion/static/src/xml/web_boton_debug.xml',
            'sicpro_app_administracion/static/src/xml/base_actions.xml',
            'sicpro_app_administracion/static/src/components/attachment_card/attachment_card.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
