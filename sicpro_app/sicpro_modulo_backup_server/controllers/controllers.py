# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import os
import logging
import datetime
import pytz
import shutil
import subprocess
import tempfile
import json
import odoo
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import AccessError, UserError
from odoo.tools.misc import exec_pg_environ, find_pg_tool

_logger = logging.getLogger(__name__)

class BackupController(http.Controller):
    @http.route('/backupfile/download', type='http', auth='user')
    def file_download(self, **kwargs):
        file_path = request.httprequest.args.get('path')   # La ruta del archivo real
        backup_location = request.httprequest.args.get('backup_location') or 'local'
        _logger.info(f"=====ubicación de respaldo========= {backup_location} ====== ruta del archivo ====== {file_path}")
        try:
            
            # Asegúrese de que la ruta del archivo sea absoluta para evitar el cruce de rutas
            if '..' in file_path or not os.path.isabs(file_path):
                return Response("Invalid file path", status=400)

            file_name = file_path.split('/')[-1]
            # Abrir archivo en modo binario para transmisión
            def file_stream():
                with open(file_path, 'rb') as f:
                    while chunk := f.read(1024 * 1024 * 10):  # 10 MB chunks
                        yield chunk
                    
                # Elimine el archivo de copia de seguridad remota del servidor principal
                if backup_location == 'remote':
                    os.remove(file_path)
                        
            headers = [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{file_name}"'),
                ('Cache-Control', 'no-store, no-cache, must-revalidate'),
                ('Pragma', 'no-cache'),
                ('Expires', '0')
            ]
            
            return Response(file_stream(), headers=headers)
            
        except Exception as e:
            _logger.info(f"======= Error de descarga del archivo de copia de seguridad ======= {e} ========")
            raise UserError(e)

    @http.route('/saas/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def db_backup(self, **kwargs):
        master_pwd = kwargs.get('master_pwd')
        dbname = kwargs.get('name')
        backup_format = kwargs.get('backup_format') or 'zip'
        response = None
        user = request.env['res.users'].sudo().browse([2]) 
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        time_now = pytz.utc.localize(datetime.datetime.now()).astimezone(tz)
        ts = time_now.strftime("%m-%d-%Y-%H.%M.%S")
        filename = "%s_%s.%s" % (dbname, ts, backup_format)
        try:
            odoo.service.db.check_super(master_pwd)
            dump_stream = self.dump_db(dbname, None, backup_format)
            response = request.make_response(dump_stream)
            response.headers['Content-Disposition'] = f"attachment; filename={filename}"
            response.mimetype = 'application/octet-stream'
        except Exception as e:
            error = "Error de copia de seguridad de la base de datos: %s" % (str(e) or repr(e))
            _logger.exception('Database.backup --- %r', error)
            response = request.make_response(error)
            response.mimetype = 'text/html'

        response.headers['Backup-Filename'] = filename
        response.headers['Backup-Time'] = time_now.strftime("%m-%d-%Y-%H:%M:%S")
        return response

    def dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100, 100)
        cr.execute("SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
        modules = dict(cr.fetchall())
        manifest = {
            'odoo_dump': '1',
            'db_name': cr.dbname,
            'version': odoo.release.version,
            'version_info': odoo.release.version_info,
            'major_version': odoo.release.major_version,
            'pg_version': pg_version,
            'modules': modules,
        }
        return manifest

    # Vuelque la base de datos `db` en un objeto similar a un archivo `stream` si el flujo es Ninguno
    # devolver un objeto de archivo con el volcado
    def dump_db(self, db_name, stream, backup_format='zip'):
        _logger.info('DUMP DB: %s format %s', db_name, backup_format)

        cmd = [find_pg_tool('pg_dump'), '--no-owner', db_name]
        env = exec_pg_environ()

        if backup_format == 'zip':
            with tempfile.TemporaryDirectory() as dump_dir:
                filestore = odoo.tools.config.filestore(db_name)
                if os.path.exists(filestore):
                    shutil.copytree(filestore, os.path.join(dump_dir, 'filestore'))
                with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                    db = odoo.sql_db.db_connect(db_name)
                    with db.cursor() as cr:
                        json.dump(self.dump_db_manifest(cr), fh, indent=4)
                cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
                subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
                if stream:
                    odoo.tools.osutil.zip_dir(dump_dir, stream, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                else:
                    t=tempfile.TemporaryFile()
                    odoo.tools.osutil.zip_dir(dump_dir, t, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                    t.seek(0)
                    return t
        else:
            cmd.insert(-1, '--format=c')
            stdout = subprocess.Popen(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout
            if stream:
                shutil.copyfileobj(stdout, stream)
            else:
                return stdout
