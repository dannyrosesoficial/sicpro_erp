# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class OrdensAnexo3(models.TransientModel):
    _name = "sicpro.app.ordenes.trabajo.anexo3"
    _description = "Modelo para visualizar el Anexo 3"

    def _modelo_anexo_3(self):
        active_id = self.env.context.get('active_id')
        return active_id if active_id else False

    orden_trabajo_id = fields.Many2one(
        comodel_name='sicpro.app.ordenes.trabajo', string='Orden',
        default=_modelo_anexo_3, required=True)
    tipo = fields.Selection(string='Tipo', required=True, default='comienzo',
                            selection=[('comienzo', 'Comienzo de Obra'), (
                            'terminacion', 'Terminación de Obra'), ], )
    certifica = fields.Many2one('res.users', string='Certifica',
                                required=True, )
    comentario = fields.Text(string="Comentario", required=False)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 related='orden_trabajo_id.company_id')
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto')
    sap_titulo = fields.Char(string="Titulo SAP",
                             related='orden_trabajo_id.sap_titulo')
    pep = fields.Char(string='Sap', related='orden_trabajo_id.pep')
    territorio = fields.Many2one(comodel_name='res.country.state',
                                 string='Provincia',
                                 related='orden_trabajo_id.provincia_id')
    uo = fields.Char(string='Unidad Organizativa',
                     related='orden_trabajo_id.uo_abreviatura')
    especialidad_id = fields.Many2one(
        comodel_name='sicpro.nomenclador.especialidad', string='Especialidad',
        related='orden_trabajo_id.especialidad_id')
    fecha_inicio_cronograma = fields.Date(string='Inicio Cronograma',
                                          related='orden_trabajo_id.fecha_inicio_cronograma')
    fecha_fin_cronograma = fields.Date(string='Fin Cronograma',
                                       related='orden_trabajo_id.fecha_fin_cronograma')
    fecha_inicio_real = fields.Date(string='Inicio Real',
                                    related='orden_trabajo_id.fecha_inicio_real')
    fecha_fin_real = fields.Date(string='Fin Real',
                                 related='orden_trabajo_id.fecha_fin_real')

    # Uso de campos computados para fecha actual precisa según contexto del
    # usuario
    dia = fields.Char(string="Día", compute="_compute_fecha_actual")
    mes = fields.Char(string="Mes", compute="_compute_fecha_actual")
    anio = fields.Char(string="Año", compute="_compute_fecha_actual")
    cargo = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                            'Puesto de Trabajo',
                            related="certifica.ocupacion_id")

    @api.depends_context('uid')
    def _compute_fecha_actual(self):
        hoy = fields.Date.context_today(self)
        for record in self:
            record.dia = hoy.strftime("%d")
            record.mes = hoy.strftime("%m")
            record.anio = hoy.strftime("%Y")

    def generar_reporte_anexo3(self):
        return self.env.ref(
            'sicpro_app_ordenes_trabajo.informe_modelo_ordenes_anexo3_action').report_action(
            self.id)