# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ApiConector(models.Model):
    _name = 'sicpro.modulo.api.conector'
    _order = "id asc"
    _description = 'Configura las conexiones con las apis externas'

    name = fields.Selection([], string="Aplicación", required=True, )
    app_id = fields.Char('ID Aplicación', required=True,)
    usuario = fields.Char('Usuario', required=False)
    password = fields.Char('Contraseña', required=False)
    web = fields.Char('Sitio Web', required=False)
    url_login = fields.Char('Url Login', required=False)
    url_data = fields.Char('Url API', required=False)
    url_config_data = fields.Char('Dato Variable', required=False,
                                  help="Url o transacción que se utiliza para la consulta dinámica para API REST")
    url_cierre = fields.Char('Url Cierre', required=False)
    descripcion = fields.Char('Descripción', required=False)
    company_id = fields.Many2one('res.company', string='Proceso', default=lambda self: self.env.company)
    active = fields.Boolean(string='Activo', required=False, default=True)
    tipo_autenticacion = fields.Selection(string='Tipo de Autenticación',
                                          selection=[('usuario_contraseña', 'Usuario y Contraseña'),
                                                     ('token', 'Token'), ], required=True, default="usuario_contraseña")
    token = fields.Char(string='Token', required=False)

    # verífico que no se repita el trabajador en el registro
    @api.constrains('name')
    def _check_aplicacion_unico(self):
        uniq = self.env['sicpro.modulo.api.conector'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡Ya existe la aplicación en la configuración actual!. "
                                    "Si cree que es un error contacte al administrador"))

    # necesario para la herencia
    def conector_api_cron(self):
        raise ValidationError(_("Ejecución del Cron Api."))

    # necesario para la herencia
    def conector_api_test(self):
        raise ValidationError(_("Ejecución del test Api."))




