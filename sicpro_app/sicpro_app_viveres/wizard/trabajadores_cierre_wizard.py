# -*- coding: utf-8 -*-


from odoo import fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class TrabajadoresCierreWizard(models.TransientModel):
    _inherit = "sicpro.app.trabajadores.cierre.wizard"

    def llenar_datos_cierre(self, mes, anio):
        nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                ['&', ('active', '=', True), ('codigo_mes', '=', mes)])
        areas = self.env['sicpro.app.viveres.areas'].search([('active', '=', True)])

        for area in areas:
            trabajadores_cierre = []
            trabajadores_altas_bajas = []
            if area.name.tipo_registro == 'sin_categoría':
                trabajadores_cierre = self.env['sicpro.app.trabajadores.cierre'].search([
                    '&', ('active', '=', True), ('name.id', '=' , area.name.id), ('codigo_mes', '=', mes), ('anio', '=', anio)])
                trabajadores_altas_bajas = self.env['sicpro.app.trabajadores.areas.altas.bajas'].search([
                    '&', ('active', '=', True), ('name.id', '=' , area.name.id), ('codigo_mes', '=', mes), ('anio', '=', anio)])
            else:
                trabajadores_cierre = self.env['sicpro.app.trabajadores.cierre'].search([
                    '&', ('active', '=', True), ('codigo_mes', '=', mes), ('anio', '=', anio), 
                    '|', ('name.id', '=' , area.name.id), ('name.parent_id.id', '=' , area.name.id)])
                trabajadores_altas_bajas = self.env['sicpro.app.trabajadores.areas.altas.bajas'].search([
                    '&', ('active', '=', True), ('codigo_mes', '=', mes), ('anio', '=', anio),
                    '|', ('name.id', '=' , area.name.id), ('name.parent_id.id', '=' , area.name.id)])
            
            total_area = 0
            total_area_altas = 0
            total_area_bajas = 0
            for cierre_ch in trabajadores_cierre:
                if cierre_ch:
                    total_area = total_area + cierre_ch.total
                    total_area_altas = total_area_altas + cierre_ch.altas
                    total_area_bajas = total_area_bajas + cierre_ch.bajas

            cierre_viveres = self.env['sicpro.app.viveres.cierre'].search(
            ['&', ('name', '=', area.id), 
                ('mes', '=', nombre_mes.id), 
                ('anio', '=', anio)])

            if cierre_viveres:
                cierre_viveres.sudo().write({'active': False})

                self.env['sicpro.app.viveres.cierre'].sudo().create({
                    'name': area.id, 
                    'mes': nombre_mes.id,
                    'anio': anio,
                    'total': total_area, 
                    'altas': total_area_altas,
                    'bajas': total_area_bajas,
                    'estado': cierre_ch.estado})
            else:
                self.env['sicpro.app.viveres.cierre'].sudo().create({
                    'name': area.id, 
                    'mes': nombre_mes.id,
                    'anio': anio,
                    'total': cierre_ch.total, 
                    'altas': cierre_ch.altas,
                    'bajas': cierre_ch.bajas,
                    'estado': cierre_ch.estado})

            for alta_o_baja in trabajadores_altas_bajas:
                trabajador = self.env['sicpro.app.viveres.areas.altas.bajas'].search(
                    [('trabajador', '=', alta_o_baja.trabajador.id)])

                if trabajador:
                    trabajador.sudo().write({'active': False})

                    self.env['sicpro.app.viveres.areas.altas.bajas'].sudo().create({
                            'name': alta_o_baja.name.id, 
                            'mes': alta_o_baja.mes.id,
                            'anio': alta_o_baja.anio,
                            'trabajador': alta_o_baja.trabajador.id,
                            'estado': alta_o_baja.estado,
                            'fecha': alta_o_baja.fecha})
                
                else:
                    self.env['sicpro.app.viveres.areas.altas.bajas'].sudo().create({
                            'name': alta_o_baja.name.id, 
                            'mes': alta_o_baja.mes.id,
                            'anio': alta_o_baja.anio,
                            'trabajador': alta_o_baja.trabajador.id,
                            'estado': alta_o_baja.estado,
                            'fecha': alta_o_baja.fecha})

    def generar_cierre(self):

        super(TrabajadoresCierreWizard, self).generar_cierre()
        
        hoy = datetime.today() 
        mes, anio = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        self.llenar_datos_cierre(mes, anio)