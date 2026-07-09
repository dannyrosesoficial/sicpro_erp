# -*- coding: utf-8 -*-


import logging
import os
import sys
import threading
import time
try:
    from werkzeug.middleware.shared_data import SharedDataMiddleware
except ImportError:
    from werkzeug.wsgi import SharedDataMiddleware

try:
    import psutil
except ImportError:
    psutil = None

import odoo
from odoo.http import memory_info, NO_POSTMORTEM, replace_request_password

_logger = logging.getLogger(__name__)
rpc_request = logging.getLogger(__name__ + '.rpc.request')
rpc_response = logging.getLogger(__name__ + '.rpc.response')


def dispatch_rpc_sql(service_name, method, params):
    """ Handle a RPC call.

    This is pure Python code, the actual marshalling (from/to XML-RPC) is done
    in a upper layer.
    """
    try:
        rpc_request_flag = rpc_request.isEnabledFor(logging.DEBUG)
        rpc_response_flag = rpc_response.isEnabledFor(logging.DEBUG)
        if rpc_request_flag or rpc_response_flag:
            start_time = time.time()
            start_memory = 0
            if psutil:
                start_memory = memory_info(psutil.Process(os.getpid()))
            if rpc_request and rpc_response_flag:
                odoo.netsvc.log(rpc_request, logging.DEBUG, '%s.%s' % (service_name, method), replace_request_password(params))

        threading.current_thread().uid = None
        threading.current_thread().dbname = None
        if service_name == 'common':
            dispatch = odoo.service.common.dispatch
        elif service_name == 'db':
            dispatch = odoo.addons.sicpro_modulo_web_base_datos.service.db.dispatch_sql
        elif service_name == 'object':
            dispatch = odoo.service.model.dispatch
        result = dispatch(method, params)

        if rpc_request_flag or rpc_response_flag:
            end_time = time.time()
            end_memory = 0
            if psutil:
                end_memory = memory_info(psutil.Process(os.getpid()))
            logline = '%s.%s time:%.3fs mem: %sk -> %sk (diff: %sk)' % (service_name, method, end_time - start_time, start_memory / 1024, end_memory / 1024, (end_memory - start_memory)/1024)
            if rpc_response_flag:
                odoo.netsvc.log(rpc_response, logging.DEBUG, logline, result)
            else:
                odoo.netsvc.log(rpc_request, logging.DEBUG, logline, replace_request_password(params), depth=1)

        return result
    except NO_POSTMORTEM:
        raise
    except Exception as e:
        _logger.exception(odoo.tools.exception_to_unicode(e))
        odoo.tools.debugger.post_mortem(odoo.tools.config, sys.exc_info())
        raise


