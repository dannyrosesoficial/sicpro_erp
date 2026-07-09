# -*- coding: utf-8 -*-


from odoo import fields, models, api


def get_graficos_ids(graficos):
    ids_graf = []
    for graf in graficos:
        ids_graf.append(graf._origin.id)
    return ids_graf


# noinspection SpellCheckingInspection
class SeccionesConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.secciones'
    _description = "Secciones del dashboard"
    _order = 'sequencia asc,id asc'

    # El nombre del grupo es para describir lo que contiene,
    # no se muestra en ningún lugar
    name = fields.Char(
        string='Nombre de la Sección',
        help='No se muestra en el tablero, es solo para identificarlo', )
    app = fields.Many2one(
        'ir.module.module', string='Aplicación',
        help='Nombre de la Aplicación, utilizado para vincular los gráficos, '
             'grupos y secciones (Ejemplo: En las secciones solo aparecerán '
             'los grupos que posean la misma aplicación. Lo mismo sucede con '
             'los grupos y gráficos)',
        required=True,
        ondelete='no action',
        )
    app_name = fields.Char(
        string='Nombre Aplicación',
        related='app.name',
    )
    sequencia = fields.Integer(
        string='Orden',
        help='Orden (de arriba hacia abajo) en que aparecerán las secciones en'
             ' el dashboard. Tener en cuenta que cada sección es una '
             'fila del dashboard',
        required=True,
        )
    grupos = fields.Many2many(
        'sicpro.modulo.dashboard.grupos', 'sicpro_modulo_dashboard_grup_rel',
        help='Grupos que contendrá la sección. Máximo 4 y generalmente se '
             'utiliza como cantidad de grupos un múltiplo de 12, '
             'debido al funcionamiento del css', string='Grupos',)
    graficos_izq = fields.Many2many(
        'sicpro.modulo.dashboard.graficos', 'sicpro_modulo_dashboard_graficos_izq_rel',
        help='Gráfico o gráficos que irán a la izquierda de la sección.\n'
             'Máximo 2 gráficos', string='Graf. Izq.',)
    grupo_izq = fields.Many2one(
        'sicpro.modulo.dashboard.grupos',
        help='Grupo que irá a la izquierda de la sección.', 
        string='Grupo Izq.',)
    graficos_centro_1 = fields.Many2many(
        'sicpro.modulo.dashboard.graficos', 'sicpro_modulo_dashboard_graficos_cent1_rel',
        help='Gráfico o gráficos que irán en el centro de la sección.\n'
             'Máximo 2 gráficos', string='Graf. Centro 1',)
    grupo_centro_1 = fields.Many2one(
        'sicpro.modulo.dashboard.grupos',
        help='Grupo que irá en el centro de la sección.', 
        string='Grupo Centro 1',)
    graficos_centro_2 = fields.Many2many(
        'sicpro.modulo.dashboard.graficos', 'sicpro_modulo_dashboard_graficos_cent2_rel',
        help='Gráfico o gráficos que irán en el centro de la sección luego de los gráficos \n'
             'de centro 1.\nMáximo 2 gráficos', string='Graf. Centro 2',)
    grupo_centro_2 = fields.Many2one(
        'sicpro.modulo.dashboard.grupos',
        help='Grupo que irá en el centro de la sección (despues de centro 1) de la sección.', 
        string='Grupo Centro 2',)
    graficos_der = fields.Many2many(
        'sicpro.modulo.dashboard.graficos', 'sicpro_modulo_dashboard_graficos_der_rel',
        help='Gráfico o gráficos que irán a la derecha de la sección.\n'
             'Máximo 2 gráficos', string='Graf. Der.',)
    grupo_der = fields.Many2one(
        'sicpro.modulo.dashboard.grupos',
        help='Grupo que irá a la derecha de la sección.', 
        string='Grupo Der.',)

    active = fields.Boolean('Activo', default=True)
    tableros_contenido = fields.Many2many('sicpro.modulo.dashboard.tableros',
                                          'sicpro_modulo_dashboard_tableros_rel',
                                          string='Tableros',)

    @api.onchange('graficos_izq', 'graficos_centro_1', 'graficos_centro_2', 'graficos_der')
    def _onchange_graficos(self):
        self.grupos=[(5,0,0)]
        if self.graficos_izq:
            ids_graf = get_graficos_ids(self.graficos_izq)
            if not self.grupo_izq:
                values_group = {'app': self.app.id, 'sequencia': '1', 'graficos': [(6,0,ids_graf)], 'name': str(self._origin.id) + '-izq'}
                id_grupo_creado = self.env['sicpro.modulo.dashboard.grupos'].create(values_group).id
                self.grupo_izq = id_grupo_creado
            else:
                self.grupo_izq.graficos = [(6,0,ids_graf)]
                self.grupo_izq.sequencia = '1'
            self.grupos = [(4,self.grupo_izq.id)]

        if self.graficos_centro_1:
            ids_graf = get_graficos_ids(self.graficos_centro_1)
            if not self.grupo_centro_1:
                values_group = {'app': self.app.id, 'sequencia': '2', 'graficos': [(6,0,ids_graf)], 'name': str(self._origin.id) + '-centro_1'}
                id_grupo_creado = self.env['sicpro.modulo.dashboard.grupos'].create(values_group).id
                self.grupo_centro_1 = id_grupo_creado
            else:
                self.grupo_centro_1.graficos = [(6,0,ids_graf)]
                self.grupo_centro_1.sequencia = '2'
            self.grupos = [(4,self.grupo_centro_1.id)]

        if self.graficos_centro_2:
            ids_graf = get_graficos_ids(self.graficos_centro_2)
            if not self.grupo_centro_2:
                values_group = {'app': self.app.id, 'sequencia': '3', 'graficos': [(6,0,ids_graf)], 'name': str(self._origin.id) + '-centro_2'}
                id_grupo_creado = self.env['sicpro.modulo.dashboard.grupos'].create(values_group).id
                self.grupo_centro_2 = id_grupo_creado
            else:
                self.grupo_centro_2.graficos = [(6,0,ids_graf)]
                self.grupo_centro_2.sequencia = '3'
            self.grupos = [(4,self.grupo_centro_2.id)]

        if self.graficos_der:
            ids_graf = get_graficos_ids(self.graficos_der)
            if not self.grupo_der:
                values_group = {'app': self.app.id, 'sequencia': '4', 'graficos': [(6,0,ids_graf)], 'name': str(self._origin.id) + '-der'}
                id_grupo_creado = self.env['sicpro.modulo.dashboard.grupos'].create(values_group).id
                self.grupo_der = id_grupo_creado
            else:
                self.grupo_der.graficos = [(6,0,ids_graf)]
                self.grupo_der.sequencia = '4'
            self.grupos = [(4,self.grupo_der.id)]


    def write(self, vals):
        res = super(SeccionesConfig, self).write(vals)
        if 'graficos_izq' in vals or 'graficos_centro_1' in vals or 'graficos_centro_2' in vals or 'graficos_der' in vals:
            self._onchange_graficos()
        return res



        
