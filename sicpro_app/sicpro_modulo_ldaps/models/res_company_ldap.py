# -*- coding: utf-8 -*-

import logging
import ldap

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CompanyLDAP(models.Model):
    _inherit = "res.company.ldap"
    _description = "Configuración del Certificado LDAPS"

    ssl = fields.Boolean(string="Usar LDAPS", default=True)
    validar_certificado = fields.Boolean(
        string="Omitir la validación del certificado", default=True
    )

    def _get_ldap_dicts(self):
        res = super()._get_ldap_dicts()
        for data in res:
            ldap = self.sudo().browse(data["id"])
            data["ssl"] = ldap.ssl or False
            data["validar_certificado"] = ldap.validar_certificado or False
        return res

    def _connect(self, conf):
        if conf["ssl"]:
            uri = "ldaps://%s:%d" % (conf["ldap_server"], conf["ldap_server_port"])
            connection = ldap.initialize(uri)
            if conf["validar_certificado"]:
                connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
            if conf["ldap_tls"]:
                connection.start_tls_s()
            return connection
        return super()._connect(conf)
