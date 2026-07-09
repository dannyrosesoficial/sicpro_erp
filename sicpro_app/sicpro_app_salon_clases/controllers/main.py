# -*- coding: utf-8 -*-


import base64
import functools
import json
import unicodedata
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from odoo.tools import pycompat
from odoo.tools.translate import _
from odoo import http
from odoo.http import request, serialize_exception as _serialize_exception, \
    _logger


def clean(name): return name.replace('\x3c', '')


def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            _logger.exception("An exception occurred during an http request")
            se = _serialize_exception(e)
            error = {'code': 200, 'message': "Odoo Server Error", 'data': se}
            return werkzeug.exceptions.InternalServerError(json.dumps(error))

    return wrap


class BinarySalon(http.Controller):
    @http.route(
        ['/salon_clases/content', '/salon_clases/content/<string:xmlid>',
         '/salon_clases/content/<string:xmlid>/<string:filename>',
         '/salon_clases/content/<int:id>',
         '/salon_clases/content/<int:id>/<string:filename>',
         '/salon_clases/content/<string:model>/<int:id>/<string:field>',
         '/salon_clases/content/<string:model>/<int:id>/<string:field>/<string:filename>'],
        type='http', auth="public")
    def content_common(self, xmlid=None,
                       model='sicpro.app.salon.clases.adjuntos', id=None,
                       field='datas', filename=None, filename_field='name',
                       unique=None, mimetype=None, download=None, data=None,
                       token=None, access_token=None, **kw):

        return request.env['sicpro.app.salon.clases.http']._get_content_common(
            xmlid=xmlid, model=model, res_id=id, field=field, unique=unique,
            filename=filename, filename_field=filename_field,
            download=download, mimetype=mimetype, access_token=access_token,
            token=token)

    @http.route('/salon_clases/binary/upload', type='http', auth="user")
    @serialize_exception
    def upload(self, ufile, callback=None):
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        try:
            data = ufile.read()
            args = [len(data), ufile.filename, ufile.content_type,
                    pycompat.to_text(base64.b64encode(data))]
        except Exception as e:
            args = [False, str(e)]
        return out % (json.dumps(clean(callback)),
                      json.dumps(args)) if callback else json.dumps(args)

    @http.route('/salon_clases/binary/upload_attachment', type='http',
                auth="user")
    @serialize_exception
    def upload_attachment(self, model, id, ufile, callback=None):
        files = request.httprequest.files.getlist('ufile')
        Model = request.env['sicpro.app.salon.clases.adjuntos']
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        args = []
        for ufile in files:

            filename = ufile.filename
            if request.httprequest.user_agent.browser == 'safari':
                filename = unicodedata.normalize('NFD', ufile.filename)

            try:
                attachment = Model.create({'name': filename,
                                           'datas': base64.encodebytes(
                                               ufile.read()),
                                           'res_model': model,
                                           'res_id': int(id)})
                attachment._post_add_create()
            except Exception:
                args.append({'error': _("Something horrible happened")})
                _logger.exception(
                    "Fail to upload attachment %s" % ufile.filename)
            else:
                args.append({'filename': clean(filename),
                             'mimetype': ufile.content_type,
                             'id': attachment.id,
                             'size': attachment.file_size})
        return out % (json.dumps(clean(callback)),
                      json.dumps(args)) if callback else json.dumps(args)
