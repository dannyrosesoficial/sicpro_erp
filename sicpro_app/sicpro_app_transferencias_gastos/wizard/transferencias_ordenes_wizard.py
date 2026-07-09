# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class TransferenciasGastosImportarWizardOrdenes(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.importar.wizard.ordenes"
    _description = "Modificar valor de órdenes"

    def _objeto_sap(self):
        active_ids = self.env.context.get(
            'active_model') == 'sicpro.app.transferencias.gastos.importar' and self.env.context.get(
            'active_ids') or []
        if not active_ids:
            return False

        # Extraemos los campos necesarios en un solo viaje a la base de datos
        gastos_records = self.env[
            'sicpro.app.transferencias.gastos.importar'].browse(active_ids)
        gastos_id = gastos_records.mapped('objeto')
        estados = gastos_records.mapped('name')

        # compruebo que todos los elementos de la lista son iguales y que no esten en estado de importado
        val_importado = estados.count(estados[0]) == len(estados)
        if val_importado:
            # compruebo que todos los elementos de la lista son iguales para ejecutar la función de cambio
            val_gasto = gastos_id.count(gastos_id[0]) == len(gastos_id)
            if val_gasto:
                return gastos_id[0]
            else:
                raise ValidationError(
                    "¡Solo se puede seleccionar el mismo objeto de orden!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "¡No se pueden modificar objetos de orden con estados diferentes!.\n\n" + MSG_SOPORTE_SICPRO)

    orden_trabajo_id = fields.Many2one(
        comodel_name='sicpro.app.ordenes.trabajo', string='Orden',
        required=True)
    objeto = fields.Char(string='Tipo', required=True, default=_objeto_sap,
                         readonly=True)

    # modifico el nomenclador de la orden de trabajo
    def modificar_objeto_orden(self):
        orden_trabajo = self.orden_trabajo_id
        active_ids = self.env.context.get(
            'active_model') == 'sicpro.app.transferencias.gastos.importar' and self.env.context.get(
            'active_ids') or []

        if active_ids:
            gastos_seleccionados = self.env[
                'sicpro.app.transferencias.gastos.importar'].sudo().browse(
                active_ids)

            # Ejecutamos una única consulta masiva UPDATE en la base de datos (Optimización de Rendimiento)
            gastos_seleccionados.write(
                {'orden': orden_trabajo.id, 'objeto': orden_trabajo.name,
                    'name': 'pendiente'})