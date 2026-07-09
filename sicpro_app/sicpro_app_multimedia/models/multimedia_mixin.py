# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields, api

class SicproMultimediaMixin(models.AbstractModel):
    _name = 'sicpro.multimedia.mixin'
    _description = 'Mixin de Conexión Multimedia Centralizada'

    multimedia_count = fields.Integer(string='Cantidad de Medios', compute='_compute_multimedia_count')

    def _compute_multimedia_count(self):
        for record in self:
            record.multimedia_count = self.env['sicpro.multimedia.asset'].search_count([
                ('res_model', '=', record._name),
                ('res_id', '=', record.id)
            ])

    def action_view_associated_multimedia(self):
        """Acción de pasarela para abrir la galería filtrada de este registro específico"""
        self.ensure_one()
        model_id = self.env['ir.model'].search([('model', '=', self._name)], limit=1)
        return {
            'name': 'Galería Multimedia',
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.multimedia.asset',
            'view_mode': 'kanban,list,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {
                'default_res_model_id': model_id.id,
                'default_res_id': self.id,
                'default_name': f'Adjunto_{self.display_name}'
            },
            'target': 'current',
        }

    def unlink(self):
        """Garantiza la integridad referencial borrando los medios asociados al destruir el padre"""
        for record in self:
            associated_assets = self.env['sicpro.multimedia.asset'].search([
                ('res_model', '=', record._name),
                ('res_id', '=', record.id)
            ])
            if associated_assets:
                associated_assets.unlink()
        return super(SicproMultimediaMixin, self).unlink()
