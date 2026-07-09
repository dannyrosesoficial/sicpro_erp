# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class TransferenciasGastosImportarWizardOrdenes(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.importar.wizard.ordenes"
    _description = "Modificar valor de órdenes"

    def _objeto_sap(self):
        gastos_id = []
        estados = []
        gastos = self._context.get('active_model') == 'sicpro.app.transferencias.gastos.importar' and self._context.get(
            'active_ids') or []
        for item in self.env['sicpro.app.transferencias.gastos.importar'].browse(gastos):
            gastos_id.append(item.objeto)
            estados.append(item.name)

        # compruebo que todos los elementos de la lista son iguales y que no esten en estado de importado
        val_importado = estados.count(estados[0]) == len(estados)
        if val_importado:
            # compruebo que todos los elementos de la lista son iguales para ejecutar la función de cambio
            val_gasto = gastos_id.count(gastos_id[0]) == len(gastos_id)
            if val_gasto:
                return gastos_id[0]
            else:
                raise ValidationError(_("¡Solo se puede seleccionar el mismo objeto de orden!. "
                                        "Si cree que es un error contacte al administrador"))
        else:
            raise ValidationError(_("¡No se pueden modificar objetos de orden con estados diferentes!. "
                                    "Si cree que es un error contacte al administrador"))

    orden_trabajo_id = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo', string='Orden', required=True)
    objeto = fields.Char(string='Tipo', required=True, default=_objeto_sap, readonly=True)

    # modifico el nomenclador de la orden de trabajo
    def modificar_objeto_orden(self):
        objeto = self.objeto
        orden_trabajo = self.orden_trabajo_id
        gastos_sap = self.env['sicpro.app.transferencias.gastos.importar'].sudo().search([('objeto', '=', objeto)])
        for item in gastos_sap:
            item.orden = orden_trabajo.id
            item.objeto = orden_trabajo.name
            item.name = 'pendiente'
