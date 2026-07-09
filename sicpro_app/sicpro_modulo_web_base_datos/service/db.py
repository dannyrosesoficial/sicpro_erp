# -*- coding: utf-8 -*-

import logging
from contextlib import closing

from psycopg2 import sql

import odoo
import odoo.release
import odoo.sql_db
import odoo.tools
from odoo.service.db import list_dbs, _drop_conn, check_db_management_enabled, check_super

_logger = logging.getLogger(__name__)


@check_db_management_enabled
def exp_drop_sql(db_name):
    if db_name not in list_dbs(True):
        return False
    odoo.modules.registry.Registry.delete(db_name)
    odoo.sql_db.close_db(db_name)

    db = odoo.sql_db.db_connect('postgres')
    with closing(db.cursor()) as cr:
        # database-altering operations cannot be executed inside a transaction
        cr._cnx.autocommit = True
        _drop_conn(cr, db_name)

        try:
            cr.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(db_name)))
        except Exception as e:
            _logger.info('DROP DB: %s failed:\n%s', db_name, e)
            raise Exception("Couldn't drop database %s: %s" % (db_name, e))
        else:
            _logger.info('DROP DB: %s', db_name)

    return True


# ----------------------------------------------------------
# db service dispatch
# ----------------------------------------------------------

def dispatch_sql(method, params):
    g = globals()
    exp_method_name = 'exp_' + method
    if method in ['db_exist', 'list', 'list_lang', 'server_version']:
        return g[exp_method_name](*params)
    elif exp_method_name in g:
        passwd = params[0]
        params = params[1:]
        check_super(passwd)
        return g[exp_method_name](*params)
    else:
        raise KeyError("Method not found: %s" % method)
