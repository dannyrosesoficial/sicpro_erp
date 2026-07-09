# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import datetime

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class SicproWebVersion(models.Model):
    _name = 'sicpro.modulo.web.version'
    _description = 'Configuración de la Version del Sistema'
    _order = 'name asc'

    name = fields.Char(string='Número de Versión', required=True)
    date_release = fields.Date(string='Fecha de Lanzamiento',
                               default=fields.Date.context_today)
    line_ids = fields.One2many('sicpro.modulo.web.version.line', 'version_id',
                               string='Cambios Realizados')
    version_actual = fields.Boolean(string='Versión Actual', default=False)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('version_actual')
    def _check_single_current_version(self):
        for record in self:
            if record.version_actual:
                if self.search_count([('version_actual', '=', True),
                                      ('id', '!=', record.id)]) > 0:
                    raise ValidationError(
                        "Ya existe una versión marcada como actual.\n\n" + MSG_SOPORTE_SICPRO)

    @api.model
    def get_roadmap_data(self):
        return self.sudo().search([], order="name desc")

    # este metodo calcula las estadísticas en tiempo real para la web inicial
    # no tiene que ver con el modelo de versiones, lo pongo aquí porque
    # necesito de un modelo para ejecutarlo
    @api.model
    def get_sicpro_estadisticas_web(self):
        current_year = datetime.now().year
        year_start = datetime(current_year, 1, 1)

        # 1. Cantidad de usuarios (Especialistas: no externos/portal)
        users_count = self.env['res.users'].sudo().search_count(
            [('active', '=', True)])

        # 2. Cantidad de Compañías / Entidades
        companies_count = self.env['res.company'].sudo().search_count([])

        # 3. Solicitudes de trabajo del año actual (Basado en Tareas de Proyecto)
        # Se filtra por fecha de creación mayor o igual al 1ro de enero del año actual
        requests_count = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().search_count(
            [('create_date', '>=', year_start)])

        return {'usuarios': f"{users_count}",
                'companias': f"{companies_count}",
                'solicitudes': f"{requests_count}", 'auditoria': "100%",
                'anio_actual': current_year
                # Lo pasamos por si quieres usarlo en el texto
                }

    # este metodo calcula indicadores reales de SICPRO en tiempo real para
    # la web inicial
    # no tiene que ver con el modelo de versiones, lo pongo aquí porque
    # necesito de un modelo para ejecutarlo
    @api.model
    def get_dashboard_data_web(self):
        current_year = datetime.now().year
        year_start = datetime(current_year, 1, 1)

        # 1. Solicitudes Procesadas (Solicitudes convertidas en oportunidad)
        total_solicitudes = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().search_count(
            [('create_date', '>=', year_start)])
        procesadas = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().search_count(
            [('create_date', '>=', year_start), ('type', '=', 'oportunidad')
             # O el estado que uses para "Procesada"
             ])
        porcentaje_solicitudes = int((
                                             procesadas / total_solicitudes * 100)) if total_solicitudes > 0 else 0

        # 2. Órdenes de Trabajo Ejecutándose
        total_ot = self.env['sicpro.app.ordenes.trabajo'].sudo().search_count(
            [('create_date', '>=', year_start)])
        ejecutadas_ot = self.env[
            'sicpro.app.ordenes.trabajo'].sudo().search_count(
            [('create_date', '>=', year_start), ('is_en_proceso', '=', True)])
        porcentaje_ot = int(
            (ejecutadas_ot / total_ot * 100)) if total_ot > 0 else 0

        # 3. Gastos Certificados (Comparativa vs Meta o Presupuesto)
        # Aquí podrías comparar el monto certificado contra el total planeado
        total_gastos = self.env[
            'sicpro.app.transferencias.gastos'].sudo().search_count(
            [('create_date', '>=', year_start)])
        certificados = self.env[
            'sicpro.app.transferencias.gastos'].sudo().search_count(
            [('create_date', '>=', year_start), ('contabilizado', '=', True)])
        porcentaje_gastos = int(
            (certificados / total_gastos * 100)) if total_gastos > 0 else 0

        return {'solicitudes': {'valor': porcentaje_solicitudes,
                                'texto': f"{procesadas} de {total_solicitudes} finalizadas"},
                'ot': {'valor': porcentaje_ot,
                       'texto': f"{ejecutadas_ot} de {total_ot} cerradas"},
                'gastos': {'valor': porcentaje_gastos,
                           'texto': f"{certificados} certificaciones emitidas"},
                'anio': current_year}


class SicproWebVersionLine(models.Model):
    _name = 'sicpro.modulo.web.version.line'
    _description = 'Líneas de Cambio de Versión'

    version_id = fields.Many2one('sicpro.modulo.web.version', string='Versión',
                                 ondelete='cascade')
    name = fields.Char(string='Descripción del Cambio', required=True)
    tipo = fields.Selection(
        [('feat', 'Mejora/Nueva Función'), ('fix', 'Corrección de Error'),
            ('security', 'Seguridad'), ('ui', 'Interfaz / UX')],
        string='Tipo de Cambio', default='feat', required=True)
