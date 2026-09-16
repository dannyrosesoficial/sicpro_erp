# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, SUPERUSER_ID
import json

def post_init_hook(env):
    """ Se ejecuta justo después de instalar el módulo con soporte JSONB """
    # Creamos el formato JSON que Odoo 19 espera para campos traducibles
    # Usamos dict para asegurar que tanto en inglés como en español cambie
    name_json = json.dumps({
        "en_US": "Actividades",
        "es_CU": "Actividades",
        "es_ES": "Actividades"
    })

    query = """
        UPDATE ir_ui_menu 
        SET name = %s::jsonb 
        WHERE id = (
            SELECT res_id 
            FROM ir_model_data 
            WHERE module = 'project' AND name = 'menu_main_pm'
        );
    """
    env.cr.execute(query, [name_json])

def uninstall_hook(env):
    """ Se ejecuta al desinstalar el módulo, devolviendo a Project """
    name_json = json.dumps({
        "en_US": "Project",
        "es_CU": "Proyecto",
        "es_ES": "Proyecto"
    })

    query = """
        UPDATE ir_ui_menu 
        SET name = %s::jsonb 
        WHERE id = (
            SELECT res_id 
            FROM ir_model_data 
            WHERE module = 'project' AND name = 'menu_main_pm'
        );
    """
    env.cr.execute(query, [name_json])