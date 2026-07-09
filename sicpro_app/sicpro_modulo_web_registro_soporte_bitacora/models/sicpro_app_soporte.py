# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models, api
from odoo.exceptions import UserError


class SoporteTicket(models.Model):
    _inherit = "sicpro.app.soporte"

    # Campos originales solicitados
    id_solicitud_acceso = fields.Integer(string='Id_solicitud_acceso',
                                         required=False)
    numero_consecutivo = fields.Char(string='Número Consecutivo', copy=False)
    bitacora_count = fields.Integer(string='Cuenta Bitácora',
                                    compute='_compute_counts')
    solicitudes_count = fields.Integer(string='Solicitudes',
                                       compute='_compute_counts')

    @api.depends('id_solicitud_acceso', 'numero_consecutivo')
    def _compute_counts(self):
        """Calcula ambos contadores de forma eficiente en un solo proceso"""
        for item in self:
            # Contador de solicitudes (basado en el ID entero)
            if item.id_solicitud_acceso:
                # Usamos search_count para no cargar objetos pesados en memoria
                item.solicitudes_count = self.env[
                    'sicpro.modulo.solicitud.acceso'].search_count(
                    [('id', '=', item.id_solicitud_acceso)])
            else:
                item.solicitudes_count = 0

            # Contador de registros de bitácora (basado en el consecutivo)
            if item.numero_consecutivo:
                item.bitacora_count = self.env[
                    'sicpro.app.soporte.bitacora'].search_count(
                    [('numero_consecutivo', '=', item.numero_consecutivo)])
            else:
                item.bitacora_count = 0

    def action_registro_bitacora(self):
        """Abre la bitácora filtrando por el número consecutivo"""
        self.ensure_one()
        if not self.numero_consecutivo:
            raise UserError(
                "Este ticket no tiene un número consecutivo asignado.")

        bitacoras = self.env['sicpro.app.soporte.bitacora'].search(
            [('numero_consecutivo', '=', self.numero_consecutivo)])

        if not bitacoras:
            raise UserError(
                "El Ticket seleccionado no tiene una bitácora asociada.")

        action = {'name': 'Bitácora del Usuario',
                  'type': 'ir.actions.act_window',
                  'res_model': 'sicpro.app.soporte.bitacora',
                  'view_mode': 'list,form', 'domain': [
                ('numero_consecutivo', '=', self.numero_consecutivo)],
                  'context': {
                      'default_numero_consecutivo': self.numero_consecutivo},
                  'target': 'current', }

        # Si solo hay un registro, lo abrimos directamente en vista formulario
        if len(bitacoras) == 1:
            action.update({'view_mode': 'form', 'res_id': bitacoras.id, })
        return action

    def solicitudes_acceso_view(self):
        """Abre la solicitud de acceso usando el ID guardado"""
        self.ensure_one()

        # Validaciones de seguridad y flujo
        if not self.user_id:
            raise UserError(
                "Debe asignar un ejecutante antes de continuar.")

        if not self.id_solicitud_acceso:
            raise UserError(
                "El Ticket seleccionado no tiene una solicitud asociada.")

        # Verificamos que el registro realmente exista en la DB
        solicitud = self.env['sicpro.modulo.solicitud.acceso'].browse(
            self.id_solicitud_acceso)
        if not solicitud.exists():
            raise UserError(
                "La solicitud asociada (ID: %s) ya no existe en el sistema." % self.id_solicitud_acceso)

        return {'name': 'Solicitud de Acceso',
                'type': 'ir.actions.act_window',
                'res_model': 'sicpro.modulo.solicitud.acceso',
                'view_mode': 'form', 'res_id': self.id_solicitud_acceso,
                'target': 'current', }
