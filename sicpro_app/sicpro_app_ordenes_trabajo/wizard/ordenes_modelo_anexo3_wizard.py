# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdensAnexo3(models.TransientModel):
    _name = "sicpro.app.ordenes.trabajo.anexo3"
    _description = "Modelo para visualizar el Anexo 3"

    def _modelo_anexo_3(self):
        orden_id = ''
        orden = self._context.get('active_model') == 'sicpro.app.ordenes.trabajo' and self._context.get(
            'active_ids') or []
        for item in self.env['sicpro.app.ordenes.trabajo'].browse(orden):
            orden_id = item
        return orden_id

    orden_trabajo_id = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo', string='Orden',
                                       default=_modelo_anexo_3, required=True)
    tipo = fields.Selection(string='Tipo', required=True, default='comienzo',
                            selection=[('comienzo', 'Comienzo de Obra'), ('terminacion', 'Terminación de Obra'), ], )
    certifica = fields.Many2one('res.users', string='Certifica', required=True, )
    comentario = fields.Text(string="Comentario", required=False)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', related='orden_trabajo_id.company_id',)
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    sap_titulo = fields.Char(string="Titulo SAP", related='orden_trabajo_id.sap_titulo')
    pep = fields.Char(string='Sap', related='orden_trabajo_id.pep')
    territorio = fields.Many2one(comodel_name='res.country.state', string='Provincia', 
                                 related='orden_trabajo_id.provincia_id')
    uo = fields.Char(string='Unidad Organizativa', related='orden_trabajo_id.uo_abreviatura')
    especialidad_id = fields.Many2one(comodel_name='sicpro.nomenclador.especialidad', string='Especialidad',
                                      related='orden_trabajo_id.especialidad_id')
    fecha_inicio_cronograma = fields.Date(string='Inicio Cronograma', related='orden_trabajo_id.fecha_inicio_cronograma')
    fecha_fin_cronograma = fields.Date(string='Fin Cronograma', related='orden_trabajo_id.fecha_fin_cronograma')
    fecha_inicio_real = fields.Date(string='Inicio Real', related='orden_trabajo_id.fecha_inicio_real')
    fecha_fin_real = fields.Date(string='Fin Real', related='orden_trabajo_id.fecha_fin_real')
    dia = fields.Char(string="Día", required=False, default=fields.Datetime.now().strftime("%d"), )
    mes = fields.Char(string="Mes", required=False, default=fields.Datetime.now().strftime("%m"), )
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    cargo = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de Trabajo', related="certifica.ocupacion_id")

    def generar_reporte_anexo3(self):
        return self.env.ref('sicpro_app_ordenes_trabajo.informe_modelo_ordenes_anexo3_action').report_action(self.id)
