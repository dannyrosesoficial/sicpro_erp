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
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


def _default_color():
    return randint(1, 11)


class AppCMIPerspectivas(models.Model):
    _name = 'sicpro.app.cmi.perspectivas'
    _order = "id asc"
    _description = 'Perspectivas del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    name = fields.Char(string='Nombre', size=35, required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, tracking=True, index=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    detalles = fields.Char(string="Detalles", size=100, required=False, )
    porciento_superior = fields.Integer(string='Peso', required=True)

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
    obj_estrategico_ids = fields.One2many(
        'sicpro.app.cmi.objetivos.estrategicos', 'perspectivas_id',
        string='Objetivos Estratégicos')
    json_estrategicos = fields.Text(compute="_json_estrategicos")
    json_anuales = fields.Text(compute="_json_anuales")
    json_indicadores = fields.Text(compute="_json_indicadores")
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

    # calcula real y acumulado anual de sus indicadores
    def compute_acumulado(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        for data in self:
            real = 0
            meta = 0
            incumplido = 0
            datos = data.env['sicpro.app.cmi.objetivos.estrategicos'].search(
                [('perspectivas_id', '=', data.id),
                 ('obj_anuales_ids.anio', '=', anio_activo)])
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

    # Busca los datos de los objetivos estratégicos
    def _json_estrategicos(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        dic = []
        for data in self:
            for obj in data.obj_estrategico_ids:
                objetivos_incumplido = 0
                for anu in obj.obj_anuales_ids.filtered(
                        lambda l: l.anio == str(anio_activo)):
                    for ind in anu.obj_indicadores_ids:
                        for valores in ind.indicadores_ids.filtered(
                                lambda l: l.mes == str(periodo)):
                            objetivos_incumplido += valores.incumplido

                dic.append({"id": obj.id,
                            "name": obj.name,
                            "incumplido": objetivos_incumplido,
                            })
            data.json_estrategicos = json.dumps(dic)
            dic.clear()

    # Busca los datos de los objetivos anuales
    def _json_anuales(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        dic = []
        for data in self:
            for est in data.obj_estrategico_ids:
                for obj in est.obj_anuales_ids.filtered(
                        lambda l: l.anio == str(anio_activo)):

                    objetivo_incumplido = 0
                    for ind in obj.obj_indicadores_ids:
                        for valores in ind.indicadores_ids.filtered(
                                lambda l: l.mes == str(periodo)):
                            objetivo_incumplido += valores.incumplido

                    dic.append(
                        {"id": obj.id,
                         "id_estrategico": est.id,
                         "name": obj.name,
                         "incumplido": objetivo_incumplido,
                         })
            data.json_anuales = json.dumps(dic)
            dic.clear()

    # Busca los datos de los indicadores
    def _json_indicadores(self):
        dic = []
        for data in self:
            for est in data.obj_estrategico_ids:
                for obj in est.obj_anuales_ids:
                    for ind in obj.obj_indicadores_ids:
                        dic.append(
                            {"id_anual": obj.id,
                             "id": ind.id,
                             "name": ind.name,
                             "condicion_presupuesto": ind.condicion_presupuesto,
                             "diferencia_acumulado": ind.diferencia_acumulado,
                             "porciento_barra1": round(ind.porciento_avance_barra)
                             })
            data.json_indicadores = json.dumps(dic)
            dic.clear()

    # llamada para ir al objetivo estratégico especifico
    def action_objetivos_estrategicos(self):
        anio_activo = self.env.context.get('default_anual')
        periodo = self.env.context.get('default_periodo')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.cmi_objetivos_estrategicos_dashboard_action')
        action['context'] = {'default_anual': anio_activo,
                             'default_periodo': periodo,
                             'default_perspectivas_id': self._origin.id}
        action['domain'] = [('perspectivas_id', '=', self.id)]
        return action

    # llamada para ir al objetivo anual especifico
    def action_objetivos_anual(self):
        anio_activo = self.env.context.get('default_anual')
        obj_estrategico_id = self.env.context.get('default_obj_estrategico_id')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.call_cmi_objetivos_anuales_dashboard_action')
        action['context'] = {'default_anual': anio_activo}
        action['domain'] = [('obj_estrategico_id', '=', obj_estrategico_id),
                            ('anio', '=', anio_activo)]
        return action

        # llamada para ir al objetivo anual especifico

    def action_indicadores_general(self):
        obj_anuales_id = self.env.context.get('default_obj_anuales_id')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.call_cmi_indicadores_dashboard_action')
        action['context'] = {'obj_anuales_id': obj_anuales_id}
        action['domain'] = [('obj_anuales_id', '=', obj_anuales_id)]
        return action

    # llamada para buscar al indicador especifico
    def action_indicadores(self):
        active_id = self.env.context.get('default_id')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.call_form_cmi_indicadores_dashboard_action')
        action['views'] = [(False, 'form')]
        action['res_id'] = active_id
        return action

    @api.constrains('porciento_superior')
    def _check_valor_peso(self):
        valor = 0
        datos = self.env['sicpro.app.cmi.perspectivas'].search(
            [('active', '=', True)])

        for item in datos:
            valor += item.porciento_superior
        if valor > 100:
            raise ValidationError("El valor del peso es superior al establecido, verifíquelo.\n\n" + MSG_SOPORTE_SICPRO)
