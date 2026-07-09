# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Nomencladores',
    'version': '19.0.0.0.1',
    'category': 'Administración',
    'summary': "Este módulo agrega todas las bases de nomencladores que "
               "serán utilizados",
    'description': "Este módulo agrega todas las bases de nomencladores que "
               "serán utilizados",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': ['base',
                'resource',
                'sicpro_app_administracion',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/trimestres_views.xml',
        'views/meses_views.xml',
        'views/especialidades.views.xml',
        'views/territorios_views.xml',
        'views/cuentas_contables_views.xml',
        'views/res_municipality.xml',
        'views/res_state.xml',
        'views/centro_costo_views.xml',
        'views/locales_cc_views.xml',
        'views/departamentos_views.xml',
        'views/anios_views.xml',
        'views/centro_planificacion_views.xml',
        'views/emplazamiento_views.xml',
        'views/areas_empresa_views.xml',
        'data/res_country_state.xml',
        'data/res_municipality.xml',
        'data/sicpro_nomenclador_meses.xml',
        'data/sicpro_nomenclador_territorios.xml',
        'data/sicpro_nomenclador_trimestre.xml',
        'data/sicpro_nomenclador_especialidad.xml',
        'data/sicpro_nomenclador_anios.xml',
        'data/sicpro_nomenclador_centro_planificacion.xml',
        'data/sicpro_nomenclador_emplazamientos.xml',
        'data/sicpro_nomenclador_areas_empresa.xml',
        'views/nomencladores_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
