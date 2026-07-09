# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from base64 import b64decode
from datetime import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, \
    NoEncryption, PrivateFormat, pkcs12
from pytz import timezone
from odoo import api, fields, models, tools
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class AdministrarCertificadosDigitales(models.Model):
    _name = 'sicpro.modulo.certificados.digitales'
    _description = 'Gestión de control de los certificados digitales'
    _order = 'date_start desc, id desc'
    _rec_name = 'date_start'

    content = fields.Binary(string="Certificado", required=True,
                            help="Certificado PFX o P12")
    clave_privada = fields.Many2many('ir.attachment',
                                     'certificados_digitales_clave_privada_rel',
                                     string="Clave Privada", required=False, )
    clave_publica = fields.Many2many('ir.attachment',
                                     'certificados_digitales_clave_publica_rel',
                                     string="Clave Publica", required=False, )
    password = fields.Char(string="Contraseña", required=True)
    date_start = fields.Datetime(string="Fecha inicio", readonly=True,
                                 help="La fecha en la que el certificado comienza a ser válido.")
    date_end = fields.Datetime(string="Fecha fin", readonly=True,
                               help="La fecha en la que caduca el certificado.")
    company_id = fields.Many2one(string='Proceso', comodel_name='res.company',
                                 required=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Active', required=False, default=True, index=True)

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    @api.model
    def _get_es_current_datetime(self):
        return datetime.now(timezone('Europe/Madrid'))

    # extraigo los datos del certificado digital
    @tools.ormcache('self.content', 'self.password')
    def _decode_certificate(self):
        self.ensure_one()

        if not self.password:
            return None, None, None

        private_key, certificado, dummy = pkcs12.load_key_and_certificates(
            b64decode(self.content), self.password.encode(),
            backend=default_backend(), )

        clave_publica = certificado.public_bytes(Encoding.PEM)
        clave_privada = private_key.private_bytes(Encoding.PEM,
                                                  format=PrivateFormat.TraditionalOpenSSL,
                                                  encryption_algorithm=NoEncryption(), )
        return clave_publica, clave_privada, certificado

    @api.model
    def create(self, vals):
        record = super().create(vals)

        spain_tz = timezone('Europe/Madrid')
        spain_dt = self._get_es_current_datetime()
        try:
            clave_publica, clave_privada, certificado = record._decode_certificate()
            cert_date_start = spain_tz.localize(certificado.not_valid_before)
            cert_date_end = spain_tz.localize(certificado.not_valid_after)
        except Exception:
            raise ValidationError(
                "Ha habido un problema con el certificado, algunos problemas habituales pueden ser:\n"
                "- La contraseña proporcionada o el certificado no son válidos.\n"
                "- El contenido del certificado no es válido.\n\n" + MSG_SOPORTE_SICPRO)

        # creo el registro de la clave publica en el filestore
        attachment_publica = self.env['ir.attachment'].create(
            {'name': 'clave_publica.pem', 'datas': clave_publica,
             'res_model': 'sicpro.modulo.certificados.digitales',
             'res_id': record['id'], 'type': 'binary',
             'mimetype': 'application/pem-certificate-chain', })

        # creo el registro de la clave publica en el filestore
        attachment_privada = self.env['ir.attachment'].create(
            {'name': 'clave_privada.pem', 'datas': clave_privada,
             'res_model': 'sicpro.modulo.certificados.digitales',
             'res_id': record['id'], 'type': 'binary',
             'mimetype': 'application/pem-certificate-chain', })

        # Asignar valores extraídos del certificado
        record.write({'date_start': fields.Datetime.to_string(cert_date_start),
            'date_end': fields.Datetime.to_string(cert_date_end),
            'clave_privada': attachment_privada,
            'clave_publica': attachment_publica, })
        if spain_dt > cert_date_end:
            raise ValidationError("El certificado ha caducado desde %s",
                                  record.date_end + MSG_SOPORTE_SICPRO)
        return record
