# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO - Depuración e Inspección de Módulos al Inicio',
    'version': '19.0.1.0.0',
    'summary': 'Validador automático de sintaxis y referencias Python '
               'para la suite sicpro_app_',
    'category': 'Technical',
    'author': 'División de Proyectos y Ejecución - ETECSA / Danny Rose',
    'website': 'https://www.etecsa.cu',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [],
    'post_init_hook': 'post_init_hook_verificar_modulos',
    'installable': True,
    'auto_install': False,
    'application': False,
}