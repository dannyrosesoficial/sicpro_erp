# -*- coding: utf-8 -*-


from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransportePiquera(models.Model):
    _name = 'sicpro.app.transporte.piquera'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gestión de la Piquera de Transporte'
    _order = 'id desc'

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    sequence_consecutivo = fields.Char(string='Secuencia', copy=False, readonly=True, )
    active = fields.Boolean(default=True)
    name = fields.Char(string="Servicio", default="Solicitud de Piquera", readonly=True, copy=False)
    solicitante = fields.Many2one('res.users', required=True, string='Solicitante')
    cargo = fields.Many2one('sicpro.app.trabajadores.ocupacion', string='Cargo', store=True, copy=False,
                            related="solicitante.trabajador.ocupacion_id")
    movil = fields.Char(string="Teléfono", store=True, copy=False, related='solicitante.trabajador.movil_trabajo')
    departamento = fields.Many2one('sicpro.app.trabajadores.areas', copy=False, string="Departamento", store=True,
                                   related="solicitante.trabajador.area_id")
    proceso = fields.Many2one('res.company', string="Proceso", store=True, copy=False,
                              related='solicitante.trabajador.company_id')
    fecha_servicio = fields.Date(string="Fecha de Servicio", required=True)
    hora_salida = fields.Float(string='Hora Salida', required=True)
    hora_regreso = fields.Float(string='Hora Regreso', required=True)
    hora_modificada = fields.Boolean(string='Hora Modificada', default=False)
    solicitado = fields.Many2one('res.users', string='Elaborado por:', default=lambda self: self.env.uid,
                                 tracking=True)
    salida = fields.Many2one('sicpro.app.transporte.distancia', string='Salida', tracking=True, required=True)
    destino = fields.Text(string="Destino", required=True)
    cantidad_personas = fields.Integer(string='No. de Personas', required=True)
    rechaza = fields.Many2one('res.users', string='Rechaza o Cancela', tracking=True)
    cargo_rechaza = fields.Many2one('sicpro.app.trabajadores.ocupacion', string='Ocupación', store=True, copy=False,
                                    related="rechaza.trabajador.ocupacion_id")
    movil_rechaza = fields.Char(string="Móvil", store=True, copy=False, related='rechaza.trabajador.movil_trabajo')
    transporte_id = fields.Many2one(comodel_name='sicpro.app.transporte.general', string='Vehiculo',
                                    domain="[('piquera', '=', True)]")
    chapa = fields.Char(string="Chapa", store=True, copy=False, related='transporte_id.matricula')
    chofer = fields.Char(string="Chofer", store=True, copy=False, related='transporte_id.choferNombre')
    contacto = fields.Char(string="Contacto", store=True, copy=False)
    image = fields.Binary(related='transporte_id.image_128', string="Imagen")
    color = fields.Char(string="Color", related='transporte_id.color', store=True, copy=False)
    marca = fields.Char(string="Marca", store=True, copy=False, related='transporte_id.marcaNombre')
    modelo = fields.Char(string="Modelo", store=True, copy=False, related='transporte_id.modeloNombre')
    indice_consumo = fields.Float(string="Indice Consumo", compute="_compute_indice_consumo")
    observaciones = fields.Text(string="Observaciones")
    notas = fields.Text(string="Detalles & Notas")
    estado = fields.Selection(
        [('borrador', 'Borrador'), ('pendiente', 'Pendiente'), ('rechazado', 'Rechazado'), ('cancelado', 'Cancelado'),
         ('aprobado', 'Aprobado')], string="Estado", default="borrador", copy=False, tracking=True)
    grupo_ejecutor = fields.Boolean(string='grupo_ejecutor', compute='_compute_grupo_ejecutor')
    motivo_rechazo = fields.Text(string="Motivo de Rechazo", tracking=True)
    rechazado = fields.Boolean(string='Rechazado', default=False, required=False)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", tracking=True)
    cancelado = fields.Boolean(string='Cancelado', default=False, required=False)
    desfasado = fields.Boolean(string='Desfasado', default=False, required=False)
    recorridos_ids = fields.One2many('sicpro.app.transporte.piquera.recorridos', 'name', string="Recorridos")
    combustible = fields.Many2one(comodel_name='sicpro.app.transporte.tipo.combustible', string='Combustible',
                                  required=False)
    company_id = fields.Many2one('res.company', string='Proceso solicitante', required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True, related='company_id.currency_id')
    total_km = fields.Float(string="Total (Kilómetros)", readonly=True, copy=False)
    valor_combustible = fields.Monetary(string="Valor del Combustible", related='combustible.costo',
                                        currency_field='company_currency', store=True, copy=False)
    total_litros = fields.Float(string="Consumo Total (L)", copy=False)
    total_costo = fields.Monetary(string="Total", readonly=True, copy=False, currency_field='company_currency', )
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    # Actualiza los valores del costo del combustible
    @api.constrains('recorridos_ids', 'transporte_id', 'combustible')
    def total_updater(self):
        total_km = 0.0
        for item in self.recorridos_ids:
            total_km += item.km
        self.total_km = total_km
        if self.transporte_id:
            self.total_litros = total_km / self.indice_consumo
            self.total_costo = self.total_litros * self.valor_combustible
        else:
            raise ValidationError(_("Debe seleccionar un vehículo para continuar"))

    # Convierte el valor de índice de consumo normado a entero
    @api.depends('transporte_id')
    def _compute_indice_consumo(self):
        ic_texto = self.transporte_id.indiceConsumoNormado
        self.indice_consumo = float(ic_texto)

    # actualiza el numero de contacto del chofer
    @api.onchange('transporte_id')
    def _onchange_transporte_id(self):
        self.contacto = self.transporte_id.chofer_trabajador_id.movil_trabajo

    # verifica que la fecha de servicio sea posterior a los 3 días
    @api.onchange('fecha_servicio')
    def _onchange_fecha_servicio(self):
        hoy = fields.Date.context_today(self)
        control = hoy + timedelta(days=3)
        for item in self:
            if item.fecha_servicio:
                if item.fecha_servicio <= control:
                    item.desfasado = True
                else:
                    item.desfasado = False

    # verífica q el usuario activo pertenezca al grupo Ejecutor
    def _compute_grupo_ejecutor(self):
        ejecutor = self.env['res.users'].has_group('sicpro_app_transporte.grupo_app_transporte_piquera_ejecutor')
        if ejecutor:
            self.grupo_ejecutor = True
        else:
            self.grupo_ejecutor = False

    # activo el boolean para identificar que se modificó la hora de
    # solicitud de servicio y determinar el correo que será enviado
    def cambio_hora(self):
        self.hora_modificada = True

    # acción para emitir el informe de costos del servicio de piquera
    def imprimir_costos(self):
        return {'type': 'ir.actions.report', 'model': 'sicpro.app.transporte.piquera', 'report_type': 'qweb-pdf',
                'report_name': 'sicpro_app_transporte.informe_piquera_solicitud', }

    # método para solicitar el servicio de piquera
    def solicitar_piquera(self):
        self.estado = 'pendiente'
        # busco el solicitante
        solicitante = self.solicitante
        # busco los ejecutores de la piquera
        ejecutores = self.env.ref('sicpro_app_transporte.grupo_app_transporte_piquera_ejecutor').users
        # creo la lista de seguidores
        seguidores = solicitante + ejecutores
        # agrego los seguidores al modelo
        self.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envío la notificación a los seguidores
        self.message_post(body='Solicitud de piquera', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_transporte.transporte_solicitud_piquera')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_transporte.transporte_piquera_action').read()[0]
        return action

    # método para aprobar la solicitud de piquera
    def aprobar_solicitud(self):
        if self.transporte_id and self.combustible:
            self.estado = 'aprobado'
            # envío la notificación a los seguidores
            self.message_post(body='Solicitud de piquera aprobada', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                if self.hora_modificada:
                    template = self.env.ref('sicpro_app_transporte.transporte_aprobacion_mod_hora_piquera')
                else:
                    template = self.env.ref('sicpro_app_transporte.transporte_aprobacion_piquera')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_transporte.transporte_piquera_action').read()[0]
            return action
        else:
            raise ValidationError(_("Debe seleccionar un vehículo o tipo de combustible"))

    # cancela la solicitud para el solicitante
    def cancelar_solicitud(self):
        self.estado = 'cancelado'

    # el solicitante puede reiniciar la solicitud
    def reiniciar_solicitud(self):
        self.estado = 'borrador'
        self.rechazado = False

    # chequea que existan personas asignadas a la solicitud
    @api.constrains('cantidad_personas')
    def _check_cantidad_personas(self):
        for item in self:
            if item.cantidad_personas == 0:
                raise ValidationError(_("Debe seleccionar la cantidad de personas que utilizaran el vehículo."))

    # chequea q la hora de salida y de regreso no se encuentren en 0
    @api.constrains('hora_salida', 'hora_regreso')
    def _check_hora_salida_regreso(self):
        for item in self:
            if item.hora_salida == 0 or item.hora_regreso == 0:
                raise ValidationError(_("Debe seleccionar la hora de salida y regreso "
                                        "del servicio qué está solicitando."))

    @api.model
    def create(self, vals):
        res = super(TransportePiquera, self).create(vals)
        # Crear la secuencia de incremento para el consecutivo de la piquera
        res['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code('piquera_consecutivo_incrementar')
        return res


class TransportePiqueraRecorridos(models.Model):
    _name = 'sicpro.app.transporte.piquera.recorridos'
    _description = 'Gestión de recorridos de la Piquera'
    _order = 'id asc'

    name = fields.Many2one('sicpro.app.transporte.piquera', string="Piquera")
    salida = fields.Many2one(comodel_name='sicpro.app.transporte.distancia', string='Salida', required=True)
    destino = fields.Many2one(comodel_name='sicpro.app.transporte.distancia', string='Destino', required=True, )
    recorrido = fields.Many2one(comodel_name='sicpro.app.transporte.distancia.recorrido',
                                domain="['&', ('salida_id', '=', salida), "
                                       "('destino_id', '=', destino)]", string='Recorrido', required=True, )
    km = fields.Float(string='Distancia(KM)', related="recorrido.km", store=True)

    # Modifica el contenido del recorrido para agregar uno nuevo
    @api.onchange('salida', 'destino')
    def _onchange_salida_destino(self):
        for item in self:
            if item.salida and item.destino:
                recorrido = self.env['sicpro.app.transporte.distancia.recorrido'].search(
                    ['&', ('salida_id', '=', self.salida.id), ('destino_id', '=', self.destino.id)])
                if item.salida == item.destino:
                    raise ValidationError(_("La Salida y el Destino no pueden ser iguales."))
                elif not recorrido:
                    raise ValidationError(_("La Salida y el Destino no tienen un recorrido creado."))
                else:
                    item.recorrido = None


class TransportePiqueraRechazadas(models.TransientModel):
    _name = 'sicpro.app.transporte.piquera.rechazadas'
    _description = 'Motivo de Rechazo de la Piquera'

    motivo_rechazo = fields.Text(string="Motivo de Rechazo", required=True, )

    def piquera_motivo_rechazo(self):
        rechazo = self.env['sicpro.app.transporte.piquera'].browse(self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.rechaza = self.env.uid
            item.motivo_rechazo = self.motivo_rechazo
            item.estado = 'rechazado'
            item.rechazado = True
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.transporte.piquera'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Solicitud de piquera rechazada.', message_type='notification',
                          subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = self.env.ref('sicpro_app_transporte.transporte_rechazo_piquera')
            template.send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_transporte.transporte_piquera_action').sudo().read()[0]
        return action


class TransportePiqueraCanceladas(models.TransientModel):
    _name = 'sicpro.app.transporte.piquera.canceladas'
    _description = 'Motivo de Cancelación de la Piquera'

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", required=True, )

    def piquera_motivo_cancelacion(self):
        cancelacion = self.env['sicpro.app.transporte.piquera'].browse(self.env.context.get('active_ids'))
        for item in cancelacion.sudo():
            item.rechaza = self.env.uid
            item.motivo_cancelacion = self.motivo_cancelacion
            item.estado = 'cancelado'
            item.cancelado = True
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.transporte.piquera'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Solicitud de piquera cancelada.', message_type='notification',
                          subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = self.env.ref('sicpro_app_transporte.transporte_cancelacion_piquera')
            template.send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_transporte.transporte_piquera_action').sudo().read()[0]
        return action
