# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import AccessError


class SoporteTicket(models.Model):
    _inherit = "sicpro.app.soporte"

    id_solicitud_acceso = fields.Integer(string='Id_solicitud_acceso', required=False)
    numero_consecutivo = fields.Char(string='Número Consecutivo')
    bitacora_count = fields.Integer('Cuenta Bitácora', compute='_compute_bitacora_count')
    solicitudes_count = fields.Integer('Solicitudes', compute='_compute_solicitudes_count')

    # Cuenta los registros de solicitudes asociados al ticket
    def _compute_solicitudes_count(self):
        for item in self:
            solicitudes_ids = self.env['sicpro.modulo.plantilla.acceso'].search([('id', '=', self.id_solicitud_acceso)])
            item.solicitudes_count = len(solicitudes_ids)

    # Cuenta los registros de bitácora asociados al ticket
    def _compute_bitacora_count(self):
        for item in self:
            bitacora_ids = self.env['sicpro.app.soporte.bitacora'].search(
                [('numero_consecutivo', '=', self.numero_consecutivo)])
            item.bitacora_count = len(bitacora_ids)

    # ir al registro de la bitácora
    def action_registro_bitacora(self, ):
        bitacora = self.env['sicpro.app.soporte.bitacora'].search(
            [('numero_consecutivo', '=', self.numero_consecutivo)]).id

        if not bitacora:
            raise AccessError(_("El Ticket seleccionado no tiene una bitácora asociada."))
        else:
            self.ensure_one()
            domain = [('id', '=', bitacora)]
            return {'name': _('Bitácora del Usuario'), 'domain': domain, 'view_id': False, 'view_mode': 'tree,form',
                    'res_model': 'sicpro.app.soporte.bitacora', 'type': 'ir.actions.act_window', 'limit': 80, }

    # Abre la vista de las solicitudes de los usuarios en el botón inteligente
    def solicitudes_acceso_view(self):
        if not self.user_id:
            raise AccessError(_("Debe asignar un ejecutante de la tarea antes de continuar."))
        else:
            if not self.id_solicitud_acceso:
                raise AccessError(_("El Ticket seleccionado no tiene una solicitud asociada."))
            else:
                self.ensure_one()
                domain = [('id', '=', self.id_solicitud_acceso)]
                return {'name': _('Solicitudes de Accesos'), 'domain': domain, 'view_id': False, 'limit': 80,
                        'view_mode': 'tree,form', 'res_model': 'sicpro.modulo.plantilla.acceso',
                        'type': 'ir.actions.act_window', }