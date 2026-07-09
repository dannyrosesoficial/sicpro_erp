# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from calendar import monthrange
from datetime import datetime, date
from pytz import UTC, timezone
from odoo import fields, models


class CalendarPlanReport(models.Model):
    _name = 'calendar.plan.reporte'
    _description = 'Reportes del plan de trabajo'

    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', required=True)
    codigo_mes = fields.Integer(string="Código Mes", required=True,
                                related='mes.codigo_mes')
    anio = fields.Char(string='Año', required=True,
                       default=fields.Datetime.now().strftime("%Y"))
    type = fields.Selection(
        [('all', 'Todos los eventos'), ('selected', 'Organizados por mí')],
        default='all', required=True, string="Tipo")
    plan = fields.Many2one('calendar.tipo.calendario',
                           string='Plantilla Impresión', required=True)
    plan_dvpe = fields.Boolean(string='Inf. DVPE', related='plan.tipo_dvpe')

    def report_busca_dias(self):
        mes = self.codigo_mes
        anio = int(self.anio)
        dias_ids = []

        num_dias = monthrange(anio, mes)[1]
        dias_final = num_dias + 1

        dia = 1
        while dia < dias_final:
            data = {'dia': dia, 'nombre': date(anio, mes, dia).strftime(
                '%A').capitalize(), }
            dias_ids.append(data)
            dia += 1
        return dias_ids

    def report_busca_calendario(self):
        usuario = self.env.uid
        user = self.env['res.users'].search([('id', '=', usuario)])
        tz = user.tz
        partner = user.partner_id.id
        eventos_ids = []

        if self.type == 'all':
            # Busco las tareas del organizado por el usuario y también en las que participa
            records = self.env['calendar.event'].search(
                [('partner_ids', 'in', partner)])

            for obj in records:
                if obj.start.month == self.codigo_mes and obj.start.year == int(
                    self.anio):
                    if obj.allday:
                        hora_control = 'Todo el día'
                    else:
                        hora_control = datetime.strftime(
                            obj.start.replace(tzinfo=UTC).astimezone(
                                timezone(tz)).replace(tzinfo=None), "%H:%M")

                    data = {'evento': obj.name,
                            'participantes': obj.participantes_ids,
                            'dirige': obj.dirige,
                            'dirige_externos': obj.dirige_externos,
                            'tipo_ubicacion': obj.tipo_ubicacion,
                            'ubicacion': obj.location,
                            'ubicacion_dvpe': obj.ubicacion.name,
                            'fecha': datetime.strftime(
                                obj.start.replace(tzinfo=UTC).astimezone(
                                    timezone(tz)).replace(tzinfo=None),
                                "%d-%m-%Y"), 'hora': hora_control,
                            'dia': obj.start.day, 'mes': obj.start.month,
                            'anio': obj.start.year,
                            'tipo_tarea': obj.tipo_tarea, }

                    eventos_ids.append(data)
            return eventos_ids
        else:
            # Busco las tareas del organizado por el usuario
            records = self.env['calendar.event'].search(
                [('user_id', '=', usuario)])

            for obj in records:
                if obj.start.month == self.codigo_mes and obj.start.year == int(
                    self.anio):
                    if obj.allday:
                        hora_control = 'Todo el día'
                    else:
                        hora_control = datetime.strftime(
                            obj.start.replace(tzinfo=UTC).astimezone(
                                timezone(tz)).replace(tzinfo=None), "%H:%M")

                    data = {'evento': obj.name,
                            'participantes': obj.participantes_ids,
                            'dirige': obj.dirige,
                            'dirige_externos': obj.dirige_externos,
                            'tipo_ubicacion': obj.tipo_ubicacion,
                            'ubicacion': obj.location,
                            'ubicacion_dvpe': obj.ubicacion.name,
                            'fecha': datetime.strftime(
                                obj.start.replace(tzinfo=UTC).astimezone(
                                    timezone(tz)).replace(tzinfo=None),
                                "%d-%m-%Y"), 'hora': hora_control,
                            'dia': obj.start.day, 'mes': obj.start.month,
                            'anio': obj.start.year,
                            'tipo_tarea': obj.tipo_tarea, }
                    eventos_ids.append(data)
            return eventos_ids

    def generar_reporte(self):
        if self.plan_dvpe:
            return self.env.ref(
                'sicpro_app_calendario.calendar_plan_trabajo_dvpe_report_action').report_action(
                [], )
        else:
            return self.env.ref(
                'sicpro_app_calendario.calendar_plan_trabajo_report_action').report_action(
                [], )
