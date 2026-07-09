# -*- coding: utf-8 -*-

import jinja2
import json
import sys
import os
import re
import tempfile
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo.tools.misc import str2bool
from odoo import http
from odoo.http import dispatch_rpc, request
from odoo.service import db
from odoo.addons.web.controllers.main import Database

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.sicpro_app_administracion', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'
# ----------------------------------------------------------
# Odoo Web web Controllers
# ----------------------------------------------------------
db_monodb = http.db_monodb


class DatabaseHerencia(Database):

    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(
                d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager_db.html").render(d)

    @http.route('/web/database/dbstore/manager', type='http', auth="none")
    def manager(self, **kw):
        request._cr = None
        return self._render_template()

    @http.route('/web/database/duplicate', type='http', auth="none",
                methods=['POST'], csrf=False)
    def duplicate(self, master_pwd, name, new_name):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            if not re.match(DBNAME_PATTERN, new_name):
                raise Exception(
                    _('Invalid database name. Only alphanumerical characters, underscore, hyphen and dot are allowed.'))
            dispatch_rpc('db', 'duplicate_database',
                         [master_pwd, name, new_name])
            request._cr = None  # duplicating a database leads to an unusable cursor
            return http.local_redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database duplication error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/drop', type='http', auth="none",
                methods=['POST'], csrf=False)
    def drop(self, master_pwd, name):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            dispatch_rpc('db', 'drop', [master_pwd, name])
            request._cr = None  # dropping a database leads to an unusable cursor
            return http.local_redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database deletion error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/restore', type='http', auth="none",
                methods=['POST'], csrf=False)
    def restore(self, master_pwd, backup_file, name, copy=False):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            data_file = None
            db.check_super(master_pwd)
            with tempfile.NamedTemporaryFile(delete=False) as data_file:
                backup_file.save(data_file)
            db.restore_db(name, data_file.name, str2bool(copy))
            return http.local_redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database restore error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)
        finally:
            if data_file:
                os.unlink(data_file.name)

    @http.route('/web/database/change_password', type='http', auth="none",
                methods=['POST'], csrf=False)
    def change_password(self, master_pwd, master_pwd_new):
        try:
            dispatch_rpc('db', 'change_admin_password',
                         [master_pwd, master_pwd_new])
            return http.local_redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Master password update error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)
