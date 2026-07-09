# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
from datetime import datetime
from io import BytesIO
from random import randint
import qrcode
from pytz import timezone, UTC
from odoo import api
from odoo import models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_time
from odoo.tools.misc import file_open


def _default_color():
    return randint(1, 11)


class TrabajadoresGeneral(models.Model):
    _name = 'sicpro.app.trabajadores'
    _description = "Trabajadores"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin',
                'resource.mixin']

    @api.model
    def _default_image(self):
        with file_open(
            'sicpro_app_trabajadores/static/src/img/default_image.png',
            'rb') as f:
            return base64.b64encode(f.read())

    name = fields.Char(string="Nombre del trabajador", required=True,
                       tracking=True, )
    trabajador_id = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                                    string='id del Trabajador')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=False)
    plaza_id = fields.Char(string="# Plaza", required=True, tracking=True, )
    inicio_contrato = fields.Date(string="Inicio del Contrato", required=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación",
                                      required=False)
    ubicacion_laboral = fields.Text(string="Ubicación Laboral", )
    active = fields.Boolean(string='Activo', default=True, index=True)
    direccion_privada = fields.Char(string="Dirección residencia",
                                    required=False, )
    direccion_carnet = fields.Char(string="Dirección CI", required=False, )
    correo_privado = fields.Char(string="Correo")
    raza = fields.Selection(
        [('blanca', 'Blanca'), ('mestiza', 'Mestiza'), ('negra', 'Negra')],
        string="Raza", tracking=True)
    genero = fields.Selection(
        [('masculino', 'Masculino'), ('femenino', 'Femenino'), ],
        string="Género", default="masculino", tracking=True)
    estado_civil = fields.Selection(
        [('soltero', 'Soltero'), ('casado', 'Casado'),
         ('cohabitante', 'Cohabitante Legal'), ('viudo', 'Viudo'),
         ('divorciado', 'Divorciado')], string='Estado civil',
        default='soltero', tracking=True)
    hijos = fields.Integer(string='Cantidad de Hijos', tracking=True)
    madre = fields.Char(string='Nombre de la Madre')
    padre = fields.Char(string='Nombre del Padre')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento', tracking=True)
    identification_id = fields.Char(string='Carnet de Identidad',
                                    tracking=True,
                                    help="Número de identidad de 11 dígitos")
    pasaporte = fields.Char(string='No. Pasaporte', tracking=True)
    passport_expiry_date = fields.Date(string='Fecha Expiración', )
    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel',
                                        'id_ref', 'attach_ref',
                                        string="Attachment", )
    passport_attachment_id = fields.Many2many('ir.attachment',
                                              'passport_attachment_rel',
                                              'passport_ref', 'attach_ref1',
                                              string="Adjunto")
    permiso_trabajo = fields.Char(string='No. Permiso', tracking=True)
    visa_no = fields.Char(string='No. Visado', tracking=True)
    visa_expira = fields.Date(string='Expiración de Visado', tracking=True)
    fecha_salida_pais = fields.Date(string='Fecha de Salida', tracking=True)
    fecha_regreso_pais = fields.Date(string='Fecha de Entrada', tracking=True)
    incorporacion_trabajo = fields.Date(string='Fecha Incorporación', tracking=True)
    fecha_baja = fields.Date(string='Fecha Baja', tracking=True)
    motivo_salida = fields.Text(string='Motivo de Salida', )
    nivel_escolar = fields.Selection(
        [('primaria', 'Primaria'), ('secundaria', 'Secundaria Básica'),
         ('sintitulo', 'Sin Título'), ('tecnico', 'Técnico Medio'),
         ('medio', 'Medio'), ('mediosuperior', 'Medio Superior'),
         ('superior', 'Superior'), ], 'Nivel Escolar', default='tecnico',
        tracking=True)
    estudio_titulo = fields.Char(string="Nombre del Título", tracking=True)
    estudio_graduacion = fields.Char(string="Año de Graduación", tracking=True)
    estudio_especialidad = fields.Char(string="Especialidad", tracking=True)
    emergencia_contacto = fields.Char(string="Nombre", tracking=True)
    emergencia_telefono = fields.Char(string="Teléfono E.", tracking=True)
    donante = fields.Selection(string='Donante',
                               selection=[('si', 'Es Donante'),
                                          ('no', 'No es Donante'), ],
                               required=False, default='no')
    grupo_sanguineo = fields.Selection(string='Grupo Sanguíneo',
                                       required=False,
                                       selection=[('o_mas', 'Grupo: O+'),
                                                  ('o_menos', 'Grupo: O-'),
                                                  ('a_mas', 'Grupo: A+'),
                                                  ('a_menos', 'Grupo: A-'),
                                                  ('b_mas', 'Grupo: B+'),
                                                  ('b_menos', 'Grupo: B-'),
                                                  ('ab_mas', 'Grupo: AB+'), (
                                                  'ab_menos',
                                                  'Grupo: AB-'), ], )
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
    telefono_privado = fields.Char(string="Teléfono P.")
    movil_privado = fields.Char(string="Móvil")
    clase_contrato = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias',
        string='Clase de Contrato', domain="[('tipo', '=', 'contrato'),]",
        required=False)
    categoria_ocupacional = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias', required=False,
        string='Categoría Ocupacional',
        domain="[('tipo', '=', 'ocupacional'),]", )
    notas = fields.Text(string='Notas')
    pin = fields.Char(string="ID Usuario", help="Identificador del usuario")
    telefono_trabajo = fields.Char(string='Teléfono Trabajo')
    movil_trabajo = fields.Char(string='Móvil Trabajo')
    correo_trabajo = fields.Char(string='Correo Trabajo')
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    importe = fields.Monetary(string="Salario", related='ocupacion_id.salario',
                              currency_field='company_currency_id')
    salario_extra = fields.Float(string="Salario extra", store=True,
                                 compute='_compute_salario_extra')
    estado_conexion = fields.Selection(
        [('present', 'Conectado'), ('absent', 'Ausente'),
         ('to_define', 'Desconocido')], compute='_compute_presence_state',
        default='to_define')
    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")
    user_id = fields.Many2one('res.users', string='Usuario SICPRO ERP')
    user_partner_id = fields.Many2one(related='user_id.partner_id',
                                      related_sudo=False, string="Usuario")
    parent_id = fields.Many2one('sicpro.app.trabajadores', string='Jefe Inmediato')
    child_ids = fields.One2many('sicpro.app.trabajadores', 'parent_id',
                                string='Directorio de subordinados')
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   string='Puesto de trabajo',
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ocupacion_titulo = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
        compute='_compute_ocupacion_titulo', compute_sudo=True, store=True, )
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', string='Departamento',
                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    centro_costo = fields.Many2one(
        comodel_name='sicpro.nomenclador.centro.costo', string='Centro Costo',
        related="area_id.centro_costo", store=True, )
    local_id = fields.Many2many('sicpro.nomenclador.locales',
                                'sicpro_app_trabajadores_local_rel',
                                'trabajador_id', 'local_id', string='local_id')
    local_cc = fields.Many2one(comodel_name="sicpro.nomenclador.locales",
                               string="Local", required=False, tracking=True, )
    resource_id = fields.Many2one('resource.resource')
    resource_calendar_id = fields.Many2one('resource.calendar',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    tz = fields.Selection(string='Zona horaria', related='resource_id.tz',
                          store=True, readonly=False, )
    nexo_familiar_ids = fields.One2many(
        'sicpro.app.trabajadores.nexo.familiar', 'trabajadores_id',
        string='Nexo Familiar', )
    documentos_count = fields.Integer(compute='_documentos_count',
                                      string='# Documentos')
    disciplina_count = fields.Integer(compute="_compute_disciplinaria_count")
    resume_line_ids = fields.One2many('sicpro.app.trabajadores.educacion',
                                      'employee_id',
                                      string=" Registro educativo")
    employee_skill_ids = fields.One2many('sicpro.app.trabajadores.cursos',
                                         'employee_id', string=" Cursos")
    job_title = fields.Char(string="Job Title", compute="_compute_job_title",
                            store=True, readonly=False)
    subordinate_ids = fields.One2many('sicpro.app.trabajadores',
                                      string='Subordinados',
                                      compute='_compute_subordinates',
                                      compute_sudo=True)
    child_all_count = fields.Integer(string='Subordinados Indirectos Count',
                                     recursive=True,
                                     compute='_compute_subordinates',
                                     store=False, compute_sudo=True)
    equipo_tecnico_id = fields.Many2one(
        "sicpro.app.trabajadores.equipo.tecnico", string="equipo_tecnico_id")
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    equipo_tecnico = fields.Many2one("sicpro.app.trabajadores.equipo.tecnico",
                                     string="Equipo Técnico",
                                     related='area_id.equipo_tecnico_id')
    miembros = fields.Many2one("sicpro.app.trabajadores", string="Miembros")
    edad = fields.Integer(string='Edad', required=False)
    grupo_capacitador = fields.Boolean(string='grupo_capacitador',
                                       compute='_compute_grupo_capacitador')
    grupo_seguridad_salud = fields.Boolean(string='grupo_seguridad_salud',
                                           compute='_compute_grupo_seguridad_salud')
    qr_code = fields.Binary(string="Código QR", required=False)
    vacunacion_ids = fields.One2many('sicpro.app.trabajadores.vacunacion',
                                     'name', string=" Vacunación")
    intrucciones_ids = fields.One2many('sicpro.app.trabajadores.intrucciones',
                                       'name', string=" Instrucciones")
    seguridad_ids = fields.One2many(
        'sicpro.app.trabajadores.seguridad.trabajador', 'trabajador_id',
        string="Seguridad y Protección")
    seguridad_ocupacion = fields.Integer(string='SO',
                                         compute='compute_seguridad_ocupacion')

    # verífico que no se repita el carnet de Id del trabajador en el registro
    @api.constrains('identification_id')
    def _check_identification_id_integral(self):
        for record in self:
            if not record.identification_id:
                continue

            # 1. VALIDACIÓN DE FORMATO (11 dígitos numéricos)
            if not record.identification_id.isdigit():
                raise ValidationError(
                    "Error en [%s]: El Carnet de Identidad solo debe contener números." % record.identification_id + MSG_SOPORTE_SICPRO)

            if len(record.identification_id) != 11:
                raise ValidationError(
                    "Error en [%s]: El Carnet de Identidad debe tener exactamente 11 dígitos." % record.identification_id + MSG_SOPORTE_SICPRO)

            # 2. VALIDACIÓN DE UNICIDAD (Búsqueda manual en la tabla)
            # Buscamos si existe otro registro con el mismo identification_id que no sea el actual
            domain = [('identification_id', '=', record.identification_id),
                      ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "El Carnet de Identidad '%s' ya está registrado para otro trabajador." % record.identification_id + MSG_SOPORTE_SICPRO)

    # verífico que no se repita el número de plaza del trabajador en el registro
    @api.constrains('plaza_id')
    def _check_plaza_id_unico(self):
        uniq = self.env['sicpro.app.trabajadores'].search(
            ['&', '&', ("active", "=", True), ("plaza_id", "=", self.plaza_id),
             ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(
                "¡El número de plaza del trabajador seleccionado, ya se encuentra registrado!.\n\n" + MSG_SOPORTE_SICPRO)

    # genera él, id del cargo del trabajador para utilizarlo en los medios de protección
    def compute_seguridad_ocupacion(self):
        self.seguridad_ocupacion = self.ocupacion_id.name

    # genera el código QR del trabajador
    def generate_hr_qr(self):
        if self.name and self.job_title:
            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L)
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
            raise UserError(
                'Chequear el nombre del trabajador y la ocupación' + MSG_SOPORTE_SICPRO)

    # verífica qué el usuario activo pertenezca al grupo Responsable o al grupo Capacitador
    # Si no depende de campos del modelo, se deja vacío o se usa para disparar el cálculo
    @api.depends()
    def _compute_grupo_capacitador(self):
        es_responsable = self.env.user.has_group(
            'sicpro_app_trabajadores.grupo_app_trabajador_responsable')
        es_capacitador = self.env.user.has_group(
            'sicpro_app_trabajadores.grupo_app_trabajador_capacitacion')

        for record in self:
            if es_responsable:
                record.grupo_capacitador = False
            else:
                record.grupo_capacitador = es_capacitador

    # verífica que el usuario activo pertenezca al grupo Responsable o al grupo Seguridad y Salud
    # No depende de campos, sino del usuario actual
    @api.depends()
    def _compute_grupo_seguridad_salud(self):
        # Obtenemos los permisos una sola vez fuera del bucle para no saturar el servidor
        user = self.env.user
        es_responsable = user.has_group(
            'sicpro_app_trabajadores.grupo_app_trabajador_responsable')
        es_seguridad_salud = user.has_group(
            'sicpro_app_trabajadores.grupo_app_trabajador_seguridad_salud')

        for record in self:
            # Si es responsable, ocultamos/desactivamos según tu lógica
            if es_responsable:
                record.grupo_seguridad_salud = False
            else:
                record.grupo_seguridad_salud = es_seguridad_salud

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
        all_actions = self.env[
            'sicpro.app.trabajadores.disiplinaria.acciones']._read_group(
            domain=[('trabajador_id', 'in', self.ids),
                    ('estado', '=', 'action')], groupby=['trabajador_id'],
            aggregates=['__count'])

        mapping = {trabajador.id: count for trabajador, count in all_actions}
        for trabajador in self:
            trabajador.disciplina_count = mapping.get(trabajador.id, 0)

    # Abre la vista de los documentos de los trabajadores en el botón inteligente
    def disciplina_view(self):
        self.ensure_one()
        domain = [('trabajador_id', '=', self.id), ('estado', '=', 'action')]
        return {'name': 'Medidas Disciplinarias', 'domain': domain,
                'res_model': 'sicpro.app.trabajadores.disiplinaria.acciones',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form',
                'help': '''<p class="oe_view_nocontent_create">Click para crear una nueva medida disciplinaria </p>''',
                'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id}

    # Cuenta los documentos de los trabajadores
    def _documentos_count(self):
        for each in self:
            documentos_ids = self.env[
                'sicpro.app.trabajadores.documentos'].sudo().search(
                [('trabajadores_id', '=', each.id)])
            each.documentos_count = len(documentos_ids)

    # Abre la vista de los documentos de los trabajadores en el botón inteligente
    def documentos_view(self):
        self.ensure_one()
        domain = [('trabajadores_id', '=', self.id)]
        return {'name': 'Documentos', 'domain': domain,
                'res_model': 'sicpro.app.trabajadores.documentos',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form',
                'help': '''<p class="oe_view_nocontent_create"> Click para crear un nuevo documento </p>''',
                'limit': 80,
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
        data = self.env['sicpro.app.trabajadores.areas'].search(
            [('id', '=', self.area_id.id), ])
        self.local_id = data.local.ids
        # actualizo el usuario manager y departamento
        if self.area_id.manager_id:
            self.parent_id = self.area_id.manager_id

    # suma el total de salario extra
    @api.depends('resume_line_ids.pago')
    def _compute_salario_extra(self):
        for data in self:
            data.salario_extra = round(
                sum(data.resume_line_ids.mapped('pago')), 2)

    # devuelve el valor del salario completo (salàrio de la categoría ocupacional + salàrios extras)
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
    @api.depends('user_id.presence_ids.last_presence')
    def _compute_last_activity(self):
        for employee in self:
            # 1. Fallback de Zona Horaria para Cuba
            tz = employee.tz or self.env.user.tz or 'America/Havana'
            user_tz = timezone(tz)

            # 2. Acceso seguro al primer registro de presencia
            # Usamos .sudo() solo si el usuario actual no tiene permisos de lectura en presencias
            presence = employee.user_id.sudo().presence_ids[:1]

            if presence and presence.last_presence:
                last_dt_utc = presence.last_presence.replace(tzinfo=UTC)
                last_dt_local = last_dt_utc.astimezone(user_tz).replace(
                    tzinfo=None)

                employee.last_activity = last_dt_local.date()

                # 3. Comparación correcta con la fecha de Cuba
                if employee.last_activity == fields.Date.context_today(
                    employee):
                    employee.last_activity_time = format_time(self.env,
                                                              last_dt_local,
                                                              time_format='short')
                else:
                    employee.last_activity_time = False
            else:
                employee.last_activity = False
                employee.last_activity_time = False

    @api.onchange('resource_calendar_id')
    def _onchange_timezone(self):
        self.tz = self.resource_calendar_id.tz

    # envío felicitación de cumpleaños vía correo
    def send_birthday_mail(self):
        # Obtenemos la fecha actual una sola vez para evitar discrepancias de milisegundos
        today = datetime.now()
        day = today.day
        month = today.month

        birth_emps = self.env['sicpro.app.trabajadores'].search(
            [('active', '=', True), ('fecha_nacimiento', '!=', False)])

        filtered_emps = birth_emps.filtered(lambda
            r: r.fecha_nacimiento.day == day and r.fecha_nacimiento.month == month)

        if filtered_emps:
            template = self.env.ref(
                'sicpro_app_trabajadores.plantilla_felicitacion_cumpleaños',
                raise_if_not_found=False)

            if not template:
                # Manejo de error si la plantilla no existe
                return False

            for emp in filtered_emps:
                email_to = emp.correo_trabajo

                if email_to:
                    template.send_mail(emp.id, force_send=True,
                        email_values={'email_to': email_to})


    # Descarga un archivo plantilla para importar datos de los trabajadores
    @api.model
    def get_import_templates(self):
        return [{'label': (
            'Importar plantillas para Trabajadores, XMLID: "# Plaza"'),
                 'template': '/sicpro_app_trabajadores/static/xlsx/trabajadores.xlsx'}]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TrabajadoresGeneral, self).create(vals_list)
        for res in records:
            # Género el código QR
            res.generate_hr_qr()
            return res
        return None

    def unlink(self):
        resources = self.mapped('resource_id')
        super(TrabajadoresGeneral, self).unlink()
        return resources.unlink()
