# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import threading
import logging
from typing import Any

import odoo
from odoo import SUPERUSER_ID

_logger = logging.getLogger(__name__)


def _safe_create_log(registry, db, uid, values):
    try:
        # Creamos un cursor y entorno breve para la creación con el uid original
        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, uid, {})
            try:
                env['xml.rpc.log'].create(values)
                return
            except Exception as e:
                _logger.warning("Creación con uid %s falló por: %s, intentando con sudo", uid, e)
        # Fallback a SUPERUSER
        with registry.cursor() as cr:
            env_su = odoo.api.Environment(cr, SUPERUSER_ID, {})
            env_su['xml.rpc.log'].sudo().create(values)
            _logger.info("Registro xml.rpc.log creado con sudo por fallo de permisos del uid %s", uid)
    except Exception:
        _logger.exception("No se pudo crear el registro de log XML-RPC")


def dispatch(method: str, params: Any):
    # Firma compatible: params esperado similar a (db, uid, password, model, method, data)
    (db, uid, passwd) = params[0], int(params[1]), params[2]
    threading.current_thread().uid = uid

    params = params[3:]
    if method == 'obj_list':
        raise NameError("obj_list has been discontinued via RPC as of 6.0, please query ir.model directly!")
    if method not in ['execute', 'execute_kw']:
        raise NameError("Method not available %s" % method)

    # Security check: intentar usar security.check si está disponible
    try:
        from odoo.service.model import security

        security.check(db, uid, passwd)
    except Exception as e:
        # Si no existe o falla, lanzamos para evitar ejecutar sin autenticación
        _logger.exception("Fallo en security.check: %s", e)
        raise

    # Obtener registry de la base de datos
    registry = odoo.registry(db)

    # Resolver la función objetivo (execute/execute_kw) si está en el módulo actual
    fn = globals().get(method)
    if fn is None:
        raise NameError("Method not found: %s" % method)

    # Ejecutar la llamada dentro del manejo de cambios del registry cuando exista
    try:
        with registry.manage_changes():
            res = fn(db, uid, *params)

            # Preparar datos para el log
            vals = {
                'model': params[0] if len(params) > 0 else False,
                'method': params[1] if len(params) > 1 else False,
                'data': params[2] if len(params) > 2 else False,
                'return_msg': res,
            }

            # Intentar crear el registro de log con el uid original, fallback a sudo
            _safe_create_log(registry, db, uid, vals)
    except Exception:
        _logger.exception("Error ejecutando dispatch para method=%s db=%s uid=%s", method, db, uid)
        raise

    return res


# Registrar sobreescritura de dispatch en odoo.service.model si existe.
try:
    import odoo.service.model as _model_service
    _model_service.dispatch = dispatch
    _logger.info("xmlrpc dispatch patched by sicpro_modulo_historial_xmlrpc for Odoo 19 compatibility")
except Exception:
    # Si no es posible parchear, lo documentamos. ASSUMPTION: en algunas builds de Odoo19 el objeto puede no existir.
    _logger.exception("No se pudo parchear odoo.service.model.dispatch; ver MIGRATION_NOTES.md para pasos manuales")
