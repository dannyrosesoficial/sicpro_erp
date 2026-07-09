# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Trabajadores',
    'version': '1.0',
    'category': 'Trabajadores/SICPRO - APP: Trabajadores',
    'sequence': 2,
    'summary': "Esta aplicación se encargara del control de los datos "
               "de los trabajadores.",
    'author': 'Daniel Barrero Reyes',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'license': 'AGPL-3',
    'images': [
        'images/hr_department.jpeg',
        'images/hr_employee.jpeg',
        'images/hr_job_position.jpeg',
        'static/src/img/default_image.png',
    ],
    'depends': [
        'sicpro_modulo_nomencladores',
        'base_setup',
        'mail',
        'resource',
    ],
    'data': [
        'security/trabajadores_security.xml',
        'security/ir.model.access.csv',
        'views/trabajadores_trabajos_views.xml',
        'views/trabajadores_categorias_views.xml',
        'report/hr_employee_badge.xml',
        'views/trabajadores_views.xml',
        'views/trabajadores_departmentos_views.xml',
        'views/trabajadores_views_views.xml',
        'views/trabajadores_templates.xml',
        'views/mail_channel_views.xml',
        'views/nomenclador_especialidades.views.xml',
        'views/res_user.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': ['static/src/xml/hr_templates.xml'],
}
