# -*- coding: utf-8 -*-

import logging
from datetime import timedelta, datetime
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class Contratos(models.Model):
    _name = 'sicpro.app.contratos'
    _description = 'Datos de los contratos'
    _order = "prioridad desc,id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # Agrego el estado por defecto
    def _get_default_stage_ids(self):
        return self.env['sicpro.app.contratos.estados'].search(
            [], limit=1)

    name = fields.Char(required=True, string='Titulo', tracking=True, )
    observaciones = fields.Text(string="Observaciones", required=False, )
    contratos_id = fields.Many2one('sicpro.app.contratos', 'Contratos',
                                   tracking=True, copy=False)
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    prioridad = fields.Selection(Prioridades_Activas, string='Prioridad',
                                 index=True, tracking=True,
                                 default=Prioridades_Activas[0][0])
    estado_id = fields.Many2one('sicpro.app.contratos.estados',
                                string='Estados', ondelete='restrict',
                                tracking=True, index=True, copy=False,
                                group_expand='_read_group_stage_ids',
                                default=_get_default_stage_ids)
    kanban_state = fields.Selection([('normal', 'Borrador'),
                                     ('blocked', 'Rechazado'),
                                     ('done', 'Aprobado'), ],
                                    string='Estado interno',
                                    copy=False, default='normal',
                                    readonly=True)
    cuenta = fields.Char(string='Cuenta', tracking=True, required=True,
                         index=True)
    proveedor = fields.Many2one('sicpro.app.contratos.proveedores',
                                string='Proveedor', tracking=True,
                                index=True, required=True,
                                domain="[('stage_id.is_won', '=', True)]")
    tipo_contrato = fields.Many2one('sicpro.app.contratos.tipo', string='Tipo',
                                    tracking=True, index=True, required=True, )
    pep = fields.Char(string="Pep", required=True, tracking=True, )
    user_id = fields.Many2one('res.users', string='Gestor del proveedor',
                              index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,
                                       relation="res.currency")
    presupuesto_cup = fields.Monetary('Presupuesto',
                                      currency_field='company_currency',
                                      tracking=True, required=True)
    etiquetas = fields.Many2many('sicpro.app.contratos.etiquetas',
                                 'sicpro_app_contratos_etiquetas_rel',
                                 string='Etiqueta')
    anio = fields.Char(string="Año", required=False,
                       default=fields.datetime.today().strftime("%Y"), )
    vigencia_contrato_anios = fields.Integer(string='Vigencia (Años)',
                                             required=True, tracking=True)
    uodc = fields.Many2one('sicpro.app.contratos.unidades', readonly=True,
                           string='Unidad', tracking=True, index=True, )
    area_contrato = fields.Many2one(
        'sicpro.app.contratos.areas', required=True, string='Área',
        tracking=True, index=True, )
    doc_count = fields.Integer(compute='_compute_contratos_docs_count',
                               string="Documentos")
    consecutivo = fields.Char(string='Consecutivo legal', required=False)
    dias_desfasados = fields.Char(compute='_compute_dias_desfasados',
                                  string="Días Desfasados")
    dias_desfasados_valor = fields.Integer()
    fecha_inicio_contrato = fields.Date(string="Inicio del Contrato",
                                        required=False, )
    fecha_fin_contrato = fields.Date(string="Fin del Contrato",
                                     required=False, )

    estado_interno = fields.Selection([('nuevo', 'Nuevo'),
                                       ('liberado', 'Liberado'),
                                       ('contratacion', 'Contratación'),
                                       ('revisado', 'Revisado'),
                                       ('legal', 'Legal'),
                                       ('economia', 'Economía'),
                                       ('economia_dc', 'Economía DC'),
                                       ('firma_director', 'Firma Director'),
                                       ('firma_proveedor', 'Firma Proveedor'),
                                       ('activo', 'Activo'),
                                       ('devuelto', 'Devuelto'),
                                       ('cancelado', 'Cancelado'),
                                       ('terminado', 'Terminado')],
                                      index=True, required=True, tracking=15,
                                      default=lambda self: 'nuevo')
    sequence_id = fields.Many2one('ir.sequence', string='Id Secuencia',
                                  required=False, copy=False)
    sequence_consecutivo = fields.Char(string='Secuencia', copy=False,
                                       readonly=True, )

    ##########################################################################
    # Comité DE CONTRATACIÓN DEL CONTRATO
    ##########################################################################
    acta = fields.Char(string="No. Acta", required=False, )
    acuerdo_comite_contratacion = fields.Html(string="Acuerdo",
                                              required=False, )
    fecha_comite_contratacion = fields.Date(string="Fecha del Comité",
                                            required=False, )
    contratacion_fecha_inicial = fields.Date(string="Fecha Inicial",
                                             required=False, )
    contratacion_persona_contratacion = fields.Many2one(
        'res.users', string='Emitido por:', index=True, tracking=True)
    contratacion_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    contratacion_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # SOLICITUD DEL CONTRATO
    ##########################################################################
    solicitud_fecha_inicial = fields.Date(string="Fecha Inicial",
                                          required=False,
                                          default=fields.date.today())
    solicitud_persona_solicita = fields.Many2one(
        'res.users', string='Solicitado por:',
        default=lambda self: self.env.uid, index=True, tracking=True)
    solicitud_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    solicitud_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION DEL CONTRATO
    ##########################################################################
    revisado_fecha_inicial = fields.Date(string="Fecha Inicial",
                                         required=False, )
    revisado_persona_revisa = fields.Many2one(
        'res.users', string='Revisado por:', index=True, tracking=True)
    revisado_detalles_contrato = fields.Html(string='Detalles')
    revisado_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    revisado_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION LEGAL DEL CONTRATO
    ##########################################################################
    legal_fecha_inicial = fields.Date(string="Fecha Inicial", required=False, )
    legal_persona_legal = fields.Many2one(
        'res.users', string='Revisado por:', index=True, tracking=True)
    legal_detalles_contrato = fields.Html(string='Detalles')
    legal_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    legal_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # REVISION ECONOMÍA DEL CONTRATO
    ##########################################################################
    economia_fecha_inicial = fields.Date(string="Fecha Inicial",
                                         required=False, )
    economia_persona_economia = fields.Many2one(
        'res.users', string='Aprobado por:', index=True, tracking=True)
    economia_detalles_contrato = fields.Html(string='Detalles')
    economia_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    economia_dias_habiles = fields.Integer(required=False)

    ##########################################################################
    # REVISION DIRECCIÓN CENTRAL ECONOMÍA DEL CONTRATO
    ##########################################################################
    economia_dc_fecha_inicial = fields.Date(string="Fecha Inicial",
                                            required=False, )
    economia_dc_persona_economia = fields.Many2one(
        'res.users', string='Apobado por:', index=True, tracking=True)
    economia_dc_detalles_contrato = fields.Html(string='Detalles')
    economia_dc_fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    economia_dc_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # FIRMA DEL CONTRATO POR EL DIRECTOR
    ##########################################################################
    fecha_firma_director_inicial = fields.Date(string="Fecha Inicial",
                                               required=False, )
    fecha_firmado_director = fields.Date(string="Fecha de Firma",
                                         required=False, )
    fecha_firma_director_fin = fields.Date(string="Fecha Fin",
                                           required=False, )
    firma_director_persona = fields.Many2one(
        'res.users', string='Validado por:', index=True, tracking=True)
    observaciones_firma_director = fields.Html(string="Detalles",
                                               required=False, )
    firma_director_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # FIRMA DEL CONTRATO POR EL PROVEEDOR
    ##########################################################################
    fecha_firma_proveedor_inicial = fields.Date(string="Fecha Inicial",
                                                required=False, )
    fecha_firmado_proveedor = fields.Date(string="Fecha de Firma",
                                          required=False, )
    fecha_firma_proveedor_fin = fields.Date(string="Fecha Fin",
                                            required=False, )
    firma_proveedor_persona = fields.Many2one(
        'res.users', string='Validado por:', index=True, tracking=True)
    observaciones_firma_proovedor = fields.Html(string="Detalles",
                                                required=False, )
    firma_proveedor_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # DEVOLUCIÓN DEL CONTRATO
    ##########################################################################
    devuelto_estado_anterior = fields.Char(required=False)

    devuelto_persona_devuelve = fields.Many2one(
        'res.users', string='Devuelto por:', index=True, tracking=True)
    rechazar = fields.Char(string='Rechazar', required=False, readonly=True,
                           tracking=True)
    esta_rechazada = fields.Boolean(default=False)
    fecha_rechazo = fields.Date(string='Fecha de Rechazo', index=True,
                                tracking=True, copy=False, readonly=True)
    fecha_devolucion_fin = fields.Date(string="Fecha fin", required=False, )
    devolucion_dias_habiles = fields.Integer(required=False)
    ##########################################################################

    ##########################################################################
    # CANCELACIÓN DEL CONTRATO
    ##########################################################################
    cancelado_estado_cancelado = fields.Char(required=False)

    cancelado_persona_cancelado = fields.Many2one(
        'res.users', string='Cancelado por:', index=True, tracking=True)
    cancelar = fields.Char(string='Cancelar', required=False, readonly=True,
                           tracking=True)
    esta_cancelado = fields.Boolean(default=False)
    fecha_cancelado = fields.Date(string='Fecha Cancelado', index=True,
                                  tracking=True, copy=False, readonly=True)

    ##########################################################################

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # acción al cambiar el área
    @api.onchange('area_contrato')
    def _onchange_area_contrato(self):
        self.uodc = self.area_contrato.unidad

    # Cuenta los adjuntos de la documentacion del contrato
    def _compute_contratos_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count([
                '&', ('res_model', '=', 'sicpro.app.contratos'),
                ('res_id', '=', documentos.id)
            ])

    # Sube los adjuntos de la documentacion del contrato
    def contratos_docs_view_action(self):
        self.ensure_one()
        domain = [
            '&',
            ('res_model', '=', 'sicpro.app.contratos'),
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
                            Adjunte la documentación del contrato.</p>
                        '''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
                self._name, self.id)
        }

    # Calcula los días desfasados en cada estado
    def _compute_dias_desfasados(self):
        for data in self:
            # Realiza el cálculo en el estado del sin comenzar
            if data.estado_interno == 'nuevo':
                if fields.date.today() > data.solicitud_fecha_fin:
                    dias = abs(fields.date.today() - data.solicitud_fecha_fin) \
                        .days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado del sin comenzar

            # Realiza el cálculo en el estado del comite de contratación
            if data.estado_interno == 'liberado':
                if fields.date.today() > data.contratacion_fecha_fin:
                    dias = abs(
                        fields.date.today() - data.contratacion_fecha_fin) \
                        .days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado del comite de contratación

            # Realiza el cálculo en el estado de en revision
            if data.estado_interno == 'contratacion':
                if fields.date.today() > data.revisado_fecha_fin:
                    dias = abs(fields.date.today() - data.revisado_fecha_fin) \
                        .days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de en revision

            # Realiza el cálculo en el estado de legal
            if data.estado_interno == 'revisado':
                if fields.date.today() > data.legal_fecha_fin:
                    dias = abs(fields.date.today() - data.legal_fecha_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de legal

            # Realiza el cálculo en el estado de economia
            if data.estado_interno == 'legal':
                if fields.date.today() > data.economia_fecha_fin:
                    dias = abs(fields.date.today() -
                               data.economia_fecha_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de economia

            # Realiza el cálculo en el estado de dc economia
            if data.estado_interno == 'economia':
                if fields.date.today() > data.economia_dc_fecha_fin:
                    dias = abs(fields.date.today() -
                               data.economia_dc_fecha_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de dc economia

            # Realiza el cálculo en el estado de firma del director
            if data.estado_interno == 'economia_dc':
                if fields.date.today() > data.fecha_firma_director_fin:
                    dias = abs(fields.date.today() -
                               data.fecha_firma_director_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de firma del director

            # Realiza el cálculo en el estado de firma del proveedor
            if data.estado_interno == 'firma_director':
                if fields.date.today() > data.fecha_firma_proveedor_fin:
                    dias = abs(fields.date.today() -
                               data.fecha_firma_proveedor_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de firma del proveedor

            # Realiza el cálculo en el estado de rechazo del contrato
            if data.estado_interno == 'devuelto':
                if fields.date.today() > data.fecha_devolucion_fin:
                    dias = abs(fields.date.today() -
                               data.fecha_devolucion_fin).days
                    data.dias_desfasados = \
                        str(dias) + " días desfasados, Etapa: " + \
                        str(data.estado_id.name)
                    data.dias_desfasados_valor = dias
                else:
                    data.dias_desfasados = "No existen días desfasados"
            # Finaliza el cálculo en el estado de rechazo del contrato

            # Realiza el cálculo en el estado de cancelado el contrato
            if data.estado_interno == 'cancelado':
                data.dias_desfasados_valor = 0
                data.dias_desfasados = "-"
            # Finaliza el cálculo en el estado de cancelado el contrato

            # Realiza el cálculo en el estado de terminado el contrato
            if data.estado_interno == 'terminado':
                data.dias_desfasados_valor = 0
                data.dias_desfasados = "-"
            # Finaliza el cálculo en el estado de terminado el contrato

            # Realiza el cálculo en el estado de activo
            if data.estado_interno == 'activo':
                data.dias_desfasados = "-"
                data.dias_desfasados_valor = 0
            # Finaliza el cálculo en el estado de activo

    # acción para liberar el contrato
    def action_liberar_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_contratacion', '=', True)]).id
        self.estado_interno = 'liberado'
        self.estado_id = estado
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'contratacion')]).valor
        self.contratacion_fecha_inicial = fields.date.today()
        self.contratacion_dias_habiles = dias_habiles
        self.contratacion_fecha_fin = self.contratacion_fecha_inicial + \
                                      timedelta(
                                          days=self.contratacion_dias_habiles)
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato Liberado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para aprobar en el comite de contratación
    def action_contratacion_contrato(self, ):
        if self.acta and self.fecha_comite_contratacion:
            estado = self.env['sicpro.app.contratos.estados'].search(
                [('is_aprobada', '=', True)]).id
            self.estado_interno = 'contratacion'
            self.estado_id = estado
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([
                ('name', '=', 'revision')]).valor
            self.revisado_fecha_inicial = fields.date.today()
            self.revisado_dias_habiles = dias_habiles
            self.revisado_fecha_fin = self.revisado_fecha_inicial + \
                                      timedelta(
                                          days=self.revisado_dias_habiles)
            self.contratacion_persona_contratacion = self.env.uid
            # envio la notificación a los seguidores
            self.message_post(
                body='Contrato aprobado en el Comité de Contratación',
                message_type='notification',
                subtype='mail.mt_comment',
                author_id=self.env.user.partner_id.id
            )
            # redirecciono la salida
            action = self.env.ref(
                'sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(
                _('Los campos del Comité de Contratación no deben estar '
                  'nulos, por favor verifíquelo '))

    # acción para aprobar la revision del contrato
    def action_revision_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_legal', '=', True)]).id
        self.estado_interno = 'revisado'
        self.estado_id = estado
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'legal')]).valor
        self.legal_fecha_inicial = fields.date.today()
        self.legal_dias_habiles = dias_habiles
        self.legal_fecha_fin = self.legal_fecha_inicial + timedelta(
            days=self.legal_dias_habiles)
        self.revisado_persona_revisa = self.env.uid
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato aprobado en su revisión',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para la aprobación legal del contrato
    def action_legal_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_economia', '=', True)]).id
        self.estado_interno = 'legal'
        self.estado_id = estado
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'economia')]).valor
        self.economia_fecha_inicial = fields.date.today()
        self.economia_dias_habiles = dias_habiles
        self.economia_fecha_fin = self.economia_fecha_inicial + timedelta(
            days=self.economia_dias_habiles)
        self.legal_persona_legal = self.env.uid
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato aprobado por Legal',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para la aprobación economica del contrato
    def action_economia_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search(
            [('is_economia_dc', '=', True)]).id
        self.estado_interno = 'economia'
        self.estado_id = estado
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'economia_dc')]).valor
        self.economia_dc_fecha_inicial = fields.date.today()
        self.economia_dc_dias_habiles = dias_habiles
        self.economia_dc_fecha_fin = self.economia_dc_fecha_inicial + timedelta(
            days=self.economia_dc_dias_habiles)
        self.economia_persona_economia = self.env.uid
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato aprobado por Economía',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para la aprobación del DC de economía del contrato
    def action_economia_dc_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_firma_director', '=', True)]).id
        self.estado_interno = 'economia_dc'
        self.estado_id = estado
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'director_central')]).valor
        self.fecha_firma_director_inicial = fields.date.today()
        self.firma_director_dias_habiles = dias_habiles
        self.fecha_firma_director_fin = self.fecha_firma_director_inicial + timedelta(
            days=self.firma_director_dias_habiles)
        self.economia_dc_persona_economia = self.env.uid
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato aprobado por la DC. Economía',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción de la firma del contrato por el director
    def action_firma_director_contrato(self, ):
        if self.fecha_firmado_director:
            estado = self.env['sicpro.app.contratos.estados'].search([
                ('is_firma_proveedor', '=', True)]).id
            self.estado_interno = 'firma_director'
            self.estado_id = estado
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([
                ('name', '=', 'proveedor')]).valor
            self.fecha_firma_proveedor_inicial = fields.date.today()
            self.firma_proveedor_dias_habiles = dias_habiles
            self.fecha_firma_proveedor_fin = self.fecha_firma_proveedor_inicial \
                                             + timedelta(
                days=self.firma_proveedor_dias_habiles)
            self.firma_director_persona = self.env.uid
            # envio la notificación a los seguidores
            self.message_post(
                body='Contrato firmado por el Director',
                message_type='notification',
                subtype='mail.mt_comment',
                author_id=self.env.user.partner_id.id
            )
            # redirecciono la salida
            action = self.env.ref(
                'sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(
                _('Debe proporcionar la fecha de firma del Director Central,'
                  ' verifíquelo '))

    # acción de la firma del contrato por el proveedor
    def action_firma_proveedor_contrato(self, ):
        if self.fecha_firmado_proveedor:
            estado = self.env['sicpro.app.contratos.estados'].search([
                ('is_won', '=', True)]).id
            self.estado_interno = 'firma_proveedor'
            self.estado_id = estado
            self.firma_proveedor_persona = self.env.uid
            self.estado_interno = 'activo'
            self.kanban_state = 'done'
            self.fecha_inicio_contrato = fields.date.today()
            self.fecha_fin_contrato = fields.date.today() + timedelta(
                days=self.vigencia_contrato_anios * 365)
            # envio la notificación a los seguidores
            self.message_post(
                body='Contrato firmado por el Proveedor',
                message_type='notification',
                subtype='mail.mt_comment',
                author_id=self.env.user.partner_id.id
            )
            # redirecciono la salida
            action = self.env.ref(
                'sicpro_app_contratos.contratos_gestion_action').read()[0]
            return action
        else:
            raise UserError(
                _('Debe proporcionar la fecha de firma del Proveedor,'
                  ' verifíquelo '))

    # acción para terminar el contrato
    def action_terminar_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_terminada', '=', True)]).id
        self.estado_interno = 'terminado'
        self.estado_id = estado
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato Terminado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    # acción para reiniciar el contrato
    def action_reiniciar_contrato(self, ):
        estado = self.env['sicpro.app.contratos.estados'].search([
            ('is_inicial', '=', True)]).id
        self.estado_interno = 'nuevo'
        self.estado_id = estado
        self.kanban_state = 'normal'
        # Crear días hábiles y fecha fin de la solicitud del contrato
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'solicitante')]).valor
        self.solicitud_fecha_inicial = fields.date.today()
        self.solicitud_dias_habiles = dias_habiles
        self.solicitud_fecha_fin = fields.date.today() + timedelta(
            days=dias_habiles)
        self.solicitud_persona_solicita = self.env.uid
        self.fecha_inicio_contrato = ''
        self.fecha_fin_contrato = ''
        self.acta = ''
        self.fecha_comite_contratacion = ''
        self.contratacion_persona_contratacion = False
        self.contratacion_fecha_inicial = ''
        self.contratacion_fecha_fin = ''
        self.acuerdo_comite_contratacion = ''
        self.revisado_persona_revisa = False
        self.revisado_fecha_inicial = ''
        self.revisado_fecha_fin = ''
        self.revisado_detalles_contrato = ''
        self.legal_persona_legal = False
        self.consecutivo = ''
        self.legal_fecha_inicial = ''
        self.legal_fecha_fin = ''
        self.legal_detalles_contrato = ''
        self.economia_persona_economia = False
        self.economia_fecha_inicial = ''
        self.economia_fecha_fin = ''
        self.economia_detalles_contrato = ''
        self.economia_dc_persona_economia = False
        self.economia_dc_fecha_inicial = ''
        self.economia_dc_fecha_fin = ''
        self.economia_dc_detalles_contrato = ''
        self.firma_director_persona = False
        self.fecha_firma_director_inicial = ''
        self.fecha_firma_director_fin = ''
        self.fecha_firmado_director = ''
        self.observaciones_firma_director = ''
        self.firma_proveedor_persona = False
        self.fecha_firma_proveedor_inicial = ''
        self.fecha_firma_proveedor_fin = ''
        self.fecha_firmado_proveedor = ''
        self.observaciones_firma_proovedor = ''
        self.esta_rechazada = False
        self.esta_cancelado = False
        # envio la notificación a los seguidores
        self.message_post(
            body='Contrato Reiniciado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action

    @api.model
    def create(self, vals):
        if vals.get('vigencia_contrato_anios') != 0 and \
                vals.get('presupuesto_cup') != 0:
            # Crear la secuencia de incremento para el consecutivo de los
            # contratos
            seq_name = 'Consecutivo de la Preparación Técnicas'
            seq = {
                'code': 'contratos_consecutivo_incrementar',
                'name': _('%s Sequence') % seq_name,
                'implementation': 'no_gap',
                'prefix': 'Contrato/%(range_year)s/',
                'padding': 4,
                'number_increment': 1,
                'use_date_range': True,
            }
            vals['sequence_id'] = self.env['ir.sequence'].sudo().create(seq).id
            res = super(Contratos, self).create(vals)
            res['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code(
                'contratos_consecutivo_incrementar') or _('New')
            # Crear días hábiles y fecha fin de la solicitud del contrato
            dias_habiles = self.env['sicpro.app.contratos.dias'].search([
                ('name', '=', 'solicitante')]).valor
            res['solicitud_dias_habiles'] = dias_habiles
            res['solicitud_fecha_fin'] = fields.date.today() + timedelta(
                days=dias_habiles)
            return res
        else:
            raise UserError(
                _('Debe proporcionar un valor de presupuesto o los días de '
                  'vigencia del contrato, verifíquelo '))


class ContratoRechazado(models.TransientModel):
    _name = 'sicpro.app.contratos.rechazado'
    _description = 'Contratos Rechazados'

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_rechazo(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.contratos'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Contrato rechazado.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno del contrato
        estado = self.env['sicpro.app.contratos.estados'].search(
            [('is_rechazada', '=', True)]).id
        rechazo = self.env[
            'sicpro.app.contratos'].browse(
            self.env.context.get('active_ids'))
        dias_habiles = self.env['sicpro.app.contratos.dias'].search([
            ('name', '=', 'devolucion')]).valor
        for item in rechazo.sudo():
            item.rechazar = self.lost_reason_id
            item.esta_rechazada = True
            item.estado_interno = 'devuelto'
            item.sudo().estado_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_rechazo = fields.date.today()
            item.devolucion_dias_habiles = dias_habiles
            item.fecha_devolucion_fin = item.fecha_rechazo + timedelta(
                days=item.devolucion_dias_habiles)
            item.devuelto_persona_devuelve = self.env.uid
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action


class ContratoCancelado(models.TransientModel):
    _name = 'sicpro.app.contratos.cancelado'
    _description = 'Contratos Cancelados'

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_cancelado(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.contratos'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Contrato cancelado.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno del contrato
        estado = self.env['sicpro.app.contratos.estados'].search(
            [('is_cancelada', '=', True)]).id
        cancelado = self.env[
            'sicpro.app.contratos'].browse(
            self.env.context.get('active_ids'))
        for item in cancelado.sudo():
            item.cancelar = self.lost_reason_id
            item.esta_cancelado = True
            item.estado_interno = 'cancelado'
            item.sudo().estado_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_cancelado = fields.date.today()
            item.cancelado_persona_cancelado = self.env.uid
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_gestion_action').read()[0]
        return action
