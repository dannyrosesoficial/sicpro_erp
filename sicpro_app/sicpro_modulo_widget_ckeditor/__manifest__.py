# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Widget CKEditor',
    'version': '19.0.0.0.1',
    'summary': "Permite crear nuevo contenido en campos text/html usando el moderno editor WYSIWYG",
    "description": "Permite crear nuevo contenido en campos text/html usando el moderno editor WYSIWYG",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'web',
        'sicpro_app_administracion',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-editor.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-content.css',
            'sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.xml',
            'sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.scss',
            'sicpro_modulo_widget_ckeditor/static/src/widgets/UploadAdapter.js',
            'sicpro_modulo_widget_ckeditor/static/src/widgets/UploadAdapterPlugin.js',
            'sicpro_modulo_widget_ckeditor/static/src/widgets/ckeditor_widget.js',
        ],
        'web.report_assets_common': [
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-editor.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-content.css',
        ],
        'web.report_assets_pdf': [
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-editor.css',
            'sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5-content.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
