# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import timedelta, datetime
from random import randint
import pytz
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError, AccessError,UserError
from odoo.tools.misc import format_date
import json


def _default_color():
    return randint(1, 11)


PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class OrdenesTrabajo(models.Model):
    _name = 'sicpro.app.ordenes.trabajo'
    _description = "Órdenes de Trabajo"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.ordenes.estados'].search(
            [('company_id', '=', self.env.company.id)], limit=1)

    # género la lista dinámica con las órdenes de trabajo para el control de autor
    @api.model
    def _compute_ordenes_control_autor_selection(self):
        ordenes = self.env['sicpro.app.ordenes.trabajo'].sudo().search(
            ['&', '&', ('is_terminada', '=', False),
             ('is_cancelado', '=', False),
             ('company_abreviatura', 'in', ('DEOCT', 'DEOIT'))],
            order='id desc')

        dic_ordenes = []
        for item in ordenes:
            data = (str(item.id), str(item.name))
            dic_ordenes.append(data)
        return dic_ordenes

    @api.depends('company_id', 'solicitud_id')
    def _compute_solicitud_disponible_ids(self):
        for record in self:
            # Forzamos a buscar el registro real de la compañía, no el virtual de memoria
            comp_real = record.company_id._origin if record.company_id else self.env.company
            company_id = comp_real.id or self.env.company.id

            # Dominio corregido con el operador OR plano para evitar fallos con estados vacíos
            domain_ordenes = [('company_id', '=', company_id), '|',
                ('estado_id', '=', False),
                ('is_cancelado', '!=', True)]

            if record._origin.id:
                domain_ordenes.append(('id', '!=', record._origin.id))

            ordenes_activas = self.env['sicpro.app.ordenes.trabajo'].search(
                domain_ordenes)

            solicitudes_ocupadas = [o.solicitud_id.id for o in ordenes_activas
                                    if o.solicitud_id]

            # 2. Filtrado final del universo de solicitudes
            domain_solicitudes = [('active', '=', True),
                ('company_id', '=', company_id),
                ('stage_id.is_orden', '=', True)]

            if solicitudes_ocupadas:
                domain_solicitudes.append(
                    ('id', 'not in', solicitudes_ocupadas))

            solicitudes_validas = self.env[
                'sicpro.app.solicitudes.oportunidades'].search(
                domain_solicitudes)

            if record.solicitud_id:
                solicitudes_validas |= record.solicitud_id
            record.solicitud_disponible_ids = solicitudes_validas

    name = fields.Char(string="Orden de Trabajo", required=False, index=True,
                       tracking=True, default='-')
    active = fields.Boolean(string='Activo', default=True, tracking=True,
                            index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    control_active_guardado = fields.Boolean(string='Control Active',
                                             required=False, default=False)
    tipo_orden = fields.Selection(string='Tipo de Orden',
                                  selection=[('inversiones', 'Inversiones'), (
                                  'mantenimiento', 'Mantenimiento'), ],
                                  required=True, tracking=True,
                                  default='inversiones')
    trimestre = fields.Many2one(comodel_name='sicpro.nomenclador.trimestre',
                                string='Trimestre', required=False,
                                tracking=True)
    user_id = fields.Many2one('res.users', string='Solícita la Orden',
                              index=True, tracking=True,
                              default=lambda self: self.env.uid)
    estado_id = fields.Many2one('sicpro.app.ordenes.estados', string='Estados',
                                ondelete='restrict', tracking=True,
                                group_expand='_read_group_stage_ids',
                                index=True, copy=False,
                                default=_get_default_stage_id)
    is_preparacion_tecnica = fields.Boolean(
        related='estado_id.is_preparacion_tecnica',
        string="En Preparación Técnica", readonly=True)
    is_fecha_inicial = fields.Boolean(related='estado_id.is_fecha_inicial',
                                      string="Tiene Fecha Inicial",
                                      readonly=True)
    is_en_proceso = fields.Boolean(related='estado_id.is_en_proceso',
                                   string="En Proceso", readonly=True)
    is_paralizado = fields.Boolean(related='estado_id.is_paralizado',
                                   string="Paralizado", readonly=True)
    is_cancelado = fields.Boolean(related='estado_id.is_cancelado',
                                  string="Cancelado", readonly=True)
    is_terminada = fields.Boolean(related='estado_id.is_terminada',
                                  string="Terminada", readonly=True)
    etiquetas_ids = fields.Many2many('sicpro.app.ordenes.etiquetas',
                                     'sicpro_app_ordenes_etiquetas_rel',
                                     'orden_id', 'etiqueta_id',
                                     string='Etiqueta', tracking=True)
    priority = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                index=True, tracking=True,
                                default=PRIORIDADES_ACTIVAS[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
        domain="[('ejecuta_proceso', '=', True)]", required=True,
        default=lambda self: self.env.company.id
    )
    company_currency = fields.Many2one(string='Moneda',
                                       related='company_id.currency_id',
                                       readonly=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto')
    as_numero = fields.Char(string='Acuerdo de Servicio', required=False,
                            tracking=True)
    as_valor = fields.Monetary(string='Valor AS', required=False,
                               tracking=True,
                               currency_field='company_currency')
    ficha_costo_valor = fields.Monetary(string='Valor FC', required=False,
                                        tracking=True,
                                        currency_field='company_currency')
    avance_obra = fields.Float(string='Avance de obra', required=False,
                               tracking=True)
    barra_avance_obra = fields.Float(string='Barra de Avance', required=False)
    motivo_paralizacion = fields.Many2one(
        comodel_name='sicpro.app.ordenes.paralizacion',
        string='Motivo de Paralización', required=False, tracking=True)
    detalles_paralizacion = fields.Text(string="Detalles de la Paralización",
                                        tracking=True)
    clase_orden_proyecto = fields.Many2one(
        comodel_name='sicpro.app.ordenes.clases.proyecto',
        string='Clase de trabajo', required=False, tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     tracking=True)
    estado_interno = fields.Selection(string='Estado Interno', required=True,
                                      tracking=True,
                                      selection=[('borrador', 'Borrador'),
                                                 ('solicitada', 'Solicitada'),
                                                 ('validada', 'Validada'), (
                                                     'rechazar_solicitud',
                                                     'Rechazar Solicitud'), (
                                                     'rechazar_creacion',
                                                     'Rechazar Creación'), (
                                                     'pendiente_sap',
                                                     'Pendiente SAP'),
                                                 ('creada', 'Creada'),
                                                 ('terminada', 'Terminada'), ],
                                      default='borrador')
    problemas_ids = fields.One2many(
        comodel_name='sicpro.app.ordenes.trabajo.anexo.problemas',
        inverse_name='orden_id', copy=False,
        string='Problemas de la Ejecución', required=False, tracking=True)
    creada_sap = fields.Boolean(string='Creada en el SAP', required=False,
                                default=False)
    creada_sistema = fields.Boolean(string='Creada en el Sistema',
                                    required=False, default=False)
    consecutivo_unico_orden = fields.Integer(
        string='Consecutivo Único de la Orden', required=False)
    orden_principal = fields.Boolean(string='Orden Principal', required=False,
                                     default=False)
    pep_corto = fields.Char(string='Pep Corto', required=False)
    motivo_aviso_intension = fields.Text(string="Motivo del cambio",
                                         required=False, tracking=True)
    motivo_aviso_intension_enviada = fields.Boolean(
        string='Motivo intensión enviada', required=False, default=False)
    control_autor = fields.Boolean(string='Control_autor',
                                   related='clase_orden_proyecto.control_autor',
                                   required=False)
    orden_control_autor = fields.Selection(
        _compute_ordenes_control_autor_selection, string='Orden Control Autor',
        required=False, tracking=True)
    motivo_rechazo = fields.Text(string="Motivo del Rechazo", required=False,
                                 tracking=True)
    orden_rechazada = fields.Boolean(string='Orden_rechazada', required=False,
                                     default=False)
    # grupo_crear_orden = fields.Boolean(string='grupo_crear_orden',
    #                                    compute='_compute_grupo_crear_orden')
    ############### CAMPOS PARA PEGAR EN SAP ##################################
    sap_uo = fields.Char(string='Unidad Organizativa SAP', required=False,
                         related='uo_id.abreviatura')
    # OU/Provincia/Texto breve
    sap_titulo = fields.Char(string="Titulo SAP",
                             compute='_compute_sap_titulo', store=True,
                             compute_sudo=True, )
    # No.SAP/Texto Breve
    sap_titulo_sap = fields.Char(string="SAP Titulo SAP",
                                 compute='_compute_titulo_sap_orden',
                                 store=True)
    sap_fecha_solicitud_orden = fields.Date(string='Fecha de solicitud',
                                            default=lambda
                                                self: fields.Date.context_today(
                                                self))
    sap_id_solicitud = fields.Char(string='Id Solicitud SAP', required=False,
                                   related='solicitud_id.id_solicitud')
    sap_consecutivo = fields.Char(string="Consecutivo SAP",
                                  compute="_compute_sap_consecutivo",
                                  store=True)
    sap_pep = fields.Char(string="PEP SAP", compute="_compute_sap_pep",
                          store=True)
    programa_inversiones = fields.Char(string="Programa de Inversiones",
                                       compute="_compute_sap_programa_inversiones",
                                       store=True)
    sap_programa_inversiones = fields.Char(string="Prog. Inversiones SAP",
                                           compute="_compute_sap_programa_inversiones",
                                           store=True)
    sap_fecha_solicitud_orden_char = fields.Char(
        string="Fecha Solicitud SAP Texto",
        compute="_compute_sap_fecha_solicitud_orden_char", store=True)
    sap_cliente_id = fields.Char(string="Inversionista SAP",
                                 compute="_compute_sap_cliente_id", store=True)
    sap_as_numero = fields.Char(string="Número AS SAP",
                                compute="_compute_sap_as_numero", store=True)
    sap_as_valor = fields.Float(string="Valor AS SAP",
                                compute="_compute_sap_as_valor", store=True)
    sap_ficha_costo_valor = fields.Char(string="Ficha Costo SAP",
                                        compute="_compute_sap_ficha_costo_valor",
                                        store=True)
    sap_fecha_inicio_cronograma = fields.Char(
        string="Fecha Inicio Cronograma SAP",
        compute="_compute_sap_fecha_inicio_cronograma", store=True)
    sap_fecha_fin_cronograma = fields.Char(string="Fecha Fin Cronograma SAP",
                                           compute="_compute_sap_fecha_fin_cronograma",
                                           store=True)
    sap_especialidad_id = fields.Char(string="Especialidad SAP",
                                      compute="_compute_sap_especialidad_id",
                                      store=True)
    ###########################################################################

    ############### TÍTULOS DE LA ORDEN #######################################
    # Nombre de la solicitud
    texto_breve_sap = fields.Char(string="Texto breve", required=True,
                                  tracking=True)
    # OU/Provincia/Texto breve
    titulo = fields.Char(string="Titulo", compute='_compute_titulo',
                         tracking=True,
                         compute_sudo=True, )
    ###########################################################################

    ############### DESCRIPCIONES Y OBSERVACIONES #############################
    observaciones_solicitud = fields.Text(string="Detalles de la Solicitud",
                                          required=False, tracking=True)
    observaciones_creacion = fields.Text(string="Detalles de la Creación",
                                         required=False, tracking=True)
    observaciones_actualizacion = fields.Text(
        string="Observaciones de la Actualización", required=False,
        tracking=True)
    # por defecto es el de la solicitud
    alcance = fields.Text(string="Alcance", required=False,
                          tracking=True)
    ###########################################################################

    ############### ORDENES AÑOS ANTERIORES ###################################
    anteriores_orden_id = fields.Many2one(
        comodel_name='sicpro.app.ordenes.trabajo', string='Orden Anteriores',
        required=False, domain="[('company_id', '=', company_id)]",
        tracking=True)
    anteriores_as_valor = fields.Monetary(
        string='Valor Acuerdo de Servicio Anterior',
        currency_field='company_currency',
        related='anteriores_orden_id.as_valor', tracking=True)
    anteriores_FC_valor = fields.Monetary(
        string='Valor Ficha de Costo Anterior',
        currency_field='company_currency',
        related='anteriores_orden_id.ficha_costo_valor', tracking=True)
    anteriores_pep = fields.Char(string='Pep Anterior',
                                 related='anteriores_orden_id.pep',
                                 tracking=True)
    ###########################################################################

    ############### FECHAS ####################################################
    # Calculada por la Fecha Inicio real
    mes_inicio = fields.Char(string='Mes Inicio',
                             compute='_compute_mes_inicio_orden',
                             required=False,
                             tracking=True)
    # Calculada por la Fecha Fin real
    mes_fin = fields.Char(string='Mes Terminada',
                          compute='_compute_mes_fin_orden', required=False,
                          tracking=True)
    fecha_solicitud_orden = fields.Date(string='solicitud de la orden',
                                        default=fields.Date.context_today, tracking=True)
    fecha_creacion_orden = fields.Date(string='Creada en Sistema',
                                       tracking=True)
    fecha_creacion_orden_sap = fields.Date(string='Creada en SAP',
                                           tracking=True)
    fecha_cancelacion_orden = fields.Date(string='Cancelación', tracking=True)
    anio = fields.Char(string="Año", required=False,
                       default=fields.Datetime.now().strftime("%Y"), )
    fecha_inicio_cronograma = fields.Date(string='Inicio Cronograma',
                                          required=False, tracking=True)
    fecha_fin_cronograma = fields.Date(string='Fin Cronograma', required=False,
                                       tracking=True)
    fecha_fin_cronograma_original = fields.Date(string='Fecha Fin Original',
                                                required=False, tracking=True)
    # Obligatorio al cambiar a los Estados: PT o En Proceso
    fecha_inicio_real = fields.Date(string='Inicio Real', required=False,
                                    tracking=True)
    # Obligatorio al cambiar a Estado: Terminada
    fecha_fin_real = fields.Date(string='Fin Real',
                                 tracking=True)
    # fecha actual - Días Paralizados - Fecha de Inicio real
    dias_instalacion = fields.Integer(string='Días de instalación',
                                      compute='_compute_dias_instalacion',
                                      required=False,
                                      tracking=True)
    fecha_paralizacion = fields.Date(string='Fecha de Paralización',
                                     required=False, tracking=True)
    dias_paralizacion = fields.Integer(string='Días Paralizado',
                                       compute='_compute_dias_paralizados',
                                       required=False, tracking=True)
    fecha_reinicio_paralizacion = fields.Date(string='Fecha de Reinicio',
                                              required=False, tracking=True)
    fecha_rechazada = fields.Date(string='Fecha de Rechazo', required=False,
                                  tracking=True)
    fecha_termino_orden = fields.Date(string='Terminación de la Orden',
                                      required=False, tracking=True)
    fecha_emision_proyecto = fields.Date(string='Fecha Emisión Proyecto',
                                         required=False, tracking=True)
    ###########################################################################

    ############### HORAS #####################################################
    horas_estimadas = fields.Char(string='Horas Estimadas', required=False,
                                  tracking=True)
    horas_reales = fields.Char(string='Horas Reales', required=False,
                               tracking=True)
    ###########################################################################

    ############### SOLICITUD DE TRABAJO ######################################
    solicitud_id = fields.Many2one('sicpro.app.solicitudes.oportunidades',
        string='Solicitud de Trabajo', required=True)
    # Campo auxiliar Many2many que usaremos como filtro en el XML
    solicitud_disponible_ids = fields.Many2many(
        'sicpro.app.solicitudes.oportunidades',
        compute='_compute_solicitud_disponible_ids',
        string='Solicitudes Disponibles')
    id_solicitud = fields.Char(string='Id Solicitud', required=False,
                               related='solicitud_id.id_solicitud')
    pep = fields.Char(string='Sap', required=True, tracking=True)
    uo_id = fields.Many2one(comodel_name='sicpro.nomenclador.territorios',
                            string='Área', required=True, tracking=True)
    uo_abreviatura = fields.Char(string='Unidad Organizativa', required=False,
                                 related='uo_id.abreviatura', store=True)
    provincia_id = fields.Many2one(comodel_name='res.country.state',
                                   string='Provincia', required=True,
                                   store=True,
                                   domain="[('country_id.name', '=', 'Cuba')]",
                                   tracking=True)
    agrupacion_id = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.areas', string='Asignado a',
        required=True, domain="[('company_id', '=', company_id)]",
        tracking=True)
    especialista_id = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                                      string='Especialista', required=True,
                                      domain="[('company_id', '=', company_id)]",
                                      tracking=True)
    especialidad_id = fields.Many2one(
        comodel_name='sicpro.nomenclador.especialidad', string='Especialidad',
        domain="[('company_id', '=', company_id)]", required=True,
        tracking=True)
    especialidad_letra = fields.Char(string='Especialidad Letra',
                                     related='especialidad_id.letra')
    proyecto_id = fields.Char(string='Id de Proyecto', required=False,
                              tracking=True)
    tarea_tecnica_id = fields.Char(string='Tarea Técnica', required=False,
                                   tracking=True)
    image_1920 = fields.Image("Image", related='especialidad_id.image_1920',
                              max_width=1920, max_height=1920)
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    ###########################################################################

    ############### INVERSIONISTA #############################################
    cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 index=True,
                                 related='solicitud_id.partner_id')
    cliente_territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="UO",
        related='cliente_id.territorio', required=False)
    cliente_provincia_id = fields.Many2one(comodel_name="res.country.state",
                                           string="Provincia Cliente",
                                           related='cliente_id.provincias_id',
                                           required=False)
    cliente_cargo = fields.Char(string="Cargo", related='cliente_id.cargo',
                                required=False)
    cliente_telefono_fijo = fields.Char(string="Teléfono",
                                        related='cliente_id.telefono_fijo',
                                        required=False)
    cliente_telefono_movil = fields.Char(string="Móvil",
                                         related='cliente_id.telefono_movil',
                                         required=False)
    cliente_correo = fields.Char(string="Correo electrónico",
                                 related='cliente_id.correo', required=False)
    ###########################################################################
    trabajadores_ids = fields.One2many(
        comodel_name='sicpro.app.ordenes.trabajo.trabajadores',
        inverse_name='orden_id', copy=False,
        string='Trabajadores en la Ejecución', required=False, tracking=True)
    transporte_vehiculos_ids = fields.One2many(
        comodel_name='sicpro.app.ordenes.trabajo.transporte',
        inverse_name='orden_id', copy=False,
        string='Vehículos en la Ejecución', required=False, tracking=True)
    transporte_especializados_ids = fields.One2many(
        comodel_name='sicpro.app.ordenes.trabajo.equipos.especializados',
        inverse_name='orden_id', copy=False,
        string='Equipos especializados en la Ejecución', required=False,
        tracking=True)
    transporte_complementarios_ids = fields.One2many(
        comodel_name='sicpro.app.ordenes.trabajo.equipos.complementarios',
        inverse_name='orden_id', copy=False,
        string='Equipos complementarios en la Ejecución', required=False,
        tracking=True)
    trabajadores_count = fields.Integer(compute='_compute_trabajadores_count',
                                        string="Trabajadores")
    vehiculos_count = fields.Integer(compute='_compute_vehiculos_count',
                                     string="Vehículos")
    equipos_especializados_count = fields.Integer(
        compute='_compute_equipos_especializados_count',
        string="Equipos Especializados")
    equipos_complementarios_count = fields.Integer(
        compute='_compute_equipos_complementarios_count',
        string="Equipos Complementarios")

    # Cuenta los trabajadores según los estados configurados
    @api.depends('trabajadores_ids', 'trabajadores_ids.estado',
                 'trabajadores_ids.estado.contar')
    def _compute_trabajadores_count(self):
        for item in self:
            item.trabajadores_count = len(item.trabajadores_ids.filtered(
                lambda r: r.estado and r.estado.contar))

    # Cuenta los vehículos según los estados configurados
    @api.depends('transporte_vehiculos_ids', 'transporte_vehiculos_ids.estado',
                 'transporte_vehiculos_ids.estado.contar')
    def _compute_vehiculos_count(self):
        for item in self:
            item.vehiculos_count = len(item.transporte_vehiculos_ids.filtered(
                lambda r: r.estado and r.estado.contar))

    # Cuenta los equipos especializados según los estados configurados
    @api.depends('transporte_especializados_ids',
                 'transporte_especializados_ids.estado',
                 'transporte_especializados_ids.estado.contar')
    def _compute_equipos_especializados_count(self):
        for item in self:
            item.equipos_especializados_count = len(
                item.transporte_especializados_ids.filtered(
                    lambda r: r.estado and r.estado.contar))

    # Cuenta los equipos complementarios según los estados configurados
    @api.depends('transporte_complementarios_ids',
                 'transporte_complementarios_ids.estado',
                 'transporte_complementarios_ids.estado.contar')
    def _compute_equipos_complementarios_count(self):
        for item in self:
            item.equipos_complementarios_count = len(
                item.transporte_complementarios_ids.filtered(
                    lambda r: r.estado and r.estado.contar))

    # muestra vista wizard para ver los trabajadores asignados
    def action_open_trabajadores_wizard(self):
        self.ensure_one()
        if not self.trabajadores_count or self.trabajadores_count == 0:
            raise UserError(
                "No hay trabajadores asignados a esta orden de trabajo.\n\n" + MSG_SOPORTE_SICPRO)
        list_view_id = self.env.ref(
            'sicpro_app_ordenes_trabajo.view_ordenes_trabajadores_modal_list').id

        return {'name': 'Trabajadores Asignados',
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.ordenes.trabajo.trabajadores', 'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (False, 'form')],
            'domain': [('orden_id', '=', self.id)], 'target': 'new',
            'context': {'default_orden_id': self.id}, }

    # muestra vista wizard para ver los vehículos asignados
    def action_open_vehiculos_wizard(self):
        self.ensure_one()
        if not self.vehiculos_count or self.vehiculos_count == 0:
            raise UserError(
                "No hay vehículos asignados a esta orden de trabajo.\n\n" + MSG_SOPORTE_SICPRO)
        list_view_id = self.env.ref(
            'sicpro_app_ordenes_trabajo.view_ordenes_vehiculos_modal_list').id

        return {'name': 'Vehículos Asignados', 'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.ordenes.trabajo.transporte', 'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (False, 'form')],
            'domain': [('orden_id', '=', self.id)], 'target': 'new',
            'context': {'default_orden_id': self.id}, }

    # muestra vista wizard para ver los vehículos especializados asignados
    def action_open_especializados_wizard(self):
        self.ensure_one()
        if not self.equipos_especializados_count or self.equipos_especializados_count == 0:
            raise UserError(
                "No hay equipos especializados asignados a esta orden de trabajo.\n\n" + MSG_SOPORTE_SICPRO)
        list_view_id = self.env.ref(
            'sicpro_app_ordenes_trabajo.view_ordenes_equipos_especializados_modal_list').id

        return {'name': 'Equipos Especializados',
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.ordenes.trabajo.equipos.especializados',
            'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (False, 'form')],
            'domain': [('orden_id', '=', self.id)], 'target': 'new',
            'context': {'default_orden_id': self.id}, }

    # muestra vista wizard para ver los vehículos complementarios asignados
    def action_open_complementarios_wizard(self):
        self.ensure_one()
        if not self.equipos_complementarios_count or self.equipos_complementarios_count == 0:
            raise UserError(
                "No hay equipos complementarios asignados a esta orden de trabajo.\n\n" + MSG_SOPORTE_SICPRO)
        list_view_id = self.env.ref(
            'sicpro_app_ordenes_trabajo.view_ordenes_equipos_complementarios_modal_list').id

        return {'name': 'Equipos Complementarios',
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.ordenes.trabajo.equipos.complementarios',
            'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (False, 'form')],
            'domain': [('orden_id', '=', self.id)], 'target': 'new',
            'context': {'default_orden_id': self.id}, }

    # verífica que las fechas de inicio y terminación real exista para poder pasar la orden a los estados configurados
    @api.constrains('estado_id')
    def _check_estados_obligatorios(self):
        for record in self:
            if record.is_terminada and not record.fecha_fin_real:
                raise ValidationError(
                    "¡Debe agregar la fecha de terminación real de la obra!.\n\n" + MSG_SOPORTE_SICPRO)
            elif (
                record.is_fecha_inicial or record.is_en_proceso) and not record.fecha_inicio_real:
                raise ValidationError(
                    "¡Debe agregar la fecha de inicio real de la obra!.\n\n" + MSG_SOPORTE_SICPRO)

    # verífico que no se repitan las especialidades en los procesos ejecutores
    @api.constrains('especialidad_id')
    def _check_especialidad_unica(self):
        if self.company_abreviatura != 'PROYECTOS':
            pep_corto = str(self.pep[:10])
            uniq = self.env['sicpro.app.ordenes.trabajo'].search(
                ['&', '&', ('active', '=', True), ("id", "!=", self.id),
                 ('pep_corto', '=', pep_corto),
                 ('tipo_orden', '=', self.tipo_orden),
                 ('especialidad_id', '=', self.especialidad_id.id),
                 ('company_id', '=', self.company_id.id),
                 ('anio', '=', self.anio)])

            if uniq:
                raise ValidationError(
                    "¡La especialidad introducida para ese número SAP ya existe!.\n\n" + MSG_SOPORTE_SICPRO)

    # verífico que la especialidad de la orden archivada ya exista en el
    # sistema
    @api.constrains('active')
    def _check_activo_unica(self):
        if self.company_abreviatura != 'PROYECTOS':
            pep_corto = str(self.pep[:10])
            if self.control_active_guardado:
                uniq = self.env['sicpro.app.ordenes.trabajo'].search(
                    ['&', '&', ('active', '=', True), ("id", "!=", self.id),
                     ('pep_corto', '=', pep_corto),
                     ('tipo_orden', '=', self.tipo_orden),
                     ('especialidad_id', '=', self.especialidad_id.id),
                     ('company_id', '=', self.company_id.id),
                     ('anio', '=', self.anio)])

                if uniq:
                    raise ValidationError(
                        "¡No se puede desarchivar, la especialidad de la orden para ese número SAP ya "
                        "existe!.\n\n" + MSG_SOPORTE_SICPRO)

    # chequea que la fecha fin real no sea anterior a la inicial real
    @api.constrains('fecha_inicio_real', 'fecha_fin_real')
    def _check_fecha_inicio_fin_real(self):
        for item in self:
            if item.fecha_fin_real and item.fecha_inicio_real:
                if item.fecha_fin_real < item.fecha_inicio_real:
                    raise ValidationError(
                        'La fecha fin real no puede ser anterior a la fecha de inicio real.' + MSG_SOPORTE_SICPRO)

    # chequea que la fecha fin cronograma no sea anterior a la inicio cronograma
    @api.constrains('fecha_inicio_cronograma', 'fecha_fin_cronograma')
    def _check_fecha_inicio_fin_cronograma(self):
        for item in self:
            if item.fecha_fin_cronograma and item.fecha_inicio_cronograma:
                if item.fecha_fin_cronograma < item.fecha_inicio_cronograma:
                    raise ValidationError(
                        "La fecha fin del cronograma no puede ser anterior a la fecha de inicio "
                        "del cronograma.\n\n" + MSG_SOPORTE_SICPRO)

    # agrega los datos a la barra de avance de obras
    @api.onchange('avance_obra')
    def _compute_barra_avance(self):
        if self.avance_obra:
            self.barra_avance_obra = self.avance_obra * 100

    # calcula los días de paralización de la obra
    @api.onchange('fecha_paralizacion')
    def _compute_dias_paralizados(self):
        hoy = fields.Date.context_today(self)
        for item in self:
            if item.is_paralizado:
                diferencia = hoy - item.fecha_paralizacion if item.fecha_paralizacion else timedelta(
                    0)
                item.dias_paralizacion = diferencia.days
            elif item.fecha_paralizacion and item.fecha_reinicio_paralizacion:
                diferencia = item.fecha_reinicio_paralizacion - item.fecha_paralizacion
                item.dias_paralizacion = max(0, diferencia.days)
            else:
                item.dias_paralizacion = 0

    # calcula los días de instalación de la obra
    @api.onchange('dias_paralizacion', 'fecha_inicio_real')
    def _compute_dias_instalacion(self):
        hoy = fields.Date.context_today(self)
        for item in self:
            if item.is_terminada:
                diferencia = item.fecha_fin_real - item.fecha_inicio_real
                dias = diferencia - timedelta(days=item.dias_paralizacion)
                item.dias_instalacion = dias.days
            elif item.is_cancelado:
                diferencia = item.fecha_cancelacion_orden - item.fecha_inicio_real
                dias = diferencia - timedelta(days=item.dias_paralizacion)
                item.dias_instalacion = dias.days
            else:
                if item.fecha_inicio_real:
                    diferencia = hoy - item.fecha_inicio_real
                    dias = diferencia - timedelta(days=item.dias_paralizacion)
                    item.dias_instalacion = dias.days
                else:
                    item.dias_instalacion = 0

    # genera el mes de inicio de la orden
    @api.onchange('fecha_inicio_real')
    def _compute_mes_inicio_orden(self):
        for item in self:
            fecha_inicio = item.fecha_inicio_real
            if fecha_inicio:
                mes_id = fecha_inicio.month
                nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                    ['&', ('active', '=', True), ('codigo_mes', '=', mes_id)])
                item.mes_inicio = nombre_mes.name
            else:
                item.mes_inicio = '-'

    # genera el mes de fin de la orden
    @api.onchange('fecha_fin_real')
    def _compute_mes_fin_orden(self):
        for item in self:
            fecha_fin = item.fecha_fin_real
            if fecha_fin:
                mes_id = fecha_fin.month
                nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                    ['&', ('active', '=', True), ('codigo_mes', '=', mes_id)])
                item.mes_fin = nombre_mes.name
            else:
                item.mes_fin = '-'

    # crea el titulo sap de la orden
    @api.depends('pep', 'texto_breve_sap')
    def _compute_titulo_sap_orden(self):
        for item in self:
            pep_comprobado = item.pep.name if hasattr(item.pep,
                                                      'name') and item.pep else item.pep

            if pep_comprobado and item.texto_breve_sap:
                item.sap_titulo_sap = f"{pep_comprobado}/{item.texto_breve_sap}"
            else:
                item.sap_titulo_sap = '-'

    # crea el titulo de la orden
    @api.depends('uo_abreviatura', 'provincia_id', 'texto_breve_sap')
    def _compute_sap_titulo(self):
        for item in self:
            if all([item.uo_abreviatura, item.provincia_id,
                    item.texto_breve_sap]):
                item.sap_titulo = f"{item.uo_abreviatura}/{item.provincia_id.name}/{item.texto_breve_sap}"
            else:
                item.sap_titulo = '-'

    @api.depends('sap_titulo')
    def _compute_titulo(self):
        for item in self:
            item.titulo = item.sap_titulo

    # actualiza los datos de la solicitud de trabajo
    @api.onchange('solicitud_id')
    def _upgrade_solicitud_trabajo(self):
        if not self.solicitud_id:
            return

        self.pep = self.solicitud_id.pep
        self.uo_id = self.solicitud_id.territorio_id
        self.provincia_id = self.solicitud_id.provincia_id
        self.agrupacion_id = self.solicitud_id.grupo_ejecutor
        self.especialista_id = self.solicitud_id.especialista_ejecutor
        self.especialidad_id = self.solicitud_id.especialidad
        self.proyecto_id = self.solicitud_id.consecutivo_proyecto
        self.tarea_tecnica_id = self.solicitud_id.codigo_tt
        self.alcance = self.solicitud_id.description
        self.texto_breve_sap = self.solicitud_id.name
        self.cliente_id = self.solicitud_id.partner_id

    @api.depends('name')
    def _compute_sap_consecutivo(self):
        for record in self:
            if record.name:
                record.sap_consecutivo = record.name
            else:
                record.sap_consecutivo = "-"

    @api.depends('pep')
    def _compute_sap_pep(self):
        for record in self:
            if record.pep:
                record.sap_pep = record.pep
            else:
                record.sap_pep = "-"

    @api.depends('pep', 'company_id')
    def _compute_sap_programa_inversiones(self):
        for record in self:
            if record.pep:
                pep = str(record.pep)
                consecutivo = pep[:2]

                # Validación para evitar caídas si los primeros caracteres no son dígitos
                consecutivo_int = int(
                    consecutivo) if consecutivo.isdigit() else 0
                territorio = pep[5:7]

                # Usamos limit=1 para asegurar un comportamiento óptimo del search en el compute
                programa = record.env[
                    'sicpro.app.ordenes.programa.inversiones'].search(
                    [('active', '=', True),
                        ('consecutivo', '=', consecutivo_int),
                        ('company_id', '=', record.company_id.id)], limit=1)

                if programa:
                    nomenclador = f"{territorio} {programa.name}"
                    record.programa_inversiones = nomenclador
                    record.sap_programa_inversiones = nomenclador
                else:
                    msg = 'No se encontró ninguna coincidencia para el programa de inversiones'
                    record.programa_inversiones = msg
                    record.sap_programa_inversiones = msg
            else:
                record.programa_inversiones = '-'
                record.sap_programa_inversiones = '-'

    @api.depends('sap_fecha_solicitud_orden')
    def _compute_sap_fecha_solicitud_orden_char(self):
        tz_cuba = pytz.timezone('America/Havana')
        fecha_hoy_cuba = datetime.now(tz_cuba)

        for record in self:
            record.sap_fecha_solicitud_orden_char = fecha_hoy_cuba.strftime(
                '%d-%m-%Y')

    @api.depends('cliente_id')
    def _compute_sap_cliente_id(self):
        for record in self:
            if record.cliente_id:
                record.sap_cliente_id = record.cliente_id.name
            else:
                record.sap_cliente_id = "-"

    @api.depends('as_numero')
    def _compute_sap_as_numero(self):
        for record in self:
            if record.as_numero:
                record.sap_as_numero = record.as_numero
            else:
                record.sap_as_numero = "-"

    @api.depends('as_valor')
    def _compute_sap_as_valor(self):
        for record in self:
            if record.as_valor:
                record.sap_as_valor = record.as_valor
            else:
                record.sap_as_valor = 0.00

    @api.depends('ficha_costo_valor')
    def _compute_sap_ficha_costo_valor(self):
        for record in self:
            if record.ficha_costo_valor:
                record.sap_ficha_costo_valor = str(record.ficha_costo_valor)
            else:
                record.sap_ficha_costo_valor = "-"

    @api.depends('fecha_inicio_cronograma')
    def _compute_sap_fecha_inicio_cronograma(self):
        for record in self:
            if record.fecha_inicio_cronograma:
                # Si el campo destino es un Char, lo ideal es convertirlo a texto plano
                record.sap_fecha_inicio_cronograma = record.fecha_inicio_cronograma.strftime(
                    '%d-%m-%Y')
            else:
                record.sap_fecha_inicio_cronograma = "-"

    @api.depends('fecha_fin_cronograma')
    def _compute_sap_fecha_fin_cronograma(self):
        for record in self:
            if record.fecha_fin_cronograma:
                record.sap_fecha_fin_cronograma = record.fecha_fin_cronograma.strftime(
                    '%d-%m-%Y')
            else:
                record.sap_fecha_fin_cronograma = "-"

    @api.depends('especialidad_id')
    def _compute_sap_especialidad_id(self):
        for record in self:
            if record.especialidad_id:
                record.sap_especialidad_id = record.especialidad_id.name
            else:
                record.sap_especialidad_id = "'"

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

    # actualiza los datos después de crear la orden en SAP
    def action_crear_sap(self):
        if self.estado_interno == 'pendiente_sap':
            estado = self.env['sicpro.app.ordenes.estados'].search(
                ['&', ('is_preparacion_tecnica', '=', True),
                 ('company_id', '=', self.company_id.id)], limit=1).id
            self.sudo().write(
                {'fecha_creacion_orden_sap': fields.Date.context_today(self),
                    'creada_sap': True,'estado_interno': 'creada',
                 'estado_id': estado,})

    # action para ver la orden asociada de proyecto
    def orden_asociada_proyectos_view(self):
        if not self.proyecto_id:
            raise AccessError(
                "El campo de la orden asociada de proyecto esta vació.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            ordenes_buscar = self.env['sicpro.app.ordenes.trabajo'].search(
                [('active', '=', True), ('name', '=', self.proyecto_id)],
                limit=1)
            if ordenes_buscar:
                domain = ['&', ('active', '=', True),
                          ('name', '=', ordenes_buscar.name)]
                return {'name': 'Orden de Proyecto', 'domain': domain,
                        'res_model': 'sicpro.app.ordenes.trabajo',
                        'type': 'ir.actions.act_window', 'view_id': False,
                        'view_mode': 'tree,form', 'limit': 80, }
            else:
                raise AccessError(
                    "No existe la orden asociada de proyecto en el sistema.\n\n" + MSG_SOPORTE_SICPRO)

    # botón para solicitar la orden
    def action_solicitar_orden(self):
        # VALIDACIÓN DEL VALOR DEL ACUERDO DE SERVICIOS (DEBE SER DISTINTO DE 0.00)
        if not self.as_valor or self.as_valor == 0.00:
            raise ValidationError(
                "No se puede solicitar la orden porque el valor del Acuerdo de Servicios "
                "debe ser superior a 0.00. Por favor, asigne el monto correspondiente.\n\n" + MSG_SOPORTE_SICPRO)

        # VALIDACIÓN DEL NÚMERO DEL ACUERDO DE SERVICIOS (NO DEBE ESTAR EN BLANCO)
        if not self.as_numero:
            raise ValidationError(
                "No se puede solicitar la orden porque el Número del Acuerdo de Servicios "
                "está en blanco. Por favor, asigne el número correspondiente.\n\n" + MSG_SOPORTE_SICPRO)

        if self.orden_rechazada:
            self.fecha_rechazada = None
            self.motivo_rechazo = None
            self.orden_rechazada = False

        self.estado_interno = 'solicitada'
        # busco usuarios del rol validar del proceso específico de la orden
        proceso = self.company_id
        group_validar = self.env.ref(
            'sicpro_app_ordenes_trabajo.grupo_ordenes_validar',
            raise_if_not_found=False)
        validar = self.env['res.users']
        if group_validar:
            validar = group_validar.user_ids
        # agrego los seguidores al modelo
        for item in validar:
            if item.company_id == proceso:
                self.message_subscribe(partner_ids=item.partner_id.ids)
        # envío la notificación
        self.message_post(body='Solicitud de Orden',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_nueva_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action

    # botón para validar la orden
    def action_validar_orden(self):
        if self.orden_rechazada:
            self.fecha_rechazada = None
            self.motivo_rechazo = None
            self.orden_rechazada = False

        self.estado_interno = 'validada'
        # busco usuarios del rol validar del proceso específico de la orden
        proceso = self.company_id
        group_crear = self.env.ref(
            'sicpro_app_ordenes_trabajo.grupo_ordenes_ejecutor',
            raise_if_not_found=False)
        crear = self.env['res.users']
        if group_crear:
            crear = group_crear.user_ids
        # agrego los seguidores al modelo
        for item in crear:
            if item.company_id == proceso:
                self.message_subscribe(partner_ids=item.partner_id.ids)
        # envío la notificación
        self.message_post(body='Solicitud de Orden',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_solicitud_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action

    # botón para crear la orden
    def action_crear_orden(self):
        orden = ''
        valor = ''
        num_as = ''

        self.fecha_creacion_orden = fields.Date.context_today(self)
        self.estado_interno = 'pendiente_sap'

        pep_corto = str(self.pep or '')[:10]
        anio = str(self.anio or '')[2:4]

        consecutivo = self.env[
            'sicpro.app.ordenes.consecutivos'].sudo().search(
            [('tipo', '=', self.tipo_orden),
             ('company_id', '=', self.company_id.id)], limit=1)

        nomenclador = str(consecutivo.name or '')
        moneda = str(consecutivo.moneda or '')
        clase = str(self.clase_orden_proyecto.name or '')
        especialidad = str(self.especialidad_letra or '')

        # busco que ya exista el pep para asignarlo al consecutivo
        ordenes_buscar = self.env['sicpro.app.ordenes.trabajo'].search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('company_id', '=', self.company_id.id),
             ('creada_sistema', '=', True), ('anio', '=', self.anio),
             ('tipo_orden', '=', self.tipo_orden),
             ('orden_principal', '=', True), ('pep_corto', '=', pep_corto)],
            limit=1)

        # compruebo que exista el valor único de la orden, si no lo creo
        if ordenes_buscar:
            num = str(ordenes_buscar.consecutivo_unico_orden)
            count_ordenes = len(num)
            if count_ordenes == 1:
                valor = '00' + str(num)
            elif count_ordenes == 2:
                valor = '0' + str(num)
            elif count_ordenes == 3:
                valor = str(num)
        else:
            # cuento la cantidad de órdenes del tipo y proceso específico
            ordenes_count = self.env[
                'sicpro.app.ordenes.trabajo'].search_count(
                ['|', ('active', '=', True), ('active', '=', False),
                 ('creada_sistema', '=', True),
                 ('tipo_orden', '=', self.tipo_orden),
                 ('company_id', '=', self.company_id.id),
                 ('orden_principal', '=', True), ('anio', '=', self.anio)])
            # verífico que existan órdenes con los parámetros del dominio, si no creo la primera.
            if ordenes_count:
                # Creo el número de consecutivo
                count_ordenes = len(str(ordenes_count))
                num = ordenes_count + 1
                if count_ordenes == 1:
                    valor = '00' + str(num)
                elif count_ordenes == 2:
                    valor = '0' + str(num)
                elif count_ordenes == 3:
                    valor = str(num)
            else:
                # Creo el primer número de consecutivo 001
                valor = '001'
            # la marco como orden principal
            self.orden_principal = True

        # compruebo el proceso para generar la orden
        if self.company_abreviatura == 'PROYECTOS':
            if self.tipo_orden == 'inversiones':
                orden = nomenclador + moneda + anio + clase + especialidad + valor
                num_as = '1' + '/' + self.anio
            elif self.tipo_orden == 'mantenimiento':
                orden = nomenclador + moneda + anio + clase + especialidad + valor
                num_as = '1' + '/' + self.anio
        else:
            if self.tipo_orden == 'inversiones':
                orden = nomenclador + moneda + anio + especialidad + '0' + valor
                num_as = valor + '/' + self.anio
            elif self.tipo_orden == 'mantenimiento':
                orden = nomenclador + moneda + anio + especialidad + '0' + valor
                num_as = valor + '/' + self.anio

        # guardo el consecutivo generado en los campos requeridos
        self.name = orden
        self.as_numero = num_as
        self.pep_corto = pep_corto
        self.consecutivo_unico_orden = valor
        self.creada_sistema = True

        # envío la notificación
        self.message_post(body='Orden Creada', message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_crear_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

        # envío correo de aviso al proyectista de la orden
        for participante in self.solicitud_id:
            # envío el correo electrónico
            email_values = {
                'email_to': participante.especialista_ejecutor.user_id.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_asociada_orden_proyectos')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

    # botón para pasar a sin comenzar la orden
    def action_sin_comenzar_orden(self):
        estado = self.env['sicpro.app.ordenes.estados'].search(
            [('is_fecha_inicial', '=', True),
             ('company_id', '=', self.company_id.id)], limit=1).id

        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

    # botón para pasar a en proceso la orden
    def action_en_proceso_orden(self):
        # VALIDACIÓN DEL VALOR DE LA FECHA DE INICIO POR CRONOGRAMA
        # (NO PUEDE ESTAR VACÍA)
        if not self.fecha_inicio_cronograma:
            raise ValidationError(
                "No se puede pasar a En Proceso la orden porque falta la "
                "fecha de inicio del cronograma "
                "Por favor, asigne la fecha correspondiente.\n\n" + MSG_SOPORTE_SICPRO)

        # VALIDACIÓN DEL NÚMERO DE LA FECHA FIN POR CRONOGRAMA
        # (NO PUEDE ESTAR VACÍA)
        if not self.fecha_fin_cronograma:
            raise ValidationError(
                "No se puede pasar a En Proceso la orden porque falta la "
                "fecha fin del cronograma "
                "Por favor, asigne la fecha correspondiente.\n\n" +
                MSG_SOPORTE_SICPRO)

        estado = self.env['sicpro.app.ordenes.estados'].search(
            [('is_en_proceso', '=', True),
             ('company_id', '=', self.company_id.id)], limit=1).id

        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

    # botón para reiniciar la orden
    def action_reiniciar_orden(self):
        self.fecha_reinicio_paralizacion = datetime.today()
        estado = self.env['sicpro.app.ordenes.estados'].search(
            [('is_en_proceso', '=', True),
             ('company_id', '=', self.company_id.id)], limit=1).id

        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

    # botón para terminar la orden
    def action_terminar_orden(self):
        self.estado_interno = 'terminada'
        self.fecha_termino_orden = datetime.today()
        estado = self.env['sicpro.app.ordenes.estados'].search(
            [('is_terminada', '=', True),
             ('company_id', '=', self.company_id.id)], limit=1).id

        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(OrdenesTrabajo, self).create(vals_list)
        for res in records:
            res.control_active_guardado = True
        return records


# trabajadores en la ejecución
class OrdenesTrabajoTrabajadores(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.trabajadores'
    _order = "id asc"
    _description = 'Trabajadores en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                           string='Trabajador', required=True, tracking=True)
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden',
                               required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Date.context_today(
                                   self))
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    estado = fields.Many2one(
        comodel_name='sicpro.app.ordenes.estados.trabajador', string='Estado',
        required=True, tracking=True)
    company_id_orden = fields.Many2one('res.company',
                                       string='Proceso Ejecutor',
                                       related='orden_id.company_id')

    # asegurar que la fecha de salida no sea menor que la de inicio
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_trabajador(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    "La fecha de salida ('Salida') no puede ser anterior a la fecha de inicio del trabajador.\n\n" + MSG_SOPORTE_SICPRO)


# Transporte en la ejecución
class OrdenesTrabajoTransporte(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.transporte'
    _order = "id asc"
    _description = 'Transporte en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general',
                           string='Transporte', required=True, tracking=True)
    tipo_vehiculo_id_domain = fields.Char(
        compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden',
                               required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Date.context_today(
                                   self))
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    estado = fields.Many2one(
        comodel_name='sicpro.app.ordenes.estados.transporte.equipos',
        string='Estado', domain="[('tipo', '=', 'vehiculo')]", required=True,
        tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre',
                                       string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico',
                                        compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo',
                                      related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('company_id')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            [('active', '=', True), ('name', '=', 'vehiculo')], limit=1)

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                if rec.grupoEquipoNombre:
                    dic.append(str(rec.grupoEquipoNombre))

            item.tipo_vehiculo_id_domain = json.dumps(
                [('grupoEquipoNombre', 'in', dic)], ensure_ascii=False)

    # garantizar la coherencia de las fechas de uso del transporte
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_transporte(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    "La fecha de salida ('Salida') no puede ser anterior a la fecha de inicio del transporte.\n\n" + MSG_SOPORTE_SICPRO)


# Equipos especializados de la construcción en la ejecución
class OrdenesTrabajoEquiposEspecializados(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.equipos.especializados'
    _order = "id asc"
    _description = 'Equipos especializados en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general',
                           string='Transporte', required=True, tracking=True)
    tipo_vehiculo_id_domain = fields.Char(
        compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden',
                               required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Date.context_today(
                                   self))
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    estado = fields.Many2one(
        comodel_name='sicpro.app.ordenes.estados.transporte.equipos',
        string='Estado', domain="[('tipo', '=', 'equipo_especializado')]",
        required=True, tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre',
                                       string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico',
                                        compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo',
                                      related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('company_id')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            [('active', '=', True), ('name', '=', 'equipo_especializado')],
            limit=1)

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                if rec.grupoEquipoNombre:
                    dic.append(str(rec.grupoEquipoNombre))

            item.tipo_vehiculo_id_domain = json.dumps(
                [('grupoEquipoNombre', 'in', dic)], ensure_ascii=False)

    # garantizar la coherencia de las fechas de uso del equipo especializado
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_equipo_especializado(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    "La fecha de salida ('Salida') no puede ser anterior a la fecha de inicio del equipo especializado.\n\n" + MSG_SOPORTE_SICPRO)


# Equipos complementarios en la ejecución
class OrdenesTrabajoEquiposComplementarios(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.equipos.complementarios'
    _order = "id asc"
    _description = 'Equipos complemtarios en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general',
                           string='Transporte', required=True, tracking=True)
    tipo_vehiculo_id_domain = fields.Char(
        compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden',
                               required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Date.context_today(
                                   self))
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    estado = fields.Many2one(
        comodel_name='sicpro.app.ordenes.estados.transporte.equipos',
        string='Estado', domain="[('tipo', '=', 'equipo_complementario')]",
        required=True, tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre',
                                       string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico',
                                        compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo',
                                      related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('company_id')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            [('active', '=', True), ('name', '=', 'equipo_complementario')],
            limit=1)

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                if rec.grupoEquipoNombre:
                    dic.append(str(rec.grupoEquipoNombre))

            item.tipo_vehiculo_id_domain = json.dumps(
                [('grupoEquipoNombre', 'in', dic)], ensure_ascii=False)

    # garantizar la coherencia de las fechas de uso del equipo complementario
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_complementarios(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    "La fecha de salida ('Salida') no puede ser anterior a la fecha de inicio del equipo complementario.\n\n" + MSG_SOPORTE_SICPRO)


# problemas de la ejecución
class OrdenesTrabajoAnexoProblemas(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.anexo.problemas'
    _order = "id desc"
    _description = 'Tabla anexo de los problemas en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.ordenes.problemas',
                           string='Problemas', required=False, tracking=True)
    detalles_problema = fields.Text(string="Detalles del problema",
                                    tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden',
                               required=False, index=True)
    fecha_inicio = fields.Date(string="Comienzo", required=True,
                               default=lambda self: fields.Date.context_today(
                                   self))
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    fecha_fin = fields.Date(string="Resuelto", required=False, )
    estado = fields.Selection(string='Estado',
                              selection=[('resuelto', 'Resuelto'),
                                         ('no_resuelto', 'No Resuelto'), ],
                              required=True, default='no_resuelto')

    # Actualizo la fecha fin de resuelto el problema
    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado == 'resuelto':
            self.fecha_fin = fields.Date.context_today(self)
        else:
            self.fecha_fin = False

    # asegurar que la fecha de resolución no sea anterior al comienzo
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_problemas(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    "La fecha de resolución ('Resuelto') no puede ser anterior a la fecha de comienzo.\n\n" + MSG_SOPORTE_SICPRO)


# motivo de paralización
class OrdenesTrabajoMotivoParalizacion(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.paralizacion'
    _description = 'Motivo de la paralización de la orden de trabajo'

    motivo_id = fields.Many2one(comodel_name='sicpro.app.ordenes.paralizacion',
                                string="Motivo", required=True)
    detalles_paralizacion = fields.Text(string="Detalles de la Paralización",
                                        required=True)

    def action_motivo_paralizacion(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(
            self.env.context.get('active_ids'))

        for item in orden.sudo():
            estado_record = self.env['sicpro.app.ordenes.estados'].search(
                [('is_paralizado', '=', True),
                 ('company_id', '=', item.company_id.id)], limit=1)

            item.motivo_paralizacion = self.motivo_id
            item.detalles_paralizacion = self.detalles_paralizacion
            item.fecha_reinicio_paralizacion = None
            item.fecha_paralizacion = fields.Datetime.now()

            # Verificación de seguridad para evitar errores si no se encuentra el estado
            if estado_record:
                item.estado_id = estado_record.id

        # envío la notificación
        orden.message_post(body='Orden Paralizada',
                           message_type='notification',
                           subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(orden.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action


# motivo de rechazo
class OrdenesTrabajoMotivoRechazo(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.rechazadas'
    _description = 'Motivo de rechazo de la orden de trabajo'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(
            self.env.context.get('active_ids'))

        # Obtenemos la fecha actual usando la API de Odoo
        today = fields.Date.context_today(self)
        formatted_today = format_date(self.env, today)

        for item in orden.sudo():
            item.orden_rechazada = True
            item.fecha_rechazada = today

            if item.estado_interno == 'solicitada':
                item.motivo_rechazo = f"La orden no fue validada, se rechazó el {formatted_today} por los siguientes motivos: {self.motivo_id}"
                item.estado_interno = 'rechazar_solicitud'

            elif item.estado_interno == 'validada':
                item.motivo_rechazo = f"La orden no fue creada, se rechazó el {formatted_today} por los siguientes motivos: {self.motivo_id}"
                item.estado_interno = 'rechazar_creacion'

        # envío la notificación
        orden.message_post(body='Orden Rechazada', message_type='notification',
                           subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_rechazo_orden')
            template.with_context(local_context).send_mail(orden.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action


# motivo de cancelación
class OrdenesTrabajoMotivoCancelacion(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.canceladas'
    _description = 'Motivo de cancelación de la orden de trabajo'

    motivo_id = fields.Text(string="Motivo de Cancelación", required=True)

    def action_motivo_cancelacion(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(
            self.env.context.get('active_ids'))

        for item in orden.sudo():
            estado_record = self.env['sicpro.app.ordenes.estados'].search(
                [('is_cancelado', '=', True),
                 ('company_id', '=', item.company_id.id)], limit=1)

            item.motivo_cancelacion = self.motivo_id
            item.fecha_cancelacion_orden = fields.Datetime.now()

            # Verificación de seguridad para evitar errores si no se encuentra el estado
            if estado_record:
                item.estado_id = estado_record.id

        # envío la notificación
        orden.message_post(body='Orden Cancelada', message_type='notification',
                           subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_cambios_orden')

            template.with_context(local_context).send_mail(orden.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action


# aviso de intensión
class OrdenesTrabajoAvisoIntension(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.aviso.intension'
    _description = 'Aviso de intensión de la orden de trabajo'

    nueva_fecha = fields.Date(string="Nueva fecha", required=True, )
    motivo_aviso_intension = fields.Text(string="Motivo del cambio",
                                         required=True)

    def action_motivo_cambio(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(
            self.env.context.get('active_ids'))

        # Preparamos las fechas formateadas para el mensaje
        for item in orden.sudo():
            fecha_original_fmt = format_date(self.env,
                                             item.fecha_fin_cronograma)
            nueva_fecha_fmt = format_date(self.env, self.nueva_fecha)

            item.fecha_fin_cronograma_original = item.fecha_fin_cronograma
            item.fecha_fin_cronograma = self.nueva_fecha
            item.motivo_aviso_intension_enviada = True
            item.motivo_aviso_intension = (
                f"La fecha fin de la obra por el cronograma estaba prevista para el {fecha_original_fmt}, "
                f"fue necesario modificarla para el {nueva_fecha_fmt} "
                f"por los siguientes motivos: {self.motivo_aviso_intension}")

        # envío la notificación
        orden.message_post(body='Aviso de Intensión.',
                           message_type='notification',
                           subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_ordenes_trabajo.ordenes_aviso_intension_orden')

            template.with_context(local_context).send_mail(orden.id,
                                                           force_send=True,
                                                           email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[
            0]
        return action