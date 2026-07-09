# -*- coding: utf-8 -*-

import logging
from datetime import timedelta

from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class Contratos(models.Model):
    _name = 'sicpro.app.contratos'
    _description = 'Gestión de Contratos'
    _order = "prioridad desc, id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # Agrego el estado por defecto
    def _get_default_stage_ids(self):
        return self.env['sicpro.app.contratos.estados'].search([], limit=1)

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(required=True, string='Titulo', tracking=True)
    observaciones = fields.Text(string="Objeto del contrato", required=False, )
    contratos_id = fields.Many2one('sicpro.app.contratos', 'Contratos', tracking=True, copy=False)
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    prioridad = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, tracking=True,
                                 default=Prioridades_Activas[0][0])
    estado_id = fields.Many2one('sicpro.app.contratos.estados', string='Estados', ondelete='restrict', tracking=True,
                                index=True, copy=False, group_expand='_read_group_stage_ids',
                                default=_get_default_stage_ids)
    kanban_state = fields.Selection([('normal', 'Borrador'), ('blocked', 'Rechazado'), ('done', 'Aprobado'), ],
                                    string='Estado interno', copy=False, default='normal', readonly=True)
    cuentas_ids = fields.One2many('sicpro.app.contratos.cuentas', 'name', 'Cuentas')
    proveedor = fields.Many2one('sicpro.app.contratos.proveedores', string='Proveedor', tracking=True, index=True,
                                required=True, domain="[('stage_id.is_won', '=', True)]")
    tipo_proveedor = fields.Many2one(comodel_name='sicpro.app.contratos.proveedores.tipo', string='Tipo Proveedor',
                                     related='proveedor.tipo', store=True)
    tipo_contrato = fields.Many2one('sicpro.app.contratos.tipo', string='Tipo', tracking=True, index=True,
                                    required=True, )
    pep = fields.Char(string="Código SAP", required=True, tracking=True, )
    user_id = fields.Many2one('res.users', string='Gestor del proveedor', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True, related='company_id.currency_id')
    presupuesto_cup = fields.Monetary('Valor del Contrato', tracking=True, currency_field='company_currency',
                                      required=True)
    etiquetas = fields.Many2many('sicpro.app.contratos.etiquetas', 'sicpro_app_contratos_etiquetas_rel',
                                 string='Etiqueta')
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    vigencia_contrato_anios = fields.Integer(string='Vigencia (Años)', required=True, tracking=True)
    uodc = fields.Many2one('sicpro.app.contratos.unidades', readonly=True, string='Unidad', tracking=True, index=True, )
    area_contrato = fields.Many2one('sicpro.app.contratos.areas', required=True, string='Área del contrato',
                                    tracking=True, index=True, )
    doc_count = fields.Integer(compute='_compute_contratos_docs_count', string="Documentos")
    consecutivo = fields.Char(string='Consecutivo legal', required=False)
    dias_desfasados = fields.Char(compute='_compute_dias_desfasados', string="Días Desfasados")
    dias_desfasados_valor = fields.Integer()
    fecha_inicio_contrato = fields.Date(string="Inicio del Contrato", required=False, )
    fecha_fin_contrato = fields.Date(string="Fin del Contrato", required=False, )
    estado_interno = fields.Selection(
        [('nuevo', 'Nuevo'), ('liberado', 'Liberado'), ('contratacion', 'Contratación'), ('revisado', 'Revisado'),
         ('economia', 'Economía'),  ('legal', 'Legal'), ('firma_director', 'Firma Director'),
         ('firma_proveedor', 'Firma Proveedor'), ('activo', 'Activo'), ('devuelto', 'Devuelto'),
         ('cancelado', 'Cancelado'), ('terminado', 'Terminado')], index=True, required=True, default=lambda self: 'nuevo')
    sequence_consecutivo = fields.Char(string='Secuencia del contrato', copy=False, readonly=True, )

    ##########################################################################
    # Comité DE CONTRATACIÓN DEL CONTRATO
    ##########################################################################
    acta = fields.Char(string="No. Acta", required=False, )
    acuerdo_comite_contratacion = fields.Html(string="Acuerdo", required=False, )
    fecha_comite_contratacion = fields.Date(string="Fecha del Comité", required=False, )
    contratacion_fecha_inicial = fields.Date(string="Fecha Inicial Contratación", required=False, )
    contratacion_persona_contratacion = fields.Many2one('res.users', string='Emitido por:', index=True, tracking=True)
    contratacion_fecha_fin = fields.Date(string="Fecha Fin Contratación", required=False, )
    contratacion_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # SOLICITUD DEL CONTRATO
    ##########################################################################
    solicitud_fecha_inicial = fields.Date(string="Fecha Inicial Solicitud", required=False,
                                          default=lambda self: fields.Date.context_today(self))
    solicitud_persona_solicita = fields.Many2one('res.users', string='Solicitado por:',
                                                 default=lambda self: self.env.uid, index=True, tracking=True)
    solicitud_fecha_fin = fields.Date(string="Fecha Fin Solicitud", required=False, )
    solicitud_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION DEL CONTRATO
    ##########################################################################
    revisado_fecha_inicial = fields.Date(string="Revisado Fecha Inicial", required=False, )
    revisado_persona_revisa = fields.Many2one('res.users', string='Contrato revisado por:', index=True, tracking=True)
    revisado_detalles_contrato = fields.Html(string='Detalles Revisado')
    revisado_fecha_fin = fields.Date(string="Fecha Fin Revisado", required=False, )
    revisado_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION LEGAL DEL CONTRATO
    ##########################################################################
    legal_fecha_inicial = fields.Date(string="Fecha Inicial Legal", required=False, )
    legal_persona_legal = fields.Many2one('res.users', string='Documentos revisados por:', index=True, tracking=True)
    legal_detalles_contrato = fields.Html(string='Detalles Legal')
    legal_fecha_fin = fields.Date(string="Fecha Fin Legal", required=False, )
    legal_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION ECONOMÍA DEL CONTRATO
    ##########################################################################
    economia_fecha_inicial = fields.Date(string="Fecha Inicial Económica", required=False, )
    economia_persona_economia = fields.Many2one('res.users', string='Aprobado por:', index=True, tracking=True)
    economia_detalles_contrato = fields.Html(string='Detalles Economía')
    economia_fecha_fin = fields.Date(string="Fecha Fin Economía", required=False, )
    economia_dias_habiles = fields.Integer(required=False)
    economia_aval_disponibilidad = fields.Html(string='Disponibilidad')
    economia_aval_recomendaciones = fields.Html(string='Recomendaciones')
    economia_aval_aprobacion = fields.Selection(string='Aprobación del Aval',
                                                selection=[('aprobado', 'se aprueba'), ('rechazado', 'se rechaza'), ],
                                                default='aprobado', required=True, )

    forma_pago = fields.Many2many('sicpro.app.contratos.economia.pago', 'sicpro_app_contratos_forma_pago_rel',
                                  string='Forma de Pago')
    # Tiempo en días para el pago
    plazo_pago = fields.Integer(string='Plazo de Pago', tracking=False, )
    beneficiario_nombre = fields.Many2one('sicpro.app.contratos.beneficiarios', string='Beneficiario', tracking=True,
                                          required=False)

    beneficiario_moneda = fields.Many2one('res.currency', string='Moneda', required=False,
                                          related='beneficiario_nombre.moneda', store=True)
    beneficiario_cuenta = fields.Char(string='Cuenta Bancaria', tracking=True,
                                      related='beneficiario_nombre.cuenta_beneficiario', store=True)

    ##########################################################################
    # FIRMA DEL CONTRATO POR EL DIRECTOR
    ##########################################################################
    fecha_firma_director_inicial = fields.Date(string="Fecha Inicial FD", required=False, )
    fecha_firmado_director = fields.Date(string="Fecha de Firma Director", required=False, )
    fecha_firma_director_fin = fields.Date(string="Fecha Fin FD", required=False, )
    firma_director_persona = fields.Many2one('res.users', string='Firma validado por:', index=True, tracking=True)
    observaciones_firma_director = fields.Html(string="Detalles Director", required=False, )
    firma_director_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # FIRMA DEL CONTRATO POR EL PROVEEDOR
    ##########################################################################
    fecha_firma_proveedor_inicial = fields.Date(string="Fecha Inicial FP", required=False, )
    fecha_firmado_proveedor = fields.Date(string="Fecha de Firma Proveedor", required=False, )
    fecha_firma_proveedor_fin = fields.Date(string="Fecha Fin FP", required=False, )
    firma_proveedor_persona = fields.Many2one('res.users', string='Proveedor validado por:', index=True, tracking=True)
    observaciones_firma_proovedor = fields.Html(string="Detalles Proveedor", required=False, )
    firma_proveedor_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # DEVOLUCIÓN DEL CONTRATO
    ##########################################################################
    devuelto_estado_anterior = fields.Char(required=False)

    devuelto_persona_devuelve = fields.Many2one('res.users', string='Devuelto por:', index=True, tracking=True)
    rechazar = fields.Char(string='Rechazar', required=False, readonly=True, tracking=True)
    esta_rechazada = fields.Boolean(default=False)
    fecha_rechazo = fields.Date(string='Fecha de Rechazo', index=True, tracking=True, copy=False, readonly=True)
    fecha_devolucion_fin = fields.Date(string="Fecha fin Devolución", required=False, )
    devolucion_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # CANCELACIÓN DEL CONTRATO
    ##########################################################################
    cancelado_estado_cancelado = fields.Char(required=False)

    cancelado_persona_cancelado = fields.Many2one('res.users', string='Cancelado por:', index=True, tracking=True)
    cancelar = fields.Char(string='Cancelar', required=False, readonly=True, tracking=True)
    esta_cancelado = fields.Boolean(default=False)
    fecha_cancelado = fields.Date(string='Fecha Cancelado', index=True, tracking=True, copy=False, readonly=True)
    grupo_visualizar_all = fields.Boolean(string='grupo_visualizar_all', compute='_compute_grupo_visualizar_all')

    ##########################################################################

    # acción del botón documentos: no hace ninguna función
    def action_empaty_contratos(self, ):
        action = None

    # verífico que el valor del presupuesto no sea 0
    @api.constrains('presupuesto_cup')
    def _check_presupuesto_cup(self):
        for record in self:
            if record.presupuesto_cup == 0:
                raise ValidationError(_('Debe asignar un valor de presupuesto al contrato.'))

    # verífico que el valor de la vigencia en años no sea 0
    @api.constrains('vigencia_contrato_anios')
    def _check_valor_sap_cup(self):
        for record in self:
            if record.vigencia_contrato_anios == 0:
                raise ValidationError(_('Debe asignar un valor en años de vigencia del contrato.'))

    # verifica q el usuario activo pertenezca al grupo visualizar_all
    def _compute_grupo_visualizar_all(self):
        self.grupo_visualizar_all = self.env['res.users'].has_group('sicpro_app_contratos.grupo_app_contratos_all')

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # acción al cambiar el área
    @api.onchange('area_contrato')
    def _onchange_area_contrato(self):
        self.uodc = self.area_contrato.unidad

    # Cuenta los adjuntos de la documentacion del contrato
    def _compute_contratos_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count(
                ['&', ('res_model', '=', 'sicpro.app.contratos'), ('res_id', '=', documentos.id)])

    # acción para liberar el contrato
    def action_liberar_contrato(self, ):
        if self.doc_count != 0:
            estado = self.env['sicpro.app.contratos.estados'].search([('is_contratacion', '=', True)]).id
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'contratacion')]).valor
            self.write({'contratacion_fecha_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles),
                        'estado_id': estado, 'contratacion_fecha_inicial': fields.Date.context_today(self),
                        'contratacion_dias_habiles': dias_habiles, 'estado_interno': 'liberado', })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío la notificación a los seguidores
            self.message_post(body='Contrato Liberado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Debe proporcionar una documentación válida, verifíquelo '))

    # acción para aprobar en el comité de contratación.
    def action_contratacion_contrato(self, ):
        if self.acta and self.fecha_comite_contratacion:
            estado = self.env['sicpro.app.contratos.estados'].search([('is_aprobada', '=', True)]).id
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'revision')]).valor
            self.write({'revisado_fecha_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles),
                        'estado_id': estado, 'revisado_fecha_inicial': fields.Date.context_today(self),
                        'revisado_dias_habiles': dias_habiles, 'contratacion_persona_contratacion': self.env.uid,
                        'estado_interno': 'contratacion', })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_post(body='Contrato aprobado en el Comité de Contratación', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Los campos del Comité de Contratación no deben estar '
                              'nulos, por favor verifíquelo '))

    # acción para aprobar la revision del contrato
    def action_revision_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([('is_economia', '=', True)]).id
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'economia')]).valor
        self.write(
            {'economia_fecha_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles), 'estado_id': estado,
             'economia_fecha_inicial': fields.Date.context_today(self), 'economia_dias_habiles': dias_habiles,
             'revisado_persona_revisa': self.env.uid, 'estado_interno': 'revisado', })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envió la notificación a los seguidores
        self.message_post(body='Contrato aprobado legalmente', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para la aprobación económica del contrato
    def action_economia_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([('is_legal', '=', True)]).id
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'legal')]).valor
        self.write(
            {'legal_fecha_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles), 'estado_id': estado,
             'legal_fecha_inicial': fields.Date.context_today(self), 'legal_dias_habiles': dias_habiles,
             'economia_persona_economia': self.env.uid, 'estado_interno': 'economia', })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envió la notificación a los seguidores
        self.message_post(body='Contrato aprobado en su revisión', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para la aprobación legal del contrato
    def action_legal_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([('is_firma_director', '=', True)]).id
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'director_central')]).valor
        self.write({'fecha_firma_director_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles),
                    'estado_id': estado, 'fecha_firma_director_inicial': fields.Date.context_today(self),
                    'firma_director_dias_habiles': dias_habiles,
                    'legal_persona_legal': self.env.uid, 'estado_interno': 'legal', })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envió la notificación a los seguidores
        self.message_post(body='Contrato aprobado por DC. economía', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción de la firma del contrato por el director
    def action_firma_director_contrato(self, ):
        if self.fecha_firmado_director:
            estado = self.env['sicpro.app.contratos.estados'].search([('is_firma_proveedor', '=', True)]).id
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'proveedor')]).valor
            self.write({'fecha_firma_proveedor_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles),
                        'estado_id': estado, 'fecha_firma_proveedor_inicial': fields.Date.context_today(self),
                        'firma_proveedor_dias_habiles': dias_habiles, 'firma_director_persona': self.env.uid,
                        'estado_interno': 'firma_director', })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_post(body='Contrato firmado por el director', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Debe proporcionar la fecha de firma del Director Central,'
                              ' verifíquelo '))

    # acción de la firma del contrato por el proveedor
    def action_firma_proveedor_contrato(self, ):
        if self.fecha_firmado_proveedor:
            estado = self.env['sicpro.app.contratos.estados'].search([('is_won', '=', True)]).id
            self.write({'fecha_fin_contrato': fields.Date.context_today(self) + timedelta(
                days=self.vigencia_contrato_anios * 365), 'estado_id': estado,
                        'fecha_inicio_contrato': fields.Date.context_today(self),
                        'firma_proveedor_persona': self.env.uid, 'kanban_state': 'done', 'estado_interno': 'activo', })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_post(body='Contrato firmado por el proveedor', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]

            rainbow = {'effect': {'fadeout': 'slow', 'message': 'Felicidades. El contrato está activo',
                                  'type': 'rainbow_man', }}

            return rainbow
        else:
            raise UserError(_('Debe proporcionar la fecha de firma del Proveedor,'
                              ' verifíquelo '))

    # acción para terminar el contrato
    def action_terminar_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([('is_terminada', '=', True)]).id
        self.write({'estado_interno': 'terminado', 'estado_id': estado, })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envió la notificación a los seguidores
        self.message_post(body='Contrato Terminado', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para reiniciar el contrato
    def action_reiniciar_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([('is_inicial', '=', True)]).id
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'solicitante')]).valor
        self.write({'estado_interno': 'nuevo', 'estado_id': estado, 'kanban_state': 'normal',
                    'solicitud_fecha_inicial': fields.Date.context_today(self), 'solicitud_dias_habiles': dias_habiles,
                    'solicitud_fecha_fin': fields.Date.context_today(self) + timedelta(days=dias_habiles),
                    'solicitud_persona_solicita': self.env.uid, 'fecha_inicio_contrato': '', 'fecha_fin_contrato': '',
                    'acta': '', 'fecha_comite_contratacion': '', 'contratacion_persona_contratacion': False,
                    'contratacion_fecha_inicial': '', 'contratacion_fecha_fin': '', 'acuerdo_comite_contratacion': '',
                    'revisado_persona_revisa': False, 'revisado_fecha_inicial': '', 'revisado_fecha_fin': '',
                    'revisado_detalles_contrato': '', 'legal_persona_legal': False, 'consecutivo': '',
                    'legal_fecha_inicial': '', 'legal_fecha_fin': '', 'legal_detalles_contrato': '',
                    'economia_persona_economia': False, 'economia_fecha_inicial': '', 'economia_fecha_fin': '',
                    'economia_detalles_contrato': '', 'firma_director_persona': False,
                    'fecha_firma_director_inicial': '', 'fecha_firma_director_fin': '',
                    'fecha_firmado_director': '', 'observaciones_firma_director': '', 'firma_proveedor_persona': False,
                    'fecha_firma_proveedor_inicial': '', 'fecha_firma_proveedor_fin': '', 'fecha_firmado_proveedor': '',
                    'observaciones_firma_proovedor': '', 'esta_rechazada': False, 'esta_cancelado': False, })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envío la notificación a los seguidores
        self.message_post(body='Contrato Reiniciado', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # Calcula los días desfasados en cada estado
    def _compute_dias_desfasados(self):
        hoy = fields.Date.context_today(self)
        for data in self:
            #temporal
            #data.sudo().dias_desfasados = "-"
            #########################################################
            # Realiza el cálculo en el estado del sin comenzar
            if data.estado_interno == 'nuevo':
                if hoy > data.solicitud_fecha_fin:
                    dias = abs(hoy - data.solicitud_fecha_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado del sin comenzar

            # Realiza el cálculo en el estado del comité de contratación
            if data.estado_interno == 'liberado':
                if hoy > data.contratacion_fecha_fin:
                    dias = abs(hoy - data.contratacion_fecha_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado del comité de contratación

            # Realiza el cálculo en el estado de en revision
            if data.estado_interno == 'contratacion':
                if hoy > data.revisado_fecha_fin:
                    dias = abs(hoy - data.revisado_fecha_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de en revision

            # Realiza el cálculo en el estado de economía
            if data.estado_interno == 'revisado':
                if hoy > data.economia_fecha_fin:
                    dias = abs(hoy - data.economia_fecha_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de economía

            # Realiza el cálculo en el estado de legal
            if data.estado_interno == 'economia':
                if hoy > data.legal_fecha_fin:
                    dias = abs(hoy - data.legal_fecha_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de legal

            # Realiza el cálculo en el estado de firma del director
            if data.estado_interno == 'legal':
                if hoy > data.fecha_firma_director_fin:
                    dias = abs(hoy - data.fecha_firma_director_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de firma del director

            # Realiza el cálculo en el estado de firma del proveedor
            if data.estado_interno == 'firma_director':
                if hoy > data.fecha_firma_proveedor_fin:
                    dias = abs(hoy - data.fecha_firma_proveedor_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de firma del proveedor

            # Realiza el cálculo en el estado de rechazo del contrato
            if data.estado_interno == 'devuelto':
                if hoy > data.fecha_devolucion_fin:
                    dias = abs(hoy - data.fecha_devolucion_fin).days
                    data.sudo().dias_desfasados = str(dias) + " días desfasados, Etapa: " + str(data.estado_id.name)
                    data.sudo().dias_desfasados_valor = dias
                else:
                    data.sudo().dias_desfasados_valor = 0
                    data.sudo().dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de rechazo del contrato

            # Realiza el cálculo en el estado de cancelado, terminado o activo del contrato
            # aunque ya no está activo el estado de la 'economia_dc' no puede eliminarse el control
            # porque existen registros con ese estado y va a dar error si se elimina.
            if data.estado_interno == 'economia_dc' or data.estado_interno == 'cancelado' or \
                    data.estado_interno == 'terminado' or data.estado_interno == 'activo':
                data.sudo().dias_desfasados_valor = 0
                data.sudo().dias_desfasados = "-"
            # Finaliza el cálculo en el estado de cancelado, terminado o activo del contrato - ····economia_dc····

    @api.model
    def create(self, vals):
        # Crear la secuencia de incremento para el consecutivo de los contratos
        vals['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code('contratos_consecutivo_incrementar')
        res = super(Contratos, self).create(vals)
        # Crear días hábiles y fecha fin de la solicitud del contrato
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'solicitante')]).valor
        res['solicitud_dias_habiles'] = dias_habiles
        res['solicitud_fecha_fin'] = fields.Date.context_today(self) + timedelta(days=dias_habiles)

        # busco los usuarios con permisos de visualización
        visualizar = self.env.ref('sicpro_app_contratos.grupo_app_contratos_all').users
        gestor = self.env.ref('sicpro_app_contratos.grupo_app_contratos_validar_gestor').users
        contratacion = self.env.ref('sicpro_app_contratos.grupo_app_contratos_validar_comite_contratacion').users
        revision = self.env.ref('sicpro_app_contratos.grupo_app_contratos_validar_area').users
        legal = self.env.ref('sicpro_app_contratos.grupo_app_contratos_validar_legal').users
        economia = self.env.ref('sicpro_app_contratos.grupo_app_contratos_validar_economica').users
        # creo la lista de seguidores
        seguidores = visualizar + gestor + contratacion + revision + legal + economia
        # agrego los seguidores al modelo
        res.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envió la notificación a los seguidores
        res.message_post(body='Contrato creado', subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in seguidores:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            template = self.env.ref('sicpro_app_contratos.contratos_contrato_nuevos')
            template.send_mail(res.id, force_send=True, email_values=email_values)
        return res


class ContratoRechazado(models.TransientModel):
    _name = 'sicpro.app.contratos.rechazado'
    _description = 'Contratos Rechazados'
    _inherit = ['mail.thread']

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_rechazo(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.contratos'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Contrato rechazado.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno del contrato
        estado = self.env['sicpro.app.contratos.estados'].search([('is_rechazada', '=', True)]).id
        rechazo = self.env['sicpro.app.contratos'].browse(self.env.context.get('active_ids'))
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([('name', '=', 'devolucion')]).valor
        for item in rechazo.sudo():
            item.rechazar = self.lost_reason_id
            item.esta_rechazada = True
            item.estado_interno = 'devuelto'
            item.sudo().estado_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_rechazo = fields.Date.context_today(self)
            item.devolucion_dias_habiles = dias_habiles
            item.fecha_devolucion_fin = item.fecha_rechazo + timedelta(days=item.devolucion_dias_habiles)
            item.devuelto_persona_devuelve = self.env.uid
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action


class ContratoCancelado(models.TransientModel):
    _name = 'sicpro.app.contratos.cancelado'
    _description = 'Contratos Cancelados'
    _inherit = ['mail.thread']

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_cancelado(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.contratos'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Contrato cancelado.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno del contrato
        estado = self.env['sicpro.app.contratos.estados'].search([('is_cancelada', '=', True)]).id
        cancelado = self.env['sicpro.app.contratos'].browse(self.env.context.get('active_ids'))
        for item in cancelado.sudo():
            item.cancelar = self.lost_reason_id
            item.esta_cancelado = True
            item.estado_interno = 'cancelado'
            item.sudo().estado_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_cancelado = fields.Date.context_today(self)
            item.cancelado_persona_cancelado = self.env.uid
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action


class ContratosCuentas(models.Model):
    _name = 'sicpro.app.contratos.cuentas'
    _description = 'Cuentas de los contratos'
    _inherit = ['mail.thread']

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Many2one('sicpro.app.contratos', 'Contratos', required=False, index=True)
    cuenta_gasto = fields.Many2one('sicpro.nomenclador.cuentas.contables', string='Cuenta de Gastos')
    cuenta_gasto_name = fields.Char(related='cuenta_gasto.descripcion', store=True)
    tipo_moneda = fields.Many2one('res.currency', string='Moneda', required=True)
    monto_disponible = fields.Monetary(string='Monto disponible', tracking=True, currency_field='tipo_moneda', )
