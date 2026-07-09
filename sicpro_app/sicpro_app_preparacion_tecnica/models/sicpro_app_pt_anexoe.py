# -*- coding: utf-8 -*-

from odoo import fields, models


class PreparacionTecnicaNomencladorEnexoE(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.nomenclador.anexoe'
    _description = 'Nomenclador Anexo E de la Preparación Técnica'
    _order = "sequence, name, id"

    name = fields.Char('Prueba', required=True, )
    sequence = fields.Integer('Secuencia', default=1, )
    descripcion = fields.Char('Requerimientos')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)


class PreparacionTecnicaEnexoE(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.anexoe'
    _description = 'Anexo E de la Preparación Técnica'
    _order = "sequence, name, id"

    name = fields.Many2one(
        comodel_name='sicpro.app.preparacion.tecnica.nomenclador.anexoe',
        string='Pruebas', required=True,
        domain="[('company_id', '=', company_id)]")
    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    sequence = fields.Integer('Secuencia', related="name.sequence", store=True)
    descripcion = fields.Char('Requerimientos', related='name.descripcion',
                              readonly=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    vals = fields.Integer(default=1)
