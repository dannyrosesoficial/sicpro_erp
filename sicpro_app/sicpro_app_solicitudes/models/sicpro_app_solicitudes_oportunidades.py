# -*- coding: utf-8 -*-


from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class SolicitudesOportunidades(models.Model):
    _name = 'sicpro.app.solicitudes.oportunidades'
    _description = "Solicitudes y oportunidades"
    _order = 'priority desc, id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # agrego el cliente por defecto
    def _default_partner_id(self):
        users_id = self.env.user.user_inversionista
        if users_id:
            data = self.env['sicpro.app.clientes'].search([('id', '=', self.env.user.nombre_inversionista.id), ])
            valor = data.id
            return valor
        else:
            return

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.solicitudes.estados'].search([], limit=1)

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Oportunidad", required=True, index=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    oportunidad_especialidad = fields.Many2one(comodel_name='sicpro.app.solicitudes.oportunidades',
                                               string='Oportunidad.', required=False,
                                               domain=[('estado_interno', '=', 'nuevo'), ('tipo', '=', 'principal')], )
    id_solicitud = fields.Char(string='Solicitud ID', tracking=True, copy=False, readonly=True, )
    id_solicitud_creado = fields.Boolean(string='Id_solicitud_creado', required=False, default=False)
    partner_id = fields.Many2one('sicpro.app.clientes', string='Cliente', tracking=10, index=True,
                                 domain=[('tipo_registro', '=', 'persona')],
                                 default=lambda self: self._default_partner_id(), )
    partner_name = fields.Char("Nombre de la entidad", related='partner_id.entidad.name')
    territorio_id = fields.Many2one(comodel_name="sicpro.nomenclador.territorios", string="Unidad Organizativa",
                                    related='partner_id.territorio', store=True)
    provincia_id = fields.Many2one(comodel_name="res.country.state", string="Provincia",
                                   related='partner_id.provincias_id', store=True)
    website = fields.Char('Sitio Web', help="Website of the contact", related='partner_id.entidad.pagina_web')
    cargo = fields.Char(string="Cargo", required=False, related='partner_id.cargo')
    telefono_fijo = fields.Char(string="Teléfono", required=False, related='partner_id.telefono_fijo')
    telefono_movil = fields.Char(string="Móvil", required=False, related='partner_id.telefono_movil')
    correo = fields.Char(string="Correo electrónico", required=False, related='partner_id.correo')
    pagina_web = fields.Char(string="Pagina Web", required=False, related='partner_id.pagina_web')
    active = fields.Boolean('Activo', default=True, tracking=True)
    color = fields.Integer('Índice de colores', default=0)
    # se realizaron cambios y el especialista_ejecutor pertenece ahora al proyectista o jefe de agrupaciones
    especialista_ejecutor = fields.Many2one(comodel_name="sicpro.app.trabajadores", string='Responsable', tracking=True)
    cargo_especialista = fields.Many2one(comodel_name="sicpro.app.trabajadores.ocupacion", string='Cargo Responsable',
                                         related="especialista_ejecutor.ocupacion_id", store=True)
    # se realizaron cambios y el especialista_ejecutante pertenece ahora especialista que trabajara directo en la obra
    especialista_ejecutante = fields.Many2one(comodel_name="sicpro.app.trabajadores", string='Ejecutante', tracking=True)
    cargo_especialista_ejecutante = fields.Many2one(comodel_name="sicpro.app.trabajadores.ocupacion",
                                                    string='Cargo Ejecutante',
                                         related="especialista_ejecutante.ocupacion_id", store=True)
    especialista_ejecutante_bool = fields.Boolean(string='Especialista_ejecutante_bool', required=False)
    description = fields.Text('Notes', required=False, tracking=True)
    observaciones_grupo_ejecutor = fields.Text('Alcance General', required=False, tracking=True)
    tag_ids = fields.Many2many('sicpro.app.solicitudes.etiquetas', 'sicpro_app_solicitudes_iniciativas_etiquetas_rel',
                               'lead_id', 'tag_id', string='Etiqueta', tracking=True)
    priority = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    departamento = fields.Many2one('sicpro.app.trabajadores.areas', string="Departamento", required=False,
                                   domain="[('company_id', '=', company_id)]")
    grupo_ejecutor = fields.Many2one('sicpro.app.trabajadores.areas', string="Grupo Ejecutor", required=False,
                                     domain="[('company_id', '=', company_id)]")
    company_cliente = fields.Many2one('res.company', string='Proceso del Cliente', index=True, readonly=True,
                                      default=lambda self: self.env.company.id)
    fecha_solicitud_trabajo = fields.Date(string='Fecha de solicitud',
                                          default=lambda self: fields.Date.context_today(self))
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    fecha_aprobacion = fields.Date('Fecha de aprobación')
    fecha_asignacion = fields.Date('Fecha de asignación')
    fecha_revision = fields.Date('Fecha de revisión')
    pep_corto = fields.Char(string='Número SAP', size=10, required=True, index=True)
    ejecucion_proyecto = fields.Boolean(string="Tiene Proyecto", tracking=True)
    consecutivo_proyecto = fields.Char(string="Consecutivo", required=False, )
    ejecucion_tt = fields.Boolean(string="Tiene Tarea Técnica", tracking=True)
    codigo_tt = fields.Char(string="Código TT", required=False, )
    datos_equipamiento_1 = fields.Boolean(string="En Espera llegada a Cuba", )
    datos_equipamiento_2 = fields.Boolean(string="En Almacén de ETECSA", )
    datos_equipamiento_3 = fields.Boolean(string="En Almacén de Terceros", )
    datos_equipamiento_4 = fields.Boolean(string="En el lugar de Ejecución", )
    datos_equipamiento_5 = fields.Boolean(string="No Procede", )
    datos_materiales_1 = fields.Boolean(string="Con Reserva SAP", )
    datos_materiales_2 = fields.Boolean(string="Pdte por Reservar", )
    datos_materiales_3 = fields.Boolean(string="Por el Ejecutor", )
    datos_materiales_4 = fields.Boolean(string="No Procede.", )
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, )
    valor_sap_cup = fields.Monetary('Presupuesto', currency_field='company_currency', tracking=True, required=True)
    valor_sap_total = fields.Monetary('Presupuesto Total', store=True, currency_field='company_currency',
                                      compute='_compute_valor_sap_total')
    stage_id = fields.Many2one('sicpro.app.solicitudes.estados', string='Estados', ondelete='restrict', tracking=True,
                               group_expand='_read_group_stage_ids', index=True, copy=False,
                               default=_get_default_stage_id)
    type = fields.Selection([('iniciativa', 'Iniciativa'), ('oportunidad', 'Oportunidad')], index=True, required=True,
                            tracking=15, string='Tipo', default=lambda self: 'iniciativa', )
    estado_interno = fields.Selection(
        [('nuevo', 'Nuevo'), ('liberada', 'Liberada'), ('revision', 'Revisión'), ('aprobada', 'Aprobada'),
         ('rechazada_revision', 'Rechazada Revisión'), ('aprobar_revision', 'Aprobada Revisión'),
         ('cancelada_cliente', 'Cancelada'), ('cancelada_ejecutor', 'Cancelada'), ('rechazada_dtp', 'Rechazada DVPE'),
         ('rechazada_ejecutor', 'Rechazada Ejecutor'), ('rechazada_agrupacion', 'Rechazada Especialista'),
         ('oportunidad', 'Oportunidad')], index=True, required=True, tracking=15, default=lambda self: 'nuevo')
    tipo = fields.Selection([('principal', 'Principal'), ('subsolicitud', 'Subsolicitud')], string='Denominación',
                            index=True, required=True, tracking=15, default=lambda self: 'principal',
                            help="Determina si es una solicitud principal o una subsolicitud")
    pep = fields.Char(string='Sap', required=False)
    solicitud = fields.Many2one(comodel_name="sicpro.app.solicitudes.oportunidades", string="Solicitud",
                                required=False, )
    hijos_ids = fields.One2many(comodel_name="sicpro.app.solicitudes.oportunidades", inverse_name="solicitud",
                                string="Especialidad.", required=False, )
    especialidad = fields.Many2one(comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
                                   domain="[('company_id', '=', company_id)]", required=False, )
    codigo_especialidad = fields.Integer(string="Código", related='especialidad.codigo', index=False)
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", related='especialidad.image_1920', max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    motivo_rechazo = fields.Many2one('sicpro.app.solicitudes.rechazadas', string='Motivo de Rechazo', tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", tracking=True)

    user_id = fields.Many2one('res.users', string='Gestor de la Solicitud', index=True, tracking=True, )
    meeting_count = fields.Integer('# Meetings', compute='_compute_meeting_count')
    dias_aprobar = fields.Integer(compute='_compute_dias_aprobar', string='Días en aprobar', store=True)
    dias_asignar = fields.Integer(compute='_compute_dias_asignar', string='Dias en asignar', store=True)

    date_last_stage_update = fields.Datetime(string='Last Stage Update', index=True, default=fields.Datetime.now)
    date_conversion = fields.Datetime('Conversion Date', readonly=True)
    partner_address_name = fields.Char('Partner Contact Name', readonly=True)
    partner_address_email = fields.Char('Partner Contact Email', readonly=True)
    partner_address_phone = fields.Char('Partner Contact Phone', readonly=True)
    user_email = fields.Char('User Email', related='user_id.email', readonly=True)
    user_login = fields.Char('User Login', related='user_id.login', readonly=True)
    temporal_1 = fields.Boolean(string='temp1', default=False)  # control del campo stage_id
    temporal_2 = fields.Boolean(string='temp2', default=False)  # control del campo especialista_ejecutor
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    rechazada_subsolicitud = fields.Boolean(string='Rechazada_subsolicitud', required=False)
    pestana_especialidades = fields.Boolean(string='Pestana_especialidades', required=False, default=False)
    microlocalizacion = fields.Char(string='Micro Localización', required=False, default='N/P')
    enia = fields.Char(string='Estudio de la ENIA', required=False, default='N/P')
    ipf = fields.Date(string='Aprobación del IPF', required=False, )
    pg_revisado = fields.Boolean()
    pg_rechazado = fields.Boolean()
    tipo_plan = fields.Selection(string="Tipo de Plan",
                                 selection=[('n/p', 'N/P'), ('preparacion', 'Plan de Preparación'),
                                            ('ejecucion', 'Plan de Ejecución'), ], default='n/p')
    c_mep = fields.Char(string='C.MEP', required=False, help='Código MEP')
    lugar_trabajo = fields.Char(string='Lugar de Trabajo', required=False)
    solicitud_horizontal = fields.Boolean(string='Solicitud Horizontal', required=False, default=False)
    motivo_solicitud_horizontal = fields.Text('Motivo de Solicitud Horizontal', required=False, tracking=True)
    solicitante_solicitud_horizontal = fields.Many2one('res.users', string='Solicitante de Solicitud Horizontal',
                                                       index=True, tracking=True, )

    # verífico que el valor del presupuesto no sea 0
    @api.constrains('valor_sap_cup')
    def _check_valor_sap_cup(self):
        for record in self:
            if not record.solicitud_horizontal:
                if record.valor_sap_cup == 0:
                    raise ValidationError(_('Debe asignar un valor al presupuesto SAP.'))
                else:
                    if record.tipo != 'principal':
                        data = self.env['sicpro.app.solicitudes.oportunidades'].search(
                            [('id', '=', record.oportunidad_especialidad.id)]).valor_sap_cup
                        if record.valor_sap_cup > data:
                            raise ValidationError(_('Debe asignar un valor superior al presupuesto SAP general.'))

    # acción al seleccionar la solicitud para crear sub solicitudes
    @api.onchange('oportunidad_especialidad')
    def _onchange_oportunidad_especialidad(self, ):
        self.company_id = self.oportunidad_especialidad.company_id
        self.name = self.oportunidad_especialidad.name
        self.partner_id = self.oportunidad_especialidad.partner_id
        self.tipo = 'subsolicitud'
        self.tag_ids = self.oportunidad_especialidad.tag_ids
        self.pep_corto = self.oportunidad_especialidad.pep_corto
        self.priority = self.oportunidad_especialidad.priority

    @api.model
    def create(self, vals):
        res = super(SolicitudesOportunidades, self).create(vals)
        res['pestana_especialidades'] = True
        # Crear un duplicado de la solicitud en la tabla solicitudes
        res.env['sicpro.app.solicitudes.tabla.oportunidades'].sudo().create({'oportunidades': res._origin.id})
        return res

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # calcula el presupuesto total
    @api.depends('valor_sap_total')
    def _compute_valor_sap_total(self):
        if self.valor_sap_cup > 0:
            valor = self.valor_sap_cup
            return valor

    # calcula total de días entre la fecha de solicitud y aprobación
    @api.depends('dias_aprobar')
    def _compute_dias_aprobar(self):
        leads = self.filtered(lambda l: l.fecha_solicitud_trabajo and l.fecha_aprobacion)
        others = self - leads
        others.dias_aprobar = None
        for lead in leads:
            fecha_solicitud = fields.Datetime.from_string(lead.fecha_solicitud_trabajo)
            fecha_aprobacion = fields.Datetime.from_string(lead.fecha_aprobacion)
            lead.dias_aprobar = abs((fecha_aprobacion - fecha_solicitud).days)

    # calcula total de días entre la fecha de aprobación y asignación
    @api.depends('dias_asignar')
    def _compute_dias_asignar(self):
        leads = self.filtered(lambda l: l.fecha_aprobacion and l.fecha_asignacion)
        others = self - leads
        others.day_close = None
        for lead in leads:
            fecha_asignacion = fields.Datetime.from_string(lead.fecha_asignacion)
            fecha_aprobacion = fields.Datetime.from_string(lead.fecha_aprobacion)
            lead.dias_asignar = abs((fecha_asignacion - fecha_aprobacion).days)

    # acción al cambiar el el estado
    @api.onchange('stage_id')
    def _onchange_stage_id(self, ):
        self.temporal_1 = True

    # acción al cambiar el especialista ejecutor y agregar especialista seguidor y notificación
    @api.onchange('especialista_ejecutor')
    def _onchange_especialista_ejecutor(self, ):
        if self.especialista_ejecutor:
            self.temporal_2 = True
            self.stage_id = 2
        else:
            self.temporal_2 = False
            self.stage_id = 1

    # acción al cambiar la especialidad
    @api.onchange('especialidad')
    def _onchange_especialidad(self, ):
        if self.especialidad:
            self.pep = "{}.{}".format(self.pep_corto, self.codigo_especialidad)
        else:
            self.pep = "-"

    # acción del botón de Archivar Sub solicitud
    def action_archivar_subsolicitud(self, ):
        self.active = False

    # acción del botón de desarchivar Sub solicitud
    def action_desarchivar_subsolicitud(self, ):
        self.active = True

    # acción para llamar a las actividades en el calendario
    # del formulario oportunidades
    def action_calendario_oportunidades(self):
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        action['context'] = {'default_opportunity_id': self.id if self.type == 'oportunidad' else False,
                             'default_partner_id': self.partner_id.id, 'default_partner_ids': partner_ids,
                             'default_name': self.name, }
        return action

    # acción para contar las actividades en el botón calendario del formulario oportunidades
    def _compute_meeting_count(self):
        meeting_data = self.env['calendar.event'].read_group([('opportunity_id', 'in', self.ids)], ['opportunity_id'],
                                                             ['opportunity_id'])
        mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count'] for m in meeting_data}
        for lead in self:
            lead.meeting_count = mapped_data.get(lead.id, 0)

    def unlink(self):
        for value in self:
            data = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', value.id), ])
            for items in data:
                items.unlink()
        return super(SolicitudesOportunidades, self).unlink()

    def write(self, data):
        res = super(SolicitudesOportunidades, self).write(data)
        # activo o desactivo las sub solicitudes
        for value in self:
            if value.active:
                data = self.env['sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', value.id), ('active', '=', False)])
                for items in data:
                    items.active = value.active
            else:
                data = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', value.id), ])
                for items in data:
                    items.active = value.active

        # envío notificación al cambiar el estado
        if self.temporal_1:
            self.temporal_1 = False
            if 'stage_id' in data:
                self.message_post(body='La oportunidad cambió de estado', subtype_xmlid='mail.mt_comment',
                                  author_id=self.env.user.partner_id.id)

        # envío notificación al cambiar el especialista_ejecutor
        if self.temporal_2:
            self.temporal_2 = False
            if 'especialista_ejecutor' in data:
                self.message_subscribe(partner_ids=self.especialista_ejecutor.user_id.partner_id.ids)
                self.message_post(body='Oportunidad asignada.', subtype_xmlid='mail.mt_comment',
                                  author_id=self.env.user.partner_id.id)
                # Selecciono el registro de seguidores
                for participante in self.message_partner_ids:
                    # envío el correo electrónico
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                    template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        return res

    ###########################################################################
    ########################## INVERSIONISTAS #################################
    # acción del botón de liberar
    def action_inversionista_liberar(self, ):
        if self.hijos_ids:
            # Agrego seguidores de negocios
            usuario = self.env['res.users'].sudo().search([('company_id', '=', self.company_id.id), (
                'groups_id', '=', self.env.ref('sicpro_app_solicitudes.grupo_app_negocio_ejecutor').id)])
            self.message_subscribe(partner_ids=usuario.partner_id.ids)
            # Agrego seguidores de negocios de las sub solicitudes
            iniciativas = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
            for items in iniciativas.sudo():
                items.message_subscribe(partner_ids=self.env['res.users'].sudo().search(
                    [('company_id', '=', self.company_id.id), ('groups_id', '=', self.env.ref(
                        'sicpro_app_solicitudes.grupo_app_negocio_ejecutor').id)]).partner_id.ids)

            # envío notificación a los seguidores de negocios
            self.message_post(body='Iniciativa creada para negocio.', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_solicitudes.solicitudes_nueva_solicitud')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # cambio el estado interno de las solicitudes y sub solicitudes
            self.sudo().estado_interno = 'liberada'
            # cambio el estado interno de las subsolicitudes
            iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
            for items in iniciativa.sudo():
                items.estado_interno = 'liberada'
            # redirecciono la salida
            action = self.env.ref('sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[0]
            return action
        else:
            raise ValidationError(_('Para liberar la solicitud debe agregar especialidades de trabajo.'))

    # acción del botón de restaurar solicitud rechazada
    def action_inversionista_restaurar_rechazada(self, ):
        # cambio el estado interno de las solicitudes y sub solicitudes
        self.sudo().estado_interno = 'liberada'
        self.pg_revisado = False
        self.pg_rechazado = False
        # cambio el estado interno de las subsolicitudes
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_inicial', '=', True)]).id
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
            items.stage_id = estado
            items.pg_revisado = False
            items.pg_rechazado = False

        # envío notificación a los seguidores de negocios
        self.message_post(body='Iniciativa restaurada para negocio.', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_nueva_solicitud')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[0]
        return action

    # acción del botón de restaurar solicitud cancelada
    def action_inversionista_restaurar_cancelada(self, ):
        self.sudo().estado_interno = 'liberada'
        self.pg_revisado = False
        self.pg_rechazado = False
        # cambio el estado interno de las subsolicitudes
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_inicial', '=', True)]).id
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
            items.stage_id = estado
            items.pg_revisado = False
            items.pg_rechazado = False
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[0]
        return action

    ###########################################################################
    ########################## Revisión del Negocio ###########################
    # acción del botón de enviar a revisión
    def action_negociacion_pg_aprobar(self, ):
        self.fecha_revision = fields.Date.context_today(self)
        # cambio el estado interno de las solicitudes y sub solicitudes
        self.sudo().estado_interno = 'revision'
        data1 = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
        for items in data1.sudo():
            items.estado_interno = 'revision'
            items.fecha_revision = fields.Date.context_today(self)
            # suscribo los usuarios para revisión
            items.message_subscribe(partner_ids=self.env['res.users'].sudo().search(
                [('company_id', '=', items.company_id.id), ('groups_id', '=', self.env.ref(
                    'sicpro_app_solicitudes.grupo_app_negocio_pg_ejecutor').id)]).partner_id.ids)
            items.message_post(body='Iniciativa en revisión.', message_type='notification',
                               subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[0]
        return action

    # acción del botón de aprobar revisión
    def action_negociacion_pg_aprobar_revision(self, ):
        # cambio el estado interno de las solicitudes y sub solicitudes
        self.sudo().estado_interno = 'aprobar_revision'
        self.pg_revisado = True
        # cambio el estado interno de las sub solicitudes
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
        for items in iniciativa.sudo():
            items.estado_interno = 'aprobar_revision'
        self.message_post(body='Iniciativa revisada.', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_pg_action').sudo().read()[0]
        return action

    ###########################################################################
    ########################## Aprobar Negocio ################################
    # acción del botón de generar el consecutivo de la solicitud
    def action_negociacion_generar_id_solicitud(self, ):
        # Crear la secuencia de incremento para el consecutivo de la solicitud
        if not self.id_solicitud_creado:
            self.id_solicitud = self.env['ir.sequence'].next_by_code('solicitudes_id_consecutivo_incrementar')
            self.id_solicitud_creado = True
            # paso él, id de la solicitud a las sub solicitudes
            data2 = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
            for items in data2:
                items.id_solicitud = self.id_solicitud
                items.id_solicitud_creado = True

    # acción del botón de aprobada
    def action_negociacion_aprobar(self, ):
        self.fecha_aprobacion = fields.Date.context_today(self)
        # cambio el estado interno de las solicitudes y sub solicitudes
        self.sudo().estado_interno = 'aprobada'
        data1 = self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', self.id), ])
        for items in data1.sudo():
            if items.departamento:
                items.estado_interno = 'aprobada'
                items.fecha_aprobacion = fields.Date.context_today(self)
            else:
                raise ValidationError(_('La especialidad: ' + str(
                    items.especialidad.name) + ', no tiene un departamento ejecutor asociado. Verifíquelo'))

            # suscribo los usuarios distribuidores
            items.message_subscribe(partner_ids=self.env['res.users'].sudo().search(
                [('company_id', '=', items.company_id.id), ('groups_id', '=', self.env.ref(
                    'sicpro_app_solicitudes.grupo_app_ejecutor_ejecutor').id)]).partner_id.ids)
            items.message_post(body='Iniciativa aprobada.', message_type='notification',
                               subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in items.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                template.with_context(local_context).send_mail(items.id, force_send=True, email_values=email_values)
        # creo el id de la solicitud
        self.action_negociacion_generar_id_solicitud()
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[0]
        return action

    # acción del botón de restaurar ejecutor
    def action_negociacion_restaurar_ejecutor(self, ):
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_inicial', '=', True)]).id
        self.fecha_aprobacion = fields.Date.context_today(self)
        self.sudo().tipo = 'subsolicitud'
        self.sudo().estado_interno = 'aprobada'
        self.sudo().stage_id = estado
        # envío la notificación a los seguidores
        self.message_post(body='Iniciativa restaurada.', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[0]
        return action

    ###########################################################################
    ###########################################################################
    # oportunidad
    oportunidad_id = fields.Many2one(comodel_name="sicpro.app.solicitudes.oportunidades",
                                     string='Oportunidades')
    ###########################################################################


# Solicitudes horizontales
class SolicitudesOportunidadesHorizontales(models.TransientModel):
    _name = 'sicpro.app.grupo.ejecutor.horizontal'
    _description = 'Grupo Ejecutor Solicitudes Horizontales'

    # id de la solicitud por defecto
    def _default_solicitud_id(self):
        solicitud_id = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        return solicitud_id

    # generar el consecutivo especial de la sub solicitud
    def _default_consecutivo_subsolicitud(self):
        solicitud_id = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        sol_id_original = self.env['sicpro.app.solicitudes.oportunidades'].sudo().search(
            ['&', ('active', '=', True), ('id', '=', solicitud_id.solicitud.id)])
        sol_id = self.env['sicpro.app.solicitudes.oportunidades'].sudo().search(
            ['&', '&', ('active', '=', True), ('solicitud', '=', solicitud_id.solicitud.id),
             ('solicitud_horizontal', '=', True)])

        # género la lista con los consecutivos de las solicitudes horizontales
        consecutivos_sh = []
        for item in sol_id:
            count = len(item.id_solicitud)
            indice = item.id_solicitud.find('.') + 1
            consecutivos_sh.append(int(item.id_solicitud[indice:count]))

        # busco el consecutivo mayor de la lista para agregarle 1
        consecutivos_max = None
        for num in consecutivos_sh:
            if consecutivos_max is None or num > consecutivos_max:
                consecutivos_max = num

        if sol_id:
            consecutivo = str(sol_id_original.id_solicitud) + '.' + str(consecutivos_max + 1)
            return consecutivo
        else:
            consecutivo = str(sol_id_original.id_solicitud) + '.1'
            return consecutivo

    id_solicitud = fields.Char(string='Solicitud ID', copy=False, default=_default_consecutivo_subsolicitud)
    solicitud = fields.Many2one(comodel_name="sicpro.app.solicitudes.oportunidades", string="Solicitud",
                                default=_default_solicitud_id)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', related='solicitud.company_id', store=True)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, )
    valor_sap_cup = fields.Monetary('Presupuesto', currency_field='company_currency', required=False)
    especialidad = fields.Many2one(comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
                                   domain="[('company_id', '=', company_id)]", required=True, )
    codigo_especialidad = fields.Integer(string="Código", related='especialidad.codigo', index=False)
    motivo_solicitud_horizontal = fields.Text('Motivo de Solicitud Horizontal', required=True)
    priority = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, default=Prioridades_Activas[0][0])
    departamento = fields.Many2one('sicpro.app.trabajadores.areas', string="Departamento", required=True,
                                   domain="[('company_id', '=', company_id)]")
    tag_ids = fields.Many2many('sicpro.app.solicitudes.etiquetas', 'sicpro_app_solicitudes_horizotales_etiquetas_rel',
                               'lead_id', 'tag_id', string='Etiqueta')
    microlocalizacion = fields.Char(string='Micro Localización', required=False, default='N/P')
    enia = fields.Char(string='Estudio de la ENIA', required=False, default='N/P')
    ipf = fields.Date(string='Aprobación del IPF', required=False, )
    ejecucion_proyecto = fields.Boolean(string="Tiene Proyecto")
    consecutivo_proyecto = fields.Char(string="Consecutivo", required=False, )
    ejecucion_tt = fields.Boolean(string="Tiene Tarea Técnica")
    codigo_tt = fields.Char(string="Código TT", required=False, )
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    datos_equipamiento_1 = fields.Boolean(string="En Espera llegada a Cuba", )
    datos_equipamiento_2 = fields.Boolean(string="En Almacén de ETECSA", )
    datos_equipamiento_3 = fields.Boolean(string="En Almacén de Terceros", )
    datos_equipamiento_4 = fields.Boolean(string="En el lugar de Ejecución", )
    datos_equipamiento_5 = fields.Boolean(string="No Procede", )
    datos_materiales_1 = fields.Boolean(string="Con Reserva SAP", )
    datos_materiales_2 = fields.Boolean(string="Pdte por Reservar", )
    datos_materiales_3 = fields.Boolean(string="Por el Ejecutor", )
    datos_materiales_4 = fields.Boolean(string="No Procede.", )
    description = fields.Text('Notes', required=False, )
    solicitante_solicitud_horizontal = fields.Many2one('res.users', string='Solicitante de Solicitud Horizontal',
                                                       index=True, default=lambda self: self.env.uid)

    # Creo una sub solicitud horizontal vinculada a la solicitud principal
    def action_crear_solicitud_horizontal(self):
        oportunidad = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))

        # creo la solicitud horizontal
        value = {'name': oportunidad.name, 'oportunidad_especialidad': oportunidad.oportunidad_especialidad.id,
                 'company_id': oportunidad.company_id.id, 'id_solicitud_creado': True,
                 'partner_id': oportunidad.partner_id.id, 'partner_name': oportunidad.partner_name,
                 'territorio_id': oportunidad.territorio_id.id, 'provincia_id': oportunidad.provincia_id.id,
                 'website': oportunidad.website, 'cargo': oportunidad.cargo, 'telefono_fijo': oportunidad.telefono_fijo,
                 'tipo': oportunidad.tipo, 'telefono_movil': oportunidad.telefono_movil, 'correo': oportunidad.correo,
                 'pagina_web': oportunidad.pagina_web, 'anio': oportunidad.anio,
                 'company_cliente': oportunidad.company_cliente.id, 'fecha_aprobacion': oportunidad.fecha_aprobacion,
                 'fecha_solicitud_trabajo': oportunidad.fecha_solicitud_trabajo, 'type': oportunidad.type,
                 'fecha_asignacion': oportunidad.fecha_asignacion, 'stage_id': oportunidad.stage_id.id,
                 'fecha_revision': oportunidad.fecha_revision, 'estado_interno': oportunidad.estado_interno,
                 'solicitud': oportunidad.solicitud.id,
                 'observaciones_grupo_ejecutor': oportunidad.observaciones_grupo_ejecutor,
                 'date_last_stage_update': oportunidad.date_last_stage_update, 'tipo_plan': oportunidad.tipo_plan,
                 'date_conversion': oportunidad.date_conversion,
                 'partner_address_name': oportunidad.partner_address_name,
                 'partner_address_email': oportunidad.partner_address_email, 'c_mep': oportunidad.c_mep,
                 'partner_address_phone': oportunidad.partner_address_phone, 'lugar_trabajo': oportunidad.lugar_trabajo,
                 'pestana_especialidades': oportunidad.pestana_especialidades, 'solicitud_horizontal': True,
                 'pep_corto': oportunidad.pep_corto,
                 'solicitante_solicitud_horizontal': self.solicitante_solicitud_horizontal.id,
                 'pep': "{}.{}".format(oportunidad.pep_corto, self.codigo_especialidad),
                 'id_solicitud': self.id_solicitud, 'company_currency': oportunidad.company_currency.id,
                 'valor_sap_cup': self.valor_sap_cup, 'especialidad': self.especialidad.id,
                 'codigo_especialidad': self.codigo_especialidad,
                 'motivo_solicitud_horizontal': self.motivo_solicitud_horizontal, 'priority': self.priority,
                 'departamento': self.departamento.id, 'tag_ids': self.tag_ids,
                 'microlocalizacion': self.microlocalizacion, 'enia': self.enia, 'ipf': self.ipf,
                 'ejecucion_proyecto': self.ejecucion_proyecto, 'consecutivo_proyecto': self.consecutivo_proyecto,
                 'ejecucion_tt': self.ejecucion_tt, 'codigo_tt': self.codigo_tt, 'attachment_ids': self.attachment_ids,
                 'datos_equipamiento_1': self.datos_equipamiento_1, 'datos_equipamiento_2': self.datos_equipamiento_2,
                 'datos_equipamiento_3': self.datos_equipamiento_3, 'datos_equipamiento_4': self.datos_equipamiento_4,
                 'datos_equipamiento_5': self.datos_equipamiento_5, 'datos_materiales_1': self.datos_materiales_1,
                 'datos_materiales_2': self.datos_materiales_2, 'datos_materiales_3': self.datos_materiales_3,
                 'datos_materiales_4': self.datos_materiales_4, 'description': self.description, }

        # creo el registro nuevo
        registro_nuevo = self.env['sicpro.app.solicitudes.oportunidades'].sudo().create(value)

        sol_id_notifica = self.env['sicpro.app.solicitudes.oportunidades'].sudo().search(
            ['&', ('active', '=', True), ('id', '=', registro_nuevo.id)])

        # Agrego seguidores para grupo ejecutor
        sol_id_notifica.message_subscribe(partner_ids=oportunidad.message_partner_ids.ids)
        # envío notificación a los seguidores de negocios
        sol_id_notifica.message_post(body='Solicitud Horizontal Creada.', message_type='notification',
                                     subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in sol_id_notifica.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_nueva_solicitud_horizontal')
            template.with_context(local_context).send_mail(sol_id_notifica.id, force_send=True,
                                                           email_values=email_values)
            # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_ejecutor_action').sudo().read()[0]
        return action


# inversionista
class CanceladasT2(models.TransientModel):
    _name = 'sicpro.app.solicitudes.canceladas.t2'
    _description = 'Canceladas T2'

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", required=True, )

    def action_motivo_cancelacion_t2(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_cancelado', '=', True)]).id
        for item in cancelada:
            item.motivo_cancelacion = self.motivo_cancelacion
            item.estado_interno = 'cancelada_cliente'
            item.stage_id = estado
        # cambio el estado interno de las sub solicitudes
        for items in self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', cancelada.id), ]):
            items.estado_interno = 'cancelada_cliente'
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Iniciativa cancelada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[0]
        return action


# negociación
class RechazadasT3(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t3'
    _description = 'Rechazadas T3'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas', string="Motivo", required=True)

    def action_motivo_rechazo_t3(self):
        # cambio el estado interno de la solicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_detenido', '=', True)]).id
        for item in rechazo.sudo():
            item.motivo_rechazo = self.lost_reason_id.id
            item.sudo().estado_interno = 'rechazada_dtp'
            item.stage_id = estado
        # cambio el estado interno de las subsolicitudes
        subsolic = self.env['sicpro.app.solicitudes.oportunidades'].sudo().search([('solicitud', '=', rechazo.id), ])
        for items in subsolic.sudo():
            items.sudo().estado_interno = 'rechazada_dtp'
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Iniciativa rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[0]
        return action


# negociación
class CanceladasT3(models.TransientModel):
    _name = 'sicpro.app.solicitudes.canceladas.t3'
    _description = 'Canceladas T3'

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", required=True, )

    def action_motivo_cancelacion_t3(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_cancelado', '=', True)]).id
        for item in cancelada:
            item.motivo_cancelacion = self.motivo_cancelacion
            item.estado_interno = 'cancelada_ejecutor'
            item.stage_id = estado
        # cambio el estado interno de las sub solicitudes
        for items in self.env['sicpro.app.solicitudes.oportunidades'].search([('solicitud', '=', cancelada.id), ]):
            items.estado_interno = 'cancelada_ejecutor'
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Iniciativa cancelada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[0]
        return action


# revisión de la negociación
class RechazadasT6(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t6'
    _description = 'Rechazadas T6'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas', string="Motivo", required=True)

    def action_motivo_rechazo_t6(self):
        # cambio el estado interno de la solicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_detenido', '=', True)]).id
        for item in rechazo.sudo():
            item.motivo_rechazo = self.lost_reason_id.id
            item.sudo().estado_interno = 'rechazada_revision'
            item.stage_id = estado
            item.pg_revisado = True
            item.pg_rechazado = True

        # cambio el estado interno de las subsolicitudes
        subsolic = self.env['sicpro.app.solicitudes.oportunidades'].sudo().search([('solicitud', '=', rechazo.id), ])
        for items in subsolic.sudo():
            items.sudo().estado_interno = 'rechazada_revision'
        # llamo al método para crear la notificación

        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Revisión rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_negociacion_pg_action').sudo().read()[0]
        return action


# grupos o departamentos
class RechazadasT4(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t4'
    _description = 'Rechazadas T4'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas', string="Motivo", required=True)

    def action_motivo_rechazo_t4(self):
        # cambio el estado interno de la subsolicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_detenido', '=', True)]).id
        for item in rechazo:
            item.motivo_rechazo = self.lost_reason_id.id
            item.estado_interno = 'rechazada_ejecutor'
            item.tipo = 'principal'
            item.rechazada_subsolicitud = True
            item.stage_id = estado
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Iniciativa rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_ejecutor_action').sudo().read()[0]
        return action


# grupos o departamento
class GrupoEjecutorT4(models.TransientModel):
    _name = 'sicpro.app.grupo.ejecutor.t4'
    _description = 'Grupo Ejecutor T4'

    company_id = fields.Many2one('res.company', string='Proceso', index=True, readonly=True,
                                 default=lambda self: self.env.company.id)
    grupo_ejecutor = fields.Many2one('sicpro.app.trabajadores.areas', string="Grupo Ejecutor", required=False,
                                     domain="[('company_id', '=', company_id)]")
    especialista_ejecutor = fields.Many2one(comodel_name="sicpro.app.trabajadores", string='Asignar a',
                                            domain="[('company_id', '=', company_id)]", required=True)
    # inicio esta sección esta sin funcionamiento
    ejecucion = fields.Selection(
        [('convertir', 'Convertir a oportunidad'), ('fusionar', 'Fusionar con oportunidad existente')],
        'Acciones de conversión', default="convertir", required=True)

    # fin esta sección esta sin funcionamiento

    def action_grupo_ejecutor_t4(self):
        # cambio el estado interno de la sub solicitud
        oportunidad = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_inicial', '=', True)]).id
        for item in oportunidad.sudo():
            item.grupo_ejecutor = self.grupo_ejecutor
            item.especialista_ejecutor = self.especialista_ejecutor
            item.type = 'oportunidad'
            item.fecha_aprobacion = fields.Date.context_today(self)
            if self.especialista_ejecutor:
                item.stage_id = estado
            # Agrego seguidores para grupo ejecutor
            if item.especialista_ejecutor:
                item.message_subscribe(partner_ids=item.especialista_ejecutor.user_id.partner_id.ids)
            # envío notificación a los seguidores de negocios
            item.message_post(body='Oportunidad creada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in item.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_ejecutor_action').sudo().read()[0]
        return action


# especialistas
class RechazadasT5(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t5'
    _description = 'Rechazadas T5'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas', string="Motivo", required=True)

    def action_motivo_rechazo_t5(self):
        # cambio el estado interno de la sub solicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_detenido', '=', True)]).id
        for item in rechazo:
            item.motivo_rechazo = self.lost_reason_id.id
            item.estado_interno = 'rechazada_agrupacion'
            item.type = 'iniciativa'
            item.tipo = 'subsolicitud'
            item.rechazada_subsolicitud = True
            item.stage_id = estado
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Oportunidad rechazada', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_grupos_action').sudo().read()[0]
        return action


# especialista
class GrupoEjecutorT5(models.TransientModel):
    _name = 'sicpro.app.grupo.ejecutor.t5'
    _description = 'Grupo Ejecutor T5'

    company_id = fields.Many2one('res.company', string='Proceso', index=True, readonly=True,
                                 default=lambda self: self.env.company.id)
    especialista_ejecutor = fields.Many2one(comodel_name="sicpro.app.trabajadores", string='Asignar a', required=True)

    def action_grupo_ejecutor_t5(self, ):
        # cambio el estado interno de la sub solicitud
        oportunidad = self.env['sicpro.app.solicitudes.oportunidades'].browse(self.env.context.get('active_ids'))
        estado = self.env['sicpro.app.solicitudes.estados'].search([('is_inicial', '=', True)]).id
        for item in oportunidad.sudo():

             item.especialista_ejecutante = self.especialista_ejecutor
             if self.especialista_ejecutor:
                 item.stage_id = estado
            # Agrego seguidores para grupo ejecutor
             if item.especialista_ejecutante:
                 item.message_subscribe(partner_ids=item.especialista_ejecutante.user_id.partner_id.ids)
            # # envío notificación a los seguidores de negocios
             item.message_post(body='oportunidad transferida.', message_type='notification',
                               subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
             for participante in item.message_partner_ids:
            #     # envío el correo electrónico
                 email_values = {'email_to': participante.email_formatted, }
                 local_context = self.env.context.copy()
                 template = self.env.ref('sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                 template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes.solicitudes_grupos_action').sudo().read()[0]
        return action
