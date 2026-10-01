# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
# CORREGIDO para Odoo 19:
#  - Envuelve el dispatch original en lugar de reimplementarlo.
#  - El logging NUNCA interrumpe la llamada XML-RPC.
#  - Compatible con cualquier versión de Odoo (15, 16, 17, 18, 19).
##############################################################################

import logging
import threading

import odoo
from odoo import SUPERUSER_ID
from odoo.service import model as _model_service

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Guardar referencia al dispatch original (una sola vez)
# ---------------------------------------------------------------------------
if not hasattr(_model_service, "_sicpro_original_dispatch"):
    _model_service._sicpro_original_dispatch = _model_service.dispatch

_ORIGINAL_DISPATCH = _model_service._sicpro_original_dispatch


# ---------------------------------------------------------------------------
# Crear el registro en xml.rpc.log sin romper nunca la llamada
# ---------------------------------------------------------------------------
def _safe_create_log(db, uid, method, params, result):
    try:
        registry = odoo.registry(db)
        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, uid, {})
            vals = {
                "model": params[0] if len(params) > 0 else False,
                "method": params[1] if len(params) > 1 else False,
                "data": params[2] if len(params) > 2 else False,
                "return_msg": result,
            }
            try:
                env["xml.rpc.log"].create(vals)
                return
            except Exception as e:
                _logger.debug(
                    "xml.rpc.log.create con uid %s falló: %s. Reintentando con sudo.",
                    uid, e,
                )

        # Fallback con SUPERUSER
        with registry.cursor() as cr:
            env_su = odoo.api.Environment(cr, SUPERUSER_ID, {})
            env_su["xml.rpc.log"].sudo().create(vals)
    except Exception:
        # Cualquier fallo en el logging es silencioso para no romper XML-RPC
        _logger.exception("No se pudo crear el registro xml.rpc.log (ignorado)")


# ---------------------------------------------------------------------------
# Dispatch envolvente
# ---------------------------------------------------------------------------
def dispatch(method, params):
    """
    Envuelve el dispatch original de Odoo añadiendo logging en xml.rpc.log.
    Cualquier fallo en el logging se captura y NO interrumpe la llamada.
    """
    # Guardamos el uid en el hilo (comportamiento del módulo original)
    try:
        if len(params) > 1:
            threading.current_thread().uid = int(params[1])
    except Exception:
        pass

    # Llamar al dispatch original: él hace TODA la lógica real
    result = _ORIGINAL_DISPATCH(method, params)

    # Logging posterior (aislado, no puede romper la respuesta)
    try:
        if method in ("execute", "execute_kw") and len(params) >= 4:
            db = params[0]
            uid = int(params[1])
            # En execute_kw los params reales empiezan en el índice 3
            real_params = params[3:] if method == "execute_kw" else params[3:]
            _safe_create_log(db, uid, method, real_params, result)
    except Exception:
        _logger.exception("Error en logging xmlrpc (ignorado)")

    return result


# ---------------------------------------------------------------------------
# Parchear odoo.service.model.dispatch
# ---------------------------------------------------------------------------
try:
    _model_service.dispatch = dispatch
    _logger.info(
        "xmlrpc dispatch wrapped by sicpro_modulo_historial_xmlrpc "
        "(compat Odoo 19)"
    )
except Exception:
    _logger.exception(
        "No se pudo parchear odoo.service.model.dispatch. "
        "El módulo de historial XML-RPC quedará inactivo, "
        "pero el resto de Odoo seguirá funcionando."
    )