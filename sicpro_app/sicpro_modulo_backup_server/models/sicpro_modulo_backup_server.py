# -*- coding: utf-8 -*-


import datetime
import errno
import ftplib
import json
import logging
import os
import shutil
import tempfile
from datetime import timedelta
from random import randint

import dropbox
import paramiko
import requests
from git import Repo
from werkzeug import urls

import odoo
from odoo import models, fields, api, _
from odoo import tools
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.service import db

_logger = logging.getLogger(__name__)

ONEDRIVE_SCOPE = ['offline_access openid Files.ReadWrite.All']
MICROSOFT_GRAPH_END_POINT = "https://graph.microsoft.com"
GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_API_BASE_URL = 'https://www.googleapis.com'


class AutoDatabaseBackup(models.Model):
    _name = 'sicpro.modulo.backup.server.local'
    _description = 'Copia de seguridad automática de la base de datos'

    def _default_db_name(self):
        return self._cr.dbname

    name = fields.Char(string='Nombre', required=True)
    db_name = fields.Char(string='Base de Datos', default=_default_db_name, required=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    master_pwd = fields.Char(string='Contraseña maestra', required=False)
    tipo_backup = fields.Selection([('backup', 'Backup'), ('sincronizar', 'Sincronizar')], string='Tipo de Acción',
                                   compute='_tipo_backup_destination', required=True)
    backup_format = fields.Selection([('zip', 'Zip'), ('dump', 'Dump')], string='Formato del Backup', default='zip',
                                     required=True)
    backup_destination = fields.Selection(
        [('local', 'Almacenamiento local'), ('google_drive', 'Google Drive'), ('ftp', 'FTP'), ('sftp', 'SFTP'),
         ('dropbox', 'Dropbox'), ('gitlab', 'GitLab'), ('onedrive', 'Onedrive')], string='Destino del Backup')
    backup_path = fields.Char(string='Ruta de respaldo', help='Ruta del directorio de almacenamiento local')
    sftp_host = fields.Char(string='Host SFTP')
    sftp_port = fields.Char(string='Puerto SFTP', default=22)
    sftp_user = fields.Char(string='Usuario SFTP', copy=False)
    sftp_password = fields.Char(string='Contraseña SFTP', copy=False)
    sftp_path = fields.Char(string='Ruta SFTP')
    ftp_host = fields.Char(string='Host FTP')
    ftp_port = fields.Char(string='Puerto FTP', default=21)
    ftp_user = fields.Char(string='Usuario FTP', copy=False)
    ftp_password = fields.Char(string='Contraseña FTP', copy=False)
    ftp_path = fields.Char(string='Ruta FTP')
    dropbox_client_id = fields.Char(string='Dropbox Cliente ID', copy=False)
    dropbox_client_secret = fields.Char(string='Dropbox Cliente Secret', copy=False)
    dropbox_refresh_token = fields.Char(string='Dropbox Refresh Token', copy=False)
    is_dropbox_token_generated = fields.Boolean(string='Dropbox Token Generado',
                                                compute='_compute_is_dropbox_token_generated', copy=False)
    dropbox_folder = fields.Char('Dropbox Carpeta')
    active = fields.Boolean(string='Activo', default=True)
    auto_remove = fields.Boolean(string='Eliminar copias de seguridad antiguas')
    days_to_remove = fields.Integer(string='Quitar después',
                                    help='Eliminar automáticamente las copias de seguridad almacenadas después de '
                                         'este número de días especificado')
    google_drive_folderid = fields.Char(string='Drive Carpeta ID')
    notify_user = fields.Boolean(string='Notificar al usuario',
                                 help='Envíe una notificación por correo electrónico al usuario cuando la operación de'
                                      ' respaldo sea exitosa o falle')
    user_id = fields.Many2one('res.users', string='Usuario a Notificar')
    backup_filename = fields.Char(string='Nombre de la copia de seguridad',
                                  help='Para almacenar el nombre de archivo de copia de seguridad generado')
    generated_exception = fields.Char(string='Excepción',
                                      help='Se encontró una excepción durante la generación de la copia de seguridad')
    onedrive_client_id = fields.Char(string='Onedrive Cliente ID', copy=False)
    onedrive_client_secret = fields.Char(string='Onedrive Cliente Secret', copy=False)
    onedrive_access_token = fields.Char(string='Onedrive Access Token', copy=False)
    onedrive_refresh_token = fields.Char(string='Onedrive Refresh Token', copy=False)
    onedrive_token_validity = fields.Datetime(string='Onedrive Token Validación', copy=False)
    onedrive_folder_id = fields.Char(string='Carpeta ID')
    is_onedrive_token_generated = fields.Boolean(string='onedrive Tokens Generado',
                                                 compute='_compute_is_onedrive_token_generated', copy=False)
    gdrive_refresh_token = fields.Char(string='Google drive Refresh Token', copy=False)
    gdrive_access_token = fields.Char(string='Google drive Access Token', copy=False)
    is_google_drive_token_generated = fields.Boolean(string='Google drive Token Generated',
                                                     compute='_compute_is_google_drive_token_generated', copy=False)
    gdrive_client_id = fields.Char(string='Google Drive Cliente ID', copy=False)
    gdrive_client_secret = fields.Char(string='Google Drive Cliente Secret', copy=False)
    gdrive_token_validity = fields.Datetime(string='Google Drive Token Validación', copy=False)
    gdrive_redirect_uri = fields.Char(string='Google Drive Redirect URI', compute='_compute_redirect_uri')
    onedrive_redirect_uri = fields.Char(string='Onedrive Redirect URI', compute='_compute_redirect_uri')

    gitlab_conector = fields.Many2one(comodel_name='sicpro.modulo.api.conector', string='API Conector ID',
                                      required=False)
    gitlab_usuario = fields.Char(string='Usuario', related='gitlab_conector.usuario', required=False)
    gitlab_password = fields.Char(string='Contraseña', related='gitlab_conector.password', required=False)
    gitlab_url = fields.Char(string='Url', related='gitlab_conector.url_data', required=False)
    gitlab_proyecto = fields.Char(string='Proyecto', related='gitlab_conector.url_config_data', required=False)
    gitlab_rama = fields.Char(string='Rama', required=False)
    gitlab_directorio = fields.Char(string='Directorio', required=False)

    @api.onchange('backup_destination')
    def _tipo_backup_destination(self):
        for item in self:
            if item.backup_destination == 'gitlab':
                item.tipo_backup = 'sincronizar'
            else:
                item.tipo_backup = 'backup'

    @api.depends('backup_destination')
    def _compute_redirect_uri(self):
        for rec in self:
            base_url = request.env['ir.config_parameter'].get_param('web.base.url')
            rec.onedrive_redirect_uri = base_url + '/onedrive/authentication'
            rec.gdrive_redirect_uri = base_url + '/google_drive/authentication'

    # Establezca True si se genera el token de actualización de Google Drive
    @api.depends('gdrive_access_token', 'gdrive_refresh_token')
    def _compute_is_google_drive_token_generated(self):
        for rec in self:
            rec.is_google_drive_token_generated = bool(rec.gdrive_access_token) and bool(rec.gdrive_refresh_token)

    # Generar código de autorización de Google Drive
    def action_get_gdrive_auth_code(self):
        action = self.env["ir.actions.act_window"].sudo()._for_xml_id(
            "sicpro_modulo_backup_server.action_view_backup_server")
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url_return = base_url + '/web#id=%d&action=%d&view_type=form&model=%s' % (
        self.id, action['id'], 'sicpro.modulo.backup.server.local')
        state = {'backup_config_id': self.id, 'url_return': url_return}
        encoded_params = urls.url_encode({'response_type': 'code', 'client_id': self.gdrive_client_id,
            'scope': 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file',
            'redirect_uri': base_url + '/google_drive/authentication', 'access_type': 'offline',
            'state': json.dumps(state), 'approval_prompt': 'force', })
        auth_url = "%s?%s" % (GOOGLE_AUTH_ENDPOINT, encoded_params)
        return {'type': 'ir.actions.act_url', 'target': 'self', 'url': auth_url, }

    # generar token de acceso a Google Drive a partir del token de actualización si ha caducado
    def generate_gdrive_refresh_token(self):
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {'refresh_token': self.gdrive_refresh_token, 'client_id': self.gdrive_client_id,
            'client_secret': self.gdrive_client_secret, 'grant_type': 'refresh_token', }
        try:
            res = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({'gdrive_access_token': response.get('access_token'),
                    'gdrive_token_validity': fields.Datetime.now() + timedelta(
                        seconds=expires_in) if expires_in else False, })
        except requests.HTTPError as error:
            error_key = error.response.json().get("error", "nc")
            error_msg = _("Ocurrió un error al generar el token. Su código de autorización puede no ser válido o "
                          "ya ha caducado [%s]. "
                          "Debe verificar su ID de cliente y su secreto en la plataforma de API de Google o intentar detener y"
                          " reiniciar la sincronización de su calendario..", error_key)
            raise UserError(error_msg)

    # Genere tokens de onedrive a partir del código de autorización
    def get_gdrive_tokens(self, authorize_code):
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {'code': authorize_code, 'client_id': self.gdrive_client_id, 'client_secret': self.gdrive_client_secret,
            'grant_type': 'authorization_code', 'redirect_uri': base_url + '/google_drive/authentication'}
        try:
            res = requests.post(GOOGLE_TOKEN_ENDPOINT, params=data, headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({'gdrive_access_token': response.get('access_token'),
                    'gdrive_refresh_token': response.get('refresh_token'),
                    'gdrive_token_validity': fields.Datetime.now() + timedelta(
                        seconds=expires_in) if expires_in else False, })
        except requests.HTTPError:
            error_msg = _("Algo salió mal durante la generación de tokens. "
                          "Tal vez su código de autorización no sea válido")
            raise UserError(error_msg)

    # Establecer verdadero si se generan tokens de onedrive
    @api.depends('onedrive_access_token', 'onedrive_refresh_token')
    def _compute_is_onedrive_token_generated(self):
        for rec in self:
            rec.is_onedrive_token_generated = bool(rec.onedrive_access_token) and bool(rec.onedrive_refresh_token)

    # Establezca True si se genera el token de actualización de Dropbox
    @api.depends('dropbox_refresh_token')
    def _compute_is_dropbox_token_generated(self):
        for rec in self:
            rec.is_dropbox_token_generated = bool(rec.dropbox_refresh_token)

    # Abra un asistente para configurar el código de autorización de Dropbox
    def action_get_dropbox_auth_code(self):
        return {'type': 'ir.actions.act_window', 'name': 'Dropbox Authorization Wizard',
            'res_model': 'sicpro.modulo.backup.dropbox.auth', 'view_mode': 'form', 'target': 'new', }

    # Generar código de autorización de onedrive
    def action_get_onedrive_auth_code(self):
        AUTHORITY = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        action = self.env["ir.actions.act_window"].sudo()._for_xml_id(
            "sicpro_modulo_backup_server.action_view_backup_server")
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url_return = base_url + '/web#id=%d&action=%d&view_type=form&model=%s' % (
        self.id, action['id'], 'sicpro.modulo.backup.server.local')
        state = {'backup_config_id': self.id, 'url_return': url_return}
        encoded_params = urls.url_encode(
            {'response_type': 'code', 'client_id': self.onedrive_client_id, 'state': json.dumps(state),
                'scope': ONEDRIVE_SCOPE, 'redirect_uri': base_url + '/onedrive/authentication', 'prompt': 'consent',
                'access_type': 'offline'})
        auth_url = "%s?%s" % (AUTHORITY, encoded_params)
        return {'type': 'ir.actions.act_url', 'target': 'self', 'url': auth_url, }

    # generar token de acceso de onedrive a partir del token de actualización si caduca
    def generate_onedrive_refresh_token(self):
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        data = {'client_id': self.onedrive_client_id, 'client_secret': self.onedrive_client_secret,
            'scope': ONEDRIVE_SCOPE, 'grant_type': "refresh_token",
            'redirect_uri': base_url + '/onedrive/authentication', 'refresh_token': self.onedrive_refresh_token}
        try:
            res = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=data,
                                headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({'onedrive_access_token': response.get('access_token'),
                    'onedrive_refresh_token': response.get('refresh_token'),
                    'onedrive_token_validity': fields.Datetime.now() + timedelta(
                        seconds=expires_in) if expires_in else False, })
        except requests.HTTPError as error:
            _logger.exception("Bad microsoft onedrive request : %s !", error.response.content)
            raise error

    # Genere tokens de onedrive a partir del código de autorización
    def get_onedrive_tokens(self, authorize_code):
        headers = {"content-type": "application/x-www-form-urlencoded"}
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        data = {'code': authorize_code, 'client_id': self.onedrive_client_id,
            'client_secret': self.onedrive_client_secret, 'grant_type': 'authorization_code', 'scope': ONEDRIVE_SCOPE,
            'redirect_uri': base_url + '/onedrive/authentication'}
        try:
            res = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=data,
                                headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({'onedrive_access_token': response.get('access_token'),
                    'onedrive_refresh_token': response.get('refresh_token'),
                    'onedrive_token_validity': fields.Datetime.now() + timedelta(
                        seconds=expires_in) if expires_in else False, })
        except requests.HTTPError as error:
            _logger.exception("Bad microsoft onedrive request : %s !", error.response.content)
            raise error

    # Devolver URL de autorización de Dropbox
    def get_dropbox_auth_url(self):
        dbx_auth = dropbox.oauth.DropboxOAuth2FlowNoRedirect(self.dropbox_client_id, self.dropbox_client_secret,
                                                             token_access_type='offline')
        auth_url = dbx_auth.start()
        return auth_url

    # Genere y configure el token de actualización de Dropbox a partir del código de autorización
    def set_dropbox_refresh_token(self, auth_code):
        dbx_auth = dropbox.oauth.DropboxOAuth2FlowNoRedirect(self.dropbox_client_id, self.dropbox_client_secret,
                                                             token_access_type='offline')
        outh_result = dbx_auth.finish(auth_code)
        self.dropbox_refresh_token = outh_result.refresh_token

    # Válida el nombre de la base de datos y la contraseña maestra ingresada
    @api.constrains('db_name')
    def _check_db_credentials(self):
        database_list = db.list_dbs()
        if self.db_name not in database_list:
            raise ValidationError(_("Nombre de base de datos no válido!"))
        try:
            odoo.service.db.check_super(self.master_pwd)
        except Exception:
            raise ValidationError(_("Contraseña maestra no válida!"))

    # Prueba la conexión sftp y ftp usando las credenciales ingresadas
    def test_connection(self):
        if self.backup_destination == 'sftp':
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(hostname=self.sftp_host, username=self.sftp_user, password=self.sftp_password,
                               port=self.sftp_port)
                sftp = client.open_sftp()
                sftp.close()
            except Exception as e:
                raise UserError(_("SFTP Excepción: %s", e))
            finally:
                client.close()
        elif self.backup_destination == 'ftp':
            try:
                ftp_server = ftplib.FTP()
                ftp_server.connect(self.ftp_host, int(self.ftp_port))
                ftp_server.login(self.ftp_user, self.ftp_password)
                ftp_server.quit()
            except Exception as e:
                raise UserError(_("FTP Excepción: %s", e))
        title = _("Prueba de conexión exitosa!")
        message = _("Todo parece estar correctamente configurado!")
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
            'params': {'title': title, 'message': message, 'sticky': False, }}

    # inicializo la carpeta git que sera sincronizada
    # si ya esta inicializado solo lanzo el aviso
    def inicializar_repositorio_git(self):
        try:
            repo = Repo(self.gitlab_directorio)
            rama_activa = str(repo.active_branch)
            if rama_activa == self.gitlab_rama:
                # notifico que el directorio está inicializado.
                title = _("¡El directorio ya está inicializado!")
                message = _("Todo parece estar correctamente configurado!")
                return {'type': 'ir.actions.client', 'tag': 'display_notification',
                        'params': {'title': title, 'message': message, 'type': 'warning', }}
            else:
                # notifico que el directorio está inicializado con otra rama.
                title = _("¡El directorio está inicializado con una rama diferente!")
                message = _("Verifique que este correctamente configurado!")
                return {'type': 'ir.actions.client', 'tag': 'display_notification',
                        'params': {'title': title, 'message': message, 'type': 'danger', }}

        except Exception:
            # Creo la carpeta temporal para clonar el repositorio de gitlab
            dir_temporal = '/opt/odoo/sicpro_erp/temp/git_clone/'
            nombre_temporal = str(randint(1000, 10000))
            carpeta_temporal = dir_temporal + nombre_temporal
            # modifico los valores generales de git del servidor
            os.environ['GIT_USERNAME'] = self.gitlab_usuario
            os.environ['GIT_PASSWORD'] = self.gitlab_password
            os.environ[
                'GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_backup_server/static/src/python/askpass.py'
            os.environ['GIT_SSL_NO_VERIFY'] = "1"
            repo_gitlab = self.gitlab_url + self.gitlab_proyecto + '.git'
            Repo.clone_from(repo_gitlab, carpeta_temporal, branch=self.gitlab_rama)

            # copiar la carpeta .git al directorio seleccionado
            shutil.move(carpeta_temporal + '/.git', self.gitlab_directorio + '/.git')
            # eliminar la carpeta .git temporal
            shutil.rmtree(carpeta_temporal)

            # notifico que la inicialización del directorio se realizó correctamente
            title = _("Directorio inicializado correctamente!")
            message = _("Todo parece estar correctamente configurado!")
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': title, 'message': message, 'type': 'success', }}

    # Prueba la configuración git
    def test_connection_git(self):
        try:
            repo = Repo(self.gitlab_directorio)
            os.environ['GIT_USERNAME'] = self.gitlab_usuario
            os.environ['GIT_PASSWORD'] = self.gitlab_password
            os.environ['GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_backup_server/static/src/python/askpass.py'
            os.environ['GIT_SSL_NO_VERIFY'] = "1"
            origin = repo.remote(name="origin")
            pull = origin.pull()
        except (OSError, Exception) as err:
            raise ValidationError(_("Conexión fallida, intente reinicializar el repositorio o verifique las "
                                    "credenciales de acceso. Error: %s", tools.ustr(err)))

        if origin.exists():
            title = _("Prueba de conexión exitosa!")
            message = _("Todo parece estar correctamente configurado!")
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': title, 'message': message, 'type': 'success', }}

    # realizar la sincronización manual del backup
    def gitlab_sincronizar_manual(self):
        try:
            for item in self:
                # commit
                backup_time = datetime.datetime.utcnow().strftime("%d-%m-%Y_%H:%M:%S")
                repo = Repo(item.gitlab_directorio)
                repo.git.add(item.gitlab_directorio)
                repo.index.commit("Sync: db: " + item.db_name + '/fecha: ' + backup_time)

                # push
                repo = Repo(self.gitlab_directorio)
                os.environ['GIT_USERNAME'] = item.gitlab_usuario
                os.environ['GIT_PASSWORD'] = item.gitlab_password
                os.environ['GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_backup_server/static/src/python/askpass.py'
                os.environ['GIT_SSL_NO_VERIFY'] = "1"
                origin = repo.remote(name="origin")
                origin.push()

                title = _("¡Sincronización realizada!")
                message = _("¡La sincronización del backup se realizó correctamente!")
                return {'type': 'ir.actions.client', 'tag': 'display_notification',
                        'params': {'title': title, 'message': message, 'type': 'success', }}

        except (OSError, Exception) as err:
            raise ValidationError(_("La sincronización del backup ha fallado. Error: %s", tools.ustr(err)))

    # Cron para generar y almacenar copias de seguridad
    # Se creará una copia de seguridad de la base de datos para todos los registros activos en el modelo
    # de configuración de copias de seguridad
    def _schedule_auto_backup(self):
        records = self.search([])
        mail_template_success = self.env.ref('sicpro_modulo_backup_server.mail_template_data_db_backup_successful')
        mail_template_failed = self.env.ref('sicpro_modulo_backup_server.mail_template_data_db_backup_failed')
        for rec in records:
            backup_time = datetime.datetime.utcnow().strftime("%d-%m-%Y_%H:%M:%S")
            backup_filename = "%s_%s.%s" % (rec.db_name, backup_time, rec.backup_format)
            rec.backup_filename = backup_filename
            # Local backup
            if rec.backup_destination == 'local':
                try:
                    if not os.path.isdir(rec.backup_path):
                        os.makedirs(rec.backup_path)
                    backup_file = os.path.join(rec.backup_path, backup_filename)
                    f = open(backup_file, "wb")
                    odoo.service.db.dump_db(rec.db_name, f, rec.backup_format)
                    f.close()
                    # remove older backups
                    if rec.auto_remove:
                        for filename in os.listdir(rec.backup_path):
                            file = os.path.join(rec.backup_path, filename)
                            create_time = datetime.datetime.fromtimestamp(os.path.getctime(file))
                            backup_duration = datetime.datetime.utcnow() - create_time
                            if backup_duration.days >= rec.days_to_remove:
                                os.remove(file)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('FTP Excepción: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # FTP backup
            elif rec.backup_destination == 'ftp':
                try:
                    ftp_server = ftplib.FTP()
                    ftp_server.connect(rec.ftp_host, int(rec.ftp_port))
                    ftp_server.login(rec.ftp_user, rec.ftp_password)
                    ftp_server.encoding = "utf-8"
                    temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                    try:
                        ftp_server.cwd(rec.ftp_path)
                    except ftplib.error_perm:
                        ftp_server.mkd(rec.ftp_path)
                        ftp_server.cwd(rec.ftp_path)
                    with open(temp.name, "wb+") as tmp:
                        odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                    ftp_server.storbinary('STOR %s' % backup_filename, open(temp.name, "rb"))
                    if rec.auto_remove:
                        files = ftp_server.nlst()
                        for f in files:
                            create_time = datetime.datetime.strptime(ftp_server.sendcmd('MDTM ' + f)[4:],
                                                                     "%Y%m%d%H%M%S")
                            diff_days = (datetime.datetime.now() - create_time).days
                            if diff_days >= rec.days_to_remove:
                                ftp_server.delete(f)
                    ftp_server.quit()
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('FTP Exception: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # SFTP backup
            elif rec.backup_destination == 'sftp':
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    client.connect(hostname=rec.sftp_host, username=rec.sftp_user, password=rec.sftp_password,
                                   port=rec.sftp_port)
                    sftp = client.open_sftp()
                    temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                    with open(temp.name, "wb+") as tmp:
                        odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                    try:
                        sftp.chdir(rec.sftp_path)
                    except IOError as e:
                        if e.errno == errno.ENOENT:
                            sftp.mkdir(rec.sftp_path)
                            sftp.chdir(rec.sftp_path)
                    sftp.put(temp.name, backup_filename)
                    if rec.auto_remove:
                        files = sftp.listdir()
                        expired = list(filter(lambda fl: (datetime.datetime.now() - datetime.datetime.fromtimestamp(
                            sftp.stat(fl).st_mtime)).days >= rec.days_to_remove, files))
                        for file in expired:
                            sftp.unlink(file)
                    sftp.close()
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('SFTP Excepción: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
                finally:
                    client.close()
            # Google Drive backup
            elif rec.backup_destination == 'google_drive':
                if rec.gdrive_token_validity <= fields.Datetime.now():
                    rec.generate_gdrive_refresh_token()
                temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                with open(temp.name, "wb+") as tmp:
                    odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                try:
                    # access_token = self.env['google.drive.config'].sudo().get_access_token()
                    headers = {"Authorization": "Bearer %s" % rec.gdrive_access_token}
                    para = {"name": backup_filename, "parents": [rec.google_drive_folderid], }
                    files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                        'file': open(temp.name, "rb")}
                    requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                        headers=headers, files=files)
                    if rec.auto_remove:
                        query = "parents = '%s'" % rec.google_drive_folderid
                        files_req = requests.get("https://www.googleapis.com/drive/v3/files?q=%s" % query,
                                                 headers=headers)
                        files = files_req.json()['files']
                        for file in files:
                            file_date_req = requests.get(
                                "https://www.googleapis.com/drive/v3/files/%s?fields=createdTime" % file['id'],
                                headers=headers)
                            create_time = file_date_req.json()['createdTime'][:19].replace('T', ' ')
                            diff_days = (datetime.datetime.now() - datetime.datetime.strptime(create_time,
                                                                                              '%Y-%m-%d %H:%M:%S')).days
                            if diff_days >= rec.days_to_remove:
                                requests.delete("https://www.googleapis.com/drive/v3/files/%s" % file['id'],
                                                headers=headers)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('Google Drive Excepción: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # Dropbox backup
            elif rec.backup_destination == 'dropbox':
                temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                with open(temp.name, "wb+") as tmp:
                    odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                try:
                    dbx = dropbox.Dropbox(app_key=rec.dropbox_client_id, app_secret=rec.dropbox_client_secret,
                                          oauth2_refresh_token=rec.dropbox_refresh_token)
                    dropbox_destination = rec.dropbox_folder + '/' + backup_filename
                    dbx.files_upload(temp.read(), dropbox_destination)
                    if rec.auto_remove:
                        files = dbx.files_list_folder(rec.dropbox_folder)
                        file_entries = files.entries
                        expired_files = list(
                            filter(lambda fl: (datetime.datetime.now() - fl.client_modified).days >= rec.days_to_remove,
                                   file_entries))
                        for file in expired_files:
                            dbx.files_delete_v2(file.path_display)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as error:
                    rec.generated_exception = error
                    _logger.info('Dropbox Excepción: %s', error)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # Onedrive Backup
            elif rec.backup_destination == 'onedrive':
                if rec.onedrive_token_validity <= fields.Datetime.now():
                    rec.generate_onedrive_refresh_token()
                temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                with open(temp.name, "wb+") as tmp:
                    odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                headers = {'Authorization': 'Bearer %s' % rec.onedrive_access_token, 'Content-Type': 'application/json'}
                upload_session_url = MICROSOFT_GRAPH_END_POINT + "/v1.0/me/drive/items/%s:/%s:/createUploadSession" % (
                rec.onedrive_folder_id, backup_filename)
                try:
                    upload_session = requests.post(upload_session_url, headers=headers)
                    upload_url = upload_session.json().get('uploadUrl')
                    requests.put(upload_url, data=temp.read())
                    if rec.auto_remove:
                        list_url = MICROSOFT_GRAPH_END_POINT + "/v1.0/me/drive/items/%s/children" % rec.onedrive_folder_id
                        response = requests.get(list_url, headers=headers)
                        files = response.json().get('value')
                        for file in files:
                            create_time = file['createdDateTime'][:19].replace('T', ' ')
                            diff_days = (datetime.datetime.now() - datetime.datetime.strptime(create_time,
                                                                                              '%Y-%m-%d %H:%M:%S')).days
                            if diff_days >= rec.days_to_remove:
                                delete_url = MICROSOFT_GRAPH_END_POINT + "/v1.0/me/drive/items/%s" % file['id']
                                requests.delete(delete_url, headers=headers)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as error:
                    rec.generated_exception = error
                    _logger.info('Onedrive Excepción: %s', error)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # Gitlab Backup
            elif rec.backup_destination == 'gitlab':
                try:
                    # commit
                    repo = Repo(rec.gitlab_directorio)
                    repo.git.add(rec.gitlab_directorio)
                    repo.index.commit("Sync: db: " + rec.db_name + '/fecha: ' + backup_time)
                    # push
                    repo = Repo(rec.gitlab_directorio)
                    os.environ['GIT_USERNAME'] = rec.gitlab_usuario
                    os.environ['GIT_PASSWORD'] = rec.gitlab_password
                    os.environ[
                        'GIT_ASKPASS'] = '/opt/odoo/sicpro_erp/apps/sicpro_modulo_backup_server/static/src/python/askpass.py'
                    os.environ['GIT_SSL_NO_VERIFY'] = "1"
                    origin = repo.remote(name="origin")
                    origin.push()
                    # envío el correo de notificación
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as error:
                    rec.generated_exception = error
                    _logger.info('GitLab Excepción: %s', error)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
