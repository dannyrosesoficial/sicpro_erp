# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import timedelta, datetime


class TrabajadoresCierreWizard(models.TransientModel):
    _name = "sicpro.app.trabajadores.cierre.wizard"
    _description = "Generar cierre de Capital Humano"

    def _areas_ids(self):
        areas = self.env['sicpro.app.trabajadores.areas'].search([('active', '=', True)])
        if areas:
            return areas

    areas = fields.Many2many('sicpro.app.trabajadores.areas', 'areas_cierre_wizard_rel', 'areas_id', 'wizard_id',
                             string="Áreas", default=_areas_ids, )

    def analizar_totales(self, area_id, total_altas, total_bajas):
        hoy = datetime.today()
        mes_cierre, anio_cierre = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        mes_anterior, anio = (mes_cierre - 1, anio_cierre) if hoy.month != 1 else (12, anio_cierre - 1)

        area_totales_mes_cierre = self.env['sicpro.app.trabajadores.areas.totales'].search(
            ['&', ('name', '=', area_id), ('codigo_mes', '=', mes_cierre), ('anio', '=', anio_cierre)])
        area_totales_mes_anterior = self.env['sicpro.app.trabajadores.areas.totales'].search(
            ['&', ('name', '=', area_id), ('codigo_mes', '=', mes_anterior), ('anio', '=', anio)])

        if area_totales_mes_cierre and area_totales_mes_anterior:
            supuesto_total = area_totales_mes_anterior.total + total_altas - total_bajas
            if area_totales_mes_cierre.total != supuesto_total:
                area_totales_mes_cierre.write({'estado': 'error'})
                return 'error'
        return 'ok'

    def existe_cierre_anterior(self):
        hoy = datetime.today()
        mes, anio = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        nombre_mes = self.env['sicpro.nomenclador.meses'].search(['&', ('active', '=', True), ('codigo_mes', '=', mes)])
        historial_cierre = self.env['sicpro.app.trabajadores.cierre.historial'].search(
            ['&', ('mes', '=', nombre_mes.id), ('anio', '=', anio)])
        if historial_cierre:
            historial_cierre.write({'name': 'archivado'})
            return {'name': 'Atención', 'type': "ir.actions.act_window",
                    'res_model': "sicpro.app.trabajadores.dialog.wizard", 'view_mode': 'form', 'view_type': 'form',
                    'target': "new", 'context': {'default_areas': self.areas}}
        else:
            return self.generar_cierre()

    def generar_cierre(self):

        hoy = datetime.today()
        total_trabajdores = 0
        total_bajas = 0
        total_altas = 0
        mes_anterior, anio = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        cierre = None

        nombre_mes = self.env['sicpro.nomenclador.meses'].search(
            ['&', ('active', '=', True), ('codigo_mes', '=', mes_anterior)])

        areas = self._areas_ids()

        for area in areas:

            trabajadores_activos = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', True), ('area_id.id', '=', area.id)])
            trabajadores_inactivos = self.env['sicpro.app.trabajadores'].search(
                ['&', ('active', '=', False), ('area_id.id', '=', area.id)])
            total_activo = len(trabajadores_activos)
            altas = []
            bajas = []

            for trabajador in trabajadores_activos:
                if trabajador:
                    fecha = trabajador.inicio_contrato
                    if fecha and fecha.month == mes_anterior and fecha.year == anio:
                        altas.append(trabajador)

            for trabajador in trabajadores_inactivos:
                fecha = trabajador.fecha_baja
                if fecha and fecha.month == mes_anterior and fecha.year == anio:
                    bajas.append(trabajador)

            cierre = self.env['sicpro.app.trabajadores.cierre'].search(
                ['&', ('name', '=', area.id), ('mes', '=', nombre_mes.id), ('anio', '=', anio)])
            if cierre:
                cierre.write({'active': False})

                cierre = self.env['sicpro.app.trabajadores.cierre'].create(
                    {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'total': total_activo, 'altas': len(altas),
                        'bajas': len(bajas)})
            else:
                cierre = self.env['sicpro.app.trabajadores.cierre'].create(
                    {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'total': total_activo, 'altas': len(altas),
                        'bajas': len(bajas)})

            area_totales = self.env['sicpro.app.trabajadores.areas.totales'].search(
                ['&', ('name', '=', area.id), ('mes', '=', nombre_mes.id), ('anio', '=', anio)])
            if area_totales:
                area_totales.write({'active': False})

                self.env['sicpro.app.trabajadores.areas.totales'].create(
                    {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'total': total_activo})

            else:
                self.env['sicpro.app.trabajadores.areas.totales'].create(
                    {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'total': total_activo})

            estado = self.analizar_totales(area.id, len(altas), len(bajas))

            cierre.write({'estado': estado})

            list_altas_bajas = self.env['sicpro.app.trabajadores.areas.altas.bajas'].search(
                ['&', ('name', '=', area.id), ('mes', '=', nombre_mes.id), ('anio', '=', anio)])

            for alta_baja in list_altas_bajas:
                if alta_baja:
                    alta_baja.write({'active': False})

            for trabajador in altas:
                if trabajador:
                    self.env['sicpro.app.trabajadores.areas.altas.bajas'].create(
                        {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'trabajador': trabajador.id,
                            'estado': 'alta', 'fecha': trabajador.inicio_contrato})

            for trabajador in bajas:
                if trabajador:
                    self.env['sicpro.app.trabajadores.areas.altas.bajas'].create(
                        {'name': area.id, 'mes': nombre_mes.id, 'anio': anio, 'trabajador': trabajador.id,
                            'estado': 'baja', 'fecha': trabajador.fecha_baja})

            total_trabajdores = total_trabajdores + total_activo
            total_altas = total_altas + len(altas)
            total_bajas = total_bajas + len(bajas)

        if cierre is not None:
            cierre.notificar_nuevo_cierre()
            self.env['sicpro.app.trabajadores.cierre.historial'].create(
                {'name': 'activo', 'mes': nombre_mes.id, 'anio': anio, 'total': total_trabajdores, 'altas': total_altas,
                    'bajas': total_bajas, 'usuario': self.env.user.id})

        action = self.env.ref('sicpro_app_trabajadores.trabajadores_cierre_action').sudo().read()[0]
        return action
