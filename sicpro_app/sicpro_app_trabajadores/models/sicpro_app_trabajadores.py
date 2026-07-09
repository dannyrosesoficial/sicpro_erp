# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models
from odoo.modules.module import get_module_resource
from ast import literal_eval
from odoo import api, fields, models
from pytz import timezone, UTC
from odoo.tools import format_time


class TrabajadoresLocales(models.Model):
    _name = 'sicpro.app.trabajadores.local'
    _description = 'Locales'

    name = fields.Char(string="Local", required=False, )
    locales_id = fields.Char(required=False, )


class TrabajadoresSalarioExtra(models.Model):
    _name = 'sicpro.app.trabajadores.salario'
    _description = 'Salario extra'

    name = fields.Monetary("Salario", currency_field='company_currency_id')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    descripcion = fields.Char(string='Descripción', required=True)
    trabajadores_ids = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general",
        string="Trabajadores", ondelete="cascade", required=True, )


class TrabajadoresGeneral(models.Model):
    _name = 'sicpro.app.trabajadores.general'
    _description = "Trabajadores"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin',
                'image.mixin']
    _mail_post_access = 'read'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_trabajadores',
                                         'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    name = fields.Char(string="Nombre del trabajador",
                       related='resource_id.name', store=True, readonly=False,
                       tracking=True)
    plaza_id = fields.Char(string="Número de Plaza", default="", required=True,
                           tracking=True, )
    inicio_contrato = fields.Date(string="Fecha Inicio del Contrato",
                                  required=False, )
    user_id = fields.Many2one('res.users', 'User',
                              related='resource_id.user_id', store=True,
                              readonly=False)
    user_partner_id = fields.Many2one(related='user_id.partner_id',
                                      related_sudo=False, string="Useruario")
    active = fields.Boolean('Active', related='resource_id.active',
                            default=True, store=True, readonly=False)
    address_home_id = fields.Char(string="Dirección privada", required=False, )
    private_email = fields.Char(string="Correo privado")
    raza = fields.Selection(
        [('blanca', 'Blanca'), ('mestiza', 'Mestiza'), ('negra', 'Negra')
         ], string="Raza", tracking=True)
    gender = fields.Selection(
        [('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')
         ], string="Sexo", default="masculino", tracking=True)
    marital = fields.Selection([('soltero', 'Soltero'), ('casado', 'Casado'),
                                ('cohabitante', 'Cohabitante Legal'),
                                ('viudo', 'Viudo'),
                                ('divorciado', 'Divorciado')],
                               string='Estado civil',
                               default='soltero', tracking=True)
    spouse_complete_name = fields.Char(string="Nombre completo del cónyuge",
                                       tracking=True)
    spouse_birthdate = fields.Date(string="Fecha de nacimiento del cónyuge",
                                   tracking=True)
    children = fields.Integer(string='Número de hijos', tracking=True)
    birthday = fields.Date('Fecha de nacimiento', tracking=True)
    ssnid = fields.Char('SSN No', help='Social Security Number', tracking=True)
    sinid = fields.Char('SIN No', help='Social Insurance Number',
                        tracking=True)
    identification_id = fields.Char(string='Carnet de identidad',
                                    tracking=True)
    passport_id = fields.Char('No. Pasaporte', tracking=True)
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Cuenta Bancaria',
        domain="[('partner_id', '=', address_home_id), '|', "
               "('company_id', '=', False), "
               "('company_id', '=', company_id)]",
        tracking=True, help='Cuenta bancaria para el salario del trabajador')
    permit_no = fields.Char('Número de permiso de trabajo', tracking=True)
    visa_no = fields.Char('Número de Visado', tracking=True)
    visa_expire = fields.Date('Fecha expiración visado', tracking=True)
    additional_note = fields.Text(string='Notas adicionales', tracking=True)
    certificate = fields.Selection(
        [('primaria', 'Primaria'), ('secundaria', 'Secundaria Básica'),
         ('sintitulo', 'Sin Titulo'), ('tecnico', 'Técnico Medio'),
         ('medio', 'Medio'),
         ('mediosuperior', 'Medio Superior'), ('superior', 'Superior'),
         ], 'Nivel de Escolar', default='tecnico', tracking=True)
    study_field = fields.Char("Nombre del Título", tracking=True)
    study_school = fields.Char("Año de Graduación", tracking=True)
    study_especialidad = fields.Char("Especialidad", tracking=True)
    emergency_contact = fields.Char("Contacto de Emergéncia", tracking=True)
    emergency_phone = fields.Char("Teléfono de Emergéncia", tracking=True)

    centro_costo_usd = fields.Many2one(
        comodel_name='sicpro.nomenclador.centro.costo',
        string='Centro Costo USD',
        related="department_id.centro_costo_usd", store=True, )
    centro_costo_cup = fields.Char('Centro Costo CUP',
                                   related="department_id.centro_costo_cup",
                                   store=True, )
    local_id = fields.Many2many(
        'sicpro.nomenclador.locales', 'sicpro_app_trabajadores_local_rel',
        'trabajador_id', 'local_id', string='local_id')
    local_cc = fields.Many2one(
        comodel_name="sicpro.nomenclador.locales",
        string="Local", required=True, tracking=True, )

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920,
                              default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    phone = fields.Char(string="Teléfono privado")
    movil = fields.Char(string="Móvil privado")
    child_ids = fields.One2many('sicpro.app.trabajadores.general', 'parent_id',
                                string='Directorio de subordinados')
    category_ids = fields.Many2many('sicpro.app.trabajadores.categorias',
                                    'sicpro_app_trabajadores_categorias_rel',
                                    'emp_id', 'category_id',
                                    string='Categorías')
    notes = fields.Text('Notas')
    color = fields.Integer('Color Index', default=0)
    pin = fields.Char(string="ID Usuario", help="Identificador del usuario")
    departure_reason = fields.Selection(
        [('fired', 'Fired'), ('resigned', 'Resigned'), ('retired', 'Retired')],
        string="Departure Reason", copy=False, tracking=True)
    departure_description = fields.Text(string="Additional Information",
                                        copy=False, tracking=True)
    message_main_attachment_id = fields.Many2one()
    color = fields.Integer('Color Index', default=0)
    department_id = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                    'Departamento',
                                    domain="['|', ('company_id', '=', False), "
                                           "('company_id', '=', company_id)]")
    job_id = fields.Many2one('sicpro.app.trabajadores.trabajos',
                             'Puesto de trabajo',
                             domain="['|', ('company_id', '=', False), "
                                    "('company_id', '=', company_id)]")
    job_title = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.trabajos',
        string="Cargo", compute='_compute_job_title',
        compute_sudo=True, store=True, )
    company_id = fields.Many2one('res.company', 'Proceso')
    address_id = fields.Many2one('res.partner', 'Dirección de trabajo',
                                 domain="['|', ('company_id', '=', False), "
                                        "('company_id', '=', company_id)]")
    work_phone = fields.Char('Teléfono trabajo')
    mobile_phone = fields.Char('Móvil del trabajo')
    work_email = fields.Char('Correo-e del trabajo')
    importe = fields.Float(string="Salario", compute='_compute_salario',
                           compute_sudo=True, store=True, )
    salario_ids = fields.One2many(
        comodel_name="sicpro.app.trabajadores.salario",
        inverse_name="trabajadores_ids", string="Salario Extra", )
    salario_extra = fields.Float("Salario extra",
                                 compute='_compute_salario_extra',
                                 store=True, )
    user_id = fields.Many2one('res.users')
    resource_id = fields.Many2one('resource.resource')
    resource_calendar_id = fields.Many2one(
        'resource.calendar', domain="['|', ('company_id', '=', False), "
                                    "('company_id', '=', company_id)]")
    parent_id = fields.Many2one('sicpro.app.trabajadores.general',
                                'Jefe Inmediato',
                                domain="['|', ('company_id', '=', False), "
                                       "('company_id', '=', company_id)]")
    coach_id = fields.Many2one('sicpro.app.trabajadores.general', 'Monitor',
                               domain="['|', ('company_id', '=', False), "
                                      "('company_id', '=', company_id)]")
    tz = fields.Selection(
        string='Zona horaria', related='resource_id.tz', readonly=False,
        help="This field is used in order to define in which "
             "timezone the resources will work.")
    hr_presence_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('to_define', 'To Define')], compute='_compute_presence_state',
        default='to_define')
    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        manager = self.parent_id
        previous_manager = self._origin.parent_id
        if manager and (
                self.coach_id == previous_manager or not self.coach_id):
            self.coach_id = manager
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'jefe_id': self.parent_id})

    @api.onchange('work_phone')
    def _onchange_work_phone(self):
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'work_phone': self.work_phone})

    @api.onchange('mobile_phone')
    def _onchange_mobile_phone(self):
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'mobile_phone': self.mobile_phone})

    @api.onchange('plaza_id')
    def _onchange_plaza_id(self):
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'plaza_id': self.plaza_id})

    @api.onchange('identification_id')
    def _onchange_identification_id(self):
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'identification_id': self.identification_id})

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            self.env['res.users'].search(
                [('id', '=', self.user_id.id)]).update({'job_id': self.job_id})

    # agrega el nombre de la categoria ocupacional
    @api.depends('job_id')
    def _compute_job_title(self):
        for data in self:
            data.job_title = data.job_id

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('department_id')
    def _onchange_department(self):
        # Busco los id de los locales para enviarlos al formulario
        data = self.env['sicpro.app.trabajadores.departmentos'].search(
            [('id', '=', self.department_id.id), ])
        self.local_id = data.local.ids
        # actualizo el usuario manager y departamento
        if self.department_id.manager_id:
            self.parent_id = self.department_id.manager_id
        self.env['res.users'].search([('id', '=', self.user_id.id)]).update(
            {'departamento': self.department_id})

    @api.onchange('resource_calendar_id')
    def _onchange_timezone(self):
        if self.resource_calendar_id and not self.tz:
            self.tz = self.resource_calendar_id.tz

    # suma el total de salario extra
    @api.depends('salario_ids.name')
    def _compute_salario_extra(self):
        for data in self:
            data.salario_extra = round(sum(data.salario_ids.mapped('name')), 2)

    # devuelve el valor del salario completo
    # (salario de la categoría ocupacional + salarios extras)
    @api.depends('job_id', 'salario_extra')
    def _compute_salario(self):
        for data in self:
            if data.job_id and data.salario_extra:
                data.importe = data.job_id.salario + data.salario_extra
            else:
                if data.job_id:
                    data.importe = data.job_id.salario
                else:
                    data.importe = 0.0

    ''' codigo para mensajes en el chart
    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals['user_id'])
            vals.update(self._sync_user(user))
            vals['name'] = vals.get('name', user.name)
        employee = super(TrabajadoresGeneral, self).create(vals)
        url = '/web#%s' % url_encode(
            {'action': 'hr.plan_wizard_action', 'active_id': employee.id, 
            'active_model': 'hr.employee'})
        employee._message_log(
            body=_('<b>Congratulations!</b> May I recommend you to setup an 
            <a href="%s">onboarding plan?</a>') % (url))
        if employee.department_id:
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', employee.department_id.id)
            ])._subscribe_users()
        return employee'''

    def unlink(self):
        resources = self.mapped('resource_id')
        super(TrabajadoresGeneral, self).unlink()
        return resources.unlink()

    @api.depends('user_id.im_status')
    def _compute_presence_state(self):
        # Chequeo el login
        check_login = literal_eval(
            self.env['ir.config_parameter'].sudo().get_param(
                'hr.hr_presence_control_login', 'False'))
        for employee in self:
            state = 'to_define'
            if check_login:
                if employee.user_id.im_status == 'online':
                    state = 'present'
                elif employee.user_id.im_status == 'offline':
                    state = 'absent'
            employee.hr_presence_state = state

    @api.depends('user_id')
    def _compute_last_activity(self):
        presences = self.env['bus.presence'].search_read(
            [('user_id', 'in', self.mapped('user_id').ids)],
            ['user_id', 'last_presence'])
        # transform the result to a dict with this format {user.id:
        # last_presence}
        presences = {p['user_id'][0]: p['last_presence'] for p in presences}

        for employee in self:
            tz = employee.tz
            last_presence = presences.get(employee.user_id.id, False)
            if last_presence:
                last_activity_datetime = last_presence.replace(
                    tzinfo=UTC).astimezone(timezone(tz)).replace(tzinfo=None)
                employee.last_activity = last_activity_datetime.date()
                if employee.last_activity == fields.Date.today():
                    employee.last_activity_time = format_time(
                        self.env, last_activity_datetime, time_format='short')
                else:
                    employee.last_activity_time = False
            else:
                employee.last_activity = False
                employee.last_activity_time = False

    '''
    # ---------------------------------------------------------
    # Messaging
    # ---------------------------------------------------------

   def _message_log(self, **kwargs):
        return super(TrabajadoresGeneral, self._post_author())._message_log(**kwargs)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        return super(TrabajadoresGeneral, self._post_author()).message_post(**kwargs)

    def _sms_get_partner_fields(self):
        return ['user_partner_id']

    def _sms_get_number_fields(self):
        return ['mobile_phone']'''
