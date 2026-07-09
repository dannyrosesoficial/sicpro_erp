# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Trabajadores',
    'version': '19.0.0.0.1',
    'category': 'Trabajadores',
    'sequence': 2,
    'summary': "Esta aplicación se encargará del control de los datos de "
               "los trabajadores.",
    'description': "Esta aplicación se encargará del control de los datos de "
               "los trabajadores.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'resource',
        'calendar',
        'bus',
        'sicpro_app_administracion',
        'sicpro_modulo_nomencladores',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_trabajadores_categorias.xml',
        'data/sicpro_app_trabajadores_familiar.xml',
        'data/sicpro_app_trabajadores_disiplinaria_categorias.xml',
        'data/sicpro_app_trabajadores_documentos_tipos.xml',
        'data/sicpro_app_trabajadores_educacion_tipos.xml',
        'data/sicpro_app_trabajadores_educacion_certificacion.xml',
        'data/sicpro_app_trabajadores_cursos_tipos.xml',
        'data/mail_template.xml', 'data/ir_cron.xml',
        'data/sicpro_app_trabajadores_tallas.xml',
        'report/trabajadores_report_views.xml',
        'informes/informe_medida_desciplinaria_views.xml',
        'views/trabajadores_ocupacion_views.xml',
        'views/trabajadores_categorias_views.xml',
        'views/res_user.xml',
        'views/trabajadores_familiar_views.xml',
        'views/trabajadores_views.xml',
        'views/trabajadores_areas_views.xml',
        'views/trabajadores_tipo_documento_view.xml',
        'views/trabajadores_plantillas_documentos_views.xml',
        'views/trabajadores_documentos_view.xml',
        'views/trabajadores_disciplinaria_categorias_view.xml',
        'views/trabajadores_disciplinarias_acciones.xml',
        'views/trabajadores_cursos_habilidades_views.xml',
        'views/trabajadores_educacion_views.xml',
        'views/trabajadores_educacion_tipos_views.xml',
        'views/trabajadores_educacion_tipos_certificacion.xml',
        'views/trabajadores_equipo_tecnico_views.xml',
        'views/trabajadores_cargos_views.xml',
        'views/trabajadores_claves_horas_views.xml',
        'views/trabajadores_vacunacion_views.xml',
        'views/trabajadores_instruciones_views.xml',
        'views/trabajadores_seguridad_proteccion_views.xml',
        'views/trabajadores_seguridad_trabajador_views.xml',
        'views/trabajadores_tallas_views.xml',
        'views/trabajadores_areas_altas_bajas_views.xml',
        'views/trabajadores_areas_totales_views.xml',
        'views/calendar_trabajadores_views.xml',
        'views/trabajadores_menu_views.xml',
    ],
    'assets': {
    'web.assets_backend': [
        # 1. Variables y Estilos (Se cargan primero)
        'sicpro_app_trabajadores/static/src/scss/variables.scss',
        'sicpro_app_trabajadores/static/src/scss/hr.scss',
        'sicpro_app_trabajadores/static/src/scss/trabajadores.scss',
        'sicpro_app_trabajadores/static/src/scss/cursos_educacion.scss',

        # 3. Plantillas XML (Antes en assets_qweb)
        'sicpro_app_trabajadores/static/src/xml/educacion_templates.xml',
        'sicpro_app_trabajadores/static/src/xml/cursos_templates.xml',
    ],
},
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
