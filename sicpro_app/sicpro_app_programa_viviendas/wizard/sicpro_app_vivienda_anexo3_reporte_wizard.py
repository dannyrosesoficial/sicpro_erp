# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ViviendaAnexo3(models.TransientModel):
    _name = 'sicpro.app.vivienda.reporte.anexo3'
    _description = 'Reportes de Anexo 3'

    etapa = fields.Many2one(comodel_name='sicpro.app.vivienda.etapas', string='Etapa', required=False)
    reporte_general = fields.Boolean(string='Reporte completo', required=False)
    especialista_obras = fields.Many2one('sicpro.app.trabajadores', string='Especialista en Obras de Ingeniería',
                                         required=False)
    jefe_logistica = fields.Many2one('sicpro.app.trabajadores', string='Jefe Dpto. Logística y Servicios',
                                     required=False)

    def report_busca_programa(self):
        demanda_ids = []

        if self.reporte_general:
            # Busco todos los materiales
            materiales_ids = self.env['sicpro.app.vivienda.materiales'].sudo().search([('active', '=', True)])
            # Busco todos los materiales
            records = self.env['sicpro.app.vivienda.trabajador.productos'].sudo().search(
                [("estado", "in", ['aprobado', 'entregado'])])

            for item in materiales_ids:
                cantidad = 0
                for value in records:
                    if value.name.id == item.id:
                        cantidad += value.cantidad

                if cantidad != 0:
                    data = {'material': item.name, 'um': item.um.name, 'cantidad': cantidad, 'unitario': None,
                            'total': None, }
                    demanda_ids.append(data)
            return demanda_ids
        else:
            if self.etapa:
                # Busco todos los materiales
                materiales_ids = self.env['sicpro.app.vivienda.materiales'].sudo().search([('active', '=', True)])
                # Busco todos los materiales
                records = self.env['sicpro.app.vivienda.trabajador.productos'].sudo().search(
                    ['&', ('solicitud_id.etapa', '=', self.etapa.id), ("estado", "in", ['aprobado', 'entregado'])])

                for item in materiales_ids:
                    cantidad = 0
                    for value in records:
                        if value.name.id == item.id:
                            cantidad += value.cantidad

                    if cantidad != 0:
                        data = {'material': item.name, 'um': item.um.name, 'cantidad': cantidad, 'unitario': None,
                                'total': None, }
                        demanda_ids.append(data)
                return demanda_ids
            else:
                raise ValidationError(_("¡Debe seleccionar una etapa para poder continuar!. "
                                        "Si cree que es un error contacte al administrador"))

    def generar_reporte(self):
        return self.env.ref('sicpro_app_programa_viviendas.informe_modelo_vivienda_anexo_3_action').report_action([], )
