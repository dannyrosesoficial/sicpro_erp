# -*- coding: utf-8 -*-
{
    'name': 'Project Gantt View',
    'version': '13.0.1.0',
    'category': 'Project',
    'description': """
Project: add new field "Color". Task: add 3 fields: Start date, End Date, Color. Add a gantt view for tasks.
    """,
    'summary': '''
Project: add new field "Color". Task: add 3 fields: Start date, End Date, Color. Add a gantt view for tasks.
    ''',
    'author': 'Domiup',
    'license': 'OPL-1',
    'support': 'domiup.contact@gmail.com',
    'website': '',
    'depends': [
        'project',
    ],
    'data': [
        # views
        'views/project_task_views.xml',
        'views/project_views.xml',
    ],

    'test': [],
    'demo': [],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'active': False,
    'application': True,
}
