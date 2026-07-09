# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import threading

import werkzeug
import werkzeug.exceptions
import werkzeug.routing
import werkzeug.utils
import odoo
from odoo import http
from odoo import tools
from odoo.addons.base.models.assetsbundle import JavascriptAsset
from odoo.addons.base.models.ir_http import _logger, FasterRule, IrHttp
from odoo.http import ROUTING_KEYS
from odoo.modules.registry import Registry
from odoo.tools.js_transpiler import transpile_javascript
from odoo.tools.misc import submap
from . import models


# verífica la versión del sistema antes de instalar
def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import UserError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if not server_serie or not server_serie.startswith('19.'):
        raise UserError(
            'El módulo está probado para Odoo 19.x. Versión detectada: %s' % (
                    server_serie or 'desconocida'))
    return True


def _uninstall_cleanup(env):
    @property
    def content(self):
        content = super(JavascriptAsset, self).content
        if self.is_transpiled:
            if not self._converted_content:
                from odoo.tools.js_transpiler import \
                    transpile_javascript  # noqa: PLC0415
                self._converted_content = transpile_javascript(self.url,
                                                               content)
            return self._converted_content
        return content

    JavascriptAsset.content = content

    def url_init(self, httprequest):
        self.httprequest = httprequest
        self.future_response = http.FutureResponse()
        self.dispatcher = http._dispatchers['http'](self)  # until we match
        # self.params = {}  # set by the Dispatcher

        self.geoip = http.GeoIP(httprequest.remote_addr)
        self.registry = None
        self.env = None

    http.Request.__init__ = url_init

    @tools.ormcache('key', cache='routing')
    def routing_map(self, key=None):
        _logger.info("Generating routing map for key %s", str(key))
        registry = Registry(threading.current_thread().dbname)
        installed = registry._init_modules.union(
            odoo.tools.config['server_wide_modules'])
        mods = sorted(installed)
        # Note : when routing map is generated, we put it on the class `cls`
        # to make it available for all instance. Since `env` create an new instance
        # of the model, each instance will regenared its own routing map and thus
        # regenerate its EndPoint. The routing map should be static.
        routing_map = werkzeug.routing.Map(strict_slashes=False,
                                           converters=self._get_converters())
        for url, endpoint in self._generate_routing_rules(mods,
                                                          converters=self._get_converters()):
            routing = submap(endpoint.routing, ROUTING_KEYS)
            if routing['methods'] is not None and 'OPTIONS' not in routing[
                'methods']:
                routing['methods'] = [*routing['methods'], 'OPTIONS']
            rule = FasterRule(url, endpoint=endpoint, **routing)
            rule.merge_slashes = False
            routing_map.add(rule)
        return routing_map

    IrHttp.routing_map = routing_map
    env['ir.http'].env.registry.clear_cache("routing")
    env['ir.attachment'].regenerate_assets_bundles()
