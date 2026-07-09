# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class MetrologiaEquipos(models.Model):
    _name = 'sicpro.app.metrologia.equipos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipos de metrología'
    _order = 'tarjeta asc, id asc'
    _check_company_auto = True

    def _default_stage(self):
        return self.env['sicpro.app.metrologia.estado.tecnico'].search([],
                                                                       limit=1)

    def _get_default_team_id(self):
        MT = self.env['sicpro.app.metrologia.direcciones']
        team = MT.search([('company_id', '=', self.env.company.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id

    name = fields.Char(string='Nombre del Equipo', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Activo', default=True, index=True)
    medicion = fields.Char(string="Limite de Medición", required=False,
                           tracking=True)
    presicion = fields.Char(string="Precisión", required=False, tracking=True)
    marca = fields.Char(string="Marca", required=True, tracking=True)
    model = fields.Char(string="Modelo")
    pais_equipo = fields.Many2one('res.country', string="País del Equipo")
    unidad_medida = fields.Char(string="Unidad de Medida")
    serial_no = fields.Char(string='Nº de Serie', copy=False)
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('calibracion', 'Calibración'),
                                       ('verificacion', 'Verificación'), ], )
    magnitud = fields.Many2one(comodel_name="sicpro.app.metrologia.magnitud",
                               string="Magnitud", required=True,
                               tracking=True, )
    area = fields.Char(string="Área", tracking=True)
    fecha_alta = fields.Date(string='Fecha de Alta', tracking=True)
    fecha_baja = fields.Date(string='Fecha de Baja', tracking=True)
    inventario = fields.Char(string="Inventario", required=True, tracking=True)
    centro_costo = fields.Many2one('sicpro.nomenclador.centro.costo',
                                   string="Centro de Costo", tracking=True,
                                   required=True)
    local = fields.Many2one('sicpro.nomenclador.locales', string="Local",
                            tracking=True)
    inmovilizado = fields.Char(string="Inmovilizado", required=True,
                               tracking=True)
    tarjeta = fields.Char(string="Tarjeta de Control", tracking=True,
                          required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Trabajador', tracking=True,
                                    domain="[('company_id', '=', company_id),]", )
    equipo_mantenimiento_id = fields.Many2one(
        'sicpro.app.metrologia.direcciones', string='Equipos', required=True,
        default=_get_default_team_id, check_company=True)
    gestores_procesos = fields.Many2many('sicpro.app.trabajadores',
                                         'sicpro_app_metrologia_gestores_rel',
                                         related='equipo_mantenimiento_id.gestores',
                                         string='Gestores de Procesos')
    usuario_gestor = fields.Many2one(comodel_name='res.users',
                                     string='Usuario_gestor',
                                     related="gestores_procesos.user_id")
    gestor_id = fields.Many2one('sicpro.app.trabajadores',
                                string='Gestor de Equipos', tracking=True,
                                required=True,
                                domain="[('id', '=', gestores_procesos)]")
    centro_calibracion = fields.Many2one(
        comodel_name="sicpro.app.metrologia.centro.calibracion",
        string="Centro de Calibración", required=True, tracking=True, )
    # Todos los campos de imagen están codificados en base64 y
    image_1_1920 = fields.Image("Imagen anterior", max_width=1920,
                                max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1_1024 = fields.Image("Image 1024", related="image_1_1920",
                                max_width=1024, max_height=1024, store=True)
    image_1_512 = fields.Image("Image 512", related="image_1_1920",
                               max_width=512, max_height=512, store=True)
    image_1_256 = fields.Image("Image 256", related="image_1_1920",
                               max_width=256, max_height=256, store=True)
    image_1_128 = fields.Image("Image 128", related="image_1_1920",
                               max_width=128, max_height=128, store=True)
    # Todos los campos de imagen están codificados en base64
    image_2_1920 = fields.Image("Imagen posterior", max_width=1920,
                                max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_2_1024 = fields.Image("Image. 1024", related="image_2_1920",
                                max_width=1024, max_height=1024, store=True)
    image_2_512 = fields.Image("Image. 512", related="image_2_1920",
                               max_width=512, max_height=512, store=True)
    image_2_256 = fields.Image("Image. 256", related="image_2_1920",
                               max_width=256, max_height=256, store=True)
    image_2_128 = fields.Image("Image. 128", related="image_2_1920",
                               max_width=128, max_height=128, store=True)
    fecha_ultimo_mtto = fields.Date(string='Último Mtto', required=True,
                                    default=fields.Date.context_today)
    fecha_siguiente_mtto = fields.Date(compute='_compute_next_maintenance',
                                       string='Siguiente Mtto', store=True)
    frecuencia_mtto = fields.Integer(string='Frecuencia del Mtto',
                                     related="magnitud.vigencia", store=True)
    frecuencia_dias_mtto = fields.Integer(string='Días', store=True,
                                          related="magnitud.dias")
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')
    costo_equipo = fields.Monetary(string='Costo del Equipo', tracking=True,
                                   currency_field='company_currency',
                                   required=False)
    notas = fields.Text(string='Notas')
    fecha_expiracion_garantia = fields.Date(string='Fin de Garantía')
    estado_id = fields.Many2one('sicpro.app.metrologia.estado.tecnico',
                                string='Estado', ondelete='restrict',
                                tracking=True,
                                group_expand='_read_group_stage_ids',
                                default=_default_stage, copy=False)
    estado_laboratorio = fields.Boolean(related="estado_id.laboratorio")
    estado_sin_calibrar = fields.Boolean(related="estado_id.sin_calibrar")
    estado_baja = fields.Boolean(related="estado_id.baja")
    transferencias_ids = fields.One2many(
        'sicpro.app.metrologia.equipos.transferencias', 'name',
        'Transferencias', )
    transferencia_pendiente = fields.Boolean(string="Transferencia Pendiente",
                                             store=True,
                                             compute="_compute_transferencia_pendiente")
    aviso_mtto = fields.Boolean()
    mes_enero = fields.Char(string='Enero', required=False, compute_sudo=True,
                            compute='mes_anio_formated', store=True)
    mes_febrero = fields.Char(string='Febrero', compute_sudo=True,
                              compute='mes_anio_formated', store=True)
    mes_marzo = fields.Char(string='Marzo', compute_sudo=True,
                            compute='mes_anio_formated', store=True)
    mes_abril = fields.Char(string='Abril', compute_sudo=True,
                            compute='mes_anio_formated', store=True)
    mes_mayo = fields.Char(string='Mayo', compute_sudo=True,
                           compute='mes_anio_formated', store=True)
    mes_junio = fields.Char(string='Junio', compute_sudo=True,
                            compute='mes_anio_formated', store=True)
    mes_julio = fields.Char(string='Julio', compute_sudo=True,
                            compute='mes_anio_formated', store=True)
    mes_agosto = fields.Char(string='Agosto', compute_sudo=True,
                             compute='mes_anio_formated', store=True)
    mes_septiembre = fields.Char(string='Septiembre', compute_sudo=True,
                                 compute='mes_anio_formated', store=True)
    mes_octubre = fields.Char(string='Octubre', compute_sudo=True,
                              compute='mes_anio_formated', store=True)
    mes_noviembre = fields.Char(string='Noviembre', compute_sudo=True,
                                compute='mes_anio_formated', store=True)
    mes_diciembre = fields.Char(string='Diciembre', compute_sudo=True,
                                compute='mes_anio_formated', store=True)
    anio_mtto = fields.Char(string='Año', required=False, compute_sudo=True,
                            compute='mes_anio_formated', store=True)

    # marca con X según el mes a ejecutar la calibración
    @api.onchange('fecha_ultimo_mtto')
    def mes_anio_formated(self):
        for item in self:
            mes = item.fecha_siguiente_mtto.strftime("%m")
            if mes == '01':
                item.mes_enero = 'X'
            else:
                item.mes_enero = None
            if mes == '02':
                item.mes_febrero = 'X'
            else:
                item.mes_febrero = None
            if mes == '03':
                item.mes_marzo = 'X'
            else:
                item.mes_marzo = None
            if mes == '04':
                item.mes_abril = 'X'
            else:
                item.mes_abril = None
            if mes == '05':
                item.mes_mayo = 'X'
            else:
                item.mes_mayo = None
            if mes == '06':
                item.mes_junio = 'X'
            else:
                item.mes_junio = None
            if mes == '07':
                item.mes_julio = 'X'
            else:
                item.mes_julio = None
            if mes == '08':
                item.mes_agosto = 'X'
            else:
                item.mes_agosto = None
            if mes == '09':
                item.mes_septiembre = 'X'
            else:
                item.mes_septiembre = None
            if mes == '10':
                item.mes_octubre = 'X'
            else:
                item.mes_octubre = None
            if mes == '11':
                item.mes_noviembre = 'X'
            else:
                item.mes_noviembre = None
            if mes == '12':
                item.mes_diciembre = 'X'
            else:
                item.mes_diciembre = None
            item.anio_mtto = item.fecha_siguiente_mtto.strftime("%Y")

    # cron para la verificación de la fecha de mantenimiento de los equipos
    def cron_ejecutar_aviso_mtto(self):
        # Busco él, id del estado: sin calibrar
        estado = self.env['sicpro.app.metrologia.estado.tecnico'].search(
            [('sin_calibrar', '=', True)]).id
        # actualizo los gestores
        equipos_tecnicos = self.env[
            'sicpro.app.metrologia.direcciones'].search(
            [('id', '=', self.equipo_mantenimiento_id.id), ])
        correos = ''
        for follower in equipos_tecnicos:
            correos += str(follower.gestores.user_id.email_formatted)

        # realizo comparación de fechas
        dias = 30
        proximo_mes = fields.Date.context_today(self) + relativedelta(
            days=dias)
        equipos = self.env['sicpro.app.metrologia.equipos'].search(
            [('estado_baja', '=', False)])
        for mtto in equipos:
            if fields.Date.context_today(
                self) < mtto.fecha_siguiente_mtto < proximo_mes:
                equipos_tecnicos = self.env[
                    'sicpro.app.metrologia.direcciones'].search(
                    [('id', '=', mtto.equipo_mantenimiento_id.id), ])

                # verífico el estado del tiempo de mantenimiento para enviar los correos de aviso
                if not mtto.aviso_mtto:
                    for participante in equipos_tecnicos.gestores:
                        # envío el correo electrónico
                        local_context = self.env.context.copy()
                        email_values = {
                            'email_to': participante.user_id.email_formatted, }
                        template = self.env.ref(
                            'sicpro_app_metrologia.metrologia_aviso_mantenimiento')
                        template.with_context(local_context).send_mail(mtto.id,
                                                                       force_send=True,
                                                                       email_values=email_values)
                # paso a true para no enviar mas el aviso
                mtto.aviso_mtto = True
                # paso a no calibrado el equipo con 30 días de espera
                mtto.estado_id = estado
            else:
                mtto.aviso_mtto = False

    @api.depends('transferencias_ids.pendiente')
    def _compute_transferencia_pendiente(self):
        if self.transferencias_ids:
            for pendiente in self.transferencias_ids:
                if pendiente.pendiente:
                    self.transferencia_pendiente = True
                else:
                    self.transferencia_pendiente = False
        else:
            self.transferencia_pendiente = False

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

    @api.depends('fecha_ultimo_mtto', 'frecuencia_mtto')
    def _compute_next_maintenance(self):
        sabado = 6
        domingo = 7
        for item in self:
            fecha = item.fecha_ultimo_mtto + relativedelta(
                days=item.frecuencia_dias_mtto)
            nombre_dia = fecha.isoweekday()

            if nombre_dia == sabado:
                item.fecha_siguiente_mtto = fecha + relativedelta(days=2)
            elif nombre_dia == domingo:
                item.fecha_siguiente_mtto = fecha + relativedelta(days=1)
            else:
                item.fecha_siguiente_mtto = fecha

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.equipo_mantenimiento_id:
            if self.equipo_mantenimiento_id.company_id and not self.equipo_mantenimiento_id.company_id.id == self.company_id.id:
                self.equipo_mantenimiento_id = False

    @api.onchange('trabajador_id')
    def _onchange_trabajador_id(self):
        self.centro_costo = self.trabajador_id.centro_costo
        # se necesita configurar en Trabajadores
        # self.local = self.trabajador_id.local_id.name
        self.area = self.trabajador_id.area_id.name

    @api.constrains('serial_no')
    def _check_unique_serial_no(self):
        for record in self:
            if record.serial_no:
                # Limpiamos espacios y comparamos sin importar mayúsculas
                # Esto es vital para números de serie técnicos
                serial_clean = record.serial_no.strip()

                duplicate = self.search([('serial_no', '=ilike', serial_clean),
                    ('id', '!=', record.id)], limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Error de Inventario! Ya existe un equipo con el número de serie '%s'.\n"
                        "Si cree que es un error o el equipo fue dado de baja anteriormente, "
                        "contacte al administrador de SICPRO." % serial_clean + MSG_SOPORTE_SICPRO)


class MetrologiaEquiposTransferencias(models.Model):
    _name = 'sicpro.app.metrologia.equipos.transferencias'
    _description = 'Transferencias de Gastos de los Equipos'
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.metrologia.equipos', 'Equipos',
                           required=False, index=True)
    centro_calibracion = fields.Many2one(
        comodel_name="sicpro.app.metrologia.centro.calibracion",
        string="Centro de Calibración", required=True, tracking=True, )
    transferencia_numero = fields.Char(string='Transferencia', tracking=True,
                                       required=True)
    fecha_recogida_laboratorio = fields.Date(string='Recogida del Laboratorio',
                                             tracking=True, )
    fecha_entrega_economia = fields.Date(string='Entrega a Economía',
                                         tracking=True, )
    fecha_recogida_economia = fields.Date(string='Recogida en Economía',
                                          tracking=True, )
    fecha_entrega_laboratorio = fields.Date(string='Entrega en Laboratorio',
                                            tracking=True, )
    tipo_moneda = fields.Many2one('res.currency', string='Moneda', )
    monto = fields.Monetary(string='Monto', tracking=True, required=True,
                            currency_field='tipo_moneda', )
    anio = fields.Char(string="Año", required=False,
                       default=lambda self: fields.Date.today().strftime(
                           "%Y"), )
    pendiente = fields.Boolean(string="Pendiente", default=True)

    @api.onchange('fecha_entrega_economia', 'fecha_recogida_economia')
    def _onchange_fecha_recogida_economia(self):
        if self.fecha_entrega_economia:
            if self.fecha_recogida_economia:
                self.pendiente = False
            else:
                self.pendiente = True
        else:
            self.pendiente = False
