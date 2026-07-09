# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ServiciosInternosLineas(models.Model):
    _name = 'sicpro.app.servicios.internos.lineas'
    _description = "Gestión de líneas"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = "name"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="No. Teléfono", required=True, tracking=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    active = fields.Boolean(default=True, )
    apns = fields.Char(string='Apns', required=True, tracking=True)
    apn_etecsa = fields.Boolean(string='APN ETECSA', default=False, required=False, tracking=True)
    apn_nauta = fields.Boolean(string='APN NAUTA', default=False, required=False, tracking=True)
    tope_voz = fields.Integer(string="Tope Voz", required=True, tracking=True)
    tope_datos = fields.Integer(string="Tope Datos", required=False, tracking=True)
    tope_sms = fields.Integer(string="Tope SMS", required=True, tracking=True)
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
    trabajador_detalles = fields.Text(string="Detalles del trabajador", required=False, tracking=True)
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', related='trabajador.user_id', store=True)
    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)
    custodia_trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Custodia', required=False,
                                          tracking=True)
    custodia_plaza_id = fields.Char(string="# Plaza de Custodia", related='custodia_trabajador.plaza_id', store=True)
    custodia_company_id = fields.Many2one('res.company', string='Proceso de Custodia', related='custodia_trabajador.company_id',
                                          store=True, tracking=True)
    custodia_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo Custodia', tracking=True,
                                            related='custodia_trabajador.ocupacion_id', store=True)
    custodia_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento Custodia',
                                       related='custodia_trabajador.area_id', store=True, tracking=True)
    custodia_identification_id = fields.Char(string='Carnet de identidad Custodia', store=True,
                                             related='custodia_trabajador.identification_id')
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    custodia_detalles = fields.Text(string="Detalles", required=False, tracking=True)
    fecha_recibida = fields.Date(string='Recibida', required=False, tracking=True,
                                 default=lambda self: fields.Date.context_today(self))
    fecha_entregada = fields.Date(string='Entregada', required=False, tracking=True)
    fecha_custodia = fields.Date(string='En custodia', required=False, tracking=True)
    fecha_cancelada = fields.Date(string='Cancelada', required=False, tracking=True)
    estado = fields.Selection(string='Estado', required=False, tracking=True,
                              selection=[('nueva', 'Nueva'), ('entregada', 'Entregada'), ('custodia', 'Custodia'),
                                         ('cancelada', 'Cancelada'), ], default='nueva')
    apn_mixta = fields.Boolean(string='Apn_mixta', compute='_onchange_apn_mixta')

    # _sql_constraints = [
    #     ('name_unique', 'unique (name)', "¡El número de teléfono existe!"),
    #     ('trabajador_unique', 'unique (trabajador)', "¡El trabajador seleccionado, ya cuenta con una línea asociada!"),
    # ]

    # verífico que no se repita el número de línea en el registro
    @api.constrains('name')
    def _check_trabajador_linea_unico(self):
        uniq = self.env['sicpro.app.servicios.internos.lineas'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡La línea seleccionada, ya cuenta con un registro creado!. "
                                    "Si cree que es un error contacte al administrador"))

    # verífico que no se repita el trabajador en el registro
    @api.constrains('trabajador')
    def _check_trabajador_trabajador_unico(self):
        uniq = self.env['sicpro.app.servicios.internos.lineas'].search(
            ['&', '&', ("active", "=", True), ("trabajador", "=", self.trabajador.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El trabajador seleccionado, ya cuenta con un registro creado!. "
                                    "Si cree que es un error contacte al administrador"))

    # control de apn mixta
    def _onchange_apn_mixta(self):
        if self.apn_nauta and self.apn_etecsa:
            self.apn_mixta = True
        else:
            self.apn_mixta = False

    # Realizo el cambio de las fechas en función del estado
    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado == 'entregada':
            self.fecha_entregada = fields.Date.context_today(self)
            self.custodia_trabajador = None
        elif self.estado == 'custodia':
            self.fecha_custodia = fields.Date.context_today(self)
            self.trabajador = None
        elif self.estado == 'cancelada':
            self.fecha_cancelada = fields.Date.context_today(self)
            self.custodia_trabajador = None
            self.trabajador = None

    # verífico que el trabajador este activo, si no archivo el registro
    def cron_verifico_trabajador_lineas_servicios_internos(self):
        lineas = self.env['sicpro.app.servicios.internos.lineas'].search([('active', '=', True)])
        # verífico el trabajador
        for item in lineas:
            # Busco si existe el trabajador activo en el servicio de correo.
            trabajador = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', True), ('id', '=', item.trabajador.id)])
            if not trabajador:
                # desactivo el registro de correo
                item.active = False

    @api.model
    def create(self, vals):
        res = super(ServiciosInternosLineas, self).create(vals)
        if res.trabajador:
            # envío el correo electrónico al jefe del trabajador
            email_values = {'email_to': res.parent_id.user_id.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_servicios_internos.servicios_internos_linea_movil')
            template.send_mail(res.id, force_send=True, email_values=email_values)
        return res

    def write(self, vals):
        res = super(ServiciosInternosLineas, self).write(vals)
        if self.trabajador and self.active:
            # envío el correo electrónico al jefe del trabajador
            local_context = self.env.context.copy()
            email_values = {'email_to': self.parent_id.user_id.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_servicios_internos.servicios_internos_linea_movil')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # verífico que no exista otro registro con la misma línea
            uniq_l = self.env['sicpro.app.servicios.internos.lineas'].search(
                ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
            if uniq_l:
                raise ValidationError(_("¡La línea seleccionada, ya cuenta con un registro creado!. "
                                        "Si cree que es un error contacte al administrador"))

            # verífico que no exista otro registro con el mismo trabajador
            uniq_t = self.env['sicpro.app.servicios.internos.lineas'].search(
                ['&', '&', ("active", "=", True), ("trabajador", "=", self.trabajador.id), ("id", "!=", self.id)])
            if uniq_t:
                raise ValidationError(_("¡El trabajador seleccionado, ya cuenta con un registro creado!. "
                                        "Si cree que es un error contacte al administrador"))

        return res


