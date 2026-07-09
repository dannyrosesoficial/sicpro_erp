# -*- coding: utf-8 -*-

from odoo import fields, models


class CalendarCumplimientoReport(models.Model):
    _name = 'calendar.cumplimiento.reporte'
    _description = 'Cumplimiento del plan de trabajo'

    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', required=True)
    codigo_mes = fields.Integer(string="Código Mes", required=True, related='mes.codigo_mes')
    anio = fields.Char(string='Año', required=True, default=fields.Datetime.now().strftime("%Y"))
    type = fields.Selection([('calendario', 'Tipo de Calendario'), ('individual', 'Individuales')], default='calendario',
                            required=True, string="Tipo")
    tipo_calendario = fields.Many2one('calendar.tipo.calendario', string='Tipo de Calendario', required=False)
    descripcion_cumplimiento = fields.Text(string="Descripción", required=True,
                                           default="No se incumplieron tareas este mes.")

    def compute_cuenta_tareas(self):
        usuario = self.env.uid
        user = self.env['res.users'].search([('id', '=', usuario)])
        partner = user.partner_id.id
        cuenta_tareas_ids = []
        t_planificadas = 0
        t_cumplidas = 0
        t_incumplidas = 0
        t_modificadas = 0
        t_nuevas = 0

        if self.type == 'calendario':
            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten planificadas
            tareas_planificadas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ])
            for obj in tareas_planificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_planificadas += 1

            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten cumplidas
            tareas_cumplidas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ('cumplimiento_tarea', '=', 'cumplida')])
            for obj in tareas_cumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_cumplidas += 1
            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten incumplidas
            tareas_incumplidas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ('cumplimiento_tarea', '=', 'incumplida')])
            for obj in tareas_incumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_incumplidas += 1
            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten modificadas
            tareas_modificadas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ('modificacion_tarea', '=', True)])
            for obj in tareas_modificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_modificadas += 1

            data = {
                'planificadas': t_planificadas,
                'cumplidas': t_cumplidas,
                'incumplidas': t_incumplidas,
                'modificadas': t_modificadas,
                'nuevas': t_nuevas,
            }

            cuenta_tareas_ids.append(data)
            return cuenta_tareas_ids
        else:

            # Busco las tareas individuales del usuario y que esten planificadas
            tareas_planificadas = self.env['calendar.event'].search([('partner_ids', 'in', partner), ])
            for obj in tareas_planificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_planificadas += 1
            # Busco las tareas individuales del usuario y que esten cumplidas
            tareas_cumplidas = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner), ('cumplimiento_tarea', '=', 'cumplida')])
            for obj in tareas_cumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_cumplidas += 1
            # Busco las tareas individuales del usuario y que esten incumplidas
            tareas_incumplidas = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner), ('cumplimiento_tarea', '=', 'incumplida')])
            for obj in tareas_incumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_incumplidas += 1
            # Busco las tareas individuales del usuario y que esten modificadas
            tareas_modificadas = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner), ('modificacion_tarea', '=', True)])
            for obj in tareas_modificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    t_modificadas += 1

            data = {
                'planificadas': t_planificadas,
                'cumplidas': t_cumplidas,
                'incumplidas': t_incumplidas,
                'modificadas': t_modificadas,
                'nuevas': t_nuevas,
            }
            cuenta_tareas_ids.append(data)
            return cuenta_tareas_ids

    def report_busca_actividades(self):
        usuario = self.env.uid
        user = self.env['res.users'].search([('id', '=', usuario)])
        tz = user.tz
        partner = user.partner_id.id
        eventos_ids = []

        if self.type == 'calendario':

            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten incumplidas
            tareas_incumplidas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ('cumplimiento_tarea', '=', 'incumplida')])
            for obj in tareas_incumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    data_incumplidas = {
                        'evento': obj.name,
                        'causa': obj.incumplimiento_causa,
                        'tipo': 'incumplidas'
                    }
                    eventos_ids.append(data_incumplidas)

            # Busco las tareas que pertenezcan el tipo de calendario seleccionado y que esten modificadas
            tareas_modificadas = self.env['calendar.event'].search(
                [('tipo', '=', self.tipo_calendario.name), ('modificacion_tarea', '=', True)])
            for obj in tareas_modificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    data_modificadas = {
                        'evento': obj.name,
                        'usuarios': obj.modificacion_usuario,
                        'tipo': 'modificadas'
                    }
                    eventos_ids.append(data_modificadas)

            return eventos_ids
        else:
            # Busco las tareas individuales del usuario y que esten incumplidas
            tareas_incumplidas = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner), ('cumplimiento_tarea', '=', 'incumplida')])
            for obj in tareas_incumplidas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    data_incumplidas = {
                        'evento': obj.name,
                        'causa': obj.incumplimiento_causa,
                        'tipo': 'incumplidas'
                    }
                    eventos_ids.append(data_incumplidas)

            # Busco las tareas individuales del usuario y que esten modificadas
            tareas_modificadas = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner), ('modificacion_tarea', '=', True)])
            for obj in tareas_modificadas:
                if obj.start.month == self.codigo_mes and obj.start.year == int(self.anio):
                    data_modificadas = {
                        'evento': obj.name,
                        'usuarios': obj.modificacion_usuario,
                        'tipo': 'modificadas'
                    }
                    eventos_ids.append(data_modificadas)

            return eventos_ids

    def generar_reporte(self):
        return self.env.ref('sicpro_app_calendario.calendar_plan_trabajo_cumplimiento_report_action').report_action([],)