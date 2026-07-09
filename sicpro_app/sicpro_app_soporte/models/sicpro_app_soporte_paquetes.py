# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SoportePaquetes(models.Model):

    _name = 'sicpro.app.soporte.paquetes'
    _description = 'Soporte de paquetes del sistema'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados.paquetes'].search([], limit=1).id

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(default=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados.paquetes',
                               string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id,)
    descripcion = fields.Text(string="Descripción", required=False)
    version_id = fields.Many2one(comodel_name='sicpro.app.soporte.versiones',
                                 string='Versión', required=True,
                                 domain="[('stage_id.inicial','=',True)]")
    aplicaciones = fields.Many2one(
        comodel_name='sicpro.app.soporte.aplicaciones', string='Aplicaciones',
        required=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados.paquetes'].search([])
        return stage_ids

    @api.constrains('version_id')
    def _crear_relacion_version(self):
        self.ensure_one()
        if self.version_id:
            paquete = self._origin.id
            version = self.version_id.id
            self.env['sicpro.app.soporte.versiones'].search(
                [('id', '=', version)]).write(
                {'paquetes_ids': [(None, paquete)], })
