# -*- coding: utf-8 -*-

from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import UserError
from odoo.fields import Datetime

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class SolicitudesOportunidades(models.Model):
    _name = 'sicpro.app.solicitudes.oportunidades'
    _description = "Solicitudes y oportunidades"
    _order = 'priority desc, id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # agrego el cliente por defecto
    def _default_partner_id(self):
        users_id = self.env.user.user_inversionista
        if users_id:
            data = self.env['sicpro.app.clientes'].search(
                [('user_id', '=', self.env.user.id), ])
            valor = data.id
            return valor
        else:
            return

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.solicitudes.estados'].search([], limit=1)

    name = fields.Char(string="Oportunidad", required=True, index=True)
    id_solicitud = fields.Char(string='Id. de la Solicitud', tracking=True,
                               readonly=True, store=True)
    partner_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 tracking=10, index=True,
                                 domain=[('tipo_registro', '=', 'persona')],
                                 default=lambda self: self._default_partner_id(),
                                 help="Linked partner (optional). Usually created when converting the lead. You can "
                                      "find a partner by its Name, TIN, Email or Internal Reference.")
    partner_name = fields.Char("Nombre de la entidad", required=True,
                               help='The name of the future partner company '
                                    'that will be created while converting the '
                                    'lead into opportunity')
    territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="Territorio",
        required=True, )
    provincia_id = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                   string="Provincia", required=True)
    website = fields.Char('Sitio Web', help="Website of the contact")
    cargo = fields.Char(string="Cargo", required=False, tracking=True, )
    telefono_fijo = fields.Char(string="Teléfono", required=False,
                                tracking=True, )
    telefono_movil = fields.Char(string="Móvil", required=False,
                                 tracking=True, )
    correo = fields.Char(string="Correo electrónico", required=False,
                         tracking=True, )
    pagina_web = fields.Char(string="Pagina Web", required=False,
                             tracking=True, )
    active = fields.Boolean('Activo', default=True, tracking=True)
    color = fields.Integer('Indice de colores', default=0)
    team_id = fields.Many2one('sicpro.app.solicitudes.grupo.ejecutor',
                              string='Grupo Ejecutor', index=True,
                              tracking=True,
                              help='When sending mails, the default email '
                                   'address is taken from the Sales Team.')
    jefe_grupo = fields.Many2one(comodel_name="sicpro.app.trabajadores.general",
                                 string='Líder del grupo',
                                 related="team_id.jefe_grupo", required=False,
                                 store=True, tracking=True)
    especialista_ejecutor = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general", string='Asignar a',
                                            tracking=True)
    cargo_especialista = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.trabajos", string='Cargo',
        related="especialista_ejecutor.job_id", store=True)
    description = fields.Text('Notes', required=False, tracking=True)
    observaciones_grupo_ejecutor = fields.Text('observaciones', required=False,
                                               tracking=True)
    tag_ids = fields.Many2many('sicpro.app.solicitudes.etiquetas',
                               'sicpro_app_solicitudes_iniciativas_etiquetas_rel',
                               'lead_id', 'tag_id', string='Etiqueta',
                               tracking=True,
                               help="Classify and analyze your lead/opportunity "
                                    "categories like: Training, Service")
    priority = fields.Selection(Prioridades_Activas, string='Prioridad',
                                index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", required=False,
                                   related='especialidad.departamento',
                                   store=True, readonly=True)
    company_cliente = fields.Many2one('res.company',
                                      string='Proceso del Cliente', index=True,
                                      readonly=True,
                                      default=lambda self: self.env.company.id)
    fecha_solicitud = fields.Date('Fecha de solicitud', readonly=True,
                                  default=fields.Datetime.now,
                                  help="Fecha en que realiza la solicitud el cliente")
    anio = fields.Char(string="Año", required=False,
                       default=fields.datetime.today().strftime("%Y"), )
    fecha_aprobacion = fields.Date('Fecha de aprobación', readonly=True,
                                   help="Fecha en que se aprueba la solicitud del cliente")
    fecha_asignacion = fields.Date('Fecha de asignación', readonly=True,
                                   help="Fecha en que realiza la asignacion de la solicitud al grupo ejecutor")
    pep_corto = fields.Char(string='Número SAP', size=10,
                            required=True, index=True)
    ejecucion_proyecto = fields.Boolean(string="Proyecto", tracking=True)
    consecutivo_proyecto = fields.Char(string="Consecutivo", required=False, )
    adjunto_proyecto = fields.Binary(string="Adjunto Proyecto",
                                     attachment=False)
    ejecucion_tt = fields.Boolean(string="Tarea Técnica", tracking=True)
    codigo_tt = fields.Char(string="Código TT", required=False, )
    adjunto_tt = fields.Binary(string="Adjunto TT", attachment=False)
    datos_equipamiento_1 = fields.Boolean(string="En Espera llegada a Cuba", )
    datos_equipamiento_2 = fields.Boolean(string="En Almacén de ETECSA", )
    datos_equipamiento_3 = fields.Boolean(string="En Almacén de Terceros", )
    datos_equipamiento_4 = fields.Boolean(string="En el lugar de Ejecución", )
    datos_equipamiento_5 = fields.Boolean(string="No Procede", )
    datos_materiales_1 = fields.Boolean(string="Con Reserva SAP", )
    datos_materiales_2 = fields.Boolean(string="Pdte por Reservar", )
    datos_materiales_3 = fields.Boolean(string="Por el Ejecutor", )
    datos_materiales_4 = fields.Boolean(string="No Procede", )
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,
                                       relation="res.currency")
    valor_sap_cup = fields.Monetary('Presupuesto CUP',
                                    currency_field='company_currency',
                                    tracking=True)
    valor_sap_cuc = fields.Monetary('Presupuesto CUC',
                                    currency_field='company_currency',
                                    tracking=True)
    valor_sap_total = fields.Monetary('Presupuesto Total',
                                      currency_field='company_currency',
                                      compute='_compute_valor_sap_total',
                                      store=True)
    stage_id = fields.Many2one('sicpro.app.solicitudes.estados',
                               string='Estados', ondelete='restrict',
                               tracking=True,
                               group_expand='_read_group_stage_ids',
                               index=True, copy=False,
                               default=_get_default_stage_id)
    type = fields.Selection([('iniciativa', 'Iniciativa'),
                             ('oportunidad', 'Oportunidad')], index=True,
                            required=True,
                            tracking=15,
                            default=lambda self: 'iniciativa',
                            help="Type is used to separate Leads and Opportunities")
    estado_interno = fields.Selection([('nuevo', 'Nuevo'),
                                       ('liberada', 'Liberada'),
                                       ('aprobada', 'Aprobada'),
                                       ('cancelada_cliente', 'Cancelada'),
                                       ('cancelada_ejecutor', 'Cancelada'),
                                       ('rechazada_dtp', 'Rechazada DTP'),
                                       ('rechazada_ejecutor', 'Rechazada Ejecutor'),
                                       ('rechazada_agrupacion', 'Rechazada Agrupacion'),
                                       ('oportunidad', 'Oportunidad')],
                                      index=True, required=True, tracking=15,
                                      default=lambda self: 'nuevo')
    tipo = fields.Selection([('principal', 'Principal'),
                             ('subsolicitud', 'Subsolicitud')], index=True,
                            required=True,
                            tracking=15, default=lambda self: 'principal',
                            help="Determina si es una solicitud principal o una subsolicitud")
    pep = fields.Char(string='Sap', required=False)
    solicitud = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        string="Solicitud", required=False, )
    hijos_ids = fields.One2many(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        inverse_name="solicitud", string="Especialidad", required=False, )
    especialidad = fields.Many2one(
        comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
        domain="[('company_id', '=', company_id)]", required=False, )
    codigo_especialidad = fields.Integer(string="Código",
                                         related='especialidad.codigo',
                                         index=False)
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", related='especialidad.image_1920',
                              max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920",
                             max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920",
                             max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920",
                             max_width=128, max_height=128, store=True)
    motivo_rechazo = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     string='Motivo de Rechazo', tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     tracking=True)

    user_id = fields.Many2one('res.users', string='Gestor de la Solicitud',
                              index=True, tracking=True, )
    meeting_count = fields.Integer('# Meetings',
                                   compute='_compute_meeting_count')
    dias_aprobar = fields.Float(compute='_compute_dias_aprobar',
                                string='Días en aprobar', store=True)
    dias_asignar = fields.Float(compute='_compute_dias_asignar',
                                string='Dias en asignar', store=True)

    date_last_stage_update = fields.Datetime(string='Last Stage Update',
                                             index=True, default=fields.Datetime.now)
    date_conversion = fields.Datetime('Conversion Date', readonly=True)
    partner_address_name = fields.Char('Partner Contact Name', readonly=True)
    partner_address_email = fields.Char('Partner Contact Email', readonly=True)
    partner_address_phone = fields.Char('Partner Contact Phone', readonly=True)
    user_email = fields.Char('User Email', related='user_id.email',
                             readonly=True)
    user_login = fields.Char('User Login', related='user_id.login',
                             readonly=True)
    temporal_1 = fields.Boolean(default=False)  # control del campo stage_id
    temporal_2 = fields.Boolean(default=False)  # control del campo especialista_ejecutor

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # calcula el presupuesto total
    @api.depends('valor_sap_total')
    def _compute_valor_sap_total(self):
        if self.valor_sap_cuc > 0 and self.valor_sap_cup > 0:
            valor = self.valor_sap_cuc + self.valor_sap_cup
        return valor

    # calcula total de dias entre las fecha de solicitud y aprobacion
    @api.depends('dias_aprobar')
    def _compute_dias_aprobar(self):
        leads = self.filtered(lambda l: l.fecha_solicitud and l.fecha_aprobacion)
        others = self - leads
        others.dias_aprobar = None
        for lead in leads:
            fecha_solicitud = fields.Datetime.from_string(lead.fecha_solicitud)
            fecha_aprobacion = fields.Datetime.from_string(lead.fecha_aprobacion)
            lead.dias_aprobar = abs((fecha_aprobacion - fecha_solicitud).days)

    # calcula total de dias entre las fecha de aprobacion y asignacion
    @api.depends('dias_asignar')
    def _compute_dias_asignar(self):
        leads = self.filtered(lambda l: l.fecha_aprobacion and l.fecha_asignacion)
        others = self - leads
        others.day_close = None
        for lead in leads:
            fecha_asignacion = fields.Datetime.from_string(lead.fecha_asignacion)
            fecha_aprobacion = fields.Datetime.from_string(lead.fecha_aprobacion)
            lead.dias_asignar = abs((fecha_asignacion - fecha_aprobacion).days)

    # accion al cambiar el grupo ejecutor
    @api.onchange('team_id')
    def _onchange_team_id(self, ):
        self.especialista_ejecutor = None
        self.stage_id = 1

    # accion al cambiar el el estado
    @api.onchange('stage_id')
    def _onchange_stage_id(self, ):
        self.temporal_1 = True

    # accion al cambiar el especialista ejecutor
    # accion agregar especialista seguidor y notificacion
    @api.onchange('especialista_ejecutor')
    def _onchange_especialista_ejecutor(self, ):
        if self.especialista_ejecutor:
            self.temporal_2 = True
            self.stage_id = 2
        else:
            self.temporal_2 = False
            self.stage_id = 1

    # accion al cambiar el cliente
    @api.onchange('partner_id')
    def _onchange_partner_id(self, ):
        data = self.env['sicpro.app.clientes'].search(
            [('id', '=', self.partner_id.id), ])
        self.partner_name = data.entidad.name
        self.territorio_id = data.territorio.id
        self.provincia_id = data.provincia.id
        self.website = data.entidad.pagina_web
        self.cargo = data.cargo
        self.telefono_fijo = data.telefono_fijo
        self.telefono_movil = data.telefono_movil
        self.correo = data.correo
        self.pagina_web = data.pagina_web

    # accion al cambiar la especialidad
    @api.onchange('especialidad')
    def _onchange_especialidad(self, ):
        if self.especialidad:
            self.pep = "{}.{}".format(self.pep_corto, self.codigo_especialidad)
        else:
            self.pep = "-"

    # accion del boton de Archivar Subsolicitud
    def action_archivar_subsolicitud(self, ):
        self.active = False

    # accion del boton de desarchivar Subsolicitud
    def action_desarchivar_subsolicitud(self, ):
        self.active = True

    # accion para llamar a las actividades en el calendario
    # del formulario oportunidades
    def action_calendario_oportunidades(self):
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        action['context'] = {
            'default_opportunity_id': self.id if self.type == 'oportunidad'
            else False,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            'default_name': self.name,
        }
        return action

    # accion para contar las actividades en el boton calendario del formulario oportunidades
    def _compute_meeting_count(self):
        meeting_data = self.env['calendar.event'].read_group([
            ('opportunity_id', 'in', self.ids)], ['opportunity_id'],
            ['opportunity_id'])
        mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count']
                       for m in meeting_data}
        for lead in self:
            lead.meeting_count = mapped_data.get(lead.id, 0)

    def unlink(self):
        data = self.env['sicpro.app.solicitudes.oportunidades'].search([
            ('solicitud', '=', self.id), ])
        for items in data:
            items.unlink()
        return super(SolicitudesOportunidades, self).unlink()

    def write(self, data):
        res = super(SolicitudesOportunidades, self).write(data)
        # activo o desactivo las subsolicitudes
        if self.active:
            data = self.env['sicpro.app.solicitudes.oportunidades'].search([
                ('solicitud', '=', self.id), ('active', '=', False)])
            for items in data:
                items.active = self.active
        else:
            data = self.env['sicpro.app.solicitudes.oportunidades'].search([
                ('solicitud', '=', self.id), ])
            for items in data:
                items.active = self.active

        # envio notificacion al cambiar el estado
        if self.temporal_1:
            self.temporal_1 = False
            if 'stage_id' in data:
                self.message_post(
                    body='La oportunidad cambio de estado.',
                    message_type='notification',
                    subtype='mail.mt_comment',
                    author_id=self.env.user.partner_id.id
                )

        # envio notificacion al cambiar el especialista_ejecutor
        if self.temporal_2:
            self.temporal_2 = False
            if 'especialista_ejecutor' in data:
                self.message_subscribe(
                    partner_ids=self.especialista_ejecutor.user_id.partner_id.ids)
                self.message_post(
                    body='oportunidad asignada.',
                    message_type='notification',
                    subtype='mail.mt_comment',
                    author_id=self.env.user.partner_id.id
                )

        return res
