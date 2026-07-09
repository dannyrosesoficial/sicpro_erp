# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's 🌹)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import datetime
from random import randint
from odoo import fields, models, api, _
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError, UserError


def _default_color():
    return randint(1, 11)


PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class ControlInformacion(models.Model):
    _name = 'sicpro.app.control.informacion'
    _description = "Control de Información de la DVPE"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('sicpro.app.control.informacion.actividad',
                           string='Actividad', required=True, index=True,
                           tracking=True, domain="[('areas', 'in', area)]")
    version = fields.Integer(string='Versión', required=False)
    descripcion = fields.Char(string="Descripción", related='name.descripcion')
    gestores = fields.Many2many(comodel_name='res.users', string='Gestores',
                                required=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True,
                              default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 related='user_id.company_id', store=True)
    identificador_corto = fields.Char(string='Id corto',
                                      related='company_id.identificador_corto',
                                      store=True)
    documentos_ids = fields.Many2many('ir.attachment',
                                      'documentos_informacion_rel',
                                      'documentos_informacion_id',
                                      'attachment_id', string="Documentos")
    etiquetas_ids = fields.Many2many(
        'sicpro.app.control.informacion.etiquetas',
        'etiquetas_informacion_rel', 'etiquetas_id', 'etiqueta_id',
        string='Etiqueta', tracking=True)
    area = fields.Many2one('sicpro.app.control.informacion.areas',
                           string='Área Informativa')
    fecha_entrega = fields.Date(string='Fecha de Entrega',
                                default=lambda self: fields.Date.context_today(
                                    self))
    anio = fields.Char(string="Año", required=False,
                       default=lambda self: str(fields.Datetime.now().year))
    fecha_requerida = fields.Date(string='Fecha de Requerida',
                                  compute='_compute_fecha_requerida',
                                  store=True)
    estado = fields.Selection(string='Estado', required=True, tracking=True,
                              default='pendiente',
                              selection=[('atrasado', 'Atrasado'),
                                         ('pendiente', 'Pendiente'),
                                         ('enviado', 'Enviado'),
                                         ('validado', 'Validado'),
                                         ('devuelto', 'Devuelto'), ],
                              group_expand='_group_expand_estados')
    mes = fields.Char(string='Mes', required=False, tracking=True)
    devolucion_motivo = fields.Many2one(
        'sicpro.app.control.informacion.motivos.devolucion',
        string="Motivo de Devolución", required=False)
    devolucion_detalles = fields.Text(string="Detalles de la devolución",
                                      required=False)
    devolucion_fecha = fields.Date(string='Fecha de devolución')
    devolucion_user_id = fields.Many2one('res.users', string='Devuelto por:',
                                         index=True, tracking=True)
    observaciones = fields.Text(string="Observaciones de la información",
                                required=False)
    doc_count = fields.Integer(compute='_compute_info_docs_count',
                               string="Cuenta Documentos")

    # control de versiones
    def action_empaty_version(self):
        action = None

    # control de documentos
    def action_empaty_documentos(self):
        action = None

    @api.model
    def _group_expand_estados(self, states, domain):
        return [key for key, val in self._fields['estado'].selection]

    @api.constrains('name', 'anio', 'area', 'mes', 'estado')
    def _check_actividad_unica(self):
        for record in self:
            domain = [("active", "=", True), ("id", "!=", record.id),
                ("anio", "=", record.anio), ("area", "=", record.area.id),
                ("mes", "=", record.mes), ("name", "=", record.name.id),
                # Corregido para comparar ID
                ("estado", "in", ['enviado', 'validado'])]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡Esta información ya fue enviada!" + " " + (
                            MSG_SOPORTE_SICPRO or ""))

    @api.depends('name', 'anio')
    def _compute_fecha_requerida(self):
        for record in self:
            if record.name and record.anio:
                try:
                    mes_actual = fields.Date.today().month
                    dia = int(record.name.dia_entrega)
                    anio = int(record.anio)
                    # Uso de datetime.date de forma segura
                    record.fecha_requerida = datetime(anio, mes_actual,
                                                      dia).date()
                except (ValueError, TypeError):
                    record.fecha_requerida = False
            else:
                record.fecha_requerida = False

    @api.onchange('user_id')
    def _onchange_area_informativa(self):
        # Uso de self.env.company para Odoo 19
        control = self.env['sicpro.app.control.informacion.areas'].search(
            [('company_id', '=', self.env.company.id)], limit=1)
        if control:
            self.area = control.id
        else:
            self.area = False
            # No se recomienda raise ValidationError en onchange si se puede evitar,
            # pero lo mantenemos por tu flujo de negocio.
            if self.user_id:
                raise ValidationError(
                    "¡El usuario actual no pertenece a ninguna área de información!" + " " + (
                            MSG_SOPORTE_SICPRO or ""))

    @api.onchange('fecha_entrega')
    def _compute_mes(self):
        for item in self:
            if item.fecha_entrega:
                mes_id = item.fecha_entrega.month
                nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                    [('active', '=', True), ('codigo_mes', '=', mes_id)],
                    limit=1)
                item.mes = nombre_mes.name if nombre_mes else '-'
            else:
                item.mes = '-'

    def _compute_info_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for record in self:
            if not record._origin:
                record.doc_count = len(record.documentos_ids)
            else:
                record.doc_count = attachment_obj.search_count([
                    ('res_model', '=', 'sicpro.app.control.informacion'),
                    ('res_id', '=', record._origin.id)
                ])

    def action_enviar_info(self):
        self.ensure_one()
        self._check_actividad_unica()
        if self.doc_count > 0:
            self.estado = 'enviado'

            cuenta_version = self.search_count(
                [("active", "=", True), ("anio", "=", self.anio),
                    ("mes", "=", self.mes), ("name", "=", self.name.id)])
            self.version = cuenta_version

            control_info = self.env[
                'sicpro.app.control.informacion.control.actividades'].search(
                [], limit=1)
            if control_info:
                control_info.cron_control_informaciones()

            for gestor in self.name.gestores:
                self.message_subscribe(partner_ids=gestor.partner_id.ids)

            self.message_post(body='Validar Información',
                              subtype_xmlid='mail.mt_comment')

            template = self.env.ref(
                'sicpro_app_control_informacion.control_informacion_nueva',
                raise_if_not_found=False)
            if template:
                for participante in self.message_partner_ids.filtered(
                    lambda p: p.email):
                    template.send_mail(self.id, force_send=True, email_values={
                        'email_to': participante.email})

            return self.env.ref(
                'sicpro_app_control_informacion.control_informaciones_action').read()[
                0]
        else:
            raise UserError(
                'Debe proporcionar una documentación válida.' + " " + (
                        MSG_SOPORTE_SICPRO or ""))

    def action_validar_info(self):
        self.ensure_one()
        if self.doc_count > 0:
            self.sudo().estado = 'validado'
            control_info = self.env[
                'sicpro.app.control.informacion.control.actividades'].search(
                [], limit=1)
            if control_info:
                control_info.cron_control_informaciones()

            self.sudo().message_post(body='Información validada',
                                     subtype_xmlid='mail.mt_comment')

            template = self.env.ref(
                'sicpro_app_control_informacion.control_informacion_validada',
                raise_if_not_found=False)
            if template:
                for participante in self.sudo().message_partner_ids.filtered(
                    lambda p: p.email):
                    template.send_mail(self.id, force_send=True, email_values={
                        'email_to': participante.email})

            return self.env.ref(
                'sicpro_app_control_informacion.control_informaciones_action').sudo().read()[
                0]
        else:
            raise UserError(
                'Debe proporcionar una documentación válida.' + " " + (
                        MSG_SOPORTE_SICPRO or ""))


class ControlInformacionMotivoRechazo(models.TransientModel):
    _name = 'sicpro.app.control.informacion.devueltas'
    _description = 'Motivo de devolución de la información'

    motivo_id = fields.Many2one(
        'sicpro.app.control.informacion.motivos.devolucion',
        string="Motivo de Devolución", required=True)
    detalles = fields.Text(string="Detalles de la devolución", required=True)

    def action_motivo_devolucion(self):
        active_ids = self.env.context.get('active_ids')
        info_records = self.env['sicpro.app.control.informacion'].browse(
            active_ids)

        for item in info_records:
            item.sudo().write({'devolucion_motivo': self.motivo_id.id,
                'devolucion_detalles': self.detalles,
                'devolucion_fecha': fields.Date.today(),
                'devolucion_user_id': self.env.uid, 'estado': 'devuelto'})

            control_info = self.env[
                'sicpro.app.control.informacion.control.actividades'].search(
                [], limit=1)
            if control_info:
                control_info.cron_control_informaciones()

            item.message_post(body='Información devuelta',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment')

            template = self.env.ref(
                'sicpro_app_control_informacion.control_informacion_devuelta',
                raise_if_not_found=False)
            if template:
                for participante in item.message_partner_ids.filtered(
                    lambda p: p.email):
                    template.send_mail(item.id, force_send=True, email_values={
                        'email_to': participante.email})

        return self.env.ref(
            'sicpro_app_control_informacion.control_informaciones_action').sudo().read()[
            0]