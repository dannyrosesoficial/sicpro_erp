# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from random import randint

from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class ControlInformacionControlActividades(models.Model):
    _name = 'sicpro.app.control.informacion.control.actividades'
    _description = 'Control de las actividades de la información'
    _order = 'id desc'

    name = fields.Many2one('sicpro.app.control.informacion.actividad', string='Actividad', required=True, index=True)
    area = fields.Many2one('sicpro.app.control.informacion.areas', string='Área Informativa')
    versiones_ids = fields.Many2many('sicpro.app.control.informacion', 'control_informacion_control_rel',
                                     string='Control de Versiones', required=False)
    fecha_entrega = fields.Date(string='Fecha de Entrega')
    fecha_requerida = fields.Date(string='Fecha de Requerida')
    mes = fields.Char(string='Mes', required=True)
    mes_id = fields.Integer(string='Mes_id', required=False)
    anio = fields.Char(string="Año", required=True)
    estado = fields.Selection(string='Estado', required=True, default='pendiente',
                              selection=[('atrasado', 'Atrasado'), ('pendiente', 'Pendiente'), ('enviado', 'Enviado'),
                                         ('validado', 'Validado'), ('devuelto', 'Devuelto'), ])
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    versiones_control = fields.Char(string='Versiones', required=False)
    versiones_fechas = fields.Char(string='Control de Fechas', required=False, default='[]')
    veracidad = fields.Selection(string='Veracidad', selection=[('no', 'NO'), ('si', 'SI'), ], required=False, )
    ajuste_formato = fields.Selection(string='Ajusto a Formato', selection=[('no', 'NO'), ('si', 'SI'), ],
                                      required=False, )
    completitud = fields.Selection(string='Completitud', selection=[('no', 'NO'), ('si', 'SI'), ], required=False)
    observaciones = fields.Text(string="Observaciones", required=False)
    evaluacion_estado = fields.Float(string='Evaluación estado', required=True, default='2')
    evaluacion_version = fields.Float(string='Evaluación version', required=True, default='2')
    evaluacion_veracidad = fields.Float(string='Evaluación veracidad', required=True, default='2')
    evaluacion_formato = fields.Float(string='Evaluación formato', required=True, default='2')
    evaluacion_completitud = fields.Float(string='Evaluación completitud', required=True, default='2')
    evaluacion_final = fields.Float(string='Evaluación', required=False)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)

    # ver el registro seleccionado
    def ver_informacion(self):
        active_mes = self._context.get('default_mes')
        active_anio = self._context.get('default_anio')
        active_actividad = self._context.get('default_actividad')
        active_area = self._context.get('default_area')

        action = self.env['ir.actions.act_window']._for_xml_id('sicpro_app_control_informacion.control_informaciones_control_action')
        action['views'] = [(False, 'tree'), (False, 'form')]
        action['domain'] = ['&', '&',  ('name', '=', active_actividad), ('area', '=', active_area),
                            ('mes', '=', active_mes), ('anio', '=', active_anio)]
        return action

    # actualizo la evaluación del control
    @api.onchange('estado', 'versiones_control', 'veracidad', 'ajuste_formato', 'completitud')
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
        actividades = self.env['sicpro.app.control.informacion.actividad'].search([('active', '=', True)])

        # busco todas las actividades
        for item in actividades:
            # busco las áreas de cada actividad
            for data in item.areas:
                # busco que esten creadas las actividades para su control
                control = self.env['sicpro.app.control.informacion.control.actividades'].search(
                    ['&', '&', '&', ('active', '=', True), ('name', '=', item.id), ('area', '=', data.id),
                     ('mes', '=', mes_actual), ('anio', '=', anio_actual)])

                if not control:
                    fecha_requerida = datetime.strptime(
                        str(anio_actual) + '-' + str(mes_id) + '-' + str(item.dia_entrega), '%Y-%m-%d')

                    # creo nuevo registro porque no existen datos
                    self.env['sicpro.app.control.informacion.control.actividades'].sudo().create(
                        {'name': item.id, 'area': data.id, 'mes': mes_actual, 'anio': anio_actual,
                         'fecha_requerida': fecha_requerida, 'mes_id': mes_id, })

    # actualizo el control de informaciones del cron
    @api.model
    def actualizar_control_informaciones(self, mes_actual, anio_actual, fecha_actual):
        control = self.env['sicpro.app.control.informacion.control.actividades'].search(
            ['&', '&', ('active', '=', True), ('mes', '=', mes_actual), ('anio', '=', anio_actual)])

        for item in control:
            # busco la actividad del mes y año específico
            informaciones = self.env['sicpro.app.control.informacion'].search(
                ['&', '&', '&', ('active', '=', True), ('name', '=', item.name.id), ('area', '=', item.area.id),
                 ('mes', '=', mes_actual), ('anio', '=', anio_actual)])

            if informaciones:
                # guardo las versiones del las informaciones
                dic_info = []
                dic_fechas = []
                dic_versiones = []
                contador = 0
                for data in informaciones:
                    contador += 1
                    dic_info.append(data.id)
                    dic_versiones.append(data.version)
                    dic_fechas.append(datetime.strftime(data.fecha_entrega, '%d/%m/%Y'))

                item.versiones_ids = dic_info
                item.versiones_fechas = str(dic_fechas).replace("'", "")
                item.versiones_control = str(contador)

                # verifico la veracidad de la información
                if contador > 1:
                    item.veracidad = 'no'
                elif contador == 1:
                    item.veracidad = 'si'

                # actualizo los valores del control con los de la última version
                version_max = int(max(dic_versiones))
                if version_max > 0:
                    version_id = self.env['sicpro.app.control.informacion'].search(
                        ['&', '&', '&', ('active', '=', True), ('name', '=', item.name.id), ('area', '=', item.area.id),
                         ('mes', '=', mes_actual), ('anio', '=', anio_actual), ('version', '=', version_max)])

                    item.estado = version_id.estado
                    item.fecha_entrega = version_id.fecha_entrega

            # actualizo el estado de atrasado si no se ha enviado la información
            if fecha_actual.date() > item.fecha_requerida and item.estado == 'pendiente':
                item.estado = 'atrasado'

    # envío correo y notificaciones a las informaciones atrasadas
    @api.model
    def envio_avisos_atrasos(self, fecha_actual):
        actividades = self.env['sicpro.app.control.informacion.actividad'].search(
            ['&', ('active', '=', True), ('notificar', '!=', False)])

        # busco todas las actividades
        for item in actividades:
            for dia in item.notificar:
                hoy = fecha_actual.date()

                # busco las actividades que no están validadas
                control = self.env['sicpro.app.control.informacion.control.actividades'].search(
                    ['&', '&', ('active', '=', True), ('name', '=', item.id), ('estado', '!=', 'validado')])
                for data in control:
                    # comparo las fechas control con la del día actual, si coinciden envío la notificación
                    fecha_control = data.fecha_requerida - timedelta(days=dia.name)
                    if hoy == fecha_control:

                        # mantiene actualizado el correo de seguidores del registro
                        correos_ejecutores = ''
                        correos_especialistas = ''
                        # obtengo el listado de ejecutores que atienden la información
                        ejecutores = self.env.ref(
                            'sicpro_app_control_informacion.grupo_control_informacion_ejecutor').users
                        for ejecutor in ejecutores:
                            user_id = self.env['res.users'].search([('partner_id', '=', ejecutor.partner_id.id)])
                            if data.area.company_id == user_id.company_id:
                                correos_ejecutores += ejecutor.partner_id.email_formatted

                        # obtengo el listado de especialistas que atienden la información
                        for especialista in item.gestores:
                            correos_especialistas += especialista.email_formatted

                        email_values = {'email_to': correos_ejecutores, 'email_cc': correos_especialistas, }
                        # envío el correo a los seguidores del registro
                        local_context = item.env.context.copy()
                        template = item.env.ref('sicpro_app_control_informacion.control_informacion_atraso')
                        template.with_context(local_context).send_mail(data.id, force_send=True,
                                                                       email_values=email_values)

    # # recalculo los valores de la evaluación
    @api.model
    def evaluacion_control_informaciones(self, mes_actual, anio_actual):
        control = self.env['sicpro.app.control.informacion.control.actividades'].search(
            ['&', '&', ('active', '=', True), ('mes', '=', mes_actual), ('anio', '=', anio_actual)])
        for item in control:
            item.compute_evaluacion()

    # método de verificación de la fecha de inicio y terminación del cron
    @api.model
    def cron_control_informaciones(self):
        # busco fecha actual
        fecha_actual = datetime.today()
        # busco el mes actual
        mes_id = fecha_actual.month
        nombre_mes = self.env['sicpro.nomenclador.meses'].search(
            ['&', ('active', '=', True), ('codigo_mes', '=', mes_id)])
        mes_actual = nombre_mes.name
        # busco el año actual
        anio_actual = datetime.today().strftime("%Y")

        # llamo al método para crear los datos del control de información
        self.generar_control_informaciones(mes_actual, anio_actual, mes_id)
        # actualizo el estado del control de información
        self.actualizar_control_informaciones(mes_actual, anio_actual, fecha_actual)
        # envío notificaciones sobre el atraso de la información
        self.envio_avisos_atrasos(fecha_actual)
        # recalculo los valores de la evaluación
        self.evaluacion_control_informaciones(mes_actual, anio_actual)

