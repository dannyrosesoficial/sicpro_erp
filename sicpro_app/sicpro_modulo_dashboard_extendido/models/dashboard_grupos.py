# -*- coding: utf-8 -*-


from odoo import fields, models


class GruposConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.grupos'
    _description = "Grupos de las secciones del dashboard"

    # El nombre del grupo es para describir lo que contiene,
    # no se muestra en ningún lugar
    name = fields.Char(
        string='Nombre del Grupo',
        help='No se muestra en el tablero, es solo para identificarlo', )
    app = fields.Many2one(
        'ir.module.module', string='Aplicación',
        help='Nombre de la Aplicación, utilizado para vincular los gráficos, '
             'grupos y secciones (Ejemplo: En las secciones solo aparecerán '
             'los grupos que posean la misma aplicación. '
             'Lo mismo sucede con los grupos y gráficos)''',
        required=True,
        ondelete='no action',
        )
    app_name = fields.Char(
        string='Nombre Aplicación',
        related='app.name',
    )
    sequencia = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ], store=True,
        default='1', string="Orden",
        help='Orden (de izquierda a derecha) en que aparecerán los grupos '
             'dentro de cada sección (fila) en que se encuentran. '
             'Tener en cuenta que los grupos son como las columnas en que se '
             'divide cada sección (columnas de 1 o 2 elementos solamente)',
        required=True,
        )
    graficos = fields.Many2many(
        'sicpro.modulo.dashboard.graficos',
        'sicpro_modulo_dashboard_graficos_rel', string='Gráficos',
        help='Gráficos que contendrá el grupo. '
             'Máximo 2 (uno arriba y uno abajo). Generalmente se utiliza un '
             'grupo por cada gráfico''', )
    active = fields.Boolean('Activo', default=True)
    secciones_contenido = fields.Many2many('sicpro.modulo.dashboard.secciones',
                                           'sicpro_modulo_dashboard_secciones_rel',
                                           string='Secciones',)
            

