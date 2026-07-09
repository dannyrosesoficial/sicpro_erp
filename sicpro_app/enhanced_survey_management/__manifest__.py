# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
{'name': 'Enhanced Survey Management', 'version': '19.0.0.0.1',  # Actualizado a v19
 'category': 'Extra Tools', 'summary': 'Enhance your survey management with new question kinds and more', 'description': """
Upgrade your survey management capabilities with the addition of versatile question types.
Capture specific timeframes (month, week, range), enable file uploads, and specific fields 
like signature, many2one, and custom matrices.
""", 'author': 'Cybrosys Techno Solutions', 'company': 'Cybrosys Techno Solutions',
 'maintainer': 'Cybrosys Techno Solutions', 'website': "https://www.cybrosys.com",
 'depends': ['base', 'survey'  # Añadido ya que usas controladores de Website y rutas públicas
             ],
'external_dependencies': {
        'python': ['xlsxwriter'], # Nombre de la librería que se importa en Python
    },
 'data': ['security/ir.model.access.csv', 'views/survey_templates.xml', 'views/survey_question_views.xml',
          'views/survey_input_print_templates.xml', 'views/survey_user_views.xml', 'views/survey_survey_views.xml'],
 'assets': {  # En Odoo 19, para el frontend de encuestas se usa 'survey.assets'
     'survey.assets': [  # Se recomienda descargar flatpickr e incluirlo localmente,
         # pero si usas CDN, asegúrate de que sea compatible con los CSP de Odoo 19
         'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
         'https://cdn.jsdelivr.net/npm/flatpickr@4.6.3/dist/flatpickr.min.js',

         'enhanced_survey_management/static/src/js/survey_form.js',
         'enhanced_survey_management/static/src/js/survey_submit.js', ],
     # Si tienes estilos personalizados para los nuevos tipos de pregunta:
     # 'web.assets_frontend': [
     #     'enhanced_survey_management/static/src/scss/survey_styles.scss',
     # ],
 }, 'images': ['static/description/banner.jpg', ], 'license': 'LGPL-3', 'installable': True, 'auto_install': False,
 'application': False, }
