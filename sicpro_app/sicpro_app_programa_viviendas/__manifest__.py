# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Programa de la vivienda',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Trabajadores',
    'summary': "Módulo para el control de los materiales que se asignan a los"
               " trabajadores de la DVPE por el programa de la vivienda.",
    'description': "Módulo para el control de los materiales que se asignan a los"
               " trabajadores de la DVPE por el programa de la vivienda.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': [
                'base',
                'sicpro_app_administracion',
                'sicpro_app_trabajadores',
                'sicpro_modulo_nomencladores_sindicato',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_vivienda_escalafon.xml',
        'data/mail_template.xml',
        'views/vivienda_etapas_views.xml',
        'views/vivienda_proveedor_views.xml',
        'views/vivienda_materiales_views.xml',
        'views/vivienda_materiales_um_views.xml',
        'views/vivienda_escalafon_views.xml',
        'wizard/vivienda_anexo4_reporte_wizard_views.xml',
        'wizard/vivienda_anexo3_reporte_wizard_views.xml',
        'wizard/vivienda_estadistica_reporte_wizard_views.xml',
        'wizard/vivienda_ofertas_wizard_views.xml',
        'views/trabajadores_vivienda_views.xml',
        'views/vivienda_trabajador_views.xml',
        'views/vivienda_etapas_economia_views.xml',
        'informes/informe_vivienda_anexo_2_views.xml',
        'informes/informe_vivienda_anexo_3_views.xml',
        'informes/informe_vivienda_anexo_4_views.xml',
        'informes/informe_vivienda_estadisticas_views.xml',
        'informes/reporte_vivienda_consolidad_compras_views.xml',
        'views/vivienda_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
