# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class ApiConector(models.Model):
    _name = 'sicpro.modulo.api.conector'
    _order = "id asc"
    _description = 'Configura las conexiones con las apis externas'

    name = fields.Selection([], string="Aplicación", required=True, )
    app_id = fields.Char(string='ID Aplicación', required=True, )
    usuario = fields.Char(string='Usuario', required=False)
    password = fields.Char(string='Contraseña', required=False)
    web = fields.Char(string='Sitio Web', required=False)
    url_login = fields.Char(string='Url Login', required=False)
    url_data = fields.Char(string='Url API', required=False)
    url_config_data = fields.Char(string='Dato Variable', required=False,
                                  help="Url o transacción que se utiliza para la consulta dinámica para API REST")
    url_cierre = fields.Char(string='Url Cierre', required=False)
    descripcion = fields.Char(string='Descripción', required=False)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Activo', required=False, default=True, index=True)
    tipo_autenticacion = fields.Selection(string='Tipo de Autenticación',
                                          selection=[('usuario_contraseña',
                                                      'Usuario y Contraseña'),
                                                     ('token', 'Token'), ],
                                          required=True,
                                          default="usuario_contraseña")
    token = fields.Char(string='Token', required=False)

    # verífico que no se repita el trabajador en el registro
    @api.constrains('name')
    def _check_aplicacion_unico(self):
        uniq = self.env['sicpro.modulo.api.conector'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name),
             ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(
                "¡Ya existe la aplicación en la configuración actual!.\n\n" + MSG_SOPORTE_SICPRO)

    # necesario para la herencia
    def conector_api_cron(self):
        raise ValidationError("Ejecución del Cron Api.\n\n" + MSG_SOPORTE_SICPRO)

    # necesario para la herencia
    def conector_api_test(self):
        raise ValidationError("Ejecución del test Api.\n\n" + MSG_SOPORTE_SICPRO)
