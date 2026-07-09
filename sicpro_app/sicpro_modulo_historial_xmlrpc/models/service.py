
import threading
try:
    import psutil
except ImportError:
    psutil = None

import odoo
from odoo.service.model import security, execute_kw


def dispatch(method, params):
    (db, uid, passwd ) = params[0], int(params[1]), params[2]

    # set uid tracker - cleaned up at the WSGI
    # dispatching phase in odoo.service.wsgi_server.application
    threading.current_thread().uid = uid

    params = params[3:]
    if method == 'obj_list':
        raise NameError("obj_list has been discontinued via RPC as of 6.0, please query ir.model directly!")
    if method not in ['execute', 'execute_kw']:
        raise NameError("Method not available %s" % method)
    security.check(db,uid,passwd)
    registry = odoo.registry(db).check_signaling()
    
    fn = globals()[method]
    with registry.manage_changes():
        res = fn(db, uid, *params)
        execute_kw(db, uid, 'xml.rpc.log', 'create', [{
            'model': params[0],
            'method': params[1],
            'data': params[2],
            'return_msg': res,
            }])
    return res

odoo.service.model.dispatch = dispatch