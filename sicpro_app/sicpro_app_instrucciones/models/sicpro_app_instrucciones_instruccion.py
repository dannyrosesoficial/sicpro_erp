# -*- encoding: utf-8 -*-


from random import randint

from odoo import api, fields, models


def _default_color():
    return randint(1, 11)


class InstruccionesInstruccion(models.Model):
    _name = "sicpro.app.instrucciones.instruccion"
    _description = 'Registro de Instrucciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "fecha_inicio desc, name asc"

    name = fields.Char(string='Instrucción', required=True, tracking=True)
    fecha_creacion = fields.Date(string='Fecha Creado', copy=False,
                                 default=fields.Date.context_today)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True,
                               default=fields.Date.context_today)
    fecha_fin = fields.Date(string='Fecha Fin', required=True,
                            default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='Instructor', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    instructor = fields.Char(string='Instructor Oficial',
                             related='user_id.name', required=False)
    tel_fijo = fields.Char(string='Fijo', related='user_id.telefono_trabajo',
                           required=False)
    tel_movil = fields.Char(string='móvil', related='user_id.movil_trabajo',
                            required=False)
    correo = fields.Char(string='Correo', related="user_id.email", store=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True)
    area_id = fields.Many2many('sicpro.app.trabajadores.areas',
                               'sicpro_app_instrucciones_areaid_rel',
                               string='Departamento', required=True,
                               domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ocupacion_id = fields.Many2many('sicpro.app.trabajadores.ocupacion',
                                    'sicpro_app_instrucciones_ocupacionid_rel',
                                    string='Puesto de trabajo', required=True,
                                    domain="[('area_id', '=', area_id)]")
    descripcion = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=False, index=True)
    etiquetas = fields.Many2many('sicpro.app.instrucciones.etiquetas',
                                 'sicpro_app_instrucciones_etiquetas_rel',
                                 string='Etiqueta')
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('IG', 'INSTRUCCIÓN GENERAL'),
                                       ('IE', 'INSTRUCCIÓN ESPECÍFICA'),
                                       ('P', 'PERIÓDICA'),
                                       ('ET', 'EXTRAORDINARIA'),
                                       ('OP', 'OPERACIONAL'),
                                       ('EM', 'EMERGENCIA'),
                                       ('EP', 'ESPECIALIZADA'),
                                       ('TC', 'TOMA DE CONCIENCIA'), ], )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    es_favorito = fields.Boolean()
    attachment_ids = fields.Many2many('ir.attachment',
                                      'instrucciones_documentacion_attachment_rel',
                                      'instrucciones_id', 'attachment_id',
                                      string="Adjuntos")

    # Para el dashboard
    request_ids = fields.One2many(
        comodel_name="sicpro.app.instrucciones.trabajador",
        inverse_name="instrucciones_id", copy=False)
    todo_request_ids = fields.One2many('sicpro.app.instrucciones.trabajador',
                                       string="Cantidad", copy=False,
                                       compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Número de Instrucciones",
                                        compute='_compute_todo_requests')
    todo_request_count_aprobados = fields.Integer(string="Cantidad Aprobados",
                                                  compute='_compute_todo_requests')
    todo_request_count_suspensos = fields.Integer(string="Cantidad Suspensos",
                                                  compute='_compute_todo_requests')
    encuesta_id = fields.Many2one('survey.survey', "Cuestionario")
    cargos_evaluar = fields.Char(string="cargos_evaluar", index=True)

    # Campo calculado para facilitar el filtrado en el cron
    estado_vigencia = fields.Selection(
        [('espera', 'En Espera'), ('vigente', 'Vigente'),
         ('finalizado', 'Finalizado')], string="Estado Vigencia",
        compute="_compute_estado_vigencia", store=True)

    @api.depends('fecha_inicio', 'fecha_fin', 'active')
    def _compute_estado_vigencia(self):
        hoy = fields.Date.context_today(self)
        for rec in self:
            if rec.fecha_inicio > hoy:
                rec.estado_vigencia = 'espera'
            elif rec.fecha_inicio <= hoy <= rec.fecha_fin:
                rec.estado_vigencia = 'vigente'
            else:
                rec.estado_vigencia = 'finalizado'

    # acción para emitir el resumen del modelo de instrucción
    def emitir_modelo_instruccion(self):
        return {'type': 'ir.actions.report',
                'model': 'sicpro.app.instrucciones.trabajador',
                'report_type': 'qweb-pdf',
                'report_name': 'sicpro_app_instrucciones.informe_modelo_instruccion',
                'paperformat_id': 'formato_papel_horizontal_instrucciones', }

    # acción para buscar las áreas que realizaron la instrucción
    def buscar_areas_trabajadores(self, area_id):
        dic_areas = []

        # busco las evaluaciones vinculadas a la instrucción
        instrucciones = self.env[
            'sicpro.app.instrucciones.trabajador'].sudo().search(
            [('instrucciones_id', '=', area_id)], )
        for item in instrucciones:
            if not item.area_id.name in dic_areas:
                dic_areas.append(item.area_id.name)
        return dic_areas

    # Cuenta las evaluaciones de los trabajadores
    @api.depends('request_ids.estado_ids')
    def _compute_todo_requests(self):
        for team in self:
            team.todo_request_ids = team.request_ids

            team.todo_request_count = len(team.todo_request_ids)

            team.todo_request_count_aprobados = len(
                team.todo_request_ids.filtered(
                    lambda e: e.estado_ids == 'aprobado'))

            team.todo_request_count_suspensos = len(
                team.todo_request_ids.filtered(
                    lambda e: e.estado_ids == 'suspenso'))

    # mostrar la encuesta
    def action_mostrar_encuesta(self):
        return self.encuesta_id.action_print_survey()

    # crear nueva encuesta
    def action_nueva_encuesta(self):
        self.ensure_one()
        survey = self.env['survey.survey'].create(
            {'title': "Instrucción: %s" % (self.name or ''), })
        self.write({'encuesta_id': survey.id})

        action = {'name': 'Encuesta', 'view_mode': 'form,list',
                  'res_model': 'survey.survey',
                  'type': 'ir.actions.act_window',
                  'context': {'form_view_initial_mode': 'edit'},
                  'res_id': survey.id, }

        return action

    def enviar_aviso_instruccion(self):
        self.ensure_one()
        cargos_list = []
        for ocupacion in self.ocupacion_id:
            # name.name asume que ocupacion tiene una relación a otro modelo con name
            cargos_list.append(str(ocupacion.name.name))

            for trabajador in ocupacion.trabajadores_ids:
                if trabajador.user_id:
                    # Notificación en Odoo
                    trabajador.sudo().message_post(
                        body='Instrucción Asignada: %s' % (self.name or ''),
                        partner_ids=trabajador.user_id.partner_id.ids,
                        subtype_xmlid='mail.mt_comment')
                    # Envío de correo
                    template = self.env.ref(
                        'sicpro_app_instrucciones.instrucciones_enviar_aviso_trabajador',
                        raise_if_not_found=False)
                    if template:
                        template.send_mail(self.id, force_send=True,
                                           email_values={
                                               'email_to': trabajador.user_id.email_formatted})

        self.cargos_evaluar = " - ".join(cargos_list)

        # Notificación a Jefes
        for area in self.area_id:
            if area.manager_id and area.manager_id.user_id:
                area.sudo().message_post(
                    body='Nueva Instrucción para su Área: %s' % (
                            self.name or ''),
                    partner_ids=area.manager_id.user_id.partner_id.ids)
                template_jefe = self.env.ref(
                    'sicpro_app_instrucciones.instrucciones_enviar_aviso_jefe',
                    raise_if_not_found=False)
                if template_jefe:
                    template_jefe.send_mail(self.id, force_send=True,
                                            email_values={
                                                'email_to': area.manager_id.user_id.email_formatted})

    def cron_ejecutar_revision_fechas(self):
        hoy = fields.Date.context_today(self)
        # 1. Activar instrucciones que empiezan hoy
        instrucciones_a_activar = self.search(
            [('fecha_inicio', '=', hoy), ('active', '=', False)])
        for inst in instrucciones_a_activar:
            inst.active = True
            inst.enviar_aviso_instruccion()  # Reutilizamos la función

        # 2. Desactivar instrucciones que terminaron ayer
        instrucciones_a_desactivar = self.search(
            [('fecha_fin', '<', hoy), ('active', '=', True)])
        instrucciones_a_desactivar.write({'active': False})
