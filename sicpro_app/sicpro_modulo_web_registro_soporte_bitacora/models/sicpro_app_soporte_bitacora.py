# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models
from odoo.exceptions import UserError


class PlantillaSoporteBitacora(models.Model):
    _inherit = "sicpro.app.soporte.bitacora"

    numero_consecutivo = fields.Char(string='Número Consecutivo', copy=False)
    ticket_cerrado = fields.Boolean(string='Ticket Cerrado', default=False)

    def ver_solicitud(self):
        """Redirige a la solicitud de acceso basada en el consecutivo"""
        self.ensure_one()
        if not self.numero_consecutivo:
            raise UserError(
                "No hay un número consecutivo asignado a esta bitácora.")

        return {'name': 'Solicitudes de Accesos',
                'type': 'ir.actions.act_window',
                'res_model': 'sicpro.modulo.solicitud.acceso',
                # Ajustado al modelo de solicitud
                'view_mode': 'list,form', 'domain': [
                ('numero_consecutivo', '=', self.numero_consecutivo)],
                'target': 'current', }

    def cerrar_ticket_solicitud(self):
        """Cambia el estado del ticket de soporte a cerrado y actualiza la bitácora"""
        self.ensure_one()

        # 1. Buscar el estado de cierre (Evitamos error .id si no existe)
        estado = self.env['sicpro.app.soporte.estados'].search(
            [('closed', '=', True)], limit=1)
        if not estado:
            raise UserError(
                "No se encontró un estado configurado como 'Cerrado' en el sistema.")

        # 2. Buscar el ticket relacionado
        soporte = self.env['sicpro.app.soporte'].search(
            [('numero_consecutivo', '=', self.numero_consecutivo)], limit=1)

        if not soporte:
            raise UserError(
                _("No se encontró el ticket de soporte con el consecutivo: %s") % self.numero_consecutivo)

        # 3. Actualizar el ticket y la bitácora
        soporte.write({'stage_id': estado.id})
        self.write({'ticket_cerrado': True})

        # 4. Retornar la vista del ticket actualizado
        return {'name': _('Ticket de Soporte'),
                'type': 'ir.actions.act_window',
                'res_model': 'sicpro.app.soporte', 'view_mode': 'form',
                'res_id': soporte.id, 'target': 'current', }
