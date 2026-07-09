# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
import ldap
from odoo import fields, models, _
from odoo.addons.auth_ldap.models.res_company_ldap import LDAPWrapper

_logger = logging.getLogger(__name__)

class CompanyLDAP(models.Model):
    _inherit = "res.company.ldap"

    ssl = fields.Boolean(string="Usar LDAPS", default=True)
    validar_certificado = fields.Boolean(
        string="Omitir la validación del certificado", default=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    dir_certificado = fields.Char(string='Ubicación del Certificado')

    def _get_ldap_dicts(self):
        res = super()._get_ldap_dicts()
        for data in res:
            # Buscamos el registro real en la base de datos
            record = self.browse(data.get('id'))
            if record.exists():
                # Forzamos los valores en el diccionario que usará Odoo internamente
                data['ssl'] = record.ssl
                data['validar_certificado'] = record.validar_certificado
                data['dir_certificado'] = record.dir_certificado

                if record.ssl:
                    data['ldap_tls'] = False
        return res

    def _connect(self, conf):
        if conf.get('ssl'):
            uri = "ldaps://%s:%d" % (
            conf["ldap_server"], conf["ldap_server_port"])

            # 1. Configuración Global de TLS (como en el terminal)
            if conf.get("validar_certificado"):
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,
                                ldap.OPT_X_TLS_NEVER)
            elif conf.get("dir_certificado"):
                ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,
                                conf["dir_certificado"])

            # 2. Inicializar
            connection = ldap.initialize(uri)
            connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            connection.set_option(ldap.OPT_REFERRALS, 0)
            connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)

            _logger.info("SICPRO: Conectando vía LDAPS a %s", uri)
            return LDAPWrapper(connection)

        # Si no es SSL nuestro, dejamos que Odoo haga lo de siempre
        return super()._connect(conf)

    def test_ldap_connection(self):
        self.ensure_one()
        # Construimos el diccionario completo para la prueba manual
        conf = {'ldap_server': self.ldap_server,
            'ldap_server_port': self.ldap_server_port,
            'ldap_binddn': self.ldap_binddn,
            'ldap_password': self.ldap_password, 'ldap_base': self.ldap_base,
            'ldap_tls': self.ldap_tls, 'ssl': self.ssl,
            'validar_certificado': self.validar_certificado,
            'dir_certificado': self.dir_certificado, }

        try:
            conn = self._connect(conf)
            bind_dn = self.ldap_binddn or ''
            bind_passwd = self.ldap_password or ''
            conn.simple_bind_s(bind_dn, bind_passwd)
            conn.unbind()

            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'type': 'success', 'title': '¡Conexión Exitosa!',
                    'message':
                        "SICPRO se conectó correctamente al LDAPS de ETECSA.",
                    'sticky': False, }}
        except Exception as e:
            _logger.error("SICPRO LDAP Error: %s", e)
            # Si falla nuestra lógica, intentamos la del padre como respaldo
            return super().test_ldap_connection()