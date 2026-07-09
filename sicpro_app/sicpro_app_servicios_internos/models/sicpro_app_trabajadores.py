# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import AccessError


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    nauta_count = fields.Integer('Servicio Nauta', compute='_compute_nauta_servicios_internos')
    tope_voz = fields.Integer(string="Tope Voz", compute='_compute_lineas_servicios_internos')
    tope_datos = fields.Integer(string="Tope Datos", compute='_compute_lineas_servicios_internos')
    tope_sms = fields.Integer(string="Tope SMS", compute='_compute_lineas_servicios_internos')
    movil_trabajo = fields.Char('Móvil de Trabajo', compute='_compute_lineas_servicios_internos')
    telefono_trabajo = fields.Char('Teléfono de Trabajo', compute='_compute_fijos_servicios_internos')
    correo_trabajo = fields.Char('Correo de Trabajo', compute='_compute_correos_servicios_internos')
    linea_ids = fields.One2many('sicpro.app.servicios.internos.lineas', 'trabajador', string='S. Líneas Ids')
    fijo_ids = fields.One2many('sicpro.app.servicios.internos.fijos', 'trabajador', string='S. Fijos Ids')
    correo_ids = fields.One2many('sicpro.app.servicios.internos.correos', 'trabajador', string='S. Correos Ids')

    # busca el valor del servicio nauta
    def _compute_nauta_servicios_internos(self):
        for item in self:
            nauta_id = self.env['sicpro.app.servicios.internos.nauta'].sudo().search([('name', '=', item.id)])
            item.nauta_count = nauta_id.horas

    # busca el valor del servicio de la línea móvil
    def _compute_lineas_servicios_internos(self):
        for item in self:
            lineas_id = self.env['sicpro.app.servicios.internos.lineas'].sudo().search([('trabajador', '=', item.id)])
            item.tope_voz = lineas_id.tope_voz
            item.tope_sms = lineas_id.tope_sms
            item.tope_datos = lineas_id.tope_datos
            item.movil_trabajo = lineas_id.name

    # busca el valor del servicio de la línea fija
    def _compute_fijos_servicios_internos(self):
        for item in self:
            fijos_id = self.env['sicpro.app.servicios.internos.fijos'].sudo().search([('trabajador', '=', item.id)])
            item.telefono_trabajo = fijos_id.name

    # busca el valor del servicio de correos
    def _compute_correos_servicios_internos(self):
        for item in self:
            correo_id = self.env['sicpro.app.servicios.internos.correos'].sudo().search([('trabajador', '=', item.id)])
            item.correo_trabajo = correo_id.name

    # action de acceso a la cuenta nauta
    def nauta_trabajador_view(self):
        if self.nauta_count == 0:
            raise AccessError(_("El usuario no tiene una cuenta asociada."))
        else:
            self.ensure_one()
            domain = [('name', '=', self.id)]
            return {
                'name': _('Nauta'),
                'domain': domain,
                'res_model': 'sicpro.app.servicios.internos.nauta',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_name': %s}" % self.id
            }

    # action de acceso a los servicios móviles
    def linea_trabajador_view(self):
        if self.tope_voz == 0:
            raise AccessError(_("El usuario no tiene el servicio asociado."))
        else:
            self.ensure_one()
            domain = [('trabajador', '=', self.id)]
            return {
                'name': _('Servicios Internos'),
                'domain': domain,
                'res_model': 'sicpro.app.servicios.internos.lineas',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador': %s}" % self.id
            }

    # action de acceso a los servicios fijos
    def fijos_trabajador_view(self):
        if not self.telefono_trabajo:
            raise AccessError(_("El usuario no tiene el servicio asociado."))
        else:
            self.ensure_one()
            domain = [('trabajador', '=', self.id)]
            return {
                'name': _('Servicios Fijos'),
                'domain': domain,
                'res_model': 'sicpro.app.servicios.internos.fijos',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador': %s}" % self.id
            }

    # action de acceso a los servicios de correos (sin usar)
    def correos_trabajador_view(self):
        if not self.correo_trabajo:
            raise AccessError(_("El usuario no tiene el servicio asociado."))
        else:
            self.ensure_one()
            domain = [('trabajador', '=', self.id)]
            return {
                'name': _('Servicios de Correo Electrónico'),
                'domain': domain,
                'res_model': 'sicpro.app.servicios.internos.correos',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador': %s}" % self.id
            }