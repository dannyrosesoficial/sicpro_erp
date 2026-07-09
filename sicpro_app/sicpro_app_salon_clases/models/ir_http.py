# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import logging
import mimetypes
import os
import re
import sys
import traceback

import werkzeug
import werkzeug.exceptions
import werkzeug.routing
import werkzeug.utils

import odoo
from odoo import api, http, models, tools, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, MissingError
from odoo.http import request, content_disposition, Response
from odoo.tools import consteq, pycompat, file_open, image_process, ustr
from odoo.tools.mimetypes import guess_mimetype
from odoo.modules.module import get_resource_path, get_module_path

from odoo.http import ALLOWED_DEBUG_MODES
from odoo.tools.misc import str2bool

from odoo.addons.web.controllers.main import HomeStaticTemplateHelpers


class SalonClasesHttp(models.AbstractModel):
    _name = 'sicpro.app.salon.clases.http'
    _description = 'Salón de Clases Http'
    _inherit = 'ir.http'

    def _get_record_and_check(self, xmlid=None, model=None, id=None,
                              field='datas', access_token=None):
        record = None
        if xmlid:
            record = self._xmlid_to_obj(self.env, xmlid)
        elif id and model in self.env:
            record = self.env[model].browse(int(id))

        if not record or field not in record:
            return None, 404

        try:
            if model == 'sicpro.app.salon.clases.adjuntos':
                record_sudo = record.sudo()
                if access_token and not consteq(record_sudo.access_token or '',
                                                access_token):
                    return None, 403
                elif (access_token and consteq(record_sudo.access_token or '',
                                               access_token)):
                    record = record_sudo
                elif record_sudo.public:
                    record = record_sudo
            try:
                if not record.env.su:
                    record._cache.clear()
                record['__last_update']
            except AccessError:
                return None, 403

            return record, 200
        except MissingError:
            return None, 404

    @classmethod
    def _binary_ir_attachment_redirect_content(cls, record,
                                               default_mimetype='application/octet-stream'):
        status = content = filename = filehash = None
        mimetype = getattr(record, 'mimetype', False)
        if record.type == 'url' and record.url:
            # if url in in the form /somehint server locally
            url_match = re.match("^/(\w+)/(.+)$", record.url)
            if url_match:
                module = url_match.group(1)
                module_path = get_module_path(module)
                module_resource_path = get_resource_path(module,
                                                         url_match.group(2))

                if module_path and module_resource_path:
                    module_path = os.path.join(os.path.normpath(module_path),
                                               '')
                    module_resource_path = os.path.normpath(
                        module_resource_path)
                    if module_resource_path.startswith(module_path):
                        with open(module_resource_path, 'rb') as f:
                            content = base64.b64encode(f.read())
                        status = 200
                        filename = os.path.basename(module_resource_path)
                        mimetype = guess_mimetype(base64.b64decode(content),
                                                  default=default_mimetype)
                        filehash = '"%s"' % hashlib.md5(
                            pycompat.to_text(content).encode(
                                'utf-8')).hexdigest()

            if not content:
                status = 301
                content = record.url

        return status, content, filename, mimetype, filehash

    def _binary_record_content(self, record, field='datas', filename=None,
            filename_field='name',
            default_mimetype='application/octet-stream'):

        model = record._name
        mimetype = 'mimetype' in record and record.mimetype or False
        content = None
        filehash = 'checksum' in record and record['checksum'] or False

        field_def = record._fields[field]
        if field_def.type == 'binary' and field_def.attachment and not field_def.related:
            if model != 'sicpro.app.salon.clases.adjuntos':
                field_attachment = self.env[
                    'sicpro.app.salon.clases.adjuntos'].sudo().search_read(
                    domain=[('res_model', '=', model),
                            ('res_id', '=', record.id),
                            ('res_field', '=', field)],
                    fields=['datas', 'mimetype', 'checksum'], limit=1)
                if field_attachment:
                    mimetype = field_attachment[0]['mimetype']
                    content = field_attachment[0]['datas']
                    filehash = field_attachment[0]['checksum']
            else:
                mimetype = record['mimetype']
                content = record['datas']
                filehash = record['checksum']

        if not content:
            content = record[field] or ''

        # filename
        default_filename = False
        if not filename:
            if filename_field in record:
                filename = record[filename_field]
            if not filename:
                default_filename = True
                filename = "%s-%s-%s" % (record._name, record.id, field)

        if not mimetype:
            try:
                decoded_content = base64.b64decode(content)
            except base64.binascii.Error:
                return (404, [], None)
            mimetype = guess_mimetype(decoded_content,
                                      default=default_mimetype)

        # extension
        _, existing_extension = os.path.splitext(filename)
        if not existing_extension or default_filename:
            extension = mimetypes.guess_extension(mimetype)
            if extension:
                filename = "%s%s" % (filename, extension)

        if not filehash:
            filehash = '"%s"' % hashlib.md5(
                pycompat.to_text(content).encode('utf-8')).hexdigest()

        status = 200 if content else 404
        return status, content, filename, mimetype, filehash

    def binary_content(self, xmlid=None,
                       model='sicpro.app.salon.clases.adjuntos', id=None,
                       field='datas', unique=False, filename=None,
                       filename_field='name', download=False, mimetype=None,
                       default_mimetype='application/octet-stream',
                       access_token=None):

        record, status = self._get_record_and_check(xmlid=xmlid, model=model,
            id=id, field=field, access_token=access_token)

        if not record:
            return status or 404, [], None

        content, headers, status = None, [], None

        if record._name == 'sicpro.app.salon.clases.adjuntos':
            status, content, filename, mimetype, filehash = self._binary_ir_attachment_redirect_content(
                record, default_mimetype=default_mimetype)
        if not content:
            status, content, filename, mimetype, filehash = self._binary_record_content(
                record, field=field, filename=filename,
                filename_field=filename_field,
                default_mimetype='application/octet-stream')

        status, headers, content = self._binary_set_headers(status, content,
            filename, mimetype, unique, filehash=filehash, download=download)

        return status, headers, content

    def _response_by_status(self, status, headers, content):
        if status == 304:
            return werkzeug.wrappers.Response(status=status, headers=headers)
        elif status == 301:
            return request.redirect(content, code=301, local=False)
        elif status != 200:
            return request.not_found()

    @api.model
    def _get_content_common(self, xmlid=None,
                            model='sicpro.app.salon.clases.adjuntos',
                            res_id=None, field='datas', unique=None,
                            filename=None, filename_field='name',
                            download=None, mimetype=None, access_token=None,
                            token=None):
        status, headers, content = self.binary_content(xmlid=xmlid,
            model=model, id=res_id, field=field, unique=unique,
            filename=filename, filename_field=filename_field,
            download=download, mimetype=mimetype, access_token=access_token)
        if status != 200:
            return self._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        return response
