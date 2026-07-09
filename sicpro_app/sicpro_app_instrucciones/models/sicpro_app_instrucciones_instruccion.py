# -*- encoding: utf-8 -*-


from random import randint

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


def _default_color():
    return randint(1, 11)


class InstruccionesInstruccion(models.Model):
    _name = "sicpro.app.instrucciones.instruccion"
    _description = 'Registro de Instrucciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Instrucción', required=True)
    fecha_creacion = fields.Date(string='Fecha Creado', copy=False, default=fields.datetime.now())
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, default=fields.datetime.now())
    fecha_fin = fields.Date(string='Fecha Fin', required=True, default=fields.datetime.now())
    user_id = fields.Many2one('res.users', string='Instructor', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    instructor = fields.Char(string='Instructor Oficial', related='user_id.name', required=False)
    tel_fijo = fields.Char(string='Fijo', related='user_id.telefono_trabajo', required=False)
    tel_movil = fields.Char(string='móvil', related='user_id.movil_trabajo', required=False)
    correo = fields.Char(string='Correo', related="user_id.email", store=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True)
    area_id = fields.Many2many('sicpro.app.trabajadores.areas', 'sicpro_app_instrucciones_areaid_rel',
                               string='Departamento', required=True,
                               domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ocupacion_id = fields.Many2many('sicpro.app.trabajadores.ocupacion', 'sicpro_app_instrucciones_ocupacionid_rel',
                                    string='Puesto de trabajo', required=True, domain="[('area_id', '=', area_id)]")
    descripcion = fields.Text("Descripción")
    active = fields.Boolean(string="Activo", default=False, )
    etiquetas = fields.Many2many('sicpro.app.instrucciones.etiquetas', 'sicpro_app_instrucciones_etiquetas_rel',
                                 string='Etiqueta')
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('IG', 'INSTRUCCIÓN GENERAL'), ('IE', 'INSTRUCCIÓN ESPECÍFICA'),
                                       ('P', 'PERIÓDICA'), ('ET', 'EXTRAORDINARIA'), ('OP', 'OPERACIONAL'),
                                       ('EM', 'EMERGENCIA'), ('EP', 'ESPECIALIZADA'), ('TC', 'TOMA DE CONCIENCIA'), ], )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    es_favorito = fields.Boolean()
    attachment_ids = fields.Many2many('ir.attachment', 'instrucciones_documentacion_attachment_rel', 'instrucciones_id',
                                      'attachment_id', string="Adjuntos")

    # Para el dashboard
    request_ids = fields.One2many(comodel_name="sicpro.app.instrucciones.trabajador", inverse_name="instrucciones_id",
                                  copy=False)
    todo_request_ids = fields.One2many('sicpro.app.instrucciones.trabajador', string="Cantidad", copy=False,
                                       compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Número de Instrucciones", compute='_compute_todo_requests')
    todo_request_count_aprobados = fields.Integer(string="Cantidad Aprobados", compute='_compute_todo_requests')
    todo_request_count_suspensos = fields.Integer(string="Cantidad Suspensos", compute='_compute_todo_requests')
    encuesta_id = fields.Many2one('survey.survey', "Cuestionario")
    cargos_evaluar = fields.Char(string="cargos_evaluar", index=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    # acción para emitir el resumen del modelo de instrucción
    def emitir_modelo_instruccion(self):
        return {'type': 'ir.actions.report', 'model': 'sicpro.app.instrucciones.trabajador', 'report_type': 'qweb-pdf',
                'report_name': 'sicpro_app_instrucciones.informe_modelo_instruccion',
                'paperformat_id': 'formato_papel_horizontal_instrucciones', }

    # acción para buscar las áreas que realizaron la instrucción
    def buscar_areas_trabajadores(self, area_id):
        dic_areas = []

        # busco las evaluaciones vinculadas a la instrucción
        instrucciones = self.env['sicpro.app.instrucciones.trabajador'].sudo().search(
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
                team.todo_request_ids.filtered(lambda e: e.estado_ids == 'aprobado'))

            team.todo_request_count_suspensos = len(
                team.todo_request_ids.filtered(lambda e: e.estado_ids == 'suspenso'))

    # mostrar la encuesta
    def action_mostrar_encuesta(self):
        return self.encuesta_id.action_print_survey()

    # crear nueva encuesta
    def action_nueva_encuesta(self):
        self.ensure_one()
        survey = self.env['survey.survey'].create({'title': _("Instrucción: %s") % self.name, })
        self.write({'encuesta_id': survey.id})

        action = {'name': _('Survey'), 'view_mode': 'form,tree', 'res_model': 'survey.survey',
                  'type': 'ir.actions.act_window', 'context': {'form_view_initial_mode': 'edit'}, 'res_id': survey.id, }

        return action

    # envío notificación y correo de aviso
    def enviar_aviso_instruccion(self):
        # creo la lista de correo de jefes de área
        cargos = ''
        for item in self.ocupacion_id:
            cargos += str(item.name.name) + ' - '

            # envió la notificación a los trabajadores
            for data in item.trabajadores_ids:
                if data.user_id:
                    data.sudo().message_post(body='Instrucción Asignada', partner_ids=data.user_id.partner_id.ids,
                                             subtype_xmlid='mail.mt_comment', author_id=item.env.user.partner_id.id)
                    # envío el correo electrónico
                    email_values = {'email_to': data.user_id.email_formatted, }
                    template = self.env.ref('sicpro_app_instrucciones.instrucciones_enviar_aviso_trabajador')
                    template.send_mail(self.id, force_send=True, email_values=email_values)

        self.cargos_evaluar = cargos
        for item in self.area_id:
            # envió la notificación a los jefes
            item.sudo().message_post(body='Instrucción Asignada', partner_ids=item.manager_id.user_id.partner_id.ids,
                                     subtype_xmlid='mail.mt_comment', author_id=item.env.user.partner_id.id)
            # envío el correo electrónico
            email_values = {'email_to': item.manager_id.user_id.email_formatted, }
            template = self.env.ref('sicpro_app_instrucciones.instrucciones_enviar_aviso_jefe')
            template.send_mail(self.id, force_send=True, email_values=email_values)

    # cron para la verificación de las fechas de inicio y fin
    def cron_ejecutar_revision_fechas(self):
        dias = 1
        hoy = fields.Date.context_today(self)
        instrucciones = self.env['sicpro.app.instrucciones.instruccion'].search([('active', 'in', (True, False))])
        for item in instrucciones:
            # compruebo la fecha de inicio
            if item.fecha_inicio:
                fecha_ejecucion = item.fecha_inicio - relativedelta(days=dias)
                if hoy == fecha_ejecucion:
                    item.active = True
                    # creo la lista de correo de jefes de área
                    cargos = ''
                    for item1 in item.ocupacion_id:
                        cargos += str(item1.name.name) + ' - '

                        # envió la notificación a los trabajadores
                        for data in item1.trabajadores_ids:
                            if data.user_id:
                                data.sudo().message_post(body='Instrucción Asignada',
                                                         partner_ids=data.user_id.partner_id.ids,
                                                         subtype_xmlid='mail.mt_comment',
                                                         author_id=item1.env.user.partner_id.id)
                                # envío el correo electrónico
                                email_values = {'email_to': data.user_id.email_formatted, }
                                template = self.env.ref(
                                    'sicpro_app_instrucciones.instrucciones_enviar_aviso_trabajador')
                                template.send_mail(item.id, force_send=True, email_values=email_values)

                    item.cargos_evaluar = cargos
                    for item1 in self.area_id:
                        # envió la notificación a los jefes
                        item1.sudo().message_post(body='Instrucción Asignada',
                                                  partner_ids=item1.manager_id.user_id.partner_id.ids,
                                                  subtype_xmlid='mail.mt_comment',
                                                  author_id=item1.env.user.partner_id.id)
                        # envío el correo electrónico
                        email_values = {'email_to': item1.manager_id.user_id.email_formatted, }
                        template = self.env.ref('sicpro_app_instrucciones.instrucciones_enviar_aviso_jefe')
                        template.send_mail(item.id, force_send=True, email_values=email_values)

            # compruebo fecha final
            if item.fecha_fin:
                if item.fecha_fin == hoy:
                    item.active = False
