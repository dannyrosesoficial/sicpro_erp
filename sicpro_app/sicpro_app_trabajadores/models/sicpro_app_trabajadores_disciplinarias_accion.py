# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class TrabajadoresAccionesDisciplinarias(models.Model):
    _name = 'sicpro.app.trabajadores.disiplinaria.acciones'
    _description = 'Medidas disciplinarias'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_solicitante(self):
        solicitante = self.env.user.trabajador.id
        return solicitante

    estado = fields.Selection(
        [('borrador', 'Borrador'), ('espera_accion', 'Esperando acción'),
         ('action', 'Acción validada'), ('cancelado', 'Cancelado'), ],
        default='borrador', tracking=True)

    name = fields.Char(string='Referencia', required=False, copy=False,
                       readonly=False, )
    user_id = fields.Many2one('res.users', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    solicita_medida = fields.Many2one('sicpro.app.trabajadores',
                                      string='Solicitante', required=True,
                                      default=_default_solicitante)
    cargo_solicitante = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                        string='Cargo', store=True,
                                        related='solicita_medida.ocupacion_id')
    departamento_solicitante = fields.Many2one('sicpro.app.trabajadores.areas',
                                               string='Departamento',
                                               store=True,
                                               related='solicita_medida.area_id')
    company_id = fields.Many2one('res.company', store=True, readonly=False,
                                 related='trabajador_id.company_id')
    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Trabajador', required=True, )
    departamento = fields.Many2one('sicpro.app.trabajadores.areas',
                                   string='Área',
                                   related='trabajador_id.area_id', store=True)
    fecha_incorporacion = fields.Date(string="Incorporación",
                                      related='trabajador_id.fecha_incorporacion',
                                      store=True)
    equipo_tecnico = fields.Many2one("sicpro.app.trabajadores.equipo.tecnico",
                                     string="Equipo Técnico",
                                     related='trabajador_id.equipo_tecnico')
    motivo = fields.Many2one('sicpro.app.trabajadores.disiplinaria.categorias',
                             string='Motivo', required=True)
    action = fields.Many2one('sicpro.app.trabajadores.disiplinaria.categorias',
                             string="Medida")
    dias_validacion = fields.Integer(string='Días', required=False,
                                     related='action.vigencia', store=True)
    acciones_detalles = fields.Text(string="Detalles de la acción")
    note = fields.Text(string="Notas")
    fecha_infraccion = fields.Datetime(string="Fecha de Infracción",
                                       required=True)
    fecha_solicitud = fields.Date(string="Medida solicitada", default=lambda
        self: fields.Date.context_today(self))
    fecha_emision = fields.Date(string="Medida emitida",
                                compute='_compute_action')
    fecha_notificacion = fields.Date(string="Trabajador notificado",
                                     compute='_compute_action')
    fecha_expiracion = fields.Datetime(string='Fecha de Expiración',
                                       readonly=False)
    active = fields.Boolean(string='Activo', default=True)
    estado_secundario = fields.Char(string='estado_secundario',
                                    default='Borrador')
    motivo_description = fields.Text(string="Detalles del motivo",
                                     related='motivo.description')
    accion_description = fields.Text(string="Detalles la acción",
                                     related='action.description')
    solicitante_fecha_conocimiento = fields.Date(string="Fecha Conocimiento", )
    solicitante_via_conocimiento = fields.Char(string='Vía de Conocimiento')
    cargo = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                            string='Cargo:', store=True,
                            related='trabajador_id.ocupacion_id')
    fecha_contrato = fields.Date(string="Contratación", store=True,
                                 related='trabajador_id.inicio_contrato')
    categoria_ocupacional = fields.Many2one(
        'sicpro.app.trabajadores.categorias', string='Categoría', store=True,
        related='trabajador_id.categoria_ocupacional')

    @api.depends('fecha_notificacion', 'action')
    @api.onchange('fecha_notificacion', 'action')
    def _onchange_fecha_notificacion(self):
        if self.fecha_notificacion:
            date_1 = fields.Date.from_string(self.fecha_notificacion)
            date_2 = date_1 + relativedelta(days=self.dias_validacion)
            self.fecha_expiracion = date_2
        else:
            self.fecha_expiracion = None

    @api.onchange('trabajador_id')
    @api.depends('trabajador_id')
    def onchange_trabajador_id(self):
        if self.estado == 'action':
            raise ValidationError(
                '¡No puede editar una acción validada!!' + MSG_SOPORTE_SICPRO)

    @api.onchange('motivo')
    @api.depends('motivo')
    def onchange_reason(self):
        if self.estado == 'action':
            raise ValidationError(
                '¡No puede editar una acción validada!!' + MSG_SOPORTE_SICPRO)

    @api.depends('action')
    def _compute_action(self):
        if self.action:
            self.fecha_emision = fields.Datetime.now()
            self.fecha_notificacion = fields.Date.context_today(
                self) + timedelta(days=1)
        else:
            self.fecha_emision = None
            self.fecha_notificacion = None

    def assign_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Medida en espera de revisión',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        for rec in self:
            rec.estado = 'espera_accion'
            rec.estado_secundario = 'Esperando Acción'

        for participante in self.message_partner_ids:
            # envío el correo electrónico
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    def cancel_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Medida cancelada',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        for rec in self:
            rec.estado = 'cancelado'
            rec.estado_secundario = 'Cancelado'

        for participante in self.message_partner_ids:
            # envío el correo electrónico
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    def set_to_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Medida en estado de borrador',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        for rec in self:
            rec.estado = 'borrador'
            rec.estado_secundario = 'Borrador'

        for participante in self.message_partner_ids:
            # envío el correo electrónico
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    def action_function(self):
        for rec in self:
            if not rec.action:
                raise ValidationError(
                    '¡Debes seleccionar una acción!' + MSG_SOPORTE_SICPRO)
            if not rec.acciones_detalles:
                raise ValidationError(
                    '¡Debes que completar la información de la acción!' + MSG_SOPORTE_SICPRO)
            # envió la notificación a los seguidores
            self.message_post(body='Medida validada',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            rec.estado = 'action'
            rec.estado_secundario = 'Medida Validada'

        for participante in self.message_partner_ids:
            # envío el correo electrónico
            participantes = participante.email_formatted
            email_values = {'email_to': participantes}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    # desactivo la medida del trabajador y envío notificación y correo
    def send_expira_medida_mail(self):
        expira = fields.Datetime.now()
        trabajador = self.env[
            'sicpro.app.trabajadores.disiplinaria.acciones'].search(
            ['&', ('active', '=', True), ('fecha_expiracion', '=', expira)])
        if trabajador:
            for emp in trabajador:
                # envió la notificación a los seguidores
                emp.message_post(body='Medida disciplinaria expirada',
                                 message_type='notification',
                                 subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
                # desactivo el registro
                emp.active = False
                for participante in emp.message_partner_ids:
                    # envío el correo electrónico
                    participantes = participante.email_formatted
                    email_values = {'email_to': participantes}
                    template = self.env.ref(
                        'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_expira')
                    template.send_mail(emp.id, force_send=True,
                                       email_values=email_values, )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TrabajadoresAccionesDisciplinarias, self).create(
            vals_list)

        for res in records:
            # asignar la secuencia para el registro
            res.name = self.env['ir.sequence'].next_by_code(
                'medidas_disciplinarias')
            # suscribir automáticamente al modelo
            # busco el id del trabajador que se le aplica la medida
            # trabajador = self.env['sicpro.app.trabajadores'].search([('id', '=', vals.get('trabajador_id')), ])
            trabajador = res.trabajador_id
            # busco el líder del grupo de atención al trabajador
            lider = trabajador.equipo_tecnico.lider.user_id
            # busco los técnicos que atienden al trabajador
            tecnicos = trabajador.equipo_tecnico.member_ids.user_id
            # busco los responsables de la aplicación de trabajadores
            responsables = self.env.ref(
                'sicpro_app_trabajadores.grupo_app_trabajador_responsable').user_ids
            # busco el encargado legal del proceso
            legal = self.env.ref(
                'sicpro_app_trabajadores.grupo_app_trabajador_disciplina_legal').user_ids
            # busco los representantes del proceso del trabajador afectado
            representantes_proceso = self.env.ref(
                'sicpro_app_trabajadores.grupo_app_trabajador_disciplina_jefe').user_ids
            representantes = self.env['res.users'].search(
                ['&', ('company_id', '=', trabajador.company_id.id),
                 ('id', 'in', representantes_proceso)])
            # creo la lista de seguidores
            seguidores = tecnicos + lider + responsables + legal + representantes
            # agrego los seguidores al modelo
            res.message_subscribe(partner_ids=seguidores.partner_id.ids)
            # envió la notificación a los seguidores
            res.message_post(body='Medida disciplinaria en borrador',
                             subtype_xmlid='mail.mt_comment',
                             author_id=self.env.user.partner_id.id)

            for participante in seguidores:
                # envío el correo electrónico
                participantes = participante.email_formatted
                email_values = {'email_to': participantes}
                template = self.env.ref(
                    'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_nueva')
                template.send_mail(res.id, force_send=True,
                                   email_values=email_values, )
            return res
