# -*- encoding: utf-8 -*-


from random import randint
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class InstruccionesInstruccion(models.Model):
    _name = "sicpro.app.instrucciones.instruccion"
    _description = 'Registro de Instrucciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Instrucción', required=True)
    fecha_creacion = fields.Date(string='Fecha Creado', copy=False,
                                 default=fields.datetime.now())
    fecha_inicio = fields.Date(string='Fecha Inicio', copy=False,
                               required=True)
    fecha_fin = fields.Date(string='Fecha Fin', copy=False, required=True)
    user_id = fields.Many2one('res.users', string='Instructor', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    correo = fields.Char(string='Correo', related="user_id.email", store=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    area_id = fields.Many2many('sicpro.app.trabajadores.areas',
                               'sicpro_app_instrucciones_areaid_rel',
                               string='Departamento', required=True,
                               domain="['|', ('company_id', '=', False), "
                                      "('company_id', '=', company_id)]")
    ocupacion_id = fields.Many2many('sicpro.app.trabajadores.ocupacion',
                                    'sicpro_app_instrucciones_ocupacionid_rel',
                                    string='Puesto de trabajo', required=True,
                                    domain="[('area_id', '=', area_id)]")
    descripcion = fields.Text("Descripción")
    active = fields.Boolean(string="Activo", default=False, )
    etiquetas = fields.Many2many('sicpro.app.instrucciones.etiquetas',
                                 'sicpro_app_instrucciones_etiquetas_rel',
                                 string='Etiqueta')
    tipo = fields.Selection(string='Tipo',
                            selection=[('IG', 'INSTRUCCIÓN GENERAL'),
                                       ('IE', 'INSTRUCCIÓN ESPECÍFICA'),
                                       ('P', 'PERIÓDICA'),
                                       ('ET', 'EXTRAORDINARIA'),
                                       ('OP', 'OPERACIONAL'),
                                       ('EM', 'EMERGENCIA'),
                                       ('EP', 'ESPECIALIZADA'),
                                       ('TC', 'TOMA DE CONCIENCIA'), ],
                            required=True, )
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    es_favorito = fields.Boolean()
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")

    # Para el dashboard
    request_ids = fields.One2many(
        comodel_name="sicpro.app.instrucciones.trabajador",
        inverse_name="instrucciones_id", copy=False)
    todo_request_ids = fields.One2many('sicpro.app.instrucciones.trabajador',
                                       string="Cantidad", copy=False,
                                       compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Número de Instrucciones",
                                        compute='_compute_todo_requests')
    todo_request_count_aprobados = fields.Integer(
        string="Cantidad Aprobados", compute='_compute_todo_requests')
    todo_request_count_suspensos = fields.Integer(
        string="Cantidad Suspensos", compute='_compute_todo_requests')
    encuesta_id = fields.Many2one('survey.survey', "Cuestionario")
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    cargos_evaluar = fields.Char(string="cargos_evaluar", index=True)
    # fechas formateadas
    fecha_creacion_formated = fields.Char(compute='_fecha_creacion_formated')
    fecha_inicio_formated = fields.Char(compute='_fecha_inicio_formated')
    fecha_fin_formated = fields.Char(compute='_fecha_fin_formated')

    def _fecha_creacion_formated(self):
        for part in self:
            part.fecha_creacion_formated = part.fecha_creacion.strftime("%d/%m/%Y")

    def _fecha_inicio_formated(self):
        for part in self:
            part.fecha_inicio_formated = part.fecha_inicio.strftime("%d/%m/%Y")

    def _fecha_fin_formated(self):
        for part in self:
            part.fecha_fin_formated = part.fecha_fin.strftime("%d/%m/%Y")

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
            {'title': _("Instrucción: %s") % self.name, })
        self.write({'encuesta_id': survey.id})

        action = {'name': _('Survey'), 'view_mode': 'form,tree',
                  'res_model': 'survey.survey',
                  'type': 'ir.actions.act_window',
                  'context': {'form_view_initial_mode': 'edit'},
                  'res_id': survey.id, }

        return action

    # envío notificación y correo de aviso
    def enviar_aviso_instruccion(self):
        # creo la lista de correo de jefes de área
        seguidores = ''
        cargos = ''
        for item in self.ocupacion_id:
            cargos = str(cargos) + str(item.name.name) + ' - '
        self.cargos_evaluar = cargos
        for item in self.area_id:
            seguidores = str(seguidores) + str(item.manager_id.user_id.email_formatted)
            # envió la notificación a los jefes
            item.message_post(body='Nueva Instrucción Asignada',
                              partner_ids=item.manager_id.user_id.partner_id.ids,
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=item.env.user.partner_id.id)
        self.correo_seguidores = seguidores
        # envío el correo a los jefes
        template = self.env.ref('sicpro_app_instrucciones.instrucciones_enviar_aviso')
        template.send_mail(self.id, force_send=True)

    # cron para la verificación de las fechas de inicio y fin
    def cron_ejecutar_revision_fechas(self):
        dias = 1
        hoy = fields.Date.context_today(self)
        instrucciones = self.env[
            'sicpro.app.instrucciones.instruccion'].search(
            [('active', 'in', (True, False))])
        for item in instrucciones:
            # compruebo la fecha de inicio
            if item.fecha_inicio:
                fecha_ejecucion = item.fecha_inicio - relativedelta(days=dias)
                if hoy == fecha_ejecucion:
                    item.active = True

                    # creo la lista de correo de jefes de área
                    seguidor = ''
                    cargo = ''
                    for item1 in item.ocupacion_id:
                        cargo = str(cargo) + str(item1.name.name) + ' - '
                    item.cargos_evaluar = cargo
                    for item2 in item.area_id:
                        seguidor = str(seguidor) + str(
                            item2.manager_id.user_id.email_formatted)
                        # envió la notificación a los jefes
                        item2.message_post(body='Nueva Instrucción Asignada',
                                           partner_ids=item2.manager_id.user_id.partner_id.ids,
                                           message_type='notification',
                                           subtype_xmlid='mail.mt_comment',
                                           author_id=item2.env.user.partner_id.id)
                    item.correo_seguidores = seguidor
                    # envío el correo a los jefes
                    template = self.env.ref(
                        'sicpro_app_instrucciones.instrucciones_enviar_aviso')
                    template.send_mail(item.id, force_send=True)

            # compruebo fecha final
            if item.fecha_fin:
                if item.fecha_fin == hoy:
                    item.active = False
