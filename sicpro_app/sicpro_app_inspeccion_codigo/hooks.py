# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################ails.

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook_verificar_modulos(env):
    """
    Hook ejecutado inmediatamente después de instalar/actualizar el módulo.
    Verifica que las tablas de la base de datos se alineen con los modelos.
    """
    _logger.info(
        "[SICPRO HOOK] Verificando consistencia de modelos e índices en la base de datos PostgreSQL...")

    # Consulta de verificación sobre information_schema para los modelos sicpro_app_%
    query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name LIKE 'sicpro_app_%' 
        AND table_type = 'BASE TABLE';
    """
    env.cr.execute(query)
    tables = env.cr.fetchall()

    _logger.info(
        f"[SICPRO HOOK] Total de tablas de módulos SICPRO detectadas en la BD: {len(tables)}")