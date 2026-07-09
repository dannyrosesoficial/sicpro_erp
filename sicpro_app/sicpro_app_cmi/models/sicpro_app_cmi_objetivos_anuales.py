# -*- coding: utf-8 -*-

import json
from random import randint
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class AppCMIObjetivosAnuales(models.Model):
    _name = 'sicpro.app.cmi.objetivos.anuales'
    _order = "id asc"
    _description = 'Objetivos Anuales del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _compute_buscar_anios(self):
        anio_obj = self.env['sicpro.app.cmi.perspectivas.anios'].search(
            [('active', '=', True)])
        lst = []
        for anios in anio_obj:
            lst.append((anios.anio, anios.anio))
        return lst

    # Busca los datos de los indicadores
    def _context_anio(self):
        anio = str(self._context.get('default_anual'))
        return anio

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    obj_estrategico_id = fields.Many2one(
        'sicpro.app.cmi.objetivos.estrategicos', string='Objetivo Estratégico',
        required=True, )
    eje_estrategico_id = fields.Many2one(
        'sicpro.app.cmi.perspectivas.eje.estrategico', store=True,
        string='Eje Estratégicos',
        related='obj_estrategico_id.eje_estrategico_id')
    anio = fields.Selection(
        selection=_compute_buscar_anios, string="Año", required=True,
        default=_context_anio)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    detalles = fields.Char(string="Detalles", size=100, required=False, )
    porciento_superior = fields.Integer(string='Peso', required=True)
    obj_indicadores_ids = fields.One2many('sicpro.app.cmi.indicadores',
                                          'obj_anuales_id',
                                          string='Indicadores')
    json_indicadores = fields.Text(compute="_json_indicadores")
    real_acumulado = fields.Float(string='Real Acumulado',
                                    compute='compute_acumulado')
    meta_acumulado = fields.Float(string='Objetivo Acumulado',
                                    compute='compute_acumulado')
    incumplido = fields.Integer(string='Incumplido',
                                compute='compute_acumulado')
    diferencia_acumulado = fields.Float(
        string='diferencia', compute='compute_diferencia_porciento')
    porciento_avance = fields.Float(
        string='Porciento Avance', compute='compute_diferencia_porciento')
    porciento_avance_barra = fields.Float(
        string='Avance', compute='compute_diferencia_porciento')

    mes_temp = fields.Selection(string='Período',
        selection=[('enero', 'Enero'), ('febrero', 'Febrero'),
                   ('marzo', 'Marzo'), ('abril', 'Abril'), ('mayo', 'Mayo'),
                   ('junio', 'Junio'), ('julio', 'Julio'),
                   ('agosto', 'Agosto'), ('septiembre', 'Septiembre'),
                   ('octubre', 'Octubre'), ('noviembre', 'Noviembre'),
                   ('diciembre', 'Diciembre'), ('1t', 'Primer Trimestre'),
                   ('2t', 'Segundo Trimestre'), ('3t', 'Tercer Trimestre'),
                   ('4t', 'Cuarto Trimestre'), ('1s', 'Primer Semestre'),
                   ('2s', 'Segundo Semestre'), ('anual', 'Anual'), ],
        compute='compute_mes_temp')

    # calcula el mes temporal del context
    def compute_mes_temp(self):
        for item in self:
            item.mes_temp = self._context.get('default_periodo')

    # Busca los datos de los indicadores
    def _json_indicadores(self):
        dic = []
        for data in self:
            for ind in data.obj_indicadores_ids:
                dic.append({"id": ind.id,
                            "name": ind.name,
                            "condicion_presupuesto": ind.condicion_presupuesto,
                            "diferencia_acumulado": ind.diferencia_acumulado,
                            "porciento_barra1": round(ind.porciento_avance_barra)
                            })
            data.json_indicadores = json.dumps(dic)
            dic.clear()

    # calcula real y acumulado anual de sus indicadores
    def compute_acumulado(self):
        for data in self:
            periodo = self._context.get('default_periodo')
            real = 0
            meta = 0
            incumplido = 0
            datos = data.env['sicpro.app.cmi.indicadores'].search(
                [('obj_anuales_id', '=', data.id)])
            # sumo los valores de real y meta generales
            for item in datos:
                valores = data.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', item.id), ('mes', '=', periodo)])
                real += item.real_acumulado_kanban
                meta += item.meta_acumulado_kanban
                for cumplido in valores:
                    incumplido += cumplido.incumplido
            # paso los valores a los campos
            data.real_acumulado = real
            data.meta_acumulado = meta
            data.incumplido = incumplido
            
    # llamada para buscar al indicador especifico
    def action_indicadores(self):
        active_id = self._context.get('default_id')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.call_form_cmi_indicadores_dashboard_action')
        action['views'] = [(False, 'form')]
        action['res_id'] = active_id
        return action
    
    # calcula la diferencia y porciento del acumulado
    def compute_diferencia_porciento(self):
        for item in self:
            # calculo la diferencia del acumulado
            item.diferencia_acumulado = item.real_acumulado - item.meta_acumulado
            # calculo del porcentaje del acumulado
            if item.real_acumulado != 0 and item.meta_acumulado != 0:
                item.porciento_avance = round(item.real_acumulado / item.meta_acumulado, 2)
                item.porciento_avance_barra = round((item.real_acumulado / item.meta_acumulado) * 100, 2)
            else:
                item.porciento_avance = 0
                item.porciento_avance_barra = 0

    # llamada para ir a los indicadores
    def action_todos_indicadores(self):
        anio_activo = self._context.get('default_anual')
        periodo = self._context.get('default_periodo')
        action = self.env['ir.actions.act_window']._for_xml_id(
                'sicpro_app_cmi.cmi_indicadores_dashboard_action')
        action['context'] = {'default_anual': anio_activo,
                             'default_periodo': periodo,
                             'obj_anuales_id': self._origin.id}
        action['domain'] = [('anio', '=', anio_activo),
                            ('obj_anuales_id', '=', self.id)]
        return action

    @api.constrains('porciento_superior')
    def _check_valor_peso(self):
        valor = 0
        datos = self.env['sicpro.app.cmi.objetivos.anuales'].search(
            [('active', '=', True),
             ('obj_estrategico_id', '=', self.obj_estrategico_id.id),
             ('anio', '=', self.anio)])

        for item in datos:
            valor += item.porciento_superior
        if valor > 100:
            raise ValidationError(
                _('El valor del peso es superior al establecido, verifíquelo.'))