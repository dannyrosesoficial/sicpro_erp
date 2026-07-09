# -*- coding: utf-8 -*-

import base64
from datetime import datetime
from io import BytesIO
from random import randint

import qrcode
from pytz import timezone, UTC

from odoo import api
from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource
from odoo.tools import format_time


def _default_color():
    return randint(1, 11)


class TrabajadoresGeneral(models.Model):
    _name = 'sicpro.app.trabajadores'
    _description = "Trabajadores"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin', 'resource.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_trabajadores', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Nombre del trabajador", required="True", tracking=True, )
    trabajador_id = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Trabajador_id')
    company_id = fields.Many2one('res.company', string='Proceso', required=False)
    plaza_id = fields.Char(string="# Plaza", required=True, tracking=True, )
    inicio_contrato = fields.Date(string="Inicio del Contrato", required=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación", required=False)
    ubicacion_laboral = fields.Text(string="Ubicación Laboral", )
    active = fields.Boolean('Activo', default=True)
    direccion_privada = fields.Char(string="Dirección residencia", required=False, )
    direccion_carnet = fields.Char(string="Dirección CI", required=False, )
    correo_privado = fields.Char(string="Correo")
    raza = fields.Selection([('blanca', 'Blanca'), ('mestiza', 'Mestiza'), ('negra', 'Negra')], string="Raza",
                            tracking=True)
    genero = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino'), ], string="Género",
                              default="masculino", tracking=True)
    estado_civil = fields.Selection(
        [('soltero', 'Soltero'), ('casado', 'Casado'), ('cohabitante', 'Cohabitante Legal'), ('viudo', 'Viudo'),
         ('divorciado', 'Divorciado')], string='Estado civil', default='soltero', tracking=True)
    hijos = fields.Integer(string='Cantidad de Hijos', tracking=True)
    madre = fields.Char(string='Nombre de la Madre')
    padre = fields.Char(string='Nombre del Padre')
    fecha_nacimiento = fields.Date('Fecha de nacimiento', tracking=True)
    identification_id = fields.Char(string='Carnet de Identidad', tracking=True)
    pasaporte = fields.Char('No. Pasaporte', tracking=True)
    passport_expiry_date = fields.Date(string='Fecha Expiración', )
    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", )
    passport_attachment_id = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                              string="Adjunto")
    permiso_trabajo = fields.Char('No. Permiso', tracking=True)
    visa_no = fields.Char('No. Visado', tracking=True)
    visa_expira = fields.Date('Expiración de Visado', tracking=True)
    fecha_salida_pais = fields.Date('Fecha de Salida', tracking=True)
    fecha_regreso_pais = fields.Date('Fecha de Entrada', tracking=True)
    incorporacion_trabajo = fields.Date('Fecha Incorporación', tracking=True)
    fecha_baja = fields.Date('Fecha Baja', tracking=True)
    motivo_salida = fields.Text('Motivo de Salida', )
    nivel_escolar = fields.Selection(
        [('primaria', 'Primaria'), ('secundaria', 'Secundaria Básica'), ('sintitulo', 'Sin Título'),
         ('tecnico', 'Técnico Medio'), ('medio', 'Medio'), ('mediosuperior', 'Medio Superior'),
         ('superior', 'Superior'), ], 'Nivel Escolar', default='tecnico', tracking=True)
    estudio_titulo = fields.Char("Nombre del Título", tracking=True)
    estudio_graduacion = fields.Char("Año de Graduación", tracking=True)
    estudio_especialidad = fields.Char("Especialidad", tracking=True)
    emergencia_contacto = fields.Char("Nombre", tracking=True)
    emergencia_telefono = fields.Char("Teléfono E.", tracking=True)
    donante = fields.Selection(string='Donante', selection=[('si', 'Es Donante'), ('no', 'No es Donante'), ],
                               required=False, default='no')
    grupo_sanguineo = fields.Selection(string='Grupo Sanguíneo', required=False,
                                       selection=[('o_mas', 'Grupo: O+'), ('o_menos', 'Grupo: O-'),
                                                  ('a_mas', 'Grupo: A+'), ('a_menos', 'Grupo: A-'),
                                                  ('b_mas', 'Grupo: B+'), ('b_menos', 'Grupo: B-'),
                                                  ('ab_mas', 'Grupo: AB+'), ('ab_menos', 'Grupo: AB-'), ], )
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    telefono_privado = fields.Char(string="Teléfono P.")
    movil_privado = fields.Char(string="Móvil")
    clase_contrato = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', string='Clase de Contrato',
                                     domain="[('tipo', '=', 'contrato'),]", required=False)
    categoria_ocupacional = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', required=False,
                                            string='Categoría Ocupacional', domain="[('tipo', '=', 'ocupacional'),]", )
    notas = fields.Text('Notas')
    pin = fields.Char(string="ID Usuario", help="Identificador del usuario")
    telefono_trabajo = fields.Char('Teléfono Trabajo')
    movil_trabajo = fields.Char('Móvil Trabajo')
    correo_trabajo = fields.Char('Correo Trabajo')
    # sustituido debido a que no se actualizaba automáticamente el salario al cargar la página, se tendría q seleccionar
    # otra vez el cargo para que se calculara y como no se está poniendo salario extra pq el capacitador no agrega
    # las certificaciones se decide poner automático con un RELATED. También se cambió el formato del campo
    # importe = fields.Float(string="Salario", compute='_compute_salario', compute_sudo=True, store=True, )
    company_currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id',
                                          readonly=True)
    importe = fields.Monetary("Salario", related='ocupacion_id.salario', currency_field='company_currency_id')
    # fin del cambio en el campo de salario
    salario_extra = fields.Float("Salario extra", store=True, compute='_compute_salario_extra')
    estado_conexion = fields.Selection([('present', 'Conectado'), ('absent', 'Ausente'), ('to_define', 'Desconocido')],
                                       compute='_compute_presence_state', default='to_define')
    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP')
    user_partner_id = fields.Many2one(related='user_id.partner_id', related_sudo=False, string="Usuario")
    parent_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato')
    child_ids = fields.One2many('sicpro.app.trabajadores', 'parent_id', string='Directorio de subordinados')
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ocupacion_titulo = fields.Many2one(comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
                                       compute='_compute_ocupacion_titulo', compute_sudo=True, store=True, )
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento',
                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    centro_costo = fields.Many2one(comodel_name='sicpro.nomenclador.centro.costo', string='Centro Costo',
                                   related="area_id.centro_costo", store=True, )
    local_id = fields.Many2many('sicpro.nomenclador.locales', 'sicpro_app_trabajadores_local_rel', 'trabajador_id',
                                'local_id', string='local_id')
    local_cc = fields.Many2one(comodel_name="sicpro.nomenclador.locales", string="Local", required=False,
                               tracking=True, )
    resource_id = fields.Many2one('resource.resource')
    resource_calendar_id = fields.Many2one('resource.calendar',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    tz = fields.Selection(string='Zona horaria', related='resource_id.tz', store=True, readonly=False, )
    nexo_familiar_ids = fields.One2many('sicpro.app.trabajadores.nexo.familiar', 'trabajadores_id',
                                        string='Nexo Familiar', )
    documentos_count = fields.Integer(compute='_documentos_count', string='# Documentos')
    disciplina_count = fields.Integer(compute="_compute_disciplinaria_count")
    resume_line_ids = fields.One2many('sicpro.app.trabajadores.educacion', 'employee_id', string=" Registro educativo")
    employee_skill_ids = fields.One2many('sicpro.app.trabajadores.cursos', 'employee_id', string=" Cursos")
    job_title = fields.Char("Job Title", compute="_compute_job_title", store=True, readonly=False)
    subordinate_ids = fields.One2many('sicpro.app.trabajadores', string='Subordinados', compute='_compute_subordinates',
                                      compute_sudo=True)
    child_all_count = fields.Integer(string='Subordinados Indirectos Count', recursive=True,
                                     compute='_compute_subordinates', store=False, compute_sudo=True)
    equipo_tecnico_id = fields.Many2one("sicpro.app.trabajadores.equipo.tecnico", string="equipo_tecnico_id")
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    equipo_tecnico = fields.Many2one("sicpro.app.trabajadores.equipo.tecnico", string="Equipo Técnico",
                                     related='area_id.equipo_tecnico_id')
    miembros = fields.Many2one("sicpro.app.trabajadores", string="Miembros")
    edad = fields.Integer(string='Edad', required=False)
    grupo_capacitador = fields.Boolean(string='grupo_capacitador', compute='_compute_grupo_capacitador')
    grupo_seguridad_salud = fields.Boolean(string='grupo_seguridad_salud', compute='_compute_grupo_seguridad_salud')
    qr_code = fields.Binary("Código QR", required=False)
    vacunacion_ids = fields.One2many('sicpro.app.trabajadores.vacunacion', 'name', string=" Vacunación")
    intrucciones_ids = fields.One2many('sicpro.app.trabajadores.intrucciones', 'name', string=" Instrucciones")
    seguridad_ids = fields.One2many('sicpro.app.trabajadores.seguridad.trabajador', 'trabajador_id',
                                    string="Seguridad y Protección")
    seguridad_ocupacion = fields.Integer(string='SO', compute='compute_seguridad_ocupacion')
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    # _sql_constraints = [('plaza_ident_id_uniq',
    #                      'unique (plaza_id, identification_id)', '¡ERROR: El trabajador ya existe!'),
    #                     ]

    # verífico que no se repita el número de plaza del trabajador en el registro
    @api.constrains('plaza_id')
    def _check_plaza_id_unico(self):
        uniq = self.env['sicpro.app.trabajadores'].search(
            ['&', '&', ("active", "=", True), ("plaza_id", "=", self.plaza_id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El número de plaza del trabajador seleccionado, ya se encuentra registrado!. "
                                    "Si cree que es un error contacte al administrador"))

    # genera él, id del cargo del trabajador para utilizarlo en los medios de protección
    def compute_seguridad_ocupacion(self):
        self.seguridad_ocupacion = self.ocupacion_id.name

    # genera el código QR del trabajador
    def generate_hr_qr(self):
        if self.name and self.job_title:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(self.name)
            qr.add_data('\n')
            qr.add_data(self.job_title)
            qr.add_data('\n')
            qr.add_data('Plaza: ' + self.plaza_id)
            qr.add_data('\n')
            qr.add_data(self.sudo().company_id.name)
            qr.make()
            img = qr.make_image()
            tmp = BytesIO()
            img.save(tmp, format="PNG")
            qr_img = base64.b64encode(tmp.getvalue())
            self.qr_code = qr_img
        else:
            raise UserError(_('Chequear el nombre del trabajador y la ocupación'))

    # verífica qué el usuario activo pertenezca al grupo Responsable o al grupo Capacitador
    def _compute_grupo_capacitador(self):
        responsable = self.env['res.users'].has_group('sicpro_app_trabajadores.grupo_app_trabajador_responsable')
        if responsable:
            self.grupo_capacitador = False
        else:
            self.grupo_capacitador = self.env['res.users'].has_group(
                'sicpro_app_trabajadores.grupo_app_trabajador_capacitacion')

    # verifica q el usuario activo pertenezca al grupo Responsable o al grupo Seguridad y Salud
    def _compute_grupo_seguridad_salud(self):
        responsable = self.env['res.users'].has_group('sicpro_app_trabajadores.grupo_app_trabajador_responsable')
        if responsable:
            self.grupo_seguridad_salud = False
        else:
            self.grupo_seguridad_salud = self.env['res.users'].has_group(
                'sicpro_app_trabajadores.grupo_app_trabajador_seguridad_salud')

    # Procesa los subordinados del trabajador
    def _get_subordinates(self, parents=None):
        if not parents:
            parents = self.env[self._name]

        indirect_subordinates = self.env[self._name]
        parents |= self
        direct_subordinates = self.child_ids - parents
        for child in direct_subordinates:
            child_subordinate = child._get_subordinates(parents=parents)
            indirect_subordinates |= child_subordinate
        return indirect_subordinates | direct_subordinates

    # Cuenta los subordinados del trabajador
    @api.depends('child_ids', 'child_ids.child_all_count')
    def _compute_subordinates(self):
        for employee in self:
            employee.subordinate_ids = employee._get_subordinates()
            employee.child_all_count = len(employee.subordinate_ids)

    # Cuenta las medidas disciplinarias impuestas al trabajador
    def _compute_disciplinaria_count(self):
        all_actions = self.env['sicpro.app.trabajadores.disiplinaria.acciones'].read_group(
            [('trabajador_id', 'in', self.ids), ('estado', '=', 'action'), ], fields=['trabajador_id'],
            groupby=['trabajador_id'])
        mapping = dict([(action['trabajador_id'][0], action['trabajador_id_count']) for action in all_actions])
        for trabajador in self:
            trabajador.disciplina_count = mapping.get(trabajador.id, 0)

    # Abre la vista de los documentos de los trabajadores en el botón inteligente
    def disciplina_view(self):
        self.ensure_one()
        domain = [('trabajador_id', '=', self.id), ('estado', '=', 'action')]
        return {'name': _('Medidas Disciplinarias'), 'domain': domain,
            'res_model': 'sicpro.app.trabajadores.disiplinaria.acciones', 'type': 'ir.actions.act_window',
            'view_id': False, 'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">Click para crear una nueva medida disciplinaria </p>'''),
            'limit': 80, 'context': "{'default_trabajador_id': %s}" % self.id}

    # Cuenta los documentos de los trabajadores
    def _documentos_count(self):
        for each in self:
            documentos_ids = self.env['sicpro.app.trabajadores.documentos'].sudo().search(
                [('trabajadores_id', '=', each.id)])
            each.documentos_count = len(documentos_ids)

    # Abre la vista de los documentos de los trabajadores en el botón inteligente
    def documentos_view(self):
        self.ensure_one()
        domain = [('trabajadores_id', '=', self.id)]
        return {'name': _('Documentos'), 'domain': domain, 'res_model': 'sicpro.app.trabajadores.documentos',
            'type': 'ir.actions.act_window', 'view_id': False, 'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create"> Click para crear un nuevo documento </p>'''), 'limit': 80,
            'context': "{'default_trabajadores_id': %s}" % self.id}

    @api.onchange('donante')
    def _onchange_donante(self):
        if self.donante != 'si':
            self.grupo_sanguineo = None

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self.resource_calendar_id = self.company_id.resource_calendar_id
        else:
            self.resource_calendar_id = None

    @api.depends('ocupacion_id')
    def _compute_job_title(self):
        for trabajador in self.filtered('ocupacion_id'):
            trabajador.job_title = trabajador.ocupacion_id.name.name

    # agrega el nombre de la categoría ocupacional
    @api.depends('ocupacion_id')
    def _compute_ocupacion_titulo(self):
        for data in self:
            data.ocupacion_titulo = data.ocupacion_id

    @api.onchange('area_id')
    def _onchange_department(self):
        # Busco los id de los locales para enviarlos al formulario
        data = self.env['sicpro.app.trabajadores.areas'].search([('id', '=', self.area_id.id), ])
        self.local_id = data.local.ids
        # actualizo el usuario manager y departamento
        if self.area_id.manager_id:
            self.parent_id = self.area_id.manager_id

    # suma el total de salario extra
    @api.depends('resume_line_ids.pago')
    def _compute_salario_extra(self):
        for data in self:
            data.salario_extra = round(sum(data.resume_line_ids.mapped('pago')), 2)

    # devuelve el valor del salario completo (salario de la categoría ocupacional + salarios extras)
    @api.depends('ocupacion_id', 'salario_extra')
    def _compute_salario(self):
        for data in self:
            if data.ocupacion_id and data.salario_extra:
                data.importe = data.ocupacion_id.salario + data.salario_extra
            else:
                if data.ocupacion_id:
                    data.importe = data.ocupacion_id.salario
                else:
                    data.importe = 0.0

    # establece el estado de conexión del trabajador
    @api.depends('user_id.im_status')
    def _compute_presence_state(self):
        # Chequeo el login
        for data in self:
            estado = 'to_define'
            if data.user_id.im_status == 'online':
                estado = 'present'
            elif data.user_id.im_status == 'offline':
                estado = 'absent'
            data.estado_conexion = estado

    # establece el estado de la última conexión del trabajador
    @api.depends('user_id')
    def _compute_last_activity(self):
        presencia = self.env['bus.presence'].search_read([('user_id', 'in', self.mapped('user_id').ids)],
            ['user_id', 'last_presence'])

        presencia = {p['user_id'][0]: p['last_presence'] for p in presencia}

        for usuario in self:
            tz = usuario.tz
            last_presence = presencia.get(usuario.user_id.id, False)
            if last_presence:
                last_activity_datetime = last_presence.replace(tzinfo=UTC).astimezone(timezone(tz)).replace(tzinfo=None)
                usuario.last_activity = last_activity_datetime.date()

                if usuario.last_activity == fields.Date.context_today(self):
                    usuario.last_activity_time = format_time(self.env, last_activity_datetime, time_format='short')
                else:
                    usuario.last_activity_time = False
            else:
                usuario.last_activity = False
                usuario.last_activity_time = False

    @api.onchange('resource_calendar_id')
    def _onchange_timezone(self):
        self.tz = self.resource_calendar_id.tz

    # envío felicitación de cumpleaños vía correo
    def send_birthday_mail(self):
        local_context = self.env.context.copy()
        self.env.cr.execute("""select id from sicpro_app_trabajadores
                                WHERE 
                                    active = True
                                AND
                                    DATE_PART('day', fecha_nacimiento) = date_part('day', %s::date)
                                AND
                                    DATE_PART('month', fecha_nacimiento) = date_part('month', %s::date);""",
                            (datetime.now().date(), datetime.now().date()))
        birth_emps = self.env.cr.dictfetchall()
        if birth_emps:
            for emp in birth_emps:
                template = self.env.ref('sicpro_app_trabajadores.plantilla_felicitacion_cumpleaños')
                template.with_context(local_context).send_mail(emp['id'], force_send=True)

    # Descarga un archivo plantilla para importar datos de los trabajadores
    @api.model
    def get_import_templates(self):
        return [{'label': _('Importar plantillas para Trabajadores, XMLID: "# Plaza"'),
                 'template': '/sicpro_app_trabajadores/static/xlsx/trabajadores.xlsx'}]

    @api.model
    def create(self, vals):
        res = super(TrabajadoresGeneral, self).create(vals)
        # Género el código QR
        res.generate_hr_qr()
        return res

    def unlink(self):
        resources = self.mapped('resource_id')
        super(TrabajadoresGeneral, self).unlink()
        return resources.unlink()
