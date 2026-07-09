# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import tempfile

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from lxml import html

import odoo
import odoo.modules.registry
import odoo.modules.registry
from odoo import http
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.addons.sicpro_modulo_web_base_datos.service.http import dispatch_rpc_sql
from odoo.addons.web.controllers.main import Database
from odoo.exceptions import AccessError
from odoo.http import dispatch_rpc, request, content_disposition
from odoo.service import db
from odoo.tools.misc import file_open
from odoo.tools.misc import str2bool
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'
# ----------------------------------------------------------
# Odoo Web web Controllers
# ----------------------------------------------------------
db_monodb = http.db_monodb


class WebDatabaseHerencia(Database):

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
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]

        templates = {}

        with file_open("sicpro_modulo_web_base_datos/static/src/public/database_manager.qweb.html", "r") as fd:
            template = fd.read()
        with file_open("sicpro_modulo_web_base_datos/static/src/public/database_manager.master_input.qweb.html",
                       "r") as fd:
            templates['master_input'] = fd.read()
        with file_open("sicpro_modulo_web_base_datos/static/src/public/database_manager.create_form.qweb.html",
                       "r") as fd:
            templates['create_form'] = fd.read()

        def load(template_name, options):
            return (html.fragment_fromstring(templates[template_name]), template_name)

        return qweb_render(html.document_fromstring(template), d, load=load)

    # url del gestor de base de datos
    @http.route('/web/database/dbstore/manager', type='http', auth="none")
    def manager(self, **kw):
        request._cr = None
        return self._render_template()

    # duplicar base de datos
    @http.route('/web/database/duplicate', type='http', auth="none", methods=['POST'], csrf=False)
    def duplicate(self, master_pwd, name, new_name):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            if not re.match(DBNAME_PATTERN, new_name):
                raise Exception(
                    _('Invalid database name. Only alphanumerical characters, underscore, hyphen and dot are allowed.'))
            dispatch_rpc('db', 'duplicate_database', [master_pwd, name, new_name])
            request._cr = None
            # duplicating a database leads to an unusable cursor
            return request.redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database duplication error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    #  eliminar la base de datos (sql y adjuntos)
    @http.route('/web/database/drop', type='http', auth="none", methods=['POST'], csrf=False)
    def drop(self, master_pwd, name):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            dispatch_rpc('db', 'drop', [master_pwd, name])
            request._cr = None
            # dropping a database leads to an unusable cursor
            return request.redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database deletion error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    # eliminar la base de datos (sql)
    @http.route('/web/database/drop_sql', type='http', auth="none", methods=['POST'], csrf=False)
    def drop_sql(self, master_pwd, name):
        insecure = odoo.tools.config.verify_admin_password('admin')
        print(insecure)
        print(master_pwd)
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            dispatch_rpc_sql('db', 'drop_sql', [master_pwd, name])
            request._cr = None  # dropping a database leads to an unusable cursor
            return request.redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database deletion error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    # crear backup de la base de datos
    @http.route('/web/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def backup(self, master_pwd, name, backup_format='zip'):
        insecure = odoo.tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            odoo.service.db.check_super(master_pwd)
            ts = datetime.datetime.utcnow().strftime("%d-%m-%Y_%H-%M-%S")
            filename = "%s_%s.%s" % (name, ts, backup_format)
            # Verífica el tamaño de la descarga para verificar que está completa, se agrega 'Content-Length'
            dump_stream = tempfile.TemporaryFile()
            odoo.service.db.dump_db(name, dump_stream, backup_format)
            headers = [('Content-Type', 'application/octet-stream; charset=binary'),
                ('Content-Disposition', content_disposition(filename)), ('Content-Length', dump_stream.tell()), ]
            dump_stream.seek(0)
            response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
            return response
        except Exception as e:
            _logger.exception('Database.backup')
            error = "Database backup error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    # restaurar backup de la base de datos
    @http.route('/web/database/restore', type='http', auth="none", methods=['POST'], csrf=False)
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
            return request.redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Database restore error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)
        finally:
            if data_file:
                os.unlink(data_file.name)

    # cambiar contraseña maestra de acceso
    @http.route('/web/database/change_password', type='http', auth="none", methods=['POST'], csrf=False)
    def change_password(self, master_pwd, master_pwd_new):
        try:
            dispatch_rpc('db', 'change_admin_password', [master_pwd, master_pwd_new])
            return request.redirect('/web/database/dbstore/manager')
        except Exception as e:
            error = "Master password update error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    # #  pull a gitlab para actualizar la carpeta apps
    # @http.route('/web/database/gitlab/apps', type='http', auth="none", methods=['POST'], csrf=False)
    # def pull_gitlab_apps(self, master_pwd, git_app_directorio, git_app_usuario, git_app_password):
    #     insecure = odoo.tools.config.verify_admin_password('admin')
    #     if insecure and master_pwd:
    #         dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
    #     try:
    #         print('función ejecutada apps')
    #         print(git_app_directorio)
    #         print(git_app_usuario)
    #         print(git_app_password)
    #
    #         # pull
    #         # repo = Repo(git_app_directorio)
    #         # os.environ['GIT_USERNAME'] = git_app_usuario
    #         # os.environ['GIT_PASSWORD'] = git_app_password
    #         # os.environ[
    #         #     'GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_web_base_datos/static/src/python/askpass.py'
    #         # os.environ['GIT_SSL_NO_VERIFY'] = "1"
    #         # origin = repo.remote(name="origin")
    #         # origin.pull()
    #
    #         error = "Error en la sincronización de las Apps con GitLab"
    #         return self._render_template(warnings=error)
    #
    #         # title = _("¡Sincronización realizada!")
    #         # message = _("¡La sincronización del backup se realizó correctamente!")
    #         # return {'type': 'ir.actions.client', 'tag': 'display_notification',
    #         #         'params': {'title': title, 'message': message, 'type': 'success', }}
    #
    #         #return request.redirect('/web/database/dbstore/manager')
    #     except Exception as e:
    #         error = "Error en la sincronización de las Apps con GitLab: %s" % (str(e) or repr(e))
    #         return self._render_template(error=error)
    #
    # #  pull a gitlab para actualizar la carpeta filestore
    # @http.route('/web/database/gitlab/filestore', type='http', auth="none", methods=['POST'], csrf=False)
    # def pull_gitlab_filestore(self, master_pwd, git_filestore_directorio, git_filestore_usuario, git_filestore_password):
    #     insecure = odoo.tools.config.verify_admin_password('admin')
    #     if insecure and master_pwd:
    #         dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
    #     try:
    #
    #         # pull
    #         # repo = Repo(git_filestore_directorio)
    #         # os.environ['GIT_USERNAME'] = git_filestore_usuario
    #         # os.environ['GIT_PASSWORD'] = git_filestore_password
    #         # os.environ[
    #         #     'GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_web_base_datos/static/src/python/askpass.py'
    #         # os.environ['GIT_SSL_NO_VERIFY'] = "1"
    #         # origin = repo.remote(name="origin")
    #         # origin.pull()
    #
    #         # title = _("¡Sincronización realizada!")
    #         # message = _("¡La sincronización del backup se realizó correctamente!")
    #         # return {'type': 'ir.actions.client', 'tag': 'display_notification',
    #         #         'params': {'title': title, 'message': message, 'type': 'success', }}
    #
    #         return request.redirect('/web/database/dbstore/manager')
    #     except Exception as e:
    #         error = "Error en la sincronización del Filestore GitLab: %s" % (str(e) or repr(e))
    #         return self._render_template(error=error)
