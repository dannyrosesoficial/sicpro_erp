# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ServiciosInternosNauta(models.Model):
    _name = 'sicpro.app.servicios.internos.nauta'
    _description = "Gestión de cuentas nautas"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    active = fields.Boolean(default=True, )
    name = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Trabajador', required=False, tracking=True)
    plaza_id = fields.Char(string="# Plaza", related='name.plaza_id', store=True)
    correo_trabajo = fields.Char('Correo Trabajo', related='name.correo_trabajo', store=True)
    company_id = fields.Many2one('res.company', string='Proceso', related='name.company_id', store=True,
                                 tracking=True)
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
                                   related='name.ocupacion_id', store=True, tracking=True)
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='name.area_id', store=True,
                              tracking=True)
    parent_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato', related='name.parent_id', store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato", related='name.inicio_contrato', store=True)
    clase_contrato = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', store=True,
                                     string='Clase de Contrato', related='name.clase_contrato')
    identification_id = fields.Char(string='Carnet de identidad', store=True, related='name.identification_id')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', related='name.user_id', store=True)
    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    fecha_entregada = fields.Date(string='Entregada', required=False, tracking=True)
    horas = fields.Integer(string="Horas asignadas", required=False, tracking=True)
    usuario_nauta = fields.Char(string='Usuario Nauta', required=False)
    compromiso = fields.Boolean(string='Compromiso', required=False)

    # _sql_constraints = [
    #     ('name_unique', 'unique (name)', "¡El trabajador ya tiene una cuenta asociada!"),
    # ]

    # verífico que no se repita el trabajador en el registro
    @api.constrains('name')
    def _check_trabajador_nauta_unico(self):
        uniq = self.env['sicpro.app.servicios.internos.nauta'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El trabajador seleccionado, ya tiene una cuenta asociada!. "
                                    "Si cree que es un error contacte al administrador"))

    # verífico que el trabajador este activo, si no archivo el registro
    def cron_verifico_trabajador_nauta_servicios_internos(self):
        nauta = self.env['sicpro.app.servicios.internos.nauta'].search([('active', '=', True)])
        # verífico el trabajador
        for item in nauta:
            # Busco si existe el trabajador activo en el servicio de correo.
            trabajador = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', True), ('id', '=', item.name.id)])
            if not trabajador:
                # desactivo el registro de correo
                item.active = False

    @api.model
    def create(self, vals):
        res = super(ServiciosInternosNauta, self).create(vals)
        # envío el correo electrónico al jefe del trabajador
        email_values = {'email_to': res.parent_id.user_id.partner_id.email_formatted, }
        template = self.env.ref('sicpro_app_servicios_internos.servicios_internos_nauta')
        template.send_mail(res.id, force_send=True, email_values=email_values)
        return res

    def write(self, vals):
        res = super(ServiciosInternosNauta, self).write(vals)
        if self.name and self.active:
            # envío el correo electrónico al jefe del trabajador
            local_context = self.env.context.copy()
            email_values = {'email_to': self.parent_id.user_id.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_servicios_internos.servicios_internos_nauta')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # verífico que no exista otro registro con el mismo trabajador
            uniq = self.env['sicpro.app.servicios.internos.nauta'].search(
                ['&', '&', ("active", "=", True), ("name", "=", self.name.id), ("id", "!=", self.id)])
            if uniq:
                raise ValidationError(_("¡El trabajador seleccionado, ya tiene una cuenta asociada!. "
                                        "Si cree que es un error contacte al administrador"))
        return res
