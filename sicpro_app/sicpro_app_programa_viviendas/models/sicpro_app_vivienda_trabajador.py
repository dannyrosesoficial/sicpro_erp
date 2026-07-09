# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import json
from datetime import datetime
from random import randint
from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date


def _default_color():
    return randint(1, 11)


PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class ViviendaTrabajador(models.Model):
    _name = 'sicpro.app.vivienda.trabajador'
    _description = 'Programa de la vivienda'
    _rec_name = 'trabajador_id'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = "escalafon asc, prioridad asc, trabajador_id asc"

    # Es necesario para la inicialización la incorporación del campo id
    id = fields.Id()

    trabajador_id = fields.Many2one('sicpro.app.trabajadores', string="Trabajador", required=True,
                                    copy=False,
                                    domain="[('seccion_sindical_id', '=', user_id_seccion_sindical)]")
    name = fields.Char(string='Nombre', related='trabajador_id.name',
                       required=False)
    plaza_id = fields.Char(string="# Plaza", related='trabajador_id.plaza_id')
    telefono_trabajo = fields.Char(string='Teléfono Trabajo',
                                   related='trabajador_id.telefono_trabajo')
    movil_trabajo = fields.Char(string='Móvil Trabajo',
                                related='trabajador_id.movil_trabajo')
    correo_trabajo = fields.Char(string='Correo Trabajo',
                                 related='trabajador_id.correo_trabajo')
    company_id_trabajador = fields.Many2one('res.company',
                                            string='Proceso del Trabajador',
                                            related='trabajador_id.company_id')
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', string='Departamento',
                              related='trabajador_id.area_id')
    parent_id = fields.Many2one('sicpro.app.trabajadores', string='Jefe Inmediato',
                                related='trabajador_id.parent_id')
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   string='Puesto de trabajo',
                                   related='trabajador_id.ocupacion_id')
    inicio_contrato = fields.Date(string="Inicio del Contrato",
                                  related='trabajador_id.inicio_contrato')
    direccion_carnet = fields.Char(string="Dirección CI",
                                   related='trabajador_id.direccion_carnet')
    identification_id = fields.Char(string='Carnet de Identidad',
                                    related='trabajador_id.identification_id')
    ocupacion_titulo = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
        related='trabajador_id.ocupacion_titulo')
    clase_contrato = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias',
        string='Clase de Contrato', related='trabajador_id.clase_contrato')
    categoria_ocupacional = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias', required=False,
        string='Categoría Ocupacional',
        related='trabajador_id.categoria_ocupacional')
    # Todos los campos de imagen están codificados en base64 y son compatibles con PIL
    image_1920 = fields.Image("Image", related='trabajador_id.image_1920',
                              max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)

    sequence_consecutivo = fields.Char(string='Secuencia de la solicitud',
                                       copy=False, readonly=True)
    user_id = fields.Many2one('res.users', string='Solicitado por', index=True,
                              copy=False, default=lambda self: self.env.uid)
    user_id_seccion_sindical = fields.Many2one('sicpro.nomenclador.sindicato',
                                               string='Sindicato',
                                               related='user_id.trabajador.seccion_sindical_id',
                                               store=True)
    descripcion = fields.Text(string='Descripción de la Solicitud', copy=False,
                              required=True)
    fecha_solicitado_trabajador = fields.Date(string='Fecha de solicitud',
                                              required=True, copy=False,
                                              tracking=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    etapa = fields.Many2one('sicpro.app.vivienda.etapas', string='Etapa',
                            required=True, tracking=True, copy=False,
                            domain="[('terminado', '!=', True)]")
    seccion_sindical = fields.Many2one('sicpro.nomenclador.sindicato',
                                       string='Sección Sindical',
                                       related='trabajador_id.seccion_sindical_id',
                                       store=True)
    prioridad = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                 index=True, tracking=True,
                                 default=PRIORIDADES_ACTIVAS[0][0])
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_liberado = fields.Date(string="Fecha Liberado", required=False,
                                 tracking=True)
    fecha_validado = fields.Date(string="Fecha Validado", required=False,
                                 tracking=True)
    fecha_terminado = fields.Date(string="Fecha Terminado", required=False,
                                  tracking=True)
    fecha_reinicio = fields.Date(string="Fecha Reinicio", required=False,
                                 tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     tracking=True)
    fecha_cancelado = fields.Date(string="Fecha Cancelado", required=False,
                                  tracking=True)
    motivo_rechazo = fields.Text(string="Motivo del Rechazo", required=False,
                                 tracking=True)
    fecha_rechazado = fields.Date(string="Fecha Rechazado", required=False,
                                  tracking=True)
    materiales_ids = fields.One2many(
        comodel_name='sicpro.app.vivienda.trabajador.productos',
        string='Listado de Productos', inverse_name='solicitud_id',
        required=False, copy=False, tracking=True)
    anio = fields.Char(string='Año', required=True,
                       default=fields.Datetime.now().strftime("%Y"),
                       copy=False)
    estado = fields.Selection(string='Estado', required=True,
                              default='pendiente', tracking=True, copy=False,
                              selection=[('pendiente', 'Pendiente'),
                                         ('validar', 'Validar'),
                                         ('logistica', 'Logística'),
                                         ('terminado', 'Terminado'),
                                         ('rechazado', 'Rechazado'),
                                         ('cancelado', 'Cancelado'), ],
                              group_expand='_group_expand_estados')
    dominio_escalafon = fields.Char(compute="_compute_get_escalafon",
                                    readonly=True, store=False, copy=False)
    escalafon = fields.Many2one('sicpro.app.vivienda.escalafon',
                                string='Escalafón', required=True,
                                tracking=True, copy=False)
    observaciones = fields.Text(string='Observaciones', copy=False)
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    total_general = fields.Monetary(string='TOTAL GENERAL',
                                    currency_field='currency_id',
                                    compute='compute_calculo_total_material')
    total_materiales = fields.Integer(string='Productos',
                                      compute='compute_calculo_total_material')
    total_prioridad_muy_alto = fields.Integer(string='P Muy Alta',
                                              compute='compute_calculo_total_material')
    total_prioridad_alto = fields.Integer(string='P Alta',
                                          compute='compute_calculo_total_material')
    total_prioridad_medio = fields.Integer(string='P Media',
                                           compute='compute_calculo_total_material')
    total_prioridad_baja = fields.Integer(string='P Baja',
                                          compute='compute_calculo_total_material')
    progress_percentage = fields.Float(
        compute='compute_calculo_total_material')
    bloquear_campos = fields.Boolean(string='Bloquear_campos', default=False,
                                     required=False)
    tipo_mtto_reparacion = fields.Boolean(
        string='Vía Mantenimiento/reparación', required=False)
    tipo_terminada = fields.Boolean(string='Vía Terminación de la vivienda',
                                    required=False)
    jefe_comision = fields.Many2one('sicpro.app.trabajadores',
                                    string='Jefe Comisión Distribuidora UO',
                                    required=True, copy=False)
    secretario_sindical = fields.Many2one('sicpro.app.trabajadores',
                                          string='Secretario Sindical',
                                          required=True, copy=False)
    director = fields.Many2one('sicpro.app.trabajadores',
                               string='Vicepresidente o Director UO',
                               required=True, copy=False)

    # calcula los datos totales del material
    def compute_calculo_total_material(self, t_general=0, t_materiales=0,
                                       p_muy_alto=0, p_alto=0, p_medio=0,
                                       p_baja=0, m_aprobados=0,
                                       m_entregados=0):
        for item in self:
            if item.materiales_ids:
                datos = self.env[
                    'sicpro.app.vivienda.trabajador.productos'].search(
                    [('solicitud_id', '=', item.id)])

                for value in datos:
                    if value.estado == 'aprobado':
                        m_aprobados += 1
                    if value.estado == 'entregado':
                        t_general += (value.cantidad * value.monto)
                        t_materiales += value.cantidad
                        m_entregados += 1
                        m_aprobados += 1
                    if value.prioridad == '3':
                        p_muy_alto += 1
                    if value.prioridad == '2':
                        p_alto += 1
                    if value.prioridad == '1':
                        p_medio += 1
                    if value.prioridad == '0':
                        p_baja += 1

                item.total_general = t_general
                item.total_materiales = t_materiales
                item.total_prioridad_muy_alto = p_muy_alto
                item.total_prioridad_alto = p_alto
                item.total_prioridad_medio = p_medio
                item.total_prioridad_baja = p_baja
                if m_aprobados != 0 and m_entregados != 0:
                    item.progress_percentage = round(
                        (m_entregados / m_aprobados) * 100, 2)
                else:
                    item.progress_percentage = 0
            else:
                item.total_general = t_general
                item.total_general = t_general
                item.total_materiales = t_materiales
                item.total_prioridad_muy_alto = p_muy_alto
                item.total_prioridad_alto = p_alto
                item.total_prioridad_medio = p_medio
                item.total_prioridad_baja = p_baja
                item.progress_percentage = 0

    # expandir estados de la vista kanban
    @api.model
    def _group_expand_estados(self, states, domain):
        return [key for key, val in self._fields['estado'].selection]

    @api.constrains('tipo_mtto_reparacion', 'tipo_terminada')
    def _check_tipo_unico(self):
        if self.tipo_mtto_reparacion == False and self.tipo_terminada == False:
            raise ValidationError(
                "¡El trabajador introducido no tiene especificado una vía de trabajo!.\n\n" + MSG_SOPORTE_SICPRO)

    @api.constrains('trabajador_id', 'etapa', 'seccion_sindical')
    def _check_actividades_unico(self):
        if self.seccion_sindical:
            uniq = self.env['sicpro.app.vivienda.trabajador'].search(
                ['&', '&', '&', ("active", "=", True),
                 ("trabajador_id", "=", self.trabajador_id.id),
                 ("etapa", "=", self.etapa.id), ('estado', '!=', 'cancelado'),
                 ("id", "!=", self.id), ])
            if uniq:
                raise ValidationError(
                    "¡El trabajador introducido ya existe!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "¡El trabajador introducido no tiene asociado una sección sindical!. "
                "Si cree que es un error contacte al secretario general sindical\n\n" + MSG_SOPORTE_SICPRO)

    @api.onchange('seccion_sindical')
    def onchange_sindicato(self):
        if self.seccion_sindical:
            self.secretario_sindical = self.seccion_sindical.user_id.trabajador.id
        else:
            self.secretario_sindical = None

    @api.onchange('trabajador_id')
    def onchange_trabajador_id(self):
        if not self.trabajador_id:
            self.escalafon = None
            self.etapa = None

    @api.model
    @api.depends('etapa', 'trabajador_id')
    def _compute_get_escalafon(self):
        dic = []
        vivienda = self.env['sicpro.app.vivienda.trabajador'].sudo().search(
            ['&', '&', ('active', '=', True), ('etapa', '=', self.etapa.id),
             ('estado', '!=', 'cancelado'),
             ('seccion_sindical', '=', self.seccion_sindical.id)])
        if vivienda:
            for value in vivienda:
                dic.append(value.escalafon.id)
        self.dominio_escalafon = json.dumps([('id', 'not in', dic)])

    def action_vivienda_solicitar(self):
        self.fecha_liberado = fields.Datetime.now()
        self.estado = 'validar'

        # busco usuarios con rol validación
        validar = self.env.ref(
            'sicpro_app_programa_viviendas.grupo_app_vivienda_validar').user_ids
        # agrego los seguidores al modelo
        self.message_subscribe(partner_ids=validar.partner_id.ids)
        # envió la notificación a los seguidores
        self.message_post(body='Nueva Solicitud',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # envío el correo electrónico a los seguidores del registro
        for participante in self.message_partner_ids:
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_nueva_solicitud')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values,)
        # envío el correo electrónico al trabajador
        if self.correo_trabajo:
            email_values = {'email_to': self.correo_trabajo}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_nueva_solicitud')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values,)

    def action_vivienda_validar(self):
        materiales = self.env[
            'sicpro.app.vivienda.trabajador.productos'].search(
            ['&', '&', ('active', '=', True), ('solicitud_id', '=', self.id),
             ('estado', '=', 'pendiente')])
        if materiales:
            raise UserError(
                "¡El trabajador tiene materiales pendientes por validar!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            self.fecha_validado = fields.Datetime.now()
            self.estado = 'logistica'

            # busco usuarios con rol validación
            logistica = self.env.ref(
                'sicpro_app_programa_viviendas.grupo_app_vivienda_logistica').user_ids
            # agrego los seguidores al modelo
            self.message_subscribe(partner_ids=logistica.partner_id.ids)
            # envió la notificación a los seguidores
            self.message_post(body='Solicitud Validada',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # envío el correo electrónico
            for participante in self.message_partner_ids:
                participantes = participante.email_formatted
                email_values = {'email_to': participantes}
                template = self.env.ref(
                    'sicpro_app_programa_viviendas.vivienda_cambios_solicitud')
                template.send_mail(self.id, force_send=True,
                                   email_values=email_values,)
            # envío el correo electrónico al trabajador
            if self.correo_trabajo:
                email_values = {'email_to': self.correo_trabajo}
                template = self.env.ref(
                    'sicpro_app_programa_viviendas.vivienda_cambios_solicitud')
                template.send_mail(self.id, force_send=True,
                                   email_values=email_values,)

    def action_vivienda_reiniciar(self):
        self.fecha_reinicio = fields.Datetime.now()
        self.estado = 'pendiente'

    def action_vivienda_terminar(self):
        self.fecha_terminado = fields.Datetime.now()
        self.estado = 'terminado'

        # envió la notificación a los seguidores
        self.message_post(body='Solicitud Terminada',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # envío el correo electrónico
        for participante in self.message_partner_ids:
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_cambios_solicitud')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values,)
        # envío el correo electrónico al trabajador
        if self.correo_trabajo:
            email_values = {'email_to': self.correo_trabajo}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_cambios_solicitud')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values,)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ViviendaTrabajador, self).create(vals_list)
        for res in records:
            # Crear la secuencia de incremento para el consecutivo de las solicitudes
            res.sequence_consecutivo = self.env['ir.sequence'].next_by_code(
                'vivienda_consecutivo_incrementar')
            res.bloquear_campos = True
            return res
        return None


# listado de productos
class ViviendaTrabajadorProductos(models.Model):
    _name = 'sicpro.app.vivienda.trabajador.productos'
    _description = 'Productos del programa de la vivienda'
    _order = "id asc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Es necesario para la inicialización la incorporación del campo id
    id = fields.Id()

    name = fields.Many2one('sicpro.app.vivienda.materiales', string='Material',
                           required=True)
    solicitud_id = fields.Many2one('sicpro.app.vivienda.trabajador',
                                   'Solicitud', required=False,
                                   ondelete='cascade', index=True)
    company_id_trabajador = fields.Many2one('res.company',
                                            string='Proceso trabajador',
                                            store=True,
                                            related='solicitud_id.company_id_trabajador')
    etapa = fields.Many2one('sicpro.app.vivienda.etapas', string='Etapa',
                            store=True, related='solicitud_id.etapa')
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    proveedor_id = fields.Many2one('sicpro.app.vivienda.proveedor',
                                   'Proveedor',
                                   related='ofertas_id.proveedor_id')
    um = fields.Many2one(comodel_name='sicpro.app.vivienda.materiales.um',
                         string='UM', related='name.um')
    cantidad = fields.Integer(string='Cantidad', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    ofertas_id = fields.Many2one('sicpro.app.vivienda.ofertas',
                                 string='Oferta',
                                 domain="[('etapa_id', '=', etapa),]")
    monto = fields.Monetary(string='Monto', tracking=True, required=False,
                            currency_field='currency_id')
    total_individual = fields.Monetary(string='Total', tracking=True,
                                       compute='compute_calculo_total_individual',
                                       currency_field='currency_id')
    prioridad = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                 index=True, tracking=True,
                                 default=PRIORIDADES_ACTIVAS[0][0])
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, tracking=True, index=True)
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_entregado = fields.Date(string="Fecha Entrega", required=False)
    estado = fields.Selection(string='Estado', required=True,
                              default='pendiente',
                              selection=[('pendiente', 'Pendiente'),
                                         ('aprobado', 'Aprobado'),
                                         ('entregado', 'Entregado'),
                                         ('no_aprobado', 'No Aprobado'), ])
    grupo_logistica = fields.Boolean(string='grupo_sindicato',
                                     compute='_compute_grupo_logistica')

    @api.constrains('ofertas_id', 'name')
    def _check_oferta_material_unico(self):
        if self.ofertas_id and self.name:
            uniq = self.env['sicpro.app.vivienda.trabajador.productos'].search(
                ['&', '&', '&', ("active", "=", True),
                 ("ofertas_id", "=", self.ofertas_id.id),
                 ("name", "=", self.name.id),
                 ("solicitud_id", "=", self.solicitud_id.id),
                 ("id", "!=", self.id), ])
            if uniq:
                raise ValidationError(
                    "¡La oferta y el material introducido ya existe!.\n\n" + MSG_SOPORTE_SICPRO)

    # verífica qué el usuario activo pertenezca al grupo de logística
    def _compute_grupo_logistica(self):
        has_logistica_group = self.env.user.has_group(
            'sicpro_app_programa_viviendas.grupo_app_vivienda_logistica')

        for record in self:
            record.grupo_logistica = has_logistica_group

    # aprobar material
    def aprobar_material(self):
        self.estado = 'aprobado'

    # entregar material
    def entregar_material(self):
        if self.fecha_entregado and self.monto != 0 and self.ofertas_id:
            self.estado = 'entregado'
        else:
            raise ValidationError(
                "¡Verifique la oferta del proveedor, el monto del costo o la fecha en la que se"
                " entregó el producto!.\n\n" + MSG_SOPORTE_SICPRO)

    # no aprobar material
    def no_aprobar_material(self):
        self.estado = 'no_aprobado'

    # calcula el total individual por material
    def compute_calculo_total_individual(self):
        for item in self:
            if item.cantidad and item.monto:
                item.total_individual = item.cantidad * item.monto
            else:
                item.total_individual = 0

    # verífica que la fecha de terminación no sea anterior a la de inicio
    @api.depends('fecha_inicio')
    @api.onchange('fecha_entregado')
    def _onchange_fecha_entregado(self):
        if self.fecha_entregado:
            if self.fecha_entregado < self.fecha_inicio:
                self.fecha_entregado = None
                raise UserError(
                    "La fecha de terminación de la acción no puede ser menor que la fecha de inicio, verifíquelo.\n\n" + MSG_SOPORTE_SICPRO)


# motivo de rechazo
class ViviendaTrabajadorRechazo(models.TransientModel):
    _name = 'sicpro.app.vivienda.trabajador.rechazadas'
    _description = 'Motivo de rechazo de la solicitud'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        solicitud = self.env['sicpro.app.vivienda.trabajador'].browse(
            self.env.context.get('active_ids'))
        for item in solicitud.sudo():
            item.fecha_rechazado = datetime.today()
            item.motivo_rechazo = 'La solicitud no fue validada, se rechazó él ' + str(
                format_date(self.env,
                            datetime.today())) + ' por los siguientes motivos: ' + str(
                self.motivo_id)
            item.estado = 'rechazado'

        # envió la notificación a los seguidores
        solicitud.message_post(body='Solicitud Rechazada',
                               subtype_xmlid='mail.mt_comment',
                               message_type='notification',
                               author_id=self.env.user.partner_id.id)
        # envío el correo electrónico
        for participante in solicitud.message_partner_ids:
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_rechazo')
            template.send_mail(solicitud.id, force_send=True,
                               email_values=email_values,)
        # envío el correo electrónico al trabajador
        if solicitud.correo_trabajo:
            email_values = {'email_to': solicitud.correo_trabajo}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_rechazo')
            template.send_mail(solicitud.id, force_send=True,
                               email_values=email_values, )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_programa_viviendas.vivienda_trabajo_action').sudo().read()[
            0]
        return action


# motivo de cancelación
class ViviendaTrabajadorCancelacion(models.TransientModel):
    _name = 'sicpro.app.vivienda.trabajador.canceladas'
    _description = 'Motivo de cancelación de la solicitud'

    motivo_id = fields.Text(string="Motivo de Cancelación", required=True)

    def action_motivo_cancelacion(self):
        solicitud = self.env['sicpro.app.vivienda.trabajador'].browse(
            self.env.context.get('active_ids'))
        for item in solicitud.sudo():
            item.motivo_cancelacion = self.motivo_id
            item.fecha_cancelado = datetime.today()
            item.estado = 'cancelado'

        # envió la notificación a los seguidores
        solicitud.message_post(body='Solicitud Cancelada',
                               subtype_xmlid='mail.mt_comment',
                               message_type='notification',
                               author_id=self.env.user.partner_id.id)
        # envío el correo electrónico
        for participante in solicitud.message_partner_ids:
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_cancelacion')
            template.send_mail(solicitud.id, force_send=True,
                               email_values=email_values, )
        # envío el correo electrónico al trabajador
        if solicitud.correo_trabajo:
            email_values = {'email_to': solicitud.correo_trabajo}
            template = self.env.ref(
                'sicpro_app_programa_viviendas.vivienda_cancelacion')
            template.send_mail(solicitud.id, force_send=True,
                               email_values=email_values, )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_programa_viviendas.vivienda_trabajo_action').sudo().read()[
            0]
        return action
