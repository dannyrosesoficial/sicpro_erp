# -*- coding: utf-8 -*-

from odoo import fields, models, _


class PlantillaSoporteBitacora(models.Model):
    _inherit = "sicpro.app.soporte.bitacora"

    numero_consecutivo = fields.Char(string='Número Consecutivo')
    ticket_cerrado = fields.Boolean(string='Ticket Cerrado', default=False, required=False)

    # ver la solicitud de usuario
    def ver_solicitud(self):
        if self.numero_consecutivo:
            domain = [('numero_consecutivo', '=', self.numero_consecutivo)]
            return {'name': _('Solicitudes de Accesos'), 'domain': domain,
                    'res_model': 'sicpro.modulo.plantilla.acceso', 'type': 'ir.actions.act_window', 'view_id': False,
                    'view_mode': 'tree,form', 'limit': 80, }

    # cerrar ticket de solicitud
    def cerrar_ticket_solicitud(self):
        # buscar el estado de terminado
        estado = self.env['sicpro.app.soporte.estados'].search([('closed', '=', True)]).id
        soporte = self.env['sicpro.app.soporte'].search([('numero_consecutivo', '=', self.numero_consecutivo)])
        soporte.stage_id = estado
        # oculto el botón de cerrar ticket
        self.ticket_cerrado = True
        # redirigir al ticket cerrado
        domain = [('id', '=', soporte.id)]
        return {'name': _('Tickets de Soporte'), 'domain': domain, 'res_model': 'sicpro.app.soporte',
                'type': 'ir.actions.act_window', 'view_id': False, 'view_mode': 'tree,form', 'limit': 80, }
