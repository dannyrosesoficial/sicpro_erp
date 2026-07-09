# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.fields import Datetime


class TransferenciasGastosCertificarWizard(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.economia.wizard"
    _description = "Enviar gastos a certificar"

    def _gastos_cj74_modificar_meses(self):
        mes_ids = []
        gastos = self.env['sicpro.app.transferencias.gastos'].search([('estado', '=', 'revision_economica')])
        # verificar si tiene gastos para enviar a certificar
        if gastos:
            for item in gastos:
                mes_ids.append(item.mes.id)
            return mes_ids
        # else:
        #     raise ValidationError(_("¡No se encontraron gastos para certificar!. "
        #                             "Si cree que es un error contacte al administrador"))

    def _get_mes_domain(self):
        return [('id', 'in', self._gastos_cj74_modificar_meses())]

    anio = fields.Char(string="Año", required=True, default=fields.Datetime.now().strftime("%Y"), )
    mes_ids = fields.Many2many('sicpro.nomenclador.meses', 'transferencias_meses_rel', 'transferencia_id', 'mes_id',
                               string='Meses', default=_gastos_cj74_modificar_meses, domain=_get_mes_domain,
                               required=True)
    ordenes_ids = fields.Many2many('sicpro.app.ordenes.trabajo', 'transferencias_ordenes_rel', 'transferencia_id',
                                   'ordenes_id', string='Ordenes',  required=True)

    @api.onchange('mes_ids')
    def _compute_gastos_cj74_ordenes(self):
        ordenes_ids = []
        mes_ids = self.mes_ids
        if mes_ids:
            for mes in mes_ids:
                for item in self.env['sicpro.app.transferencias.gastos'].search(
                        ['&', ('estado', '=', 'revision_economica'), ('mes', '=', mes.ids[0])]):
                    ordenes_ids.append(item.name.id)
            self.ordenes_ids = ordenes_ids
        else:
            raise ValidationError(_("¡No se encontraron gastos para certificar!. "
                                    "Si cree que es un error contacte al administrador"))

    # modifico el nomenclador de la orden de trabajo
    def modificar_estado_gastos(self):
        meses_ids = self.mes_ids
        ordenes_ids = self.ordenes_ids
        anio = self.anio
        anio_actual = Datetime.now().strftime("%Y")
        mes_actual = self.env['sicpro.nomenclador.meses'].search([("codigo_mes", "=", Datetime.now().strftime("%m"))]).id

        for mes in meses_ids:
            for orden in ordenes_ids:
                gastos_ids = self.env['sicpro.app.transferencias.gastos'].search(
                    ['&', '&', ("anio", "=", anio), ("mes", "=", mes.id), ('estado', '=', 'revision_economica'),
                     ("name", "=", orden.id)])
                # verífico que existan órdenes con el filtro especificado
                if gastos_ids:
                    # creo datos de vinculación entre las transferencias y órdenes de trabajo
                    orden_transferencias = self.env['sicpro.app.transferencias.gastos.ordenes'].sudo().create(
                        {'orden_id': orden.id, 'anio': anio_actual, 'mes': mes_actual, })
                    # actualizo el campo de vinculación con las órdenes de trabajo y la paso al estado de revision_dtp
                    for gasto in gastos_ids:
                        # actualizo los valores de la tabla de gastos cj74
                        gasto.gasto_id = orden_transferencias.id
                        gasto.estado = 'revision_dtp'
                    # obligo a que se inicie el _compute_cantidad_cuentas_gastos para visualizar
                    # el gasto total en la vista tree
                    cantidad_cuentas = orden_transferencias.cantidad_cuentas

        group_dtp = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos').users
        id_gastos = self.env['sicpro.app.transferencias.gastos'].search([('active', '=', True)], limit=1)
        # Selecciono el registro de seguidores
        for participante in group_dtp:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted,
                            'email_from': '"SICPRO ERP" <sicproerp@etecsa.cu>',
                            }
            template = self.env.ref('sicpro_app_transferencias_gastos.gastos_revision_economica_dtp')
            template.send_mail(id_gastos.id, force_send=True, email_values=email_values, )

        rainbow = {
            'effect': {'fadeout': 'slow',
                       'message': 'Se realizó correctamente la transferencia de gastos a las ejecutoras.',
                       'type': 'rainbow_man',
                       }
        }
        return rainbow


