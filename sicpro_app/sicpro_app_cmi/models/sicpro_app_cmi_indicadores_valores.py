# -*- coding: utf-8 -*-


from random import randint
from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class AppCMIIndicadoresValores(models.Model):
    _name = 'sicpro.app.cmi.indicadores.valores'
    _order = "id asc"
    _description = 'Valores de los Indicadores del CMI'

    name = fields.Many2one('sicpro.app.cmi.indicadores', 'Nombre',
                           required=False, index=True)
    indicador_id = fields.Many2one('sicpro.app.cmi.indicadores', 'Indicadores',
                                   required=False, index=True)
    condicion_presupuesto = fields.Boolean(string="Condición de Presupuesto",
        related='indicador_id.condicion_presupuesto', )
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)

    mes = fields.Selection(
        [('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'),
         ('abril', 'Abril'), ('mayo', 'Mayo'), ('junio', 'Junio'),
         ('julio', 'Julio'), ('agosto', 'Agosto'),
         ('septiembre', 'Septiembre'), ('octubre', 'Octubre'),
         ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')], )
    real = fields.Float(string='Real', required=False)
    meta = fields.Float(string='Meta', required=False)
    diferencia = fields.Float(string='Diferencia',
                                compute='compute_diferencia')
    porciento = fields.Float(string='Porciento', required=False)
    porciento_pivot = fields.Float(string='%', required=False)
    comentario = fields.Text(string="Comentario", required=False)
    grupo_responsable = fields.Boolean(string='grupo_responsable',
                                       compute="_compute_grupo_responsable")
    incumplido = fields.Integer(string='Incumplido',
                                compute='compute_diferencia')

    # verifica q el usuario activo pertenezca al grupo Responsable
    def _compute_grupo_responsable(self):
        self.grupo_responsable = self.env['res.users'].has_group(
            'sicpro_app_cmi.grupo_app_cmi_responsable')

    # calculo el porciento y la diferencia del real y la meta
    @api.onchange("real", "meta")
    def compute_diferencia(self):
        for data in self:
            data.diferencia = data.real - data.meta

            if data.real != 0 and data.meta != 0:
                data.porciento = data.real / data.meta
                data.porciento_pivot = (data.real / data.meta) * 100
            else:
                data.porciento = 0
                data.porciento_pivot = 0

            # Comprueba si el acuerdo esta cumplido en dependencia
            # si es de presupuesto o no
            if data.condicion_presupuesto:
                if data.meta > data.real:
                    data.incumplido = 0
                else:
                    data.incumplido = 1
            else:
                if data.meta > data.real:
                    data.incumplido = 1
                else:
                    data.incumplido = 0
