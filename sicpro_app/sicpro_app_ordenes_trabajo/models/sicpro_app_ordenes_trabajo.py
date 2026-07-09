# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from random import randint

from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, AccessError
from odoo.tools import format_date
from odoo.tools.safe_eval import json


def _default_color():
    return randint(1, 11)


Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class OrdenesTrabajo(models.Model):
    _name = 'sicpro.app.ordenes.trabajo'
    _description = "Órdenes de Trabajo"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.ordenes.estados'].search([('company_id', '=', self.env.company.id)], limit=1)

    # género la lista dinámica con las órdenes de trabajo para el control de autor
    @api.model
    def _compute_ordenes_control_autor_selection(self):
        ordenes = self.env['sicpro.app.ordenes.trabajo'].sudo().search(
            ['&', '&', ('is_terminada', '=', False), ('is_cancelado', '=', False),
             ('company_abreviatura', 'in', ('DEOCT', 'DEOIT'))], order='id desc')

        dic_ordenes = []
        for item in ordenes:
            data = (str(item.id), str(item.name))
            dic_ordenes.append(data)

        return dic_ordenes

    # género la lista dinámica con las solicitudes de trabajo
    @api.model
    def _compute_solicitudes_selection(self):
        company_id = self.env.company.id
        solicitudes = self.env['sicpro.app.solicitudes.oportunidades'].search(
            ['&', '&', ('active', '=', True), ('company_id', '=', company_id), ('stage_id.is_orden', '=', True)])

        oportunidades = []
        for item in solicitudes:
            data = (str(item.id), str(item.id_solicitud) + ' - ' + str(item.especialidad.name) + ' - ' + str(item.name))
            oportunidades.append(data)

        return oportunidades

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Orden de Trabajo", required=False, index=True, tracking=True, default='-')
    active = fields.Boolean('Activo', default=True, tracking=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    control_active_guardado = fields.Boolean(string='Control Active', required=False, default=False)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    tipo_orden = fields.Selection(string='Tipo de Orden',
                                  selection=[('inversiones', 'Inversiones'), ('mantenimiento', 'Mantenimiento'), ],
                                  required=True, tracking=True, default='inversiones')
    trimestre = fields.Many2one(comodel_name='sicpro.nomenclador.trimestre', string='Trimestre', required=False,
                                tracking=True)
    user_id = fields.Many2one('res.users', string='Solícita la Orden', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    estado_id = fields.Many2one('sicpro.app.ordenes.estados', string='Estados', ondelete='restrict', tracking=True,
                                group_expand='_read_group_stage_ids', index=True, copy=False,
                                default=_get_default_stage_id)
    is_paralizado = fields.Boolean('Paralizada', related='estado_id.is_paralizado')
    is_cancelado = fields.Boolean('Cancelada', related='estado_id.is_cancelado')
    is_terminada = fields.Boolean('Terminada', related='estado_id.is_terminada')
    is_en_proceso = fields.Boolean('En Proceso', related='estado_id.is_en_proceso')
    is_fecha_inicial = fields.Boolean('Estado de inicio', related='estado_id.is_fecha_inicial')
    is_preparacion_tecnica = fields.Boolean('Sin Comenzar', related='estado_id.is_preparacion_tecnica')
    etiquetas_ids = fields.Many2many('sicpro.app.ordenes.etiquetas', 'sicpro_app_ordenes_etiquetas_rel', 'orden_id',
                                     'etiqueta_id', string='Etiqueta', tracking=True)
    priority = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    as_numero = fields.Char(string='Acuerdo de Servicio', required=False, tracking=True)
    as_valor = fields.Monetary(string='Valor AS', required=False, tracking=True, currency_field='company_currency')
    ficha_costo_valor = fields.Monetary(string='Valor FC', required=False, tracking=True,
                                        currency_field='company_currency')
    avance_obra = fields.Float(string='Avance de obra', required=False, tracking=True)
    barra_avance_obra = fields.Float(string='Barra de Avance', required=False)
    motivo_paralizacion = fields.Many2one(comodel_name='sicpro.app.ordenes.paralizacion',
                                          string='Motivo de Paralización', required=False, tracking=True)
    detalles_paralizacion = fields.Text(string="Detalles de la Paralización", tracking=True)
    programa_inversiones = fields.Char(string='Programa de Inversiones', compute='_compute_programa_inversiones',
                                       tracking=True)
    clase_orden_proyecto = fields.Many2one(comodel_name='sicpro.app.ordenes.clases.proyecto', string='Clase de trabajo',
                                           required=False, tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", tracking=True)
    estado_interno = fields.Selection(string='Estado Interno', required=True, tracking=True,
                                      selection=[('borrador', 'Borrador'), ('solicitada', 'Solicitada'),
                                                 ('validada', 'Validada'), ('rechazar_solicitud', 'Rechazar Solicitud'),
                                                 ('rechazar_creacion', 'Rechazar Creación'),
                                                 ('pendiente_sap', 'Pendiente SAP'), ('creada', 'Creada'),
                                                 ('terminada', 'Terminada'), ], default='borrador')
    problemas_ids = fields.One2many(comodel_name='sicpro.app.ordenes.trabajo.anexo.problemas', inverse_name='orden_id',
                                    copy=False, string='Problemas de la Ejecución', required=False, tracking=True)
    creada_sap = fields.Boolean(string='Creada en el SAP', required=False, default=False, tracking=True)
    creada_sistema = fields.Boolean(string='Creada en el Sistema', required=False, default=False)
    consecutivo_unico_orden = fields.Integer(string='Consecutivo Único de la Orden', required=False)
    orden_principal = fields.Boolean(string='Orden Principal', required=False, default=False)
    pep_corto = fields.Char(string='Pep Corto', required=False)
    motivo_aviso_intension = fields.Text(string="Motivo del cambio", required=False, tracking=True)
    motivo_aviso_intension_enviada = fields.Boolean(string='Motivo intensión enviada', required=False, default=False)
    control_autor = fields.Boolean(string='Control_autor', related='clase_orden_proyecto.control_autor', required=False)
    orden_control_autor = fields.Selection(_compute_ordenes_control_autor_selection, string='Orden Control Autor',
                                           required=False, tracking=True)
    motivo_rechazo = fields.Text(string="Motivo del Rechazo", required=False, tracking=True)
    orden_rechazada = fields.Boolean(string='Orden_rechazada', required=False, default=False)
    grupo_crear_orden = fields.Boolean(string='grupo_crear_orden', compute='_compute_grupo_crear_orden')
    ############### CAMPOS PARA PEGAR EN SAP ###########################################################################
    sap_consecutivo = fields.Char(string='Consecutivo SAP', compute='_compute_upgrade_sap_name')
    sap_uo = fields.Char(string='Unidad Organizativa SAP', required=False, related='uo_id.abreviatura')
    sap_especialidad_id = fields.Many2one(comodel_name='sicpro.nomenclador.especialidad', string='Especialidad SAP',
                                          compute='_compute_upgrade_sap_as_especialidad')
    sap_titulo = fields.Char(string="Titulo SAP", compute='_compute_titulo_orden', store=True, compute_sudo=True,)  # OU/Provincia/Texto breve
    sap_titulo_sap = fields.Char(string="SAP Titulo SAP", compute='_compute_titulo_sap_orden', store=True)  # No.SAP/Texto Breve
    sap_pep = fields.Char(string='No. SAP', compute='_compute_upgrade_sap_pep')
    sap_fecha_solicitud_orden = fields.Date(string='Fecha de solicitud SAP',
                                            default=lambda self: fields.Date.context_today(self))
    sap_cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente SAP',
                                     compute='_compute_upgrade_sap_cliente')
    sap_as_numero = fields.Char(string='Acuerdo de Servicio SAP', compute='_compute_upgrade_sap_as_numero')
    sap_as_valor = fields.Monetary(string='Valor AS SAP', compute='_compute_upgrade_sap_as_valor',
                                   currency_field='company_currency')
    sap_ficha_costo_valor = fields.Monetary(string='Valor FC SAP', compute='_compute_upgrade_sap_ficha_costo_valor',
                                            currency_field='company_currency')
    sap_fecha_inicio_cronograma = fields.Date(string='Inicio Cronograma SAP',
                                              compute='_compute_upgrade_sap_as_inicio_cronograma')
    sap_fecha_fin_cronograma = fields.Date(string='Fin Cronograma SAP',
                                           compute='_compute_upgrade_sap_as_fin_cronograma')
    sap_id_solicitud = fields.Char(string='Id Solicitud SAP', required=False, related='solicitud_id.id_solicitud')
    sap_programa_inversiones = fields.Char(string='Programa de Inversiones sap', compute='_compute_programa_inversiones',
                                           tracking=True)
    ####################################################################################################################

    ############### TÍTULOS DE LA ORDEN ################################################################################
    texto_breve_sap = fields.Char(string="Texto breve", required=True, tracking=True)  # Nombre de la solicitud
    titulo = fields.Char(string="Titulo", compute='_compute_titulo_orden', tracking=True, compute_sudo=True,)  # OU/Provincia/Texto breve
    ####################################################################################################################

    ############### DESCRIPCIONES Y OBSERVACIONES ######################################################################
    observaciones_solicitud = fields.Text(string="Detalles de la Solicitud", required=False, tracking=True)
    observaciones_creacion = fields.Text(string="Detalles de la Creación", required=False, tracking=True)
    observaciones_actualizacion = fields.Text(string="Observaciones de la Actualización", required=False, tracking=True)
    alcance = fields.Text(string="Alcance", required=False, tracking=True)  # por defecto es el de la solicitud
    ####################################################################################################################

    ############### ORDENES AÑOS ANTERIORES ############################################################################
    anteriores_orden_id = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo', string='Orden Anteriores',
                                          required=False, domain="[('company_id', '=', company_id)]", tracking=True)
    anteriores_as_valor = fields.Monetary(string='Valor Acuerdo de Servicio Anterior', currency_field='company_currency',
                                          related='anteriores_orden_id.as_valor', tracking=True)
    anteriores_FC_valor = fields.Monetary(string='Valor Ficha de Costo Anterior', currency_field='company_currency',
                                          related='anteriores_orden_id.ficha_costo_valor', tracking=True)
    anteriores_pep = fields.Char(string='Pep Anterior', related='anteriores_orden_id.pep', tracking=True)
    ####################################################################################################################

    ############### FECHAS #############################################################################################
    mes_inicio = fields.Char(string='Mes Inicio', compute='_compute_mes_inicio_orden', required=False,
                             tracking=True)  # Calculada por la Fecha Inicio real
    mes_fin = fields.Char(string='Mes Terminada', compute='_compute_mes_fin_orden', required=False,
                          tracking=True)  # Calculada por la Fecha Fin real
    fecha_solicitud_orden = fields.Date(string='Fecha de solicitud',
                                        default=lambda self: fields.Date.context_today(self), tracking=True)
    fecha_creacion_orden = fields.Date(string='Creada en Sistema', tracking=True)
    fecha_creacion_orden_sap = fields.Date(string='Creada en SAP', tracking=True)
    fecha_cancelacion_orden = fields.Date(string='Cancelación', tracking=True)
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    fecha_inicio_cronograma = fields.Date(string='Inicio Cronograma', required=False, tracking=True)
    fecha_fin_cronograma = fields.Date(string='Fin Cronograma', required=False, tracking=True)
    fecha_fin_cronograma_original = fields.Date(string='Fecha Fin Original', required=False, tracking=True)
    fecha_inicio_real = fields.Date(string='Inicio Real', required=False,
                                    tracking=True)  # Obligatorio al cambiar a los Estados: PT o En Proceso
    fecha_fin_real = fields.Date(string='Fin Real', tracking=True)  # Obligatorio al cambiar a Estado: Terminada
    dias_instalacion = fields.Integer(string='Días de instalación', compute='_compute_dias_instalacion',
                                      required=False, tracking=True)  # fecha actual - Días Paralizados - Fecha de Inicio real
    fecha_paralizacion = fields.Date(string='Fecha de Paralización', required=False, tracking=True)
    dias_paralizacion = fields.Integer(string='Días Paralizado', compute='_compute_dias_paralizados', required=False,
                                       tracking=True)
    fecha_reinicio_paralizacion = fields.Date(string='Fecha de Reinicio', required=False, tracking=True)
    fecha_rechazada = fields.Date(string='Fecha de Rechazo', required=False, tracking=True)
    fecha_termino_orden = fields.Date(string='Terminación de la Orden', required=False, tracking=True)
    fecha_emision_proyecto = fields.Date(string='Fecha Emisión Proyecto', required=False, tracking=True)
    ####################################################################################################################

    ############### HORAS #############################################################################################
    horas_estimadas = fields.Char(string='Horas Estimadas', required=False, tracking=True)
    horas_reales = fields.Char(string='Horas Reales', required=False, tracking=True)
    ####################################################################################################################

    ############### SOLICITUD DE TRABAJO ###############################################################################
    solicitud_id = fields.Many2one(comodel_name="sicpro.app.solicitudes.oportunidades", string="Solicitudes de Trabajo",
                                   domain="['&', '&', ('active', '=', True), ('company_id', '=', company_id),"
                                          "('stage_id.is_orden', '=', True)]", required=False, tracking=True)
    solicitud_selection = fields.Selection(_compute_solicitudes_selection, string='Solicitud de Trabajo',
                                           required=True, tracking=True)
    id_solicitud = fields.Char(string='Id Solicitud', required=False, related='solicitud_id.id_solicitud')
    pep = fields.Char(string='Sap', required=True, tracking=True)
    uo_id = fields.Many2one(comodel_name='sicpro.nomenclador.territorios', string='Área', required=True, tracking=True)
    uo_abreviatura = fields.Char(string='Unidad Organizativa', required=False, related='uo_id.abreviatura', store=True)
    provincia_id = fields.Many2one(comodel_name='res.country.state', string='Provincia', required=True, store=True,
                                   domain="[('country_id.name', '=', 'Cuba')]", tracking=True)
    agrupacion_id = fields.Many2one(comodel_name='sicpro.app.trabajadores.areas', string='Asignado a', required=True,
                                    domain="[('company_id', '=', company_id)]", tracking=True)
    especialista_id = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Especialista', required=True,
                                      domain="[('company_id', '=', company_id)]", tracking=True)
    especialidad_id = fields.Many2one(comodel_name='sicpro.nomenclador.especialidad', string='Especialidad',
                                      domain="[('company_id', '=', company_id)]", required=True, tracking=True)
    especialidad_letra = fields.Char(string='Especialidad Letra', related='especialidad_id.letra')
    proyecto_id = fields.Char(string='Id de Proyecto', required=False, tracking=True)
    tarea_tecnica_id = fields.Char(string='Tarea Técnica', required=False, tracking=True)
    # Todos los campos de imagen están codificados en base64 y son compatibles con PIL
    image_1920 = fields.Image("Image", related='especialidad_id.image_1920', max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    ####################################################################################################################

    ############### INVERSIONISTA ######################################################################################
    cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente', tracking=True, index=True,
                                 domain=[('tipo_registro', '=', 'persona')], )
    cliente_territorio_id = fields.Many2one(comodel_name="sicpro.nomenclador.territorios", string="UO",
                                            related='cliente_id.territorio', required=False)
    cliente_provincia_id = fields.Many2one(comodel_name="res.country.state", string="Provincia Cliente",
                                           related='cliente_id.provincias_id', required=False)
    cliente_cargo = fields.Char(string="Cargo", related='cliente_id.cargo', required=False)
    cliente_telefono_fijo = fields.Char(string="Teléfono", related='cliente_id.telefono_fijo', required=False)
    cliente_telefono_movil = fields.Char(string="Móvil", related='cliente_id.telefono_movil', required=False)
    cliente_correo = fields.Char(string="Correo electrónico", related='cliente_id.correo', required=False)
    ####################################################################################################################
    trabajadores_ids = fields.One2many(comodel_name='sicpro.app.ordenes.trabajo.trabajadores', inverse_name='orden_id',
                                    copy=False, string='Trabajadores en la Ejecución', required=False, tracking=True)
    transporte_vehiculos_ids = fields.One2many(comodel_name='sicpro.app.ordenes.trabajo.transporte',
                                               inverse_name='orden_id',
                                    copy=False, string='Vehículos en la Ejecución', required=False, tracking=True)
    transporte_especializados_ids = fields.One2many(comodel_name='sicpro.app.ordenes.trabajo.equipos.especializados',
                                                    inverse_name='orden_id',
                                    copy=False, string='Equipos especializados en la Ejecución', required=False,
                                                    tracking=True)
    transporte_complementarios_ids = fields.One2many(comodel_name='sicpro.app.ordenes.trabajo.equipos.complementarios',
                                                     inverse_name='orden_id',
                                    copy=False, string='Equipos complementarios en la Ejecución', required=False,
                                                     tracking=True)
    trabajadores_count = fields.Integer(compute='_compute_trabajadores_count', string="Trabajadores")
    vehiculos_count = fields.Integer(compute='_compute_vehiculos_count', string="Vehículos")
    equipos_especializados_count = fields.Integer(compute='_compute_equipos_especializados_count',
                                                  string="Equipos Especializados")
    equipos_complementarios_count = fields.Integer(compute='_compute_equipos_complementarios_count',
                                                   string="Equipos Complementarios")

    # Cuenta los trabajadores según los estados configurados
    def _compute_trabajadores_count(self):
        for item in self:
            item.trabajadores_count = item.trabajadores_ids.search_count(
                ['&', ('estado.contar', '=', True), ('orden_id', '=', item.id)])

    # Cuenta los vehículos según los estados configurados
    def _compute_vehiculos_count(self):
        for item in self:
            item.vehiculos_count = item.transporte_vehiculos_ids.search_count(
                ['&', ('estado.contar', '=', True), ('orden_id', '=', item.id)])

    # Cuenta los equipos especializados según los estados configurados
    def _compute_equipos_especializados_count(self):
        for item in self:
            item.equipos_especializados_count = item.transporte_especializados_ids.search_count(
                ['&', ('estado.contar', '=', True), ('orden_id', '=', item.id)])

    # Cuenta los equipos complementarios según los estados configurados
    def _compute_equipos_complementarios_count(self):
        for item in self:
            item.equipos_complementarios_count = item.transporte_complementarios_ids.search_count(
                ['&', ('estado.contar', '=', True), ('orden_id', '=', item.id)])


    # acción del botón inteligente trabajador: no hace ninguna función
    def action_empaty_trabajadores(self, ):
        action = None

    # acción del botón inteligente vehículos: no hace ninguna función
    def action_empaty_vehiculos(self, ):
        action = None

    # acción del botón inteligente especializado: no hace ninguna función
    def action_empaty_especializados(self, ):
        action = None

    # acción del botón inteligente complementarios: no hace ninguna función
    def action_empaty_complementarios(self, ):
        action = None


    # verífica que el usuario activo pertenezca al grupo crear orden o al grupo Admin
    def _compute_grupo_crear_orden(self):
        admin = self.env['res.users'].has_group('sicpro_app_ordenes_trabajo.grupo_ordenes_admin')
        if admin:
            self.grupo_crear_orden = True
        else:
            self.grupo_crear_orden = self.env['res.users'].has_group('sicpro_app_ordenes_trabajo.grupo_ordenes_ejecutor')

    # Actualiza la solicitud desde el selection dinámico
    @api.onchange('solicitud_selection')
    def _compute_solicitud_selection(self):
        selection = int(self.solicitud_selection)
        self.solicitud_id = selection

    # verífica que las fechas de inicio y terminación real exista para poder pasar la orden a los estados configurados
    @api.constrains('estado_id')
    def _check_estados_obligatorios(self):
        if self.estado_id.is_terminada:
            # verífica que la fecha de terminación real exista para poder pasar la orden a estado terminado
            if not self.fecha_fin_real:
                raise ValidationError(_("¡Debe agregar la fecha de terminación real de la obra para continuar!. "
                                        "Si cree que es un error contacte al administrador"))
        elif self.estado_id.is_fecha_inicial or self.estado_id.is_en_proceso:
            # verífica que la fecha de inicio real exista para poder pasar la orden al estado de
            # preparación técnica o en proceso
            if not self.fecha_inicio_real:
                raise ValidationError(_("¡Debe agregar la fecha de inicio real de la obra para continuar!. "
                                        "Si cree que es un error contacte al administrador"))

    # verífico que no se repitan las especialidades en los procesos ejecutores
    @api.constrains('especialidad_id')
    def _check_especialidad_unica(self):
        if self.company_abreviatura != 'PROYECTOS':
            pep_corto = str(self.pep[:10])
            uniq = self.env['sicpro.app.ordenes.trabajo'].search(
                ['&', '&', ('active', '=', True), ("id", "!=", self.id), ('pep_corto', '=', pep_corto),
                 ('tipo_orden', '=', self.tipo_orden), ('especialidad_id', '=', self.especialidad_id.id),
                 ('company_id', '=', self.company_id.id), ('anio', '=', self.anio)])

            if uniq:
                raise ValidationError(_("¡La especialidad introducida para ese número SAP ya existe!. "
                                        "Si cree que es un error contacte al administrador"))

    # verífico que la especialidad de la orden archivada ya exista e el sistema
    @api.constrains('active')
    def _check_activo_unica(self):
        if self.company_abreviatura != 'PROYECTOS':
            pep_corto = str(self.pep[:10])
            if self.control_active_guardado:
                uniq = self.env['sicpro.app.ordenes.trabajo'].search(
                    ['&', '&', ('active', '=', True), ("id", "!=", self.id), ('pep_corto', '=', pep_corto),
                     ('tipo_orden', '=', self.tipo_orden), ('especialidad_id', '=', self.especialidad_id.id),
                     ('company_id', '=', self.company_id.id), ('anio', '=', self.anio)])

                if uniq:
                    raise ValidationError(
                        _("¡No se puede desarchivar, la especialidad de la orden para ese número SAP ya "
                          "existe!. Si cree que es un error contacte al administrador"))

    # chequea que la fecha fin real no sea anterior a la inicial real
    @api.constrains('fecha_inicio_real', 'fecha_fin_real')
    def _check_fecha_inicio_fin_real(self):
        for item in self:
            if item.fecha_fin_real and item.fecha_inicio_real:
                if item.fecha_fin_real < item.fecha_inicio_real:
                    raise ValidationError(_('La fecha fin real no puede ser anterior a la fecha de inicio real.'))

    # chequea que la fecha fin cronograma no sea anterior a la inicio cronograma
    @api.constrains('fecha_inicio_cronograma', 'fecha_fin_cronograma')
    def _check_fecha_inicio_fin_cronograma(self):
        for item in self:
            if item.fecha_fin_cronograma and item.fecha_inicio_cronograma:
                if item.fecha_fin_cronograma < item.fecha_inicio_cronograma:
                    raise ValidationError(_('La fecha fin del cronograma no puede ser anterior a la fecha de inicio '
                                            'del cronograma.'))

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
                diferencia = hoy - item.fecha_paralizacion
                item.dias_paralizacion = diferencia.days
            else:
                if item.fecha_paralizacion and item.fecha_reinicio_paralizacion:
                    diferencia = item.fecha_reinicio_paralizacion - item.fecha_paralizacion
                    item.dias_paralizacion = diferencia.days
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
    @api.onchange('pep', 'texto_breve_sap')
    def _compute_titulo_sap_orden(self):
        for item in self:
            if item.pep and item.texto_breve_sap:
                item.sap_titulo_sap = str(item.pep) + '/' + str(item.texto_breve_sap)
            else:
                item.sap_titulo_sap = '-'

    # crea el titulo de la orden
    @api.onchange('uo_abreviatura', 'provincia_id', 'texto_breve_sap')
    def _compute_titulo_orden(self):
        for item in self:
            if item.uo_abreviatura and item.provincia_id and item.texto_breve_sap:
                item.titulo = str(item.uo_abreviatura) + '/' + str(item.provincia_id.name) + '/' + str(item.texto_breve_sap)
                item.sap_titulo = str(item.uo_abreviatura) + '/' + str(item.provincia_id.name) + '/' + str(
                    item.texto_breve_sap)
            else:
                item.titulo = '-'
                item.sap_titulo = '-'

    # actualiza los datos de la solicitud de trabajo
    @api.onchange('solicitud_id')
    def _upgrade_solicitud_trabajo(self):
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

    # actualiza los datos del consecutivo SAP
    @api.onchange('name')
    def _compute_upgrade_sap_name(self):
        self.sap_consecutivo = self.name

    # actualiza los datos del pep SAP
    @api.onchange('pep')
    def _compute_upgrade_sap_pep(self):
        self.sap_pep = self.pep

    # genero el programa de inversiones de la orden de trabajo
    @api.onchange('pep')
    def _compute_programa_inversiones(self):
        if self.pep:
            pep = str(self.pep)
            consecutivo = pep[:2]
            consecutivo_int = int(consecutivo)
            territorio = pep[5:7]
            programa = self.env['sicpro.app.ordenes.programa.inversiones'].search(
                ['&', '&', ('active', '=', True), ('consecutivo', '=', consecutivo_int),
                 ('company_id', '=', self.company_id.id)])
            if programa:
                nomenclador = territorio + ' ' + programa.name
                self.programa_inversiones = nomenclador
                self.sap_programa_inversiones = nomenclador
            else:
                self.programa_inversiones = 'No se encontró ninguna coincidencia para el programa de inversiones'
                self.sap_programa_inversiones = 'No se encontró ninguna coincidencia para el programa de inversiones'
        else:
            self.programa_inversiones = '-'
            self.sap_programa_inversiones = '-'

            # actualiza los datos del inversionista SAP

    @api.onchange('cliente_id')
    def _compute_upgrade_sap_cliente(self):
        self.sap_cliente_id = self.cliente_id

    # actualiza los datos del acuerdo de servicio SAP
    @api.onchange('as_numero')
    def _compute_upgrade_sap_as_numero(self):
        self.sap_as_numero = self.as_numero

    # actualiza los datos del valor del acuerdo de servicio SAP
    @api.onchange('as_valor')
    def _compute_upgrade_sap_as_valor(self):
        self.sap_as_valor = self.as_valor

    # actualiza los datos de la ficha de costo SAP
    @api.onchange('ficha_costo_valor')
    def _compute_upgrade_sap_ficha_costo_valor(self):
        self.sap_ficha_costo_valor = self.ficha_costo_valor

    # actualiza los datos de la fecha de inicio por cronograma SAP
    @api.onchange('fecha_inicio_cronograma')
    def _compute_upgrade_sap_as_inicio_cronograma(self):
        self.sap_fecha_inicio_cronograma = self.fecha_inicio_cronograma

    # actualiza los datos de la fecha de fin por cronograma SAP
    @api.onchange('fecha_fin_cronograma')
    def _compute_upgrade_sap_as_fin_cronograma(self):
        self.sap_fecha_fin_cronograma = self.fecha_fin_cronograma

    # actualiza los datos de la especialidad SAP
    @api.onchange('especialidad_id')
    def _compute_upgrade_sap_as_especialidad(self):
        self.sap_especialidad_id = self.especialidad_id

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # actualiza los datos después de crear la orden en SAP
    @api.onchange('creada_sap')
    def _upgrade_creada_sap(self):
        if self.estado_interno == 'pendiente_sap':
            orden_id = self.env['sicpro.app.ordenes.trabajo'].sudo().search([('id', '=', self._origin.id)])
            orden_id.write(
                {'creada_sap': True, 'fecha_creacion_orden_sap': datetime.today(), 'estado_interno': 'creada'})

    # action para ver la orden asociada de proyecto
    def orden_asociada_proyectos_view(self):
        if not self.proyecto_id:
            raise AccessError(_("El campo de la orden asociada de proyecto esta vació."))
        else:
            ordenes_buscar = self.env['sicpro.app.ordenes.trabajo'].search(
                [('active', '=', True), ('name', '=', self.proyecto_id)], limit=1)
            if ordenes_buscar:
                domain = ['&', ('active', '=', True), ('name', '=', ordenes_buscar.name)]
                return {'name': _('Orden de Proyecto'), 'domain': domain, 'res_model': 'sicpro.app.ordenes.trabajo',
                        'type': 'ir.actions.act_window', 'view_id': False, 'view_mode': 'tree,form', 'limit': 80, }
            else:
                raise AccessError(_("No existe la orden asociada de proyecto en el sistema."))

    # botón para solicitar la orden
    def action_solicitar_orden(self):
        if self.orden_rechazada:
            self.fecha_rechazada = None
            self.motivo_rechazo = None
            self.orden_rechazada = False

        self.estado_interno = 'solicitada'
        # busco usuarios del rol validar del proceso específico de la orden
        proceso = self.company_id
        validar = self.env.ref('sicpro_app_ordenes_trabajo.grupo_ordenes_validar').users
        # agrego los seguidores al modelo
        for item in validar:
            if item.company_id == proceso:
                self.message_subscribe(partner_ids=item.partner_id.ids)
        # envío la notificación
        self.message_post(body='Solicitud de Orden', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_nueva_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
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
        crear = self.env.ref('sicpro_app_ordenes_trabajo.grupo_ordenes_ejecutor').users
        # agrego los seguidores al modelo
        for item in crear:
            if item.company_id == proceso:
                self.message_subscribe(partner_ids=item.partner_id.ids)
        # envío la notificación
        self.message_post(body='Solicitud de Orden', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_solicitud_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
        return action

    # botón para crear la orden
    def action_crear_orden(self):
        global orden, valor, num_as
        self.fecha_creacion_orden = datetime.today()
        self.estado_interno = 'pendiente_sap'

        pep_corto = str(self.pep[:10])
        anio = str(self.anio[2:4])
        # busco el consecutivo que le corresponde
        consecutivo = self.env['sicpro.app.ordenes.consecutivos'].search(
            ['&', '&', ('active', '=', True), ('tipo', '=', self.tipo_orden), ('company_id', '=', self.company_id.id)])
        nomenclador = consecutivo.name
        moneda = consecutivo.moneda
        clase = self.clase_orden_proyecto.name
        especialidad = self.especialidad_letra
        # busco que ya exista el pep para asignarlo al consecutivo
        ordenes_buscar = self.env['sicpro.app.ordenes.trabajo'].search(
            ['|', ('active', '=', True), ('active', '=', False), ('company_id', '=', self.company_id.id),
             ('creada_sistema', '=', True), ('anio', '=', self.anio), ('tipo_orden', '=', self.tipo_orden),
             ('orden_principal', '=', True), ('pep_corto', '=', pep_corto)], limit=1)

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
            ordenes_count = self.env['sicpro.app.ordenes.trabajo'].search_count(
                ['|', ('active', '=', True), ('active', '=', False), ('creada_sistema', '=', True),
                 ('tipo_orden', '=', self.tipo_orden), ('company_id', '=', self.company_id.id),
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
        self.message_post(body='Orden Creada', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_crear_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

        # envío correo de aviso al proyectista de la orden
        for participante in self.solicitud_id:
            # envío el correo electrónico
            email_values = {'email_to': participante.especialista_ejecutor.user_id.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_asociada_orden_proyectos')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    # botón para pasar a sin comenzar la orden
    def action_sin_comenzar_orden(self):
        estado = self.env['sicpro.app.ordenes.estados'].search(
            ['&', ('is_fecha_inicial', '=', True), ('company_id', '=', self.company_id.id)]).id
        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    # botón para pasar a en proceso la orden
    def action_en_proceso_orden(self):
        estado = self.env['sicpro.app.ordenes.estados'].search(
            ['&', ('is_en_proceso', '=', True), ('company_id', '=', self.company_id.id)]).id
        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    # botón para reiniciar la orden
    def action_reiniciar_orden(self):
        self.fecha_reinicio_paralizacion = datetime.today()
        estado = self.env['sicpro.app.ordenes.estados'].search(
            ['&', ('is_en_proceso', '=', True), ('company_id', '=', self.company_id.id)]).id
        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    # botón para terminar la orden
    def action_terminar_orden(self):
        self.estado_interno = 'terminada'
        self.fecha_termino_orden = datetime.today()
        estado = self.env['sicpro.app.ordenes.estados'].search(
            ['&', ('is_terminada', '=', True), ('company_id', '=', self.company_id.id)]).id
        self.write({'estado_id': estado, })
        # envío la notificación
        self.message_post(body='La Orden cambio', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    @api.model
    def create(self, vals):
        res = super(OrdenesTrabajo, self).create(vals)
        res['control_active_guardado'] = True
        return res

# trabajadores en la ejecución
class OrdenesTrabajoTrabajadores(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.trabajadores'
    _order = "id asc"
    _description = 'Trabajadores en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Trabajador', required=True,
                           tracking=True)
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden', required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    estado = fields.Many2one(comodel_name='sicpro.app.ordenes.estados.trabajador', string='Estado', required=True,
                           tracking=True)
    company_id_orden = fields.Many2one('res.company', string='Proceso Ejecutor', related='orden_id.company_id')

# Transporte en la ejecución
class OrdenesTrabajoTransporte(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.transporte'
    _order = "id asc"
    _description = 'Transporte en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general', string='Transporte', required=True,
                           tracking=True)
    tipo_vehiculo_id_domain = fields.Char(compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden', required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    estado = fields.Many2one(comodel_name='sicpro.app.ordenes.estados.transporte.equipos', string='Estado',
                             domain="[('tipo', '=', 'vehiculo')]", required=True, tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre', string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico', compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo', related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('name')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            ['&', ('active', '=', True), ('name', '=', 'vehiculo')])

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                dic.append(str(rec.grupoEquipoNombre),)

            item.tipo_vehiculo_id_domain = json.dumps([('grupoEquipoNombre', 'in', dic)])

# Equipos especializados de la construcción en la ejecución
class OrdenesTrabajoEquiposEspecializados(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.equipos.especializados'
    _order = "id asc"
    _description = 'Equipos especializados en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general', string='Transporte', required=True,
                           tracking=True)
    tipo_vehiculo_id_domain = fields.Char(compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden', required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    estado = fields.Many2one(comodel_name='sicpro.app.ordenes.estados.transporte.equipos', string='Estado',
                             domain="[('tipo', '=', 'equipo_especializado')]", required=True, tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre', string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico', compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo', related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('name')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            ['&', ('active', '=', True), ('name', '=', 'equipo_especializado')])

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                dic.append(str(rec.grupoEquipoNombre),)

            item.tipo_vehiculo_id_domain = json.dumps([('grupoEquipoNombre', 'in', dic)])

# Equipos complementarios en la ejecución
class OrdenesTrabajoEquiposComplementarios(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.equipos.complementarios'
    _order = "id asc"
    _description = 'Equipos complemtarios en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.transporte.general', string='Transporte', required=True,
                           tracking=True)
    tipo_vehiculo_id_domain = fields.Char(compute="_compute_tipo_vehiculo_id_domain", store=False, )
    detalles = fields.Text(string="Detalles", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden', required=False, index=True)
    fecha_inicio = fields.Date(string="Inicio", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Salida", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    estado = fields.Many2one(comodel_name='sicpro.app.ordenes.estados.transporte.equipos', string='Estado',
                             domain="[('tipo', '=', 'equipo_complementario')]", required=True, tracking=True)
    vehiculo_combustible = fields.Char(related='name.combustibleNombre', string='Combustible', readonly=True)
    vehiculo_estado_siptc = fields.Char(string='Estado Técnico', compute='_compute_estado_siptc')
    vehiculo_estaActivo = fields.Char(string='Activo', related='name.estaActivo')

    # buscar si el equipo complementario está activo en SIPTC
    @api.depends('vehiculo_estaActivo')
    def _compute_estado_siptc(self):
        for item in self:
            if item.vehiculo_estaActivo != 'No':
                item.vehiculo_estado_siptc = 'Activo'
            else:
                item.vehiculo_estado_siptc = 'Paralizado'

    @api.depends('name')
    def _compute_tipo_vehiculo_id_domain(self):
        grupo = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            ['&', ('active', '=', True), ('name', '=', 'equipo_complementario')])

        for item in self:
            dic = []
            for rec in grupo.grupo_vehiculos:
                dic.append(str(rec.grupoEquipoNombre),)

            item.tipo_vehiculo_id_domain = json.dumps([('grupoEquipoNombre', 'in', dic)])

# problemas de la ejecución
class OrdenesTrabajoAnexoProblemas(models.Model):
    _name = 'sicpro.app.ordenes.trabajo.anexo.problemas'
    _order = "id desc"
    _description = 'Tabla anexo de los problemas en la ejecución'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.ordenes.problemas', string='Problemas', required=False,
                           tracking=True)
    detalles_problema = fields.Text(string="Detalles del problema", tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    orden_id = fields.Many2one('sicpro.app.ordenes.trabajo', 'Orden', required=False, index=True)
    fecha_inicio = fields.Date(string="Comienzo", required=True, default=lambda self: fields.Datetime.now())
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    fecha_fin = fields.Date(string="Resuelto", required=False, )
    estado = fields.Selection(string='Estado', selection=[('resuelto', 'Resuelto'), ('no_resuelto', 'No Resuelto'), ],
                              required=True, default='no_resuelto')

    # Actualizo la fecha fin de resuelto el problema
    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado == 'resuelto':
            self.fecha_fin = datetime.today()
        else:
            self.fecha_fin = None


# motivo de paralización
class OrdenesTrabajoMotivoParalizacion(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.paralizacion'
    _description = 'Motivo de la paralización de la orden de trabajo'

    motivo_id = fields.Many2one(comodel_name='sicpro.app.ordenes.paralizacion', string="Motivo", required=True)
    detalles_paralizacion = fields.Text(string="Detalles de la Paralización", required=True)

    def action_motivo_paralizacion(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(self.env.context.get('active_ids'))
        for item in orden.sudo():
            estado = self.env['sicpro.app.ordenes.estados'].search(
                ['&', ('is_paralizado', '=', True), ('company_id', '=', item.company_id.id)]).id

            item.motivo_paralizacion = self.motivo_id
            item.detalles_paralizacion = self.detalles_paralizacion
            item.fecha_reinicio_paralizacion = None
            item.fecha_paralizacion = datetime.today()
            item.estado_id = estado

        # envío la notificación
        orden.message_post(body='Orden Paralizada', message_type='notification', subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
        return action


# motivo de rechazo
class OrdenesTrabajoMotivoRechazo(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.rechazadas'
    _description = 'Motivo de rechazo de la orden de trabajo'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(self.env.context.get('active_ids'))
        for item in orden.sudo():
            item.orden_rechazada = True
            item.fecha_rechazada = datetime.today()
            if item.estado_interno == 'solicitada':
                item.motivo_rechazo = 'La orden no fue validada, se rechazó él ' + \
                                      str(format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + \
                                      str(self.motivo_id)
                item.estado_interno = 'rechazar_solicitud'
            elif item.estado_interno == 'validada':
                item.motivo_rechazo = 'La orden no fue creada, se rechazó él ' + \
                                      str(format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + \
                                      str(self.motivo_id)
                item.estado_interno = 'rechazar_creacion'

        # envío la notificación
        orden.message_post(body='Orden Rechazada', message_type='notification', subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_rechazo_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
        return action


# motivo de cancelación
class OrdenesTrabajoMotivoCancelacion(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.canceladas'
    _description = 'Motivo de cancelación de la orden de trabajo'

    motivo_id = fields.Text(string="Motivo de Cancelación", required=True)

    def action_motivo_cancelacion(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(self.env.context.get('active_ids'))
        for item in orden.sudo():
            estado = self.env['sicpro.app.ordenes.estados'].search(
                ['&', ('is_cancelado', '=', True), ('company_id', '=', item.company_id.id)]).id

            item.motivo_cancelacion = self.motivo_id
            item.fecha_cancelacion_orden = datetime.today()
            item.estado_id = estado

        # envío la notificación
        orden.message_post(body='Orden Cancelada', message_type='notification', subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
        return action


# aviso de intensión
class OrdenesTrabajoAvisoIntension(models.TransientModel):
    _name = 'sicpro.app.ordenes.trabajo.aviso.intension'
    _description = 'Aviso de intensión de la orden de trabajo'

    nueva_fecha = fields.Date(string="Nueva fecha", required=True, )
    motivo_aviso_intension = fields.Text(string="Motivo del cambio", required=True)

    def action_motivo_cambio(self):
        orden = self.env['sicpro.app.ordenes.trabajo'].browse(self.env.context.get('active_ids'))
        for item in orden.sudo():
            item.fecha_fin_cronograma_original = item.fecha_fin_cronograma
            item.fecha_fin_cronograma = self.nueva_fecha
            item.motivo_aviso_intension_enviada = True
            item.motivo_aviso_intension = 'La fecha fin de la obra por el cronograma estaba prevista para él ' + \
                                          str(format_date(self.env, item.fecha_fin_cronograma_original)) + \
                                          ', fue necesario modificarla para él ' \
                                          + str(format_date(self.env, self.nueva_fecha)) + \
                                          ' por los siguientes motivos: ' + str(self.motivo_aviso_intension)

        # envío la notificación
        orden.message_post(body='Aviso de Intensión.', message_type='notification', subtype_xmlid='mail.mt_comment',
                           author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in orden.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_aviso_intension_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_ordenes_trabajo.ordenes_trabajo_action').sudo().read()[0]
        return action