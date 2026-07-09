# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta')]


class SolicitudesOportunidades(models.Model):
    _name = 'sicpro.app.solicitudes.oportunidades'
    _description = "Solicitudes y oportunidades"
    _order = 'priority desc, id asc'
    _rec_name = 'name'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # ajusta el nombre para visualizar en el modulo de ordenes de trabajo
    def _compute_display_name(self):
        for record in self:
            especialidad_name = record.especialidad.name if record.especialidad else ''
            record.display_name = f"{record.id_solicitud or ''} - {especialidad_name} - {record.name or ''}"

    # agrego el cliente por defecto
    def _default_partner_id(self):
        users_id = self.env.user.user_inversionista
        if users_id:
            if self.env.user.nombre_inversionista:
                return self.env.user.nombre_inversionista.id
        return False

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        stage = self.env['sicpro.app.solicitudes.estados'].search([], limit=1)
        return stage.id if stage else False

    name = fields.Char(string="Oportunidad", required=True, index=True)
    oportunidad_especialidad = fields.Many2one(
        comodel_name='sicpro.app.solicitudes.oportunidades',
        string='Oportunidad.', required=False,
        domain=[('estado_interno', '=', 'nuevo'),
                ('tipo', '=', 'principal')], )
    id_solicitud = fields.Char(string='Solicitud ID', tracking=True,
                               copy=False, readonly=True, )
    id_solicitud_creado = fields.Boolean(string='Id_solicitud_creado',
                                         required=False, default=False)
    partner_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 tracking=10, index=True,
                                 domain=[('tipo_registro', '=', 'persona')],
                                 default=lambda
                                     self: self._default_partner_id(), )
    partner_name = fields.Char(string="Nombre de la entidad",
                               related='partner_id.entidad.name')
    territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios",
        string="Unidad Organizativa", related='partner_id.territorio',
        store=True)
    provincia_id = fields.Many2one(comodel_name="res.country.state",
                                   string="Provincia",
                                   related='partner_id.provincias_id',
                                   store=True)
    website = fields.Char(string='Sitio Web', help="Website of the contact",
                          related='partner_id.entidad.pagina_web')
    cargo = fields.Char(string="Cargo", required=False,
                        related='partner_id.cargo')
    telefono_fijo = fields.Char(string="Teléfono", required=False,
                                related='partner_id.telefono_fijo')
    telefono_movil = fields.Char(string="Móvil", required=False,
                                 related='partner_id.telefono_movil')
    correo = fields.Char(string="Correo electrónico", required=False,
                         related='partner_id.correo')
    pagina_web = fields.Char(string="Pagina Web", required=False,
                             related='partner_id.pagina_web')
    active = fields.Boolean(string='Activo', default=True, tracking=True)
    color = fields.Integer(string='Índice de colores', default=0)
    especialista_ejecutor = fields.Many2one(
        comodel_name="sicpro.app.trabajadores", string='Responsable',
        tracking=True)
    cargo_especialista = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.ocupacion",
        string='Cargo Responsable',
        related="especialista_ejecutor.ocupacion_id", store=True)
    especialista_ejecutante = fields.Many2one(
        comodel_name="sicpro.app.trabajadores", string='Ejecutante',
        tracking=True)
    cargo_especialista_ejecutante = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.ocupacion",
        string='Cargo Ejecutante',
        related="especialista_ejecutante.ocupacion_id", store=True)
    especialista_ejecutante_bool = fields.Boolean(
        string='Especialista_ejecutante_bool', required=False)
    description = fields.Text(string='Notes', required=False, tracking=True)
    observaciones_grupo_ejecutor = fields.Text(string='Alcance General',
                                               required=False, tracking=True)
    tag_ids = fields.Many2many('sicpro.app.solicitudes.etiquetas',
                               'sicpro_app_solicitudes_iniciativas_etiquetas_rel',
                               'lead_id', 'tag_id', string='Etiqueta',
                               tracking=True)
    priority = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                index=True, tracking=True,
                                default=PRIORIDADES_ACTIVAS[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    departamento = fields.Many2one('sicpro.app.trabajadores.areas',
                                   string="Departamento", required=False,
                                   domain="[('company_id', '=', company_id)]")
    grupo_ejecutor = fields.Many2one('sicpro.app.trabajadores.areas',
                                     string="Grupo Ejecutor", required=False,
                                     domain="[('company_id', '=', company_id)]")
    company_cliente = fields.Many2one('res.company',
                                      string='Proceso del Cliente', index=True,
                                      readonly=True,
                                      default=lambda self: self.env.company.id)
    fecha_solicitud_trabajo = fields.Date(string='Fecha de solicitud',
                                          default=lambda
                                              self: fields.Date.context_today(
                                              self))
    anio = fields.Char(string="Año", required=False,
                       default=lambda self: fields.Datetime.now().strftime(
                           "%Y"), )
    fecha_aprobacion = fields.Date(string='Fecha de aprobación')
    fecha_asignacion = fields.Date(string='Fecha de asignación')
    fecha_revision = fields.Date(string='Fecha de revisión')
    pep_corto = fields.Char(string='Número SAP', size=10, required=True,
                            index=True)
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
    company_currency = fields.Many2one(string='Moneda',
                                       related='company_id.currency_id',
                                       readonly=True, )
    valor_sap_cup = fields.Monetary(string='Presupuesto',
                                    currency_field='company_currency',
                                    tracking=True, required=True)
    valor_sap_total = fields.Monetary(string='Presupuesto Total', store=True,
                                      currency_field='company_currency',
                                      compute='_compute_valor_sap_total')
    stage_id = fields.Many2one('sicpro.app.solicitudes.estados',
                               string='Estados', ondelete='restrict',
                               tracking=True,
                               group_expand='_read_group_stage_ids',
                               index=True, copy=False,
                               default=_get_default_stage_id)
    type = fields.Selection(
        [('iniciativa', 'Iniciativa'), ('oportunidad', 'Oportunidad')],
        index=True, required=True, tracking=15, string='Tipo',
        default=lambda self: 'iniciativa', )
    estado_interno = fields.Selection(
        [('nuevo', 'Nuevo'), ('liberada', 'Liberada'),
         ('revision', 'Revisión'), ('aprobada', 'Aprobada'),
         ('rechazada_revision', 'Rechazada Revisión'),
         ('aprobar_revision', 'Aprobada Revisión'),
         ('cancelada_cliente', 'Cancelada'),
         ('cancelada_ejecutor', 'Cancelada'),
         ('rechazada_dtp', 'Rechazada DVPE'),
         ('rechazada_ejecutor', 'Rechazada Ejecutor'),
         ('rechazada_agrupacion', 'Rechazada Especialista'),
         ('oportunidad', 'Oportunidad')], index=True, required=True,
        tracking=15, default=lambda self: 'nuevo')
    tipo = fields.Selection(
        [('principal', 'Principal'), ('subsolicitud', 'Subsolicitud')],
        string='Denominación', index=True, required=True, tracking=15,
        default=lambda self: 'principal',
        help="Determina si es una solicitud principal o una subsolicitud")
    pep = fields.Char(string='Sap', required=False)
    solicitud = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        string="Solicitud", required=False, )
    hijos_ids = fields.One2many(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        inverse_name="solicitud", string="Especialidad.", required=False, )
    especialidad = fields.Many2one(
        comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
        domain="[('company_id', '=', company_id)]", required=False, )
    codigo_especialidad = fields.Integer(string="Código",
                                         related='especialidad.codigo',
                                         index=False)
    image_1920 = fields.Image("Image", related='especialidad.image_1920',
                              max_width=1920, max_height=1920)
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    motivo_rechazo = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     string='Motivo de Rechazo', tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     tracking=True)

    user_id = fields.Many2one('res.users', string='Gestor de la Solicitud',
                              index=True, tracking=True, )
    meeting_count = fields.Integer(string='# Meetings',
                                   compute='_compute_meeting_count')
    dias_aprobar = fields.Integer(compute='_compute_dias_aprobar',
                                  string='Días en aprobar', store=True)
    dias_asignar = fields.Integer(compute='_compute_dias_asignar',
                                  string='Dias en asignar', store=True)

    date_last_stage_update = fields.Datetime(string='Last Stage Update',
                                             index=True,
                                             default=fields.Datetime.now)
    date_conversion = fields.Datetime(string='Conversion Date', readonly=True)
    partner_address_name = fields.Char(string='Partner Contact Name', readonly=True)
    partner_address_email = fields.Char(string='Partner Contact Email', readonly=True)
    partner_address_phone = fields.Char(string='Partner Contact Phone', readonly=True)
    user_email = fields.Char(string='User Email', related='user_id.email',
                             readonly=True)
    user_login = fields.Char(string='User Login', related='user_id.login',
                             readonly=True)
    temporal_1 = fields.Boolean(string='temp1', default=False)
    temporal_2 = fields.Boolean(string='temp2', default=False)
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    rechazada_subsolicitud = fields.Boolean(string='Rechazada_subsolicitud',
                                            required=False)
    pestana_especialidades = fields.Boolean(string='Pestana_especialidades',
                                            required=False, default=False)
    microlocalizacion = fields.Char(string='Micro Localización',
                                    required=False, default='N/P')
    enia = fields.Char(string='Estudio de la ENIA', required=False,
                       default='N/P')
    ipf = fields.Date(string='Aprobación del IPF', required=False, )
    pg_revisado = fields.Boolean()
    pg_rechazado = fields.Boolean()
    tipo_plan = fields.Selection(string="Tipo de Plan",
                                 selection=[('n/p', 'N/P'), (
                                     'preparacion', 'Plan de Preparación'), (
                                                'ejecucion',
                                                'Plan de Ejecución'), ],
                                 default='n/p')
    c_mep = fields.Char(string='C.MEP', required=False, help='Código MEP')
    lugar_trabajo = fields.Char(string='Lugar de Trabajo', required=False)
    solicitud_horizontal = fields.Boolean(string='Solicitud Horizontal',
                                          required=False, default=False)
    motivo_solicitud_horizontal = fields.Text(string='Motivo de Solicitud Horizontal',
                                              required=False, tracking=True)
    solicitante_solicitud_horizontal = fields.Many2one('res.users',
                                                       string='Solicitante de Solicitud Horizontal',
                                                       index=True,
                                                       tracking=True, )

    # verífico que el valor del presupuesto no sea 0
    @api.constrains('valor_sap_cup')
    def _check_valor_sap_cup(self):
        for record in self:
            if not record.solicitud_horizontal:
                if record.valor_sap_cup == 0:
                    raise ValidationError(
                        'Debe asignar un valor al presupuesto SAP de la especialidad.' + MSG_SOPORTE_SICPRO)
                else:
                    if record.tipo != 'principal':
                        data = self.env[
                            'sicpro.app.solicitudes.oportunidades'].search([(
                        'id', '=',
                        record.oportunidad_especialidad.id)]).valor_sap_cup
                        if record.valor_sap_cup > data:
                            raise ValidationError(
                                'Debe asignar un valor superior al presupuesto SAP general.' + MSG_SOPORTE_SICPRO)

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

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SolicitudesOportunidades, self).create(vals_list)
        for res in records:
            res.pestana_especialidades = True
        return records

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

    # CORRECCIÓN: El depend debe ir al campo físico detonante, iterar en self y asignar en vez de retornar
    @api.depends('valor_sap_cup')
    def _compute_valor_sap_total(self):
        for record in self:
            if record.valor_sap_cup > 0:
                record.valor_sap_total = record.valor_sap_cup
            else:
                record.valor_sap_total = 0.0

    # CORRECCIÓN: Depende de fechas, requiere iteración interna y control multi-registro
    @api.depends('fecha_solicitud_trabajo', 'fecha_aprobacion')
    def _compute_dias_aprobar(self):
        for lead in self:
            if lead.fecha_solicitud_trabajo and lead.fecha_aprobacion:
                fecha_solicitud = fields.Date.to_date(
                    lead.fecha_solicitud_trabajo)
                fecha_aprobacion = fields.Date.to_date(lead.fecha_aprobacion)
                lead.dias_aprobar = abs(
                    (fecha_aprobacion - fecha_solicitud).days)
            else:
                lead.dias_aprobar = 0

    # CORRECCIÓN: Depende de fechas, corrección de day_close inexistente por asignación directa
    @api.depends('fecha_aprobacion', 'fecha_asignacion')
    def _compute_dias_asignar(self):
        for lead in self:
            if lead.fecha_aprobacion and lead.fecha_asignacion:
                fecha_asignacion = fields.Date.to_date(lead.fecha_asignacion)
                fecha_aprobacion = fields.Date.to_date(lead.fecha_aprobacion)
                lead.dias_asignar = abs(
                    (fecha_asignacion - fecha_aprobacion).days)
            else:
                lead.dias_asignar = 0

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

    def action_archivar_subsolicitud(self, ):
        self.active = False

    def action_desarchivar_subsolicitud(self, ):
        self.active = True

    def action_calendario_oportunidades(self):
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        action['context'] = {
            'default_opportunity_id': self.id if self.type == 'oportunidad' else False,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids, 'default_name': self.name, }
        return action

    def _compute_meeting_count(self):
        meeting_data = self.env['calendar.event'].read_group(
            [('opportunity_id', 'in', self.ids)], ['opportunity_id'],
            ['opportunity_id'])
        mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count'] for m
                       in meeting_data if m['opportunity_id']}
        for lead in self:
            lead.meeting_count = mapped_data.get(lead.id, 0)

    def unlink(self):
        for value in self:
            data = self.env['sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', value.id), ])
            for items in data:
                items.unlink()
        return super(SolicitudesOportunidades, self).unlink()

    def write(self, data):
        res = super(SolicitudesOportunidades, self).write(data)
        for value in self:
            if value.active:
                sub_data = self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', value.id), ('active', '=', False)])
                for items in sub_data:
                    items.active = value.active
            else:
                sub_data = self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', value.id), ])
                for items in sub_data:
                    items.active = value.active

            # CORRECCIÓN: Las notificaciones deben dispararse por cada registro del bucle para evitar caídas multi-registro
            if value.temporal_1:
                value.temporal_1 = False
                if 'stage_id' in data:
                    value.message_post(body='La oportunidad cambió de estado',
                                       subtype_xmlid='mail.mt_comment',
                                       author_id=self.env.user.partner_id.id)

            if value.temporal_2:
                value.temporal_2 = False
                if 'especialista_ejecutor' in data:
                    value.message_subscribe(
                        partner_ids=value.especialista_ejecutor.user_id.partner_id.ids)
                    value.message_post(body='Oportunidad asignada.',
                                       subtype_xmlid='mail.mt_comment',
                                       author_id=self.env.user.partner_id.id)
                    for participante in value.message_partner_ids:
                        email_values = {
                            'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref(
                            'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                        template.with_context(local_context).send_mail(
                            value.id, force_send=True,
                            email_values=email_values)
        return res

    def action_inversionista_liberar(self):
        # Obtenemos el grupo
        grupo_ejecutor = self.env.ref(
            'sicpro_app_solicitudes.grupo_app_negocio_ejecutor',
            raise_if_not_found=False)

        # Obtenemos los usuarios directamente a través de su grupo, restringiendo por compañía en la misma búsqueda
        # Al acceder a grupo_ejecutor.user_ids, obtenemos todos los usuarios del grupo
        # Luego, realizamos la búsqueda sobre ellos para aplicar el filtro de compañía
        usuarios = self.env['res.users'].search([(
        'id', 'in', grupo_ejecutor.user_ids.ids if grupo_ejecutor else []),
            ('company_id', '=', self.company_id.id)])
        partner_ids = usuarios.partner_id.ids

        if self.hijos_ids:
            # Suscripción del padre
            self.message_subscribe(partner_ids=partner_ids)

            # Buscar iniciativas relacionadas
            iniciativas = self.env[
                'sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', self.id)])

            for items in iniciativas.sudo():
                items.message_subscribe(partner_ids=partner_ids)

            self.message_post(body='Iniciativa creada para negocio.',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            for participante in self.message_partner_ids:
                if participante.email:
                    email_values = {'email_to': participante.email_formatted}
                    template = self.env.ref(
                        'sicpro_app_solicitudes.solicitudes_nueva_solicitud')
                    template.with_context(self.env.context).send_mail(self.id,
                                                                      force_send=True,
                                                                      email_values=email_values)

            self.sudo().estado_interno = 'liberada'

            # Actualizar estado de las iniciativas
            for items in iniciativas.sudo():
                items.estado_interno = 'liberada'

            action = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[
                0]
            return action
        else:
            raise ValidationError(
                'Para liberar la solicitud debe agregar especialidades de trabajo.' + MSG_SOPORTE_SICPRO)

    def action_inversionista_restaurar_rechazada(self, ):
        self.sudo().estado_interno = 'liberada'
        self.pg_revisado = False
        self.pg_rechazado = False
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        estado = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_inicial', '=', True)]).id
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
            items.stage_id = estado
            items.pg_revisado = False
            items.pg_rechazado = False

        self.message_post(body='Iniciativa restaurada para negocio.',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        for participante in self.message_partner_ids:
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_nueva_solicitud')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[
            0]
        return action

    def action_inversionista_restaurar_cancelada(self, ):
        self.sudo().estado_interno = 'liberada'
        self.pg_revisado = False
        self.pg_rechazado = False
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        estado = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_inicial', '=', True)]).id
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
            items.stage_id = estado
            items.pg_revisado = False
            items.pg_rechazado = False
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_inversionista_action').sudo().read()[
            0]
        return action

    def action_negociacion_pg_aprobar(self, ):
        self.fecha_revision = fields.Date.context_today(self)
        self.sudo().estado_interno = 'revision'
        data1 = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])

        grupo_pg_ejecutor = self.env.ref(
            'sicpro_app_solicitudes.grupo_app_negocio_pg_ejecutor',
            raise_if_not_found=False)

        for items in data1.sudo():
            items.estado_interno = 'revision'
            items.fecha_revision = fields.Date.context_today(self)

            usuarios_pg = self.env['res.users'].sudo().search([('id', 'in',
                                                                grupo_pg_ejecutor.user_ids.ids if grupo_pg_ejecutor else []),
                ('company_id', '=', items.company_id.id)])
            items.message_subscribe(partner_ids=usuarios_pg.partner_id.ids)

            items.message_post(body='Iniciativa en revisión.',
                               message_type='notification',
                               subtype_xmlid='mail.mt_comment',
                               author_id=self.env.user.partner_id.id)

        for participante in self.message_partner_ids:
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[
            0]
        return action

    def action_negociacion_pg_aprobar_revision(self, ):
        self.sudo().estado_interno = 'aprobar_revision'
        self.pg_revisado = True
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])

        grupo_pg_ejecutor = self.env.ref(
            'sicpro_app_solicitudes.grupo_app_negocio_pg_ejecutor',
            raise_if_not_found=False)

        for items in iniciativa.sudo():
            items.estado_interno = 'aprobar_revision'
            usuarios_pg = self.env['res.users'].sudo().search([('id', 'in',
                                                                grupo_pg_ejecutor.user_ids.ids if grupo_pg_ejecutor else []),
                ('company_id', '=', items.company_id.id)])
            items.message_subscribe(partner_ids=usuarios_pg.partner_id.ids)

        self.message_post(body='Iniciativa revisada.',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        for participante in self.message_partner_ids:
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_negociacion_pg_action').sudo().read()[
            0]
        return action

    def action_negociacion_generar_id_solicitud(self, ):
        self.ensure_one()

        if not self.id_solicitud_creado:
            # Generamos el consecutivo usando la secuencia
            self.id_solicitud = self.env['ir.sequence'].next_by_code(
                'solicitudes_id_consecutivo_incrementar')
            self.id_solicitud_creado = True

            # Buscamos las sub-solicitudes usando sudo() para evitar conflictos de acceso
            data2 = self.env[
                'sicpro.app.solicitudes.oportunidades'].sudo().search(
                [('solicitud', '=', self.id), ])

            # OPTIMIZACIÓN ORM: Actualizamos todos los registros de una sola vez
            if data2:
                data2.write({'id_solicitud': self.id_solicitud,
                    'id_solicitud_creado': True})

    def action_negociacion_aprobar(self, ):
        self.fecha_aprobacion = fields.Date.context_today(self)
        self.sudo().estado_interno = 'aprobada'
        data1 = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])

        grupo_ejecutor_ejecutor = self.env.ref(
            'sicpro_app_solicitudes.grupo_app_ejecutor_ejecutor',
            raise_if_not_found=False)

        for items in data1.sudo():
            if items.departamento:
                items.estado_interno = 'aprobada'
                items.fecha_aprobacion = fields.Date.context_today(self)
            else:
                raise ValidationError('La especialidad: ' + str(
                    items.especialidad.name) + ', no tiene un departamento ejecutor asociado.' + MSG_SOPORTE_SICPRO)

            usuarios_ejecutor = self.env['res.users'].sudo().search([(
            'id', 'in',
            grupo_ejecutor_ejecutor.user_ids.ids if grupo_ejecutor_ejecutor else []),
                ('company_id', '=', items.company_id.id)])
            items.message_subscribe(
                partner_ids=usuarios_ejecutor.partner_id.ids)

            items.message_post(body='Iniciativa aprobada.',
                               message_type='notification',
                               subtype_xmlid='mail.mt_comment',
                               author_id=self.env.user.partner_id.id)
            for participante in items.message_partner_ids:
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                template.with_context(local_context).send_mail(items.id,
                                                               force_send=True,
                                                               email_values=email_values)
        self.action_negociacion_generar_id_solicitud()
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[
            0]
        return action

    def action_negociacion_restaurar_ejecutor(self, ):
        estado_rec = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_inicial', '=', True)], limit=1)
        estado = estado_rec.id

        self.fecha_aprobacion = fields.Date.context_today(self)
        self.sudo().tipo = 'subsolicitud'
        self.sudo().estado_interno = 'aprobada'
        self.sudo().stage_id = estado
        self.message_post(body='Iniciativa restaurada.',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        for participante in self.message_partner_ids:
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_negociacion_action').sudo().read()[
            0]
        return action

    oportunidad_id = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        string='Oportunidades')


class SolicitudesOportunidadesHorizontales(models.TransientModel):
    _name = 'sicpro.app.grupo.ejecutor.horizontal'
    _description = 'Grupo Ejecutor Solicitudes Horizontales'

    def _default_solicitud_id(self):
        active_ids = self.env.context.get('active_ids') or []
        return self.env['sicpro.app.solicitudes.oportunidades'].browse(
            active_ids)[:1]

    def _default_consecutivo_subsolicitud(self):
        active_ids = self.env.context.get('active_ids') or []
        solicitud_id = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            active_ids)[:1]
        if not solicitud_id:
            return ''

        # Si no tiene padre (solicitud es vacía), el padre original es el registro actual
        sol_id_original = solicitud_id.solicitud if solicitud_id.solicitud else solicitud_id

        # Buscamos de forma limpia sin operadores redundantes
        sol_id = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().search(
            [('active', '=', True), ('solicitud', '=', sol_id_original.id),
                ('solicitud_horizontal', '=', True)])

        consecutivos_sh = []
        for item in sol_id:
            if item.id_solicitud and '.' in item.id_solicitud:
                suffix = item.id_solicitud.split('.')[-1]
                if suffix.isdigit():
                    consecutivos_sh.append(int(suffix))

        consecutivos_max = max(consecutivos_sh) if consecutivos_sh else 0
        consecutivo = f"{sol_id_original.id_solicitud}.{consecutivos_max + 1}"
        return consecutivo

    id_solicitud = fields.Char(string='Solicitud ID', copy=False,
                               default=_default_consecutivo_subsolicitud)
    solicitud = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        string="Solicitud", default=_default_solicitud_id)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 related='solicitud.company_id', store=True)
    company_currency = fields.Many2one(string='Moneda',
                                       related='company_id.currency_id',
                                       readonly=True, )
    valor_sap_cup = fields.Monetary(string='Presupuesto',
                                    currency_field='company_currency',
                                    required=False)
    especialidad = fields.Many2one(
        comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
        domain="[('company_id', '=', company_id)]", required=True, )
    codigo_especialidad = fields.Integer(string="Código",
                                         related='especialidad.codigo',
                                         index=False)
    motivo_solicitud_horizontal = fields.Text(string='Motivo de Solicitud Horizontal',
                                              required=True)
    priority = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                index=True, default=PRIORIDADES_ACTIVAS[0][0])
    departamento = fields.Many2one('sicpro.app.trabajadores.areas',
                                   string="Departamento", required=True,
                                   domain="[('company_id', '=', company_id)]")
    tag_ids = fields.Many2many('sicpro.app.solicitudes.etiquetas',
                               'sicpro_app_solicitudes_horizotales_etiquetas_rel',
                               'lead_id', 'tag_id', string='Etiqueta')
    microlocalizacion = fields.Char(string='Micro Localización',
                                    required=False, default='N/P')
    enia = fields.Char(string='Estudio de la ENIA', required=False,
                       default='N/P')
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
    description = fields.Text(string='Notes', required=False, )
    solicitante_solicitud_horizontal = fields.Many2one('res.users',
                                                       string='Solicitante de Solicitud Horizontal',
                                                       index=True,
                                                       default=lambda
                                                           self: self.env.uid)

    def action_crear_solicitud_horizontal(self):
        oportunidad = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))[
                      :1]  # Slicing preventivo para evitar fallos de conjunto

        value = {'name': oportunidad.name,
                 'oportunidad_especialidad': oportunidad.oportunidad_especialidad.id,
                 'company_id': oportunidad.company_id.id,
                 'id_solicitud_creado': True,
                 'partner_id': oportunidad.partner_id.id,
                 'partner_name': oportunidad.partner_name,
                 'territorio_id': oportunidad.territorio_id.id,
                 'provincia_id': oportunidad.provincia_id.id,
                 'website': oportunidad.website, 'cargo': oportunidad.cargo,
                 'telefono_fijo': oportunidad.telefono_fijo,
                 'tipo': oportunidad.tipo,
                 'telefono_movil': oportunidad.telefono_movil,
                 'correo': oportunidad.correo,
                 'pagina_web': oportunidad.pagina_web,
                 'anio': oportunidad.anio,
                 'company_cliente': oportunidad.company_cliente.id,
                 'fecha_aprobacion': oportunidad.fecha_aprobacion,
                 'fecha_solicitud_trabajo': oportunidad.fecha_solicitud_trabajo,
                 'type': oportunidad.type,
                 'fecha_asignacion': oportunidad.fecha_asignacion,
                 'stage_id': oportunidad.stage_id.id,
                 'fecha_revision': oportunidad.fecha_revision,
                 'estado_interno': oportunidad.estado_interno,
                 'solicitud': oportunidad.solicitud.id,
                 'observaciones_grupo_ejecutor': oportunidad.observaciones_grupo_ejecutor,
                 'date_last_stage_update': oportunidad.date_last_stage_update,
                 'tipo_plan': oportunidad.tipo_plan,
                 'date_conversion': oportunidad.date_conversion,
                 'partner_address_name': oportunidad.partner_address_name,
                 'partner_address_email': oportunidad.partner_address_email,
                 'c_mep': oportunidad.c_mep,
                 'partner_address_phone': oportunidad.partner_address_phone,
                 'lugar_trabajo': oportunidad.lugar_trabajo,
                 'pestana_especialidades': oportunidad.pestana_especialidades,
                 'solicitud_horizontal': True,
                 'pep_corto': oportunidad.pep_corto,
                 'solicitante_solicitud_horizontal': self.solicitante_solicitud_horizontal.id,
                 'pep': "{}.{}".format(oportunidad.pep_corto,
                                       self.codigo_especialidad),
                 'id_solicitud': self.id_solicitud,
                 'company_currency': oportunidad.company_currency.id,
                 'valor_sap_cup': self.valor_sap_cup,
                 'especialidad': self.especialidad.id,
                 'codigo_especialidad': self.codigo_especialidad,
                 'motivo_solicitud_horizontal': self.motivo_solicitud_horizontal,
                 'priority': self.priority,
                 'departamento': self.departamento.id,
                 'tag_ids': [(6, 0, self.tag_ids.ids)],
                 'attachment_ids': [(6, 0, self.attachment_ids.ids)],
                 'microlocalizacion': self.microlocalizacion,
                 'enia': self.enia, 'ipf': self.ipf,
                 'ejecucion_proyecto': self.ejecucion_proyecto,
                 'consecutivo_proyecto': self.consecutivo_proyecto,
                 'ejecucion_tt': self.ejecucion_tt,
                 'codigo_tt': self.codigo_tt,
                 'datos_equipamiento_1': self.datos_equipamiento_1,
                 'datos_equipamiento_2': self.datos_equipamiento_2,
                 'datos_equipamiento_3': self.datos_equipamiento_3,
                 'datos_equipamiento_4': self.datos_equipamiento_4,
                 'datos_equipamiento_5': self.datos_equipamiento_5,
                 'datos_materiales_1': self.datos_materiales_1,
                 'datos_materiales_2': self.datos_materiales_2,
                 'datos_materiales_3': self.datos_materiales_3,
                 'datos_materiales_4': self.datos_materiales_4,
                 'description': self.description, }

        registro_nuevo = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().create(value)
        registro_nuevo.message_subscribe(
            partner_ids=oportunidad.message_partner_ids.ids)
        registro_nuevo.message_post(body='Solicitud Horizontal Creada.',
                                    message_type='notification',
                                    subtype_xmlid='mail.mt_comment',
                                    author_id=self.env.user.partner_id.id)

        for participante in registro_nuevo.message_partner_ids:
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_solicitudes.solicitudes_nueva_solicitud_horizontal')
            template.with_context(local_context).send_mail(registro_nuevo.id,
                                                           force_send=True,
                                                           email_values=email_values)
        action = self.env.ref(
            'sicpro_app_solicitudes.solicitudes_ejecutor_action').sudo().read()[
            0]
        return action