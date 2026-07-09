# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class FuerzasMediosEstados(models.Model):
    _name = "sicpro.app.fuerzas.medios.estados"
    _description = "Estado de las fuerzas y medios"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Char('Nombre del estado', required=True)
    sequence = fields.Integer('Secuencia', default=1,)
    is_en_proceso = fields.Boolean('¿Es la Etapa de Ejecución?')
    is_terminada = fields.Boolean('¿Es la Etapa Terminada?')
    is_paralizado = fields.Boolean('¿Es la Etapa Paralizada?')
    is_cancelado = fields.Boolean('¿Es la Etapa Cancelada?')
    requirements = fields.Text('Requerimientos')
    fold = fields.Boolean('Replegado en la vista Kanban',)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    active = fields.Boolean('Activo', default=True)
