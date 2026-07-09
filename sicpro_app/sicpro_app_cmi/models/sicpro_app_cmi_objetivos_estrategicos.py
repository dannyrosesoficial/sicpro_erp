# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import json
from random import randint
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
from odoo import fields, models, api
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class AppCMIObjetivosEstrategicos(models.Model):
    _name = 'sicpro.app.cmi.objetivos.estrategicos'
    _order = "id asc"
    _description = 'Objetivos Estratégicos del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, tracking=True, index=True)
    perspectivas_id = fields.Many2one('sicpro.app.cmi.perspectivas',
                                      string='Perspectiva', required=True, )
    eje_estrategico_id = fields.Many2one(
        'sicpro.app.cmi.perspectivas.eje.estrategico', required=True,
        string='Eje Estratégicos', index=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    detalles = fields.Char(string="Detalles", size=100, required=False)
    porciento_superior = fields.Integer(string='Peso', required=True)
    obj_anuales_ids = fields.One2many(
        'sicpro.app.cmi.objetivos.anuales', 'obj_estrategico_id',
        string='Objetivos Anuales')
    json_anuales = fields.Text(compute="_json_anuales")
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
                                compute='compute_mes_anio_temp')
    anio_temp = fields.Char(string="Año", compute='compute_mes_anio_temp')

    # calcula el mes temporal del context
    def compute_mes_anio_temp(self):
        for item in self:
            item.mes_temp = self.env.context.get('default_periodo')
            item.anio_temp = self.env.context.get('default_anual')

    # Busca los datos de los objetivos anuales
    def _json_anuales(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        dic = []
        for data in self:
            for obj in data.obj_anuales_ids.filtered(
                    lambda l: l.anio == str(anio_activo)):

                objetivo_incumplido = 0
                for ind in obj.obj_indicadores_ids:
                    for valores in ind.indicadores_ids.filtered(
                            lambda l: l.mes == str(periodo)):
                        objetivo_incumplido += valores.incumplido

                dic.append({"id": obj.id,
                            "name": obj.name,
                            "incumplido": objetivo_incumplido,
                            })
            data.json_anuales = json.dumps(dic)
            dic.clear()

    # Busca los datos de los indicadores
    def _json_indicadores(self):
        dic = []
        for data in self:
            for obj in data.obj_anuales_ids:
                for ind in obj.obj_indicadores_ids:
                    dic.append(
                        {"id_anual": obj.id,
                         "id": ind.id,
                         "name": ind.name,
                         "condicion_presupuesto": ind.condicion_presupuesto,
                         "diferencia_acumulado": ind.diferencia_acumulado,
                         "porciento_barra1": round(ind.porciento_avance_barra),
                         })
            data.json_indicadores = json.dumps(dic)
            dic.clear()

    # llamada para ir al objetivo anuales específico
    def action_objetivos_anuales(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        action = self.env['ir.actions.act_window']._for_xml_id(
                'sicpro_app_cmi.cmi_objetivos_anuales_dashboard_action')
        action['context'] = {'default_anual': anio_activo,
                             'default_periodo': periodo,
                             'default_obj_estrategico_id': self._origin.id}
        action['domain'] = [('anio', '=', anio_activo),
                            ('obj_estrategico_id', '=', self.id)]
        return action

    # llamada para buscar al indicador específico
    def action_indicadores(self):
        active_id = self.env.context.get('default_id')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.call_form_cmi_indicadores_dashboard_action')
        action['views'] = [(False, 'form')]
        action['res_id'] = active_id
        return action

    # calcula real y acumulado anual de sus indicadores
    def compute_acumulado(self):
        for data in self:
            anio_activo = self.env.context.get('default_anual')
            real = 0
            meta = 0
            incumplido = 0
            datos = data.env['sicpro.app.cmi.objetivos.anuales'].search(
                [('obj_estrategico_id', '=', data.id),
                 ('anio', '=', anio_activo)])
            # sumo los valores de real y meta generales
            for item in datos:
                real = real + item.real_acumulado
                meta = meta + item.meta_acumulado
                incumplido += item.incumplido
            # paso los valores a los campos
            data.real_acumulado = real
            data.meta_acumulado = meta
            data.incumplido = incumplido

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

    @api.constrains('porciento_superior')
    def _check_valor_peso(self):
        valor = 0
        datos = self.env['sicpro.app.cmi.objetivos.estrategicos'].search(
            [('active', '=', True),
             ('perspectivas_id', '=', self.perspectivas_id.id)])

        for item in datos:
            valor += item.porciento_superior
        if valor > 100:
            raise ValidationError("El valor del peso es superior al establecido, verifíquelo.\n\n" + MSG_SOPORTE_SICPRO)