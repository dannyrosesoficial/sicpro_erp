# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class ViviendaAnexoEstadistica(models.TransientModel):
    _name = 'sicpro.app.vivienda.reporte.estadistica'
    _description = 'Reportes de Estadística RRHH'

    etapa = fields.Many2one(comodel_name='sicpro.app.vivienda.etapas',
                            string='Etapa', required=True)

    def report_busca_programa(self):
        estadisticas_ids = []
        materiales = []

        if self.etapa:
            # Busco todos los trabajadores que están en estado de logística
            viviendas_ids = self.env[
                'sicpro.app.vivienda.trabajador'].sudo().search(
                ['&', ('etapa', '=', self.etapa.id),
                 ("estado", "in", ['logistica', 'terminado'])])
            # Busco los valores de gastos de la etapa
            etapas_id = self.env['sicpro.app.vivienda.etapas'].sudo().search(
                [('id', '=', self.etapa.id)])
            # Busco todos los materiales
            materiales_ids = self.env[
                'sicpro.app.vivienda.materiales'].sudo().search(
                [('active', '=', True)])
            # Busco todos los materiales
            productos_ids = self.env[
                'sicpro.app.vivienda.trabajador.productos'].sudo().search(
                ['&', ('etapa', '=', self.etapa.id),
                 ("estado", "in", ['aprobado', 'entregado'])])

            beneficiados = 0
            mujeres = 0

            # busco los trabajadores beneficiados y los que son mujeres
            for obj in viviendas_ids:
                beneficiados += 1
                print(obj.trabajador_id.genero)
                if obj.trabajador_id.genero == 'femenino':
                    mujeres += 1

            # busco el valor general de la etapas
            avance = round((etapas_id.monto_usado / etapas_id.monto) * 100, 2)

            # busco el listado de materiales
            for item in materiales_ids:
                cantidad = 0
                for value in productos_ids:
                    if value.name.id == item.id:
                        cantidad += value.cantidad

                if cantidad != 0:
                    data = {'material': item.name, 'um': item.um.name,
                            'cantidad': cantidad, }
                    materiales.append(data)

            data = {'beneficiados': beneficiados, 'mujeres': mujeres,
                    'asignado': etapas_id.monto,
                    'ejecutado': etapas_id.monto_usado,
                    'etapa': self.etapa.name,
                    'pendiente_facturar': etapas_id.pago_anticipado,
                    'avance': avance, 'materiales': materiales, }

            estadisticas_ids.append(data)
            return estadisticas_ids

        else:
            raise ValidationError(
                "¡Debe seleccionar una etapa para poder continuar!.\n\n" + MSG_SOPORTE_SICPRO)

    def generar_reporte(self):
        return self.env.ref(
            'sicpro_app_programa_viviendas.informe_modelo_vivienda_estadisticas_action').report_action(
            [], )
