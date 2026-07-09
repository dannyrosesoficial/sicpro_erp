# -*- coding: utf-8 -*-

import logging
from datetime import timedelta, datetime

from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.tools import format_date

_logger = logging.getLogger(__name__)

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class PreparacionTecnicaPreparaciones(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.preparaciones'
    _description = 'Preparaciones de la Preparación Técnica'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "priority desc, sequence, id desc"

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.preparacion.tecnica.estados'].search(
            [], limit=1)

    name = fields.Char(string='Titulo', tracking=True, required=True,
                       index=True)
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users',
                              string='Assigned to',
                              default=lambda self: self.env.uid,
                              index=True, tracking=True)
    description = fields.Html(string='Descripción')
    priority = fields.Selection(Prioridades_Activas, string='Prioridad',
                                index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    sequence = fields.Integer(string='Sequencia', index=True, default=10, )
    especialista_ejecutor_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.ejecutor', string='Asignado a',
        default=lambda self: self.env.context.get(
            'default_especialista_ejecutor_id'), index=True, tracking=True)
    departamento_id = fields.Many2one(
        'sicpro.app.trabajadores.departmentos', string="Area",
        related="especialista_ejecutor_id.name.department_id", store=True,
        tracking=True)
    responsable = fields.Many2one("sicpro.app.trabajadores.general",
                                  string="Jefe Inmediato",
                                  related="especialista_ejecutor_id.name.parent_id",
                                  index=True, tracking=True, )
    etiquetas = fields.Many2many('sicpro.app.preparacion.tecnica.etiquetas',
                                 'sicpro_app_preparacion_etiquetas_rel',
                                 string='Etiqueta')
    cliente = fields.Many2one('sicpro.app.clientes', string='Cliente',
                              tracking=10, index=True,
                              domain=[('tipo_registro', '=', 'persona')], )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color Index')
    displayed_image_id = fields.Many2one(
        'ir.attachment',
        domain="[('res_model', '=', 'sicpro.app.preparacion.tecnica.preparaciones'), "
               "('res_id', '=', id), "
               "('mimetype', 'ilike', 'image')]",
        string='Imagen de portada')
    fecha_inicio = fields.Date("Fecha de creación", index=True,
                               default=fields.Date.context_today, )
    fecha_terminado = fields.Datetime(string='Fecha de terminación',
                                      index=True, copy=False, readonly=True)
    fecha_terminacion_planificada = fields.Date(
        string='Cierre planificado',
        compute='_compute_horas_planificadas',
        compute_sudo=True, store=True,
        copy=False, readonly=True)
    fecha_ultimo_estado_act = fields.Datetime(string='Ultimo estado',
                                              index=True,
                                              copy=False,
                                              readonly=True)
    territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="Territorio",
        related='cliente.territorio')
    provincia_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.provincia", string="Provincia",
        related='cliente.provincia')
    cargo = fields.Char(string="Cargo", related='cliente.cargo')
    telefono_fijo = fields.Char(
        string="Teléfono", related='cliente.telefono_fijo')
    telefono_movil = fields.Char(
        string="Móvil", related='cliente.telefono_movil')
    correo = fields.Char(string="Correo electrónico", related='cliente.correo')
    anio = fields.Char(string="Año", required=False,
                       default=fields.datetime.today().strftime("%Y"), )
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,
                                       relation="res.currency")
    id_solicitud = fields.Char(string='Id. de la Solicitud', tracking=True,
                               readonly=True, store=True)
    valor_sap_cup = fields.Monetary('Presupuesto CUP',
                                    currency_field='company_currency',
                                    tracking=True)
    valor_sap_cuc = fields.Monetary('Presupuesto CUC',
                                    currency_field='company_currency',
                                    tracking=True)
    pep = fields.Char(string='Sap', required=True)
    especialidad = fields.Many2one(
        comodel_name="sicpro.nomenclador.especialidad", string="Especialidad",
        domain="[('company_id', '=', company_id)]", required=True, )
    stage_id = fields.Many2one('sicpro.app.preparacion.tecnica.estados',
                               string='Estados', ondelete='restrict',
                               tracking=True,
                               group_expand='_read_group_stage_ids',
                               index=True, copy=False,
                               default=_get_default_stage_id)
    kanban_state = fields.Selection([('normal', 'Ejecución'),
                                     ('blocked', 'Pendiente aprobación'),
                                     ('done', 'Aprobado'), ],
                                    string='Estado interno',
                                    copy=False, default='normal',
                                    readonly=True)
    tipo_registro = fields.Selection(string='tipo_registro', selection=[
        ('preparacion', 'Preparación'), ('suplemento', 'Suplementos'), ],
                                     required=True, copy=False,
                                     default='preparacion', )
    rechazar = fields.Char(string='Rechazar', required=False, readonly=True,
                           tracking=True)
    esta_rechazada = fields.Boolean(default=False)
    no_aprobada = fields.Char(string='Devuelta', required=False, tracking=True)
    no_esta_aprobada = fields.Boolean(default=False)
    doc_count = fields.Integer(compute='_compute_attached_docs_count',
                               string="Cantidad de documentos")
    suplementos_count = fields.Integer(compute='_compute_suplementos_count',
                                       string="Cantidad de suplementos")
    material_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.materiales",
        inverse_name="preparaciones_id", string="Material", )
    insumos_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.insumos",
        inverse_name="preparaciones_id", string="insumos", )
    horas_planificadas = fields.Float("Horas planificadas", tracking=True)
    cantidad_materiales = fields.Integer(
        "Cantidad de Materiales",
        compute='_compute_cantidad_presupuesto_materiales', store=True, )
    total_presupuesto_materiales = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_cantidad_presupuesto_materiales', store=True, )
    cantidad_insumos = fields.Integer(
        "Cantidad de Insumos", compute='_compute_cantidad_presupuesto_insumos',
        store=True, )
    total_presupuesto_insumos = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_cantidad_presupuesto_insumos', store=True, )
    actividades_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.actividades.form",
        inverse_name="preparaciones_id", string="Actividades", )
    cantidad_actividades = fields.Float(
        "Total de Horas", compute='_compute_cantidad_dias_actividades',
        store=True, )
    total_dias_actividades = fields.Float(
        "Total de dias", compute='_compute_cantidad_dias_actividades',
        store=True, digits=(12, 0))
    fecha_temp = fields.Date(string='fecha_temp')

    transporte_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.transporte",
        inverse_name="preparaciones_id", string="Transporte", )
    total_presupuesto_combustible = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_combustible', store=True, )
    salario_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.salario",
        inverse_name="preparaciones_id", string="Salario", )
    total_presupuesto_salario = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_salario', store=True, )
    info_estimulacion = fields.Char(
        string='Estimulación',
        compute='_compute_info_estimulacion_vacaciones_social_indirecto_dieta',
        compute_sudo=True, store=True, )
    info_reserva_vacaciones = fields.Char(
        string='Reserva vacaciones',
        compute='_compute_info_estimulacion_vacaciones_social_indirecto_dieta',
        compute_sudo=True, store=True, )
    info_seguridad_social = fields.Char(
        string='Seguridad Social',
        compute='_compute_info_estimulacion_vacaciones_social_indirecto_dieta',
        compute_sudo=True, store=True, )
    info_gastos_indirectos = fields.Char(
        string='Gastos indirectos',
        compute='_compute_info_estimulacion_vacaciones_social_indirecto_dieta',
        compute_sudo=True, store=True, )
    info_dieta = fields.Monetary(
        string='Dieta',
        currency_field='company_currency',
        compute='_compute_info_estimulacion_vacaciones_social_indirecto_dieta',
        compute_sudo=True, store=True, )
    info_actividades_imprevistas = fields.Char(
        string='Actividades imprevistas',
        compute='_compute_info_actividades_imprevistas',
        compute_sudo=True, store=True, )
    dieta_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.salario",
        inverse_name="preparaciones_id", string="Dieta", )
    total_presupuesto_dieta = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_dieta', store=True, )
    alimentacion_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.salario",
        inverse_name="preparaciones_id", string="Alimentación", )
    total_presupuesto_alimentacion = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_alimentacion', store=True, )
    anexo_a = fields.Text(string="Anexo A", required=False)
    anexo_b = fields.Text(string="Anexo B", required=False)
    anexo_e = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.anexoe",
        inverse_name="preparaciones_id", string="Anexo E")
    cantidad_pruebas_anexo_e = fields.Integer("Cantidad pruebas",
                                              compute='_compute_cantidad_pruebas_anexo_e',
                                              store=True, )
    total_gastos_cuc = fields.Monetary(
        "CUC", currency_field='company_currency',
        compute='_compute_presupuesto_cuc_cup', store=True, )
    total_gastos_cup = fields.Monetary(
        "CUP", currency_field='company_currency',
        compute='_compute_presupuesto_cuc_cup', store=True, )
    fecha_solicitada_aprobacion = fields.Date(string='Solicitud de Aprobación',
                                              index=True, tracking=True,
                                              copy=False, readonly=True)
    fecha_aprobada = fields.Date(string='Fecha Aprobada',
                                 index=True, tracking=True,
                                 copy=False, readonly=True)
    fecha_devuelta = fields.Date(string='Fecha Devuelta',
                                 index=True, tracking=True,
                                 copy=False, readonly=True)
    consecutivo = fields.Char(string='Consecutivo', copy=False,
                              readonly=True, )
    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", required=False, )
    padre_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="padre", required=False, )
    sequence_id = fields.Many2one('ir.sequence', string='Secuencia',
                                  required=False, copy=False)
    sumplemento_id = fields.Integer(string='Id suplemento', required=False)

    total_gastos_as_padre_cuc = fields.Monetary(
        "CUC", currency_field='company_currency', readonly=True, store=True, )
    total_gastos_as_padre_cup = fields.Monetary(
        "CUP", currency_field='company_currency', readonly=True, store=True, )

    gastos_suplementos_cuc = fields.Monetary(
        "CUC", currency_field='company_currency', readonly=True, store=True, )
    gastos_suplementos_cup = fields.Monetary(
        "CUP", currency_field='company_currency', readonly=True, store=True, )

    total_gastos_suplementos_cuc = fields.Monetary(
        "CUC", currency_field='company_currency', readonly=True, store=True, )
    total_gastos_suplementos_cup = fields.Monetary(
        "CUP", currency_field='company_currency', readonly=True, store=True, )

    total_gastos_suplementos_cuc_final = fields.Monetary(
        "CUC", currency_field='company_currency', readonly=True, store=True, )
    total_gastos_suplementos_cup_final = fields.Monetary(
        "CUP", currency_field='company_currency', readonly=True, store=True, )
    estado_ganado = fields.Boolean(store=True, default=False)
    provincia_obra = fields.Many2one(
        string="Provincia", comodel_name="sicpro.nomenclador.provincia",
        required=True, )
    pasaje_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.pasaje",
        inverse_name="preparaciones_id", string="Pasaje", )
    hospedaje_ids = fields.One2many(
        comodel_name="sicpro.app.preparacion.tecnica.hospedaje",
        inverse_name="preparaciones_id", string="Hospedaje", )

    total_presupuesto_pasaje = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_pasaje', store=True, )
    total_presupuesto_hospedaje = fields.Monetary(
        "Presupuesto Total", currency_field='company_currency',
        compute='_compute_presupuesto_hospedaje', store=True, )

    date_deadline_formatted = fields.Char(
        compute='_compute_date_deadline_formatted')

    # devuelve la fecha de terminación planificada
    @api.depends('fecha_inicio', 'horas_planificadas')
    def _compute_horas_planificadas(self):
        if self.fecha_inicio:
            for data in self:
                horas = self.env['resource.calendar'].search(
                    [('company_id', '=', self.company_id.id)],
                    limit=1).hours_per_day
                dias = round(data.horas_planificadas, 2) / horas
                for data in self:
                    data.fecha_terminacion_planificada = data.fecha_inicio + timedelta(
                        days=dias)

    # devuelve el % de las actividades imprevistas
    @api.depends('actividades_ids', )
    def _compute_info_actividades_imprevistas(self):
        for data in self:
            imprevistos = self.env['sicpro.nomenclador.variables'].search(
                [('company_id', '=', data.company_id.id),
                 ('name', '=', 'imprevisto')], limit=1).porciento
            data.info_actividades_imprevistas = imprevistos

    # devuelve el % de la estimulacion, reserva de vacaciones,
    # seguridad social, dieta y gasto indirecto
    @api.depends('salario_ids', )
    def _compute_info_estimulacion_vacaciones_social_indirecto_dieta(self):
        for data in self:
            # devuelve el % de la estimulacion
            estimulacion = self.env['sicpro.nomenclador.variables'].search(
                [('company_id', '=', data.company_id.id),
                 ('name', '=', 'estimulacion')], limit=1).porciento
            data.info_estimulacion = estimulacion
            # devuelve el % de la reserva de vacaciones
            reserva = self.env['sicpro.nomenclador.variables'].search(
                [('company_id', '=', data.company_id.id),
                 ('name', '=', 'vacaciones')], limit=1).porciento
            data.info_reserva_vacaciones = reserva
            # devuelve el % de la seguridad social
            social = self.env['sicpro.nomenclador.variables'].search(
                [('company_id', '=', data.company_id.id),
                 ('name', '=', 'seguridad_social')], limit=1).porciento
            data.info_seguridad_social = social
            # devuelve el % de los gasto indirecto
            indirectos = self.env['sicpro.nomenclador.variables'].search(
                [('company_id', '=', data.company_id.id),
                 ('name', '=', 'gastos_indirectos')], limit=1).porciento
            data.info_gastos_indirectos = indirectos
            # devuelve el valor de la dieta aprobada
            dieta = self.env['sicpro.nomenclador.dieta'].search(
                [('company_id', '=', self.company_id.id)], limit=1).name
            data.info_dieta = dieta

    # cuanta los documentos adjuntos de la preparación técnica
    def _compute_attached_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count([
                '&', ('res_model', '=',
                      'sicpro.app.preparacion.tecnica.preparaciones'),
                ('res_id', '=', documentos.id)
            ])

    # adjunta los documentos de la preparación técnica
    def attached_docs_view_action(self):
        self.ensure_one()
        domain = [
            '&',
            ('res_model', '=', 'sicpro.app.preparacion.tecnica.preparaciones'),
            ('res_id', 'in', self.ids),
        ]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Adjunte documentos a su preparación técnica.</p>
                    '''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
                self._name, self.id)
        }

    # cuanta los suplementos de la preparación técnica
    def _compute_suplementos_count(self):
        data = self.env['sicpro.app.preparacion.tecnica.preparaciones']
        for suplementos in self:
            suplementos.suplementos_count = data.search_count(
                ['&', ('tipo_registro', '=', 'suplemento'),
                 ('padre_id', '=', self._origin.id)])

    # redirección a la vista de suplementos
    def suplementos_action(self):
        domain = ['&', ('tipo_registro', '=', 'suplemento'),
                  ('padre_id', '=', self._origin.id)]
        return {
            'name': _('Suplementos'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="o_view_nocontent_smiling_face">
                    Aquí puede visualizar los suplementos de la obra en ejecución.
                </p>'''),
            'limit': 80,
        }

    # crea suplementos para la preparación técnica
    def crear_suplementos_action(self):
        self.ensure_one()
        domain = []
        return {
            'name': _('Suplementos'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form',
            'view_type': 'form',
            'context': "{'default_tipo_registro': 'suplemento',"
                       "'default_name': '%s',"
                       "'default_especialista_ejecutor_id': %d,"
                       "'default_pep': '%s',"
                       "'default_especialidad': %d,"
                       "'default_id_solicitud': %d,"
                       "'default_padre_id': %d,"
                       "'default_cliente': %d,"
                       "}" %
                       (self.name,
                        self.especialista_ejecutor_id,
                        self.pep,
                        self.especialidad,
                        self.id_solicitud,
                        self._origin.id,
                        self.cliente
                        )
        }

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # escribe cambios en la fechas de ultima actualización y
    # ultima actualización de estados
    # cambio de estado de rechazo
    def write(self, vals):
        now = fields.Datetime.now()
        # al cambiar el estado se actualiza la fecha_ultimo_estado_act
        if 'stage_id' in vals:
            vals.update(self.update_fecha_terminado(vals['stage_id']))
            vals['fecha_ultimo_estado_act'] = now
            if self.stage_id.is_rechazada:
                vals['esta_rechazada'] = False
        result = super(PreparacionTecnicaPreparaciones, self).write(vals)
        return result

    # actualiza la fecha de terminación
    def update_fecha_terminado(self, stage_id):
        estado = self.env['sicpro.app.preparacion.tecnica.estados'].browse(
            stage_id)
        if estado.fold:
            return {'fecha_terminado': fields.Datetime.now(),
                    'estado_ganado': True
                    }
        return {'fecha_terminado': False,
                'estado_ganado': False
                }

    # suma la cantidad de pruebas del anexo E
    @api.depends('anexo_e')
    def _compute_cantidad_pruebas_anexo_e(self):
        for data in self:
            data.cantidad_pruebas_anexo_e = sum(data.anexo_e.mapped('vals'))

    # suma la cantidad y total de presupuesto de materiales
    @api.depends('material_ids.cantidad', 'material_ids.presupuesto')
    def _compute_cantidad_presupuesto_materiales(self):
        for data in self:
            # suma la cantidad total de materiales
            data.cantidad_materiales = round(
                sum(data.material_ids.mapped('cantidad')), 2)
            # suma el total de presupuesto de materiales
            data.total_presupuesto_materiales = round(
                sum(data.material_ids.mapped('presupuesto')), 2)

    # suma la cantidad y el total de presupuesto de insumos
    @api.depends('insumos_ids.cantidad', 'insumos_ids.presupuesto')
    def _compute_cantidad_presupuesto_insumos(self):
        for data in self:
            # suma la cantidad total de insumos
            data.cantidad_insumos = round(
                sum(data.insumos_ids.mapped('cantidad')), 2)
            # suma el total de presupuesto de insumo
            data.total_presupuesto_insumos = round(
                sum(data.insumos_ids.mapped('presupuesto')), 2)

    # calcula el total de dias de las actividades y la cantidad de horas
    # total de actividades
    @api.depends('actividades_ids.normas_tiempo')
    def _compute_cantidad_dias_actividades(self):
        horas = self.env['resource.calendar'].search(
            [('company_id', '=', self.company_id.id)], limit=1).hours_per_day
        imprevistos = self.env['sicpro.nomenclador.variables'].search(
            [('company_id', '=', self.company_id.id),
             ('name', '=', 'imprevisto')], limit=1).valor
        for data in self:
            # suma la cantidad de horas total de actividades
            data.cantidad_actividades = round(
                sum(data.actividades_ids.mapped('normas_tiempo')), 2)
            # calcula el total de dias de las actividades
            total_dias = round(
                sum(data.actividades_ids.mapped('normas_tiempo')), 2) / horas
            porciento = imprevistos * total_dias
            data.total_dias_actividades = total_dias + porciento

    # suma el total de presupuesto del combustible
    @api.depends('transporte_ids.presupuesto')
    def _compute_presupuesto_combustible(self):
        for data in self:
            data.total_presupuesto_combustible = round(
                sum(data.transporte_ids.mapped('presupuesto')), 2)

    # suma el total de presupuesto del salario
    @api.depends('salario_ids.presupuesto')
    def _compute_presupuesto_salario(self):
        for data in self:
            data.total_presupuesto_salario = round(
                sum(data.salario_ids.mapped('presupuesto')), 2)

    # suma el total de presupuesto de la dieta
    @api.depends('salario_ids.presupuesto_dieta')
    def _compute_presupuesto_dieta(self):
        for data in self:
            data.total_presupuesto_dieta = round(
                sum(data.salario_ids.mapped('presupuesto_dieta')), 2)

    # suma el total de presupuesto de la alimentación
    @api.depends('salario_ids.presupuesto_alimentacion')
    def _compute_presupuesto_alimentacion(self):
        for data in self:
            data.total_presupuesto_alimentacion = round(
                sum(data.salario_ids.mapped('presupuesto_alimentacion')), 2)

    # suma el total de presupuesto del pasaje
    @api.depends('pasaje_ids')
    def _compute_presupuesto_pasaje(self):
        for data in self:
            data.total_presupuesto_pasaje = round(
                sum(data.pasaje_ids.mapped('gasto')), 2)

    # suma el total de presupuesto del hospedaje
    @api.depends('hospedaje_ids')
    def _compute_presupuesto_hospedaje(self):
        for data in self:
            data.total_presupuesto_hospedaje = round(
                sum(data.hospedaje_ids.mapped('gasto')), 2)

    # suma el total de gastos CUC y CUP
    @api.depends('total_presupuesto_alimentacion', 'total_presupuesto_dieta',
                 'total_presupuesto_combustible', 'total_presupuesto_insumos',
                 'total_presupuesto_materiales', 'total_presupuesto_salario',
                 'total_presupuesto_pasaje', 'total_presupuesto_hospedaje')
    def _compute_presupuesto_cuc_cup(self):
        for data in self:
            if data.tipo_registro == 'preparacion':
                data.total_gastos_cuc = data.total_presupuesto_alimentacion + \
                                        data.total_presupuesto_dieta + \
                                        data.total_presupuesto_combustible + \
                                        data.total_presupuesto_insumos + \
                                        data.total_presupuesto_materiales + \
                                        data.total_presupuesto_pasaje + \
                                        data.total_presupuesto_hospedaje
                data.total_gastos_cup = data.total_presupuesto_salario
            else:
                data.gastos_suplementos_cuc = data.total_presupuesto_alimentacion + \
                                              data.total_presupuesto_dieta + \
                                              data.total_presupuesto_combustible + \
                                              data.total_presupuesto_insumos + \
                                              data.total_presupuesto_materiales + \
                                              data.total_presupuesto_pasaje + \
                                              data.total_presupuesto_hospedaje
                data.gastos_suplementos_cup = data.total_presupuesto_salario

                data.total_gastos_cuc = data.total_presupuesto_alimentacion + \
                                        data.total_presupuesto_dieta + \
                                        data.total_presupuesto_combustible + \
                                        data.total_presupuesto_insumos + \
                                        data.total_presupuesto_materiales + \
                                        data.total_presupuesto_pasaje + \
                                        data.total_presupuesto_hospedaje + \
                                        data.total_gastos_suplementos_cuc_final
                data.total_gastos_cup = data.total_presupuesto_salario + \
                                        data.total_gastos_suplementos_cup_final

    @api.depends('fecha_inicio')
    def _compute_date_deadline_formatted(self):
        for task in self:
            task.date_deadline_formatted = format_date(
                self.env, task.fecha_inicio) if task.fecha_inicio else None

    # accion del boton de solicitar aprobacion de la preparación
    def action_solicitar_aprovacion(self, ):
        # envio la notificacion a los seguidores
        self.message_post(
            body='Aprobación solicitad',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        estado = self.env['sicpro.app.preparacion.tecnica.estados'].search(
            [('is_aprobada', '=', True)]).id
        self.fecha_solicitada_aprobacion = fields.date.today()
        self.sudo().kanban_state = 'blocked'
        self.stage_id = estado
        # redirecciono la salida
        domain = [('tipo_registro', '=', 'preparacion')]
        return {
            'name': _('Cartera de ejecución'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_especialista_ejecutor_id': %d}" %
                       self.especialista_ejecutor_id
        }

    # accion del boton para aprobar la preparacion
    def action_aprobar(self, ):
        # envio la notificacion a los seguidores
        self.message_post(
            body='preparación aprobada',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        estado = self.env['sicpro.app.preparacion.tecnica.estados'].search(
            [('is_won', '=', True)]).id
        self.fecha_aprobada = fields.date.today()
        self.sudo().kanban_state = 'done'
        self.stage_id = estado
        # redirecciono la salida
        domain = [('tipo_registro', '=', 'preparacion')]
        return {
            'name': _('Cartera de ejecución'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_especialista_ejecutor_id': %d}" %
                       self.especialista_ejecutor_id
        }

    @api.model
    def create(self, vals):
        # Crear la secuencia de incremento para el consecutivo de la
        # preparación por proceso y por tipo de registro
        # (preparación o suplemento)
        registro = vals['tipo_registro']
        padre = vals['padre_id']
        if registro == 'preparacion':
            code = 'preparacion_tecnica_consecutivo'
            data = self.env['ir.sequence'].search(
                ['&', ('code', '=', code),
                 ('company_id', '=', self.env.company.id)])
            if data:
                res = super(PreparacionTecnicaPreparaciones, self).create(vals)
                res['sequence_id'] = data.id
                res['consecutivo'] = self.env['ir.sequence'].next_by_code(
                    'preparacion_tecnica_consecutivo') or _('New')
            else:
                prefix = 'PT/%(range_year)s/'
                seq_name = 'Consecutivo de la Preparación Técnicas'
                seq = {
                    'code': code,
                    'name': _('%s Sequence') % seq_name,
                    'implementation': 'no_gap',
                    'prefix': prefix,
                    'padding': 4,
                    'number_increment': 1,
                    'use_date_range': True,
                }
                if 'company_id' in vals:
                    seq['company_id'] = vals['company_id']
                    vals['sequence_id'] = self.env[
                        'ir.sequence'].sudo().create(seq).id
                    res = super(PreparacionTecnicaPreparaciones, self).create(
                        vals)
                    res['consecutivo'] = self.env['ir.sequence'].next_by_code(
                        'preparacion_tecnica_consecutivo') or _('New')
        else:
            # cuento la cantidad de suplementos
            data1 = self.env[
                        'sicpro.app.preparacion.tecnica.preparaciones'].search_count(
                ['&', ('tipo_registro', '=', 'suplemento'),
                 ('padre_id', '=', padre)]) + 1

            data2 = self.env[
                'sicpro.app.preparacion.tecnica.preparaciones'].search(
                [('id', '=', padre)])

            data3 = self.env[
                'sicpro.app.preparacion.tecnica.preparaciones'].search(
                ['&', ('tipo_registro', '=', 'suplemento'),
                 ('padre_id', '=', padre)])

            res = super(PreparacionTecnicaPreparaciones, self).create(vals)
            res['sequence_id'] = data2.sequence_id
            res['consecutivo'] = data2.consecutivo + ' - SU/' + str(data1)
            res['sumplemento_id'] = data1
            res['total_gastos_as_padre_cuc'] = data2.total_gastos_cuc
            res['total_gastos_as_padre_cup'] = data2.total_gastos_cup

            res['total_gastos_suplementos_cuc'] = sum(
                [item["gastos_suplementos_cuc"] for item in data3])
            res['total_gastos_suplementos_cup'] = sum(
                [item["gastos_suplementos_cup"] for item in data3])

            res['total_gastos_suplementos_cuc_final'] = res[
                                                            'total_gastos_as_padre_cuc'] + \
                                                        res[
                                                            'total_gastos_suplementos_cuc']
            res['total_gastos_suplementos_cup_final'] = res[
                                                            'total_gastos_as_padre_cup'] + \
                                                        res[
                                                            'total_gastos_suplementos_cup']
        return res


class Rechazadas(models.TransientModel):
    _name = 'sicpro.app.preparacion.tecnica.rechazadas'
    _description = 'Preparaciones Rechazadas'

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_rechazo(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.preparacion.tecnica.preparaciones'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Preparación Técnica rechazada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno de la solicitud
        estado = self.env['sicpro.app.preparacion.tecnica.estados'].search(
            [('is_rechazada', '=', True)]).id
        rechazo = self.env[
            'sicpro.app.preparacion.tecnica.preparaciones'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.rechazar = self.lost_reason_id
            item.esta_rechazada = True
            item.sudo().stage_id = estado
        # redirecciono la salida
        domain = [('tipo_registro', '=', 'preparacion')]
        return {
            'name': _('Cartera de ejecución'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_especialista_ejecutor_id': %d}" %
                       post.especialista_ejecutor_id
        }


class PreparacionNoaprobada(models.TransientModel):
    _name = 'sicpro.app.preparacion.tecnica.noaprobada'
    _description = 'Preparaciones Rechazadas'

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_noaprobada(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.preparacion.tecnica.preparaciones'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Preparación Técnica no aprobada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno de la solicitud
        estado = self.env['sicpro.app.preparacion.tecnica.estados'].search(
            [('is_aprobada', '=', True)]).id
        aprobar = self.env[
            'sicpro.app.preparacion.tecnica.preparaciones'].browse(
            self.env.context.get('active_ids'))
        for item in aprobar.sudo():
            item.no_aprobada = self.lost_reason_id
            item.no_esta_aprobada = True
            item.fecha_devuelta = fields.date.today()
            item.sudo().stage_id = estado
        # redirecciono la salida
        domain = [('tipo_registro', '=', 'preparacion')]
        return {
            'name': _('Cartera de ejecución'),
            'domain': domain,
            'res_model': 'sicpro.app.preparacion.tecnica.preparaciones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_especialista_ejecutor_id': %d}" %
                       post.especialista_ejecutor_id
        }
