# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ServiciosInternosCorreos(models.Model):
    _name = 'sicpro.app.servicios.internos.correos'
    _description = "Gestión de correos internos"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Cuenta de Correo", )
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    active = fields.Boolean(default=True, )
    trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Trabajador', required=False,
                                 tracking=True)
    plaza_id = fields.Char(string="# Plaza", related='trabajador.plaza_id', store=True)
    correo_trabajo = fields.Char('Correo Trabajo', related='trabajador.correo_trabajo', store=True)
    company_id = fields.Many2one('res.company', string='Proceso', related='trabajador.company_id', store=True,
                                 tracking=True)
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
                                   related='trabajador.ocupacion_id', store=True, tracking=True)
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='trabajador.area_id', store=True,
                              tracking=True)
    parent_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato', related='trabajador.parent_id', store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato", related='trabajador.inicio_contrato', store=True)
    clase_contrato = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', store=True,
                                     string='Clase de Contrato', related='trabajador.clase_contrato')
    identification_id = fields.Char(string='Carnet de identidad', store=True, related='trabajador.identification_id')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', related='trabajador.user_id', store=True)
    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    # verífico que no se repita el trabajador en el registro
    @api.constrains('name')
    def _check_trabajador_correo_unico(self):
        uniq = self.env['sicpro.app.servicios.internos.correos'].search(
            ['&', '&', ("active", "=", True), ("trabajador", "=", self.trabajador.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El trabajador seleccionado, ya cuenta con un registro de número fijo!. "
                                    "Si cree que es un error contacte al administrador"))

    # verífico que el trabajador este activo, si no archivo el registro
    def cron_verifico_trabajador_correos_servicios_internos(self):
        correo = self.env['sicpro.app.servicios.internos.correos'].search([('active', '=', True)])
        # verífico el trabajador
        for item in correo:
            # Busco si existe el trabajador activo en el servicio de correo.
            trabajador = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', True), ('id', '=', item.trabajador.id)])
            if not trabajador:
                # desactivo el registro de correo
                item.active = False

    def write(self, vals):
        res = super(ServiciosInternosCorreos, self).write(vals)
        # verífico que no exista otro registro con el mismo trabajador
        if self.active:
            uniq = self.env['sicpro.app.servicios.internos.correos'].search(
                ['&', '&', ("active", "=", True), ("trabajador", "=", self.trabajador.id), ("id", "!=", self.id)])
            if uniq:
                raise ValidationError(_("¡El trabajador seleccionado, ya cuenta con un registro de número fijo!. "
                                        "Si cree que es un error contacte al administrador"))
        return res
