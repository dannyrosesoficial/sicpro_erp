# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import calendar
import logging
from datetime import date, timedelta
from random import randint
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

def _default_color():
    return randint(1, 11)


class ControlInformacionControlActividades(models.Model):
    _name = 'sicpro.app.control.informacion.control.actividades'
    _description = 'Control de las actividades de la información'
    _order = 'id desc'

    name = fields.Many2one('sicpro.app.control.informacion.actividad',
                           string='Actividad', required=True, index=True)
    area = fields.Many2one('sicpro.app.control.informacion.areas',
                           string='Área Informativa')
    versiones_ids = fields.Many2many('sicpro.app.control.informacion',
                                     'control_informacion_control_rel',
                                     string='Control de Versiones',
                                     required=False)
    fecha_entrega = fields.Date(string='Fecha de Entrega')
    fecha_requerida = fields.Date(string='Fecha de Requerida')
    mes = fields.Char(string='Mes', required=True)
    mes_id = fields.Integer(string='Mes_id', required=False)
    anio = fields.Char(string="Año", required=True)
    estado = fields.Selection(string='Estado', required=True,
                              default='pendiente',
                              selection=[('atrasado', 'Atrasado'),
                                         ('pendiente', 'Pendiente'),
                                         ('enviado', 'Enviado'),
                                         ('validado', 'Validado'),
                                         ('devuelto', 'Devuelto'), ])
    active = fields.Boolean(string='Activo', default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    versiones_control = fields.Char(string='Versiones', required=False)
    versiones_fechas = fields.Char(string='Control de Fechas', required=False,
                                   default='[]')
    veracidad = fields.Selection(string='Veracidad',
                                 selection=[('no', 'NO'), ('si', 'SI'), ],
                                 required=False)
    ajuste_formato = fields.Selection(string='Ajusto a Formato',
                                      selection=[('no', 'NO'), ('si', 'SI'), ],
                                      required=False)
    completitud = fields.Selection(string='Completitud',
                                   selection=[('no', 'NO'), ('si', 'SI'), ],
                                   required=False)
    observaciones = fields.Text(string="Observaciones", required=False)
    evaluacion_estado = fields.Float(string='Evaluación estado', required=True,
                                     default='2')
    evaluacion_version = fields.Float(string='Evaluación version',
                                      required=True, default='2')
    evaluacion_veracidad = fields.Float(string='Evaluación veracidad',
                                        required=True, default='2')
    evaluacion_formato = fields.Float(string='Evaluación formato',
                                      required=True, default='2')
    evaluacion_completitud = fields.Float(string='Evaluación completitud',
                                          required=True, default='2')
    evaluacion_final = fields.Float(string='Evaluación', required=False)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    # ver el registro seleccionado
    def ver_informacion(self):
        active_mes = self.env.context.get('default_mes')
        active_anio = self.env.context.get('default_anio')
        active_actividad = self.env.context.get('default_actividad')
        active_area = self.env.context.get('default_area')

        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_control_informacion.control_informaciones_control_action')
        action['views'] = [(False, 'list'), (False, 'form')]
        action['domain'] = ['&', '&', ('name', '=', active_actividad),
                            ('area', '=', active_area),
                            ('mes', '=', active_mes),
                            ('anio', '=', active_anio)]
        return action

    # actualizo la evaluación del control
    @api.onchange('estado', 'versiones_control', 'veracidad', 'ajuste_formato',
                  'completitud')
    def compute_evaluacion(self):
        for item in self:
            # control de estados
            if item.estado == 'validado':
                item.evaluacion_estado = 5
            else:
                item.evaluacion_estado = 2

            # control de versión
            if item.versiones_control == '1':
                item.evaluacion_version = 5
            else:
                item.evaluacion_version = 2

            # control de veracidad
            if item.veracidad == 'si':
                item.evaluacion_veracidad = 5
            else:
                item.evaluacion_veracidad = 2

            # control de ajuste de formato
            if item.ajuste_formato == 'si':
                item.evaluacion_formato = 2
            else:
                item.evaluacion_formato = 5

            # control de completitud
            if item.completitud == 'si':
                item.evaluacion_completitud = 5
            else:
                item.evaluacion_completitud = 2

            suma_evalucion = item.evaluacion_estado + item.evaluacion_version + item.evaluacion_veracidad + item.evaluacion_formato + item.evaluacion_completitud
            item.evaluacion_final = suma_evalucion / 5

    # género el control de informaciones del cron
    @api.model
    def generar_control_informaciones(self, mes_actual, anio_actual, mes_id):
        # 1. Buscamos todas las actividades activas
        actividades = self.env[
            'sicpro.app.control.informacion.actividad'].search(
            [('active', '=', True)])

        # 2. Preparamos variables de fecha
        try:
            anio_int = int(anio_actual)
            mes_int = int(mes_id)
        except ValueError:
            return False

        for item in actividades:
            # Ajuste de seguridad: si el día de entrega es 31 y el mes solo tiene 28 días,
            # ajustamos automáticamente al último día del mes.
            ultimo_dia_mes = calendar.monthrange(anio_int, mes_int)[1]
            dia_entrega = min(int(item.dia_entrega), ultimo_dia_mes)

            fecha_requerida = date(anio_int, mes_int, dia_entrega)

            for area in item.areas:
                # 3. Verificamos existencia (Búsqueda optimizada)
                existe_control = self.env[
                    'sicpro.app.control.informacion.control.actividades'].search_count(
                    [('name', '=', item.id), ('area', '=', area.id),
                     ('mes', '=', mes_actual), ('anio', '=', anio_actual),
                     ('active', '=', True)])

                # 4. Creamos solo si no existe
                if not existe_control:
                    self.env[
                        'sicpro.app.control.informacion.control.actividades'].sudo().create(
                        {'name': item.id, 'area': area.id, 'mes': mes_actual,
                         'anio': anio_actual,
                         'fecha_requerida': fecha_requerida, 'mes_id': mes_id,
                         'estado': 'pendiente', # Forzamos el estado inicial
                         })

    # actualizo el control de informaciones del cron
    @api.model
    def actualizar_control_informaciones(self, mes_actual, anio_actual,
                                         fecha_actual):
        # 1. Aseguramos que fecha_actual sea solo fecha para comparar
        hoy = fields.Date.to_date(fecha_actual)

        # 2. Buscamos todos los controles del mes/año
        controles = self.env[
            'sicpro.app.control.informacion.control.actividades'].search(
            [('active', '=', True), ('mes', '=', mes_actual),
             ('anio', '=', anio_actual)])

        for item in controles:
            # 3. Buscamos las informaciones relacionadas
            informaciones = self.env['sicpro.app.control.informacion'].search(
                [('active', '=', True), ('name', '=', item.name.id),
                 ('area', '=', item.area.id), ('mes', '=', mes_actual),
                 ('anio', '=', anio_actual)],
                order='version desc')  # Ordenamos por versión para tomar la última fácil

            if informaciones:
                contador = len(informaciones)

                # Formateamos fechas de forma segura
                lista_fechas = [fields.Date.to_string(info.fecha_entrega) for
                                info in informaciones if info.fecha_entrega]

                # Actualizamos metadatos de versiones
                item.write({'versiones_ids': [(6, 0, informaciones.ids)],
                            'versiones_fechas': str(lista_fechas).replace("'",
                                                                          ""),
                            'versiones_control': str(contador),
                            'veracidad': 'no' if contador > 1 else 'si'})

                # 4. Tomamos la versión más alta (ya ordenada arriba)
                ultima_version = informaciones[0]
                item.write({'estado': ultima_version.estado,
                            'fecha_entrega': ultima_version.fecha_entrega})

            # 5. Lógica de Atraso (Independiente de si hay informaciones creadas)
            # Solo si está pendiente y ya pasó la fecha requerida
            if item.fecha_requerida and hoy > item.fecha_requerida and item.estado == 'pendiente':
                item.estado = 'atrasado'

    # envío correo y notificaciones a las informaciones atrasadas
    @api.model
    def envio_avisos_atrasos(self, fecha_actual):
        # 1. Aseguramos que fecha_actual sea un objeto date (Odoo 19 usa Date.today() por defecto)
        hoy = fields.Date.to_date(fecha_actual)

        # 2. Optimizamos la búsqueda inicial
        actividades = self.env[
            'sicpro.app.control.informacion.actividad'].search(
            [('active', '=', True), ('notificar', '!=', False)])

        # 3. Pre-cargamos el grupo de ejecutores fuera de los bucles para ganar velocidad
        grupo_ejecutor = self.env.ref(
            'sicpro_app_control_informacion.grupo_control_informacion_ejecutor')
        plantilla = self.env.ref(
            'sicpro_app_control_informacion.control_informacion_atraso',
            raise_if_not_found=False)

        if not plantilla:
            return False

        for item in actividades:
            for dia_config in item.notificar:
                # Buscamos registros de control no validados para esta actividad
                controles = self.env[
                    'sicpro.app.control.informacion.control.actividades'].search(
                    [('active', '=', True), ('name', '=', item.id),
                     ('estado', '!=', 'validado'),
                     ('fecha_requerida', '!=', False)])

                for data in controles:
                    # Calculamos la fecha de notificación
                    fecha_notif = data.fecha_requerida - timedelta(
                        days=int(dia_config.name))

                    if hoy == fecha_notif:
                        # Usamos listas para los correos (más limpio y seguro)
                        listado_ejecutores = []
                        listado_especialistas = []

                        # Filtramos ejecutores por compañía (usando el recordset directamente)
                        for ejecutor in grupo_ejecutor.users:
                            if ejecutor.company_id == data.area.company_id and ejecutor.email:
                                listado_ejecutores.append(
                                    ejecutor.email_formatted)

                        # Obtener especialistas gestores
                        for especialista in item.gestores:
                            if especialista.email:
                                listado_especialistas.append(
                                    especialista.email_formatted)

                        if listado_ejecutores:
                            # Unimos con coma para que el servidor de correo lo entienda
                            email_values = {
                                'email_to': ','.join(listado_ejecutores),
                                'email_cc': ','.join(listado_especialistas), }

                            # Envío de correo usando la plantilla
                            plantilla.send_mail(data.id, force_send=True,
                                                email_values=email_values)
                            # Opcional: Registrar en el chatter que se envió aviso
                            data.message_post(
                                body="Aviso de atraso enviado a ejecutores y especialistas.")

    # # recalculo los valores de la evaluación
    @api.model
    def evaluacion_control_informaciones(self, mes_actual, anio_actual):
        # 1. Buscamos los registros.
        # Añadimos un chequeo de seguridad para no procesar registros ya validados si no es necesario
        control = self.env[
            'sicpro.app.control.informacion.control.actividades'].search(
            [('active', '=', True), ('mes', '=', mes_actual),
             ('anio', '=', anio_actual)])

        _logger.info(
            "Calculando evaluación para %s registros de control del periodo %s/%s",
            len(control), mes_actual, anio_actual)

        for item in control:
            try:
                # 2. Llamamos al método de cálculo.
                # Asegúrate de que 'compute_evaluacion' no haga un 'self.ensure_one()'
                # innecesario o que esté bien manejado.
                item.compute_evaluacion()
            except Exception as e:
                _logger.error("Error calculando evaluación para el ID %s: %s",
                              item.id, str(e))
                continue  # Si uno falla, seguimos con el siguiente

    # método de verificación de la fecha de inicio y terminación del cron
    @api.model
    def cron_control_informaciones(self):
        # 1. Usar fields.Date y fields.Datetime de Odoo para consistencia con el servidor
        fecha_actual = fields.Date.today()
        mes_codigo = fecha_actual.month
        anio_actual = str(fecha_actual.year)

        # 2. Búsqueda segura del mes con .search(..., limit=1)
        # Agregué el limit=1 para evitar errores si hay duplicados en el nomenclador
        nombre_mes_rec = self.env['sicpro.nomenclador.meses'].search(
            [('active', '=', True), ('codigo_mes', '=', mes_codigo)], limit=1)

        if not nombre_mes_rec:
            _logger.error(
                "No se encontró el mes con código %s en sicpro.nomenclador.meses",
                mes_codigo)
            return False

        mes_actual_name = nombre_mes_rec.name

        # 3. Ejecución de procesos en bloque
        # Es recomendable envolver esto en un try-except si son muchos datos
        try:
            # Generar datos base
            self.generar_control_informaciones(mes_actual_name, anio_actual,
                                               mes_codigo)

            # Actualizar estados (pasamos fecha_actual para comparaciones)
            self.actualizar_control_informaciones(mes_actual_name, anio_actual,
                                                  fecha_actual)

            # Envío de avisos
            self.envio_avisos_atrasos(fecha_actual)

            # Recálculo de evaluaciones
            self.evaluacion_control_informaciones(mes_actual_name, anio_actual)

            _logger.info(
                "Cron de control de informaciones ejecutado exitosamente para %s/%s",
                mes_actual_name, anio_actual)

        except Exception as e:
            _logger.error("Error ejecutando cron_control_informaciones: %s",
                          str(e))
            return False

        return True
