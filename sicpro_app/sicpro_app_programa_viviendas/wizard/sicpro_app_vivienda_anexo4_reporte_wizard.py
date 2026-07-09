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


class ViviendaAnexo4(models.TransientModel):
    _name = 'sicpro.app.vivienda.reporte.anexo4'
    _description = 'Reportes de Anexo 4'

    etapa = fields.Many2one(comodel_name='sicpro.app.vivienda.etapas',
                            string='Etapa', required=False)
    reporte_general = fields.Boolean(string='Reporte completo', required=False)

    def report_busca_programa(self):
        beneficiados_ids = []

        if self.reporte_general:
            # Busco todos los trabajadores que están en estado de logística
            records = self.env['sicpro.app.vivienda.trabajador'].sudo().search(
                [('estado', '=', 'logistica')])

            for obj in records:
                monto = 0
                for value in obj.materiales_ids:
                    if value.estado in ['aprobado', 'entregado']:
                        monto += value.total_individual

                data = {'nombre': obj.trabajador_id.name,
                        'via_m_r': obj.tipo_mtto_reparacion,
                        'via_t': obj.tipo_terminada,
                        'inicio': obj.etapa.fecha_inicio,
                        'cierre': obj.etapa.fecha_fin, 'monto': monto,
                        'observaciones': obj.descripcion, }

                beneficiados_ids.append(data)
            return beneficiados_ids
        else:
            if self.etapa:
                # Busco los trabajadores que están en estado de logística y la etapa seleccionada
                records = self.env[
                    'sicpro.app.vivienda.trabajador'].sudo().search(
                    ['&', ('etapa', '=', self.etapa.id),
                     ('estado', '=', 'logistica')])

                for obj in records:
                    monto = 0
                    for value in obj.materiales_ids:
                        if value.estado in ['aprobado', 'entregado']:
                            monto += value.total_individual

                    data = {'nombre': obj.trabajador_id.name,
                            'via_m_r': obj.tipo_mtto_reparacion,
                            'via_t': obj.tipo_terminada,
                            'inicio': obj.etapa.fecha_inicio,
                            'cierre': obj.etapa.fecha_fin, 'monto': monto,
                            'observaciones': obj.descripcion, }

                    beneficiados_ids.append(data)
                return beneficiados_ids
            else:
                raise ValidationError(
                    "¡Debe seleccionar una etapa para poder continuar!.\n\n" + MSG_SOPORTE_SICPRO)

    def generar_reporte(self):
        return self.env.ref(
            'sicpro_app_programa_viviendas.informe_modelo_vivienda_anexo_4_action').report_action(
            [], )
