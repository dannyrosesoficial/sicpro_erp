# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _
import os
import logging
from odoo.exceptions import UserError
from odoo.addons.sicpro_modulo_monto_texto.models.monto2texto import Monto2Texto

_logger = logging.getLogger(__name__)

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class ContratosEconomia(models.Model):
    _name = 'sicpro.app.contratos.economia'
    _description = 'Gestión económica de los contratos'
    _order = "prioridad desc, id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # Agrego el estado por defecto
    def _get_default_stage_ids(self):
        return self.env['sicpro.app.contratos.economia.estados'].search([], limit=1)

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Many2one('sicpro.app.contratos', 'Contratos', tracking=True, required=True, index=True,
                           domain="[('estado_id.is_won', '=', True)]")
    facturas_id = fields.Many2one(comodel_name="sicpro.app.contratos.economia.facturas", string="Facturación",
                                  required=False)
    facturas_ids = fields.One2many('sicpro.app.contratos.economia.facturas', 'economia', 'Facturaciónes', )
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    prioridad = fields.Selection(Prioridades_Activas, string='Prioridad Económica', index=True, tracking=True,
                                 default=Prioridades_Activas[0][0])
    estado_id = fields.Many2one('sicpro.app.contratos.economia.estados', string='Estados', ondelete='restrict',
                                tracking=True, index=True, copy=False, group_expand='_read_group_stage_ids',
                                default=_get_default_stage_ids)
    kanban_state = fields.Selection([('normal', 'Borrador'), ('blocked', 'Rechazado'), ('done', 'Aprobado'), ],
                                    string='Estado interno', copy=False, default='normal', readonly=True)
    user_id = fields.Many2one('res.users', string='Gestor del proveedor', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                       readonly=True)
    etiquetas = fields.Many2many('sicpro.app.contratos.economia.etiquetas',
                                 'sicpro_app_contratos_economia_etiquetas_rel', string='Etiqueta')
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    doc_count = fields.Integer(compute='_compute_contratos_economia_docs_count', string="Documentos")
    facturas_count = fields.Integer(compute='_compute_contratos_economia_facturas_count', string="Facturas")
    monto_facturado = fields.Monetary(currency_field='company_currency', string="Facturado",
                                      compute='_compute_contratos_economia_suma_montos')
    monto_texto = fields.Char(string='Monto en Texto', compute='_monto_texto')
    tipo_facturacion = fields.Selection(string='Tipo de facturación', required=True,
                                        selection=[('factura', 'Factura'), ('prefactura', 'Prefactura'), ], )
    estado_interno = fields.Selection(
        [('nuevo', 'nuevo'), ('sip', 'sip'), ('emision', 'emision'), ('transito', 'transito'),
         ('terminado', 'Terminado')], index=True, required=True, default=lambda self: 'nuevo')
    banco_dvpe = fields.Many2one(comodel_name='sicpro.app.contratos.economia.bancos', string='Banco DVPE',
                                 required=False, domain="[('tipo_banco', '=', 'dvpe')]")
    cuentas_banco_dvpe = fields.Many2many('sicpro.app.contratos.economia.cuentas.dvpe',
                                          'sicpro_app_contratos_bancos_cuentas_dvpe_rel',
                                          related='banco_dvpe.cuenta_dvpe')
    cuenta_dvpe = fields.Many2one('sicpro.app.contratos.economia.cuentas.dvpe', string='Nombre DVPE',
                                  domain="[('id', 'in',cuentas_banco_dvpe)]", required=False)
    numero_cuenta_dvpe = fields.Char(string='Cuenta DVPE', compute='_onchange_cuenta_dvpe')
    tipo_banco_dvpe = fields.Selection(string='Tipo de Banco DVPE', store=True, related='banco_dvpe.filtro_banco', )
    banco_beneficiario = fields.Many2one(comodel_name='sicpro.app.contratos.economia.bancos',
                                         string='Banco Beneficiario', required=False,
                                         domain="[('tipo_banco', '=', 'beneficiario')]")
    cuentas_banco_beneficiario = fields.Many2many('sicpro.app.contratos.beneficiarios',
                                                  'sicpro_app_contratos_bancos_cuentas_beneficiario_rel',
                                                  related='banco_beneficiario.cuenta_beneficiario')
    cuenta_beneficiario = fields.Many2one('sicpro.app.contratos.beneficiarios', string='Nombre Beneficiario',
                                          required=False)  # domain="[('id', 'in',cuentas_banco_beneficiario)]",
    numero_cuenta_beneficiario = fields.Char(string='Cuenta Beneficiaro', compute='_onchange_cuenta_beneficiario')

    ###########################################################################
    # Rol_sp
    sequence_consecutivo = fields.Char(string='Secuencia del contrato', copy=False, readonly=True, )
    sp_fecha_solicitud = fields.Date(string='Fecha de Solicitud', default=lambda self: fields.Date.context_today(self))
    sol_pago_area = fields.Many2one('sicpro.app.contratos.areas', store=True, related='name.area_contrato',
                                    string='Área SP', readonly=True, )
    sol_pago_division = fields.Char(string='División', required=False,
                                    default='División de Proyectos y Ejecución de Obras', )
    sol_pago_cuenta_gasto = fields.Many2one('sicpro.nomenclador.cuentas.contables', string='Cuenta de Gastos',
                                            tracking=True)
    sol_pago_cuenta_gasto_name = fields.Char(related='sol_pago_cuenta_gasto.descripcion', store=True)
    sol_pago_centro_costo = fields.Many2one('sicpro.nomenclador.centro.costo', string='Centro de Costo', tracking=True)
    sol_pago_fecha_emision = fields.Date(string='Emisión SP', required=False, )
    sol_pago_orden_trabajo = fields.Char(string='Inversión', required=False, )
    sol_pago_concepto = fields.Text(string="Concepto de pago", required=False, )
    sol_pago_observaciones = fields.Text(string="Observaciones SP", required=False, )
    sol_pago_cumplimiento_cronograma = fields.Selection(string='Cumplimiento Cronograma',
                                                        selection=[('bl_aw', 'B/L Ó A/W'), ('ir', 'I.R'),
                                                                   ('recibo_almacen', 'Recibo en almacén'),
                                                                   ('acta_aceptacion', 'Acta de aceptación'),
                                                                   ('otros', 'Otros'), ], required=True, )

    ###########################################################################
    # Rol_sip
    sip_consecutivo = fields.Char(string='Consecutivo', tracking=True, )
    sip_sequence_consecutivo = fields.Char(string='Secuencia SIP', copy=False, readonly=True, )
    sip_beneficiario = fields.Many2one('sicpro.app.contratos.beneficiarios', string='Beneficiario', tracking=True,
                                       required=False)
    sip_beneficiario_cuenta = fields.Char(string='Cuenta Beneficiario', tracking=True,
                                          related='sip_beneficiario.cuenta_beneficiario', store=True)
    sip_fecha_emision = fields.Date(string='Emisión SIP', default=lambda self: fields.Date.context_today(self))
    sip_indicador = fields.Many2one('sicpro.app.contratos.economia.indicador', string='Indicador', tracking=True, )
    sip_acapite = fields.Many2one('sicpro.app.contratos.economia.acapite', string='Acápite', tracking=True, )
    sip_observaciones = fields.Html(string="Observaciones SIP", store=True)
    ###########################################################################
    # accion Rol_ip
    emision_sequence_consecutivo = fields.Char(string='No.', copy=False, readonly=False, tracking=True)
    emision_fecha = fields.Date(string='Fecha de Emisión', )
    emision_observaciones = fields.Html(string="Detalles Emisión", store=True)
    emision_aceptada_fecha = fields.Date(string='Emisión Aceptada', )
    emision_cancelada_fecha = fields.Date(string='Emisión Cancelada', )
    emision_motivo_cancelacion = fields.Text(string="Motivo de Cancelación de la Emisión")
    emision_cancelada_accion = fields.Selection(string='Acción al Cancelar', required=False,
                                                selection=[('emitir', 'Emitir'), ('no_emitir', 'No Emitir'), ], )
    emision_debitar = fields.Selection(string='Debitar', required=False,
                                       selection=[('transferir', 'Transferir'), ('efectivo', 'Pagar en Efectivo'),
                                                  ('cheque', 'Emitir Cheque de Gerencia'), ], )
    emision_pago_bfi = fields.Selection(string='Pago BFI', required=False,
                                        selection=[('bfi_extranjero', 'TRANSFERENCIA AL EXTRANJERO'),
                                                   ('bfi_banco', 'TRANSFERENCIA A OTRO BANCO EN CUBA'),
                                                   ('bfi_cuenta', 'TRASPASO DE FONDOS A OTRA CUENTA EN EL BFI'),
                                                   ('bfi_efectivo', 'PAGO EN EFECTIVO EN OTRA SUCURSAL BFI'),
                                                   ('otra', 'Otra'), ], )
    emision_beneficiario_bfi = fields.Selection(string='Beneficiario BFI', required=False,
                                                selection=[('cooperativas', 'Cooperativas No Agropecuarias'),
                                                           ('cuenta_propia', 'Trabajador por Cuenta Propia'),
                                                           ('dep_art_ind', 'Deportistas, Artesanos y Artistas Ind.'),
                                                           ('capital_cubano', 'Capital 100% Cubano'),
                                                           ('capital_extranjero', 'Capital 100% Extranjero'),
                                                           ('aei', 'Asociación Económica Internacional (AEI)'),
                                                           ('mixto', 'Capital Mixto'), ('otros', 'Otros'), ], )
    emision_id_bfi = fields.Char(string='ID BFI', tracking=True, size=11)
    ###########################################################################
    # accion Rol_ip
    ###########################################################################
    transito_cancelado = fields.Date(string='Cancelado', tracking=True, )
    transito_estado_cuenta = fields.Date(string='Estado Cuenta', tracking=True, )

    terminado_fecha = fields.Date(string='Fecha de Terminación', readonly=True)
    ###########################################################################
    # Campos heredados del modelo de contratos
    ###########################################################################
    sequence_consecutivo_contratos = fields.Char(string='Contrato', store=True, related='name.sequence_consecutivo')

    proveedor = fields.Many2one('sicpro.app.contratos.proveedores', store=True, string='Proveedor',
                                related='name.proveedor')
    tipo_contrato = fields.Many2one('sicpro.app.contratos.tipo', string='Tipo', related='name.tipo_contrato',
                                    store=True)
    pep = fields.Char(string="Código SAP Contrato", related='name.pep', store=True)
    solicitud_fecha_inicial = fields.Date(store=True, string="Solicitud Fecha Inicial",
                                          related='name.solicitud_fecha_inicial')
    solicitud_persona_solicita = fields.Many2one('res.users', string='Solicitado por:',
                                                 related='name.solicitud_persona_solicita', store=True)
    solicitud_fecha_fin = fields.Date(string="Solicitud Fecha Fin", store=True, related='name.solicitud_fecha_fin')
    observaciones = fields.Html(string="Observaciones economía", store=True)
    acta = fields.Char(string="No. Acta", related='name.acta', store=True)
    fecha_comite_contratacion = fields.Date(string="Fecha del Comité", related='name.fecha_comite_contratacion',
                                            store=True, )
    forma_pago_contratos = fields.Many2many('sicpro.app.contratos.economia.pago', 'sicpro_app_contratos_forma_pago_rel',
                                            related='name.forma_pago', string='Forma de Pago')
    forma_pago = fields.Many2one('sicpro.app.contratos.economia.pago', string='Método de Pago', required=False,
                                 domain="[('id', '=', forma_pago_contratos)]")
    forma_pago_genera_consecutivo = fields.Boolean()

    plazo_pago = fields.Integer(string='Plazo de Pago', related='name.plazo_pago', store=True)
    presupuesto_cup = fields.Monetary('Presupuesto', store=True, currency_field='company_currency',
                                      related='name.presupuesto_cup')
    vigencia_contrato_anios = fields.Integer(string='Vigencia (Años)', related='name.vigencia_contrato_anios',
                                             store=True)
    uodc = fields.Many2one('sicpro.app.contratos.unidades', string='Unidad', related='name.uodc', store=True)
    area_contrato = fields.Many2one('sicpro.app.contratos.areas', store=True, string='Área del contrato',
                                    related='name.area_contrato')
    prioridad_contrato = fields.Selection(string='Prioridad contrato', related='name.prioridad', store=True)
    fecha_inicio_contrato = fields.Date(string="Inicio del Contrato", related='name.fecha_inicio_contrato', store=True)
    fecha_fin_contrato = fields.Date(string="Fin del Contrato", related='name.fecha_fin_contrato', store=True)
    moneda = fields.Many2one('res.currency', string='Moneda', required=False)
    ###########################################################################
    # Campos heredados del modelo de proveedores
    ###########################################################################
    domicilio_social = fields.Char(string='Domicilio', store=True, related='name.proveedor.domicilio_social')
    nombre_directivo = fields.Char(string='Nombre Directivo', store=True, related='name.proveedor.nombre_directivo')
    cargo_directivo = fields.Char(string='Cargo', store=True, related='name.proveedor.cargo_directivo')
    telefono_fijo = fields.Char(string="Teléfono", store=True, related='name.proveedor.telefono_fijo')
    telefono_movil = fields.Char(string="Móvil", store=True, related='name.proveedor.telefono_movil')
    correo = fields.Char(string="Correo electrónico", related='name.proveedor.correo', store=True)
    codigo_reeup = fields.Char(string="Código REEUP / ONE", store=True, related='name.proveedor.codigo_reeup')
    servicio_comercializable = fields.Text(related='name.proveedor.servicio_comercializable', store=True,
                                           string="Servicio Comercial")
    pep_proveedor = fields.Char(string="Código SAP Proveedor", related='name.proveedor.pep', store=True)
    tipo = fields.Many2one(comodel_name='sicpro.app.contratos.proveedores.tipo', string='Tipo P.',
                           related='name.proveedor.tipo', store=True)
    fecha_agregado = fields.Date(string="Agregado", store=True, related='name.proveedor.fecha_agregado')

    ###########################################################################
    # Dígitos cuenta DVPE
    digito_1_cuenta_dvpe = fields.Char(string='digito_1_dvpe')
    digito_2_cuenta_dvpe = fields.Char(string='digito_2_dvpe')
    digito_3_cuenta_dvpe = fields.Char(string='digito_3_dvpe')
    digito_4_cuenta_dvpe = fields.Char(string='digito_4_dvpe')
    digito_5_cuenta_dvpe = fields.Char(string='digito_5_dvpe')
    digito_6_cuenta_dvpe = fields.Char(string='digito_6_dvpe')
    digito_7_cuenta_dvpe = fields.Char(string='digito_7_dvpe')
    digito_8_cuenta_dvpe = fields.Char(string='digito_8_dvpe')
    digito_9_cuenta_dvpe = fields.Char(string='digito_9_dvpe')
    digito_10_cuenta_dvpe = fields.Char(string='digito_10_dvpe')
    digito_11_cuenta_dvpe = fields.Char(string='digito_11_dvpe')
    digito_12_cuenta_dvpe = fields.Char(string='digito_12_dvpe')
    digito_13_cuenta_dvpe = fields.Char(string='digito_13_dvpe')
    digito_14_cuenta_dvpe = fields.Char(string='digito_14_dvpe')
    digito_15_cuenta_dvpe = fields.Char(string='digito_15_dvpe')
    digito_16_cuenta_dvpe = fields.Char(string='digito_16_dvpe')
    ###########################################################################
    # Cuenta Beneficiario
    digito_1_cuenta_beneficiario = fields.Char(string='digito_1_beneficiario')
    digito_2_cuenta_beneficiario = fields.Char(string='digito_2_beneficiario')
    digito_3_cuenta_beneficiario = fields.Char(string='digito_3_beneficiario')
    digito_4_cuenta_beneficiario = fields.Char(string='digito_4_beneficiario')
    digito_5_cuenta_beneficiario = fields.Char(string='digito_5_beneficiario')
    digito_6_cuenta_beneficiario = fields.Char(string='digito_6_beneficiario')
    digito_7_cuenta_beneficiario = fields.Char(string='digito_7_beneficiario')
    digito_8_cuenta_beneficiario = fields.Char(string='digito_8_beneficiario')
    digito_9_cuenta_beneficiario = fields.Char(string='digito_9_beneficiario')
    digito_10_cuenta_beneficiario = fields.Char(string='digito_10_beneficiario')
    digito_11_cuenta_beneficiario = fields.Char(string='digito_11_beneficiario')

    ###########################################################################

    # acción del botón documentos, presupuesto, facturas
    # no hace ninguna función
    def action_empaty_economia(self, ):
        action = None

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # Cuenta los adjuntos de la documentacion económica
    def _compute_contratos_economia_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count(
                ['&', ('res_model', '=', 'sicpro.app.contratos.economia'), ('res_id', '=', documentos.id)])

    # Cuenta las facturas o pre facturas
    def _compute_contratos_economia_facturas_count(self):
        data = self.env['sicpro.app.contratos.economia.facturas']
        for facturacion in self:
            facturacion.facturas_count = data.search_count([('economia', '=', self._origin.id)])

    # suma monto facturado
    def _compute_contratos_economia_suma_montos(self):
        data = self.env['sicpro.app.contratos.economia.facturas']
        for monto in self:
            gasto = data.search([('economia', '=', self._origin.id)])
            monto.monto_facturado = sum(gasto.mapped('factura_monto'))

    # acción para realizar la solicitud de instrumento de pago
    def action_sip(self, ):
        if self.facturas_count > 0:
            estado = self.env['sicpro.app.contratos.economia.estados'].search([('is_instrumento', '=', True)]).id
            bancos = self.env['sicpro.app.contratos.economia.bancos'].search(
                [('cuenta_beneficiario', 'in', self.name.beneficiario_nombre.id)])
            banco = 0
            for item in bancos:
                banco = item.id
            self.write({'estado_interno': 'sip', 'estado_id': estado, 'sip_beneficiario': self.name.beneficiario_nombre,
                        'sip_beneficiario_cuenta': self.name.beneficiario_cuenta, 'banco_beneficiario': banco, })

            # Crear la secuencia de incremento para el consecutivo del
            # instrumento de pago
            self.sip_sequence_consecutivo = self.env['ir.sequence'].next_by_code(
                'contratos_economia_instrumento_consecutivo_incrementar')
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_economia_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío la notificación a los seguidores
            self.message_post(body='Instrumento de pago solicitado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_economia_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Debe agregar Facturas / Pre facturas para poder continuar, '
                              'verifíquelo.'))

    # acción para realizar la emisión de pago
    def action_emision(self, ):
        if self.forma_pago and self.sip_beneficiario:
            estado = self.env['sicpro.app.contratos.economia.estados'].search([('is_emision', '=', True)]).id
            self.write({'estado_interno': 'emision', 'estado_id': estado, })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_economia_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío la notificación a los seguidores
            self.message_post(body='Emisión de pago solicitado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Crear la secuencia de incremento para el
            # consecutivo de la emisión de pago
            if self.forma_pago_genera_consecutivo:
                self.emision_sequence_consecutivo = self.env['ir.sequence'].next_by_code(
                    'contratos_economia_emision_consecutivo_incrementar')
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_economia_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Existen campos de la Solicitud de Instrumento '
                              'de pago sin completar, por favor verifíquelo.'))

    # acción para pasar la solicitud de pago a tránsito
    def action_transito(self, ):
        if self.emision_fecha and self.banco_dvpe and self.cuenta_dvpe and self.banco_beneficiario and self.sip_beneficiario_cuenta:
            estado = self.env['sicpro.app.contratos.economia.estados'].search([('transito', '=', True)]).id
            self.write({'estado_interno': 'transito', 'estado_id': estado, 'kanban_state': 'blocked', })
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_contratos.contratos_economia_cambio_estados')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío la notificación a los seguidores
            self.message_post(body='Solicitud de pago en tránsito', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_contratos.contratos_economia_gestion_action').read()[0]
            return action
        else:
            raise UserError(_('Existen campos de la emisión de pago sin completar,'
                              ' por favor verifíquelo.'))

    # acción para terminar la solicitud de pago
    def action_terminado(self, ):
        estado = self.env['sicpro.app.contratos.economia.estados'].search([('is_final', '=', True)]).id
        self.write({'estado_interno': 'terminado', 'estado_id': estado, 'kanban_state': 'done',
                    'terminado_fecha': fields.Date.context_today(self), })
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_contratos.contratos_economia_cambio_estados')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # envío la notificación a los seguidores
        self.message_post(body='Solicitud de pago terminada', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_contratos.contratos_economia_gestion_action').read()[0]

        rainbow = {'effect': {'fadeout': 'slow', 'message': 'Felicidades. Las operaciones han sido validadas '
                                                            'correctamente', 'type': 'rainbow_man', }}
        return rainbow

    # acción para volver a emitir el consecutivo de la emisión de pago
    def action_reemitir_emision(self, ):
        # Crear la secuencia de incremento para el
        # consecutivo de la emisión de pago
        self.emision_sequence_consecutivo = self.env['ir.sequence'].next_by_code(
            'contratos_economia_emision_consecutivo_incrementar')

    # verífica el cambio del banco de la dvpe
    @api.onchange('banco_dvpe')
    def _onchange_banco_dvpe(self):
        self.cuenta_dvpe = ''

    # busca el # de cuenta del banco de la dvpe
    @api.depends('cuenta_dvpe')
    def _onchange_cuenta_dvpe(self):
        self.numero_cuenta_dvpe = self.cuenta_dvpe.cuenta

    # verífica el cambio del banco del beneficiario
    @api.onchange('banco_beneficiario')
    def _onchange_banco_beneficiario(self):
        self.cuenta_beneficiario = ''

    # busca el # de cuenta del banco del beneficiario
    @api.depends('cuenta_beneficiario')
    def _onchange_cuenta_beneficiario(self):
        self.numero_cuenta_beneficiario = self.cuenta_beneficiario.cuenta_beneficiario

    # agrego la cuenta del beneficiario y moneda
    @api.onchange('sip_beneficiario')
    def _onchange_sip_beneficiario(self):
        data = self.env['sicpro.app.contratos.economia.bancos'].search(
            [('cuenta_beneficiario', 'in', self.sip_beneficiario.id)])
        banco = 0
        for item in data:
            banco = item.id
        self.sip_beneficiario_cuenta = self.sip_beneficiario.cuenta_beneficiario
        self.moneda = self.sip_beneficiario.moneda
        self.banco_beneficiario = banco

    # Convierto el monto total en texto
    def _monto_texto(self):
        num2text = Monto2Texto()
        monto = self.monto_facturado
        self.monto_texto = num2text.Numero_Texto(monto)

    # verífica si la forma de pago seleccionada genera id de consecutivo
    @api.onchange('forma_pago')
    def _onchange_forma_pago(self):
        self.forma_pago_genera_consecutivo = self.forma_pago.is_genera

    # trae la moneda que viene del contrato a la solicitud de pago
    @api.onchange('name')
    def _onchange_name(self):
        self.moneda = self.name.beneficiario_moneda

    # Relleno los dìgitos de la cuenta de la DVPE
    @api.onchange('numero_cuenta_dvpe')
    def _onchange_numero_cuenta_dvpe(self):
        if self.numero_cuenta_dvpe:
            data = self.numero_cuenta_dvpe
            digit = [str(x) for x in data]
        else:
            digit = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

        self.digito_1_cuenta_dvpe = digit[0]
        self.digito_2_cuenta_dvpe = digit[1]
        self.digito_3_cuenta_dvpe = digit[2]
        self.digito_4_cuenta_dvpe = digit[3]
        self.digito_5_cuenta_dvpe = digit[4]
        self.digito_6_cuenta_dvpe = digit[5]
        self.digito_7_cuenta_dvpe = digit[6]
        self.digito_8_cuenta_dvpe = digit[7]
        self.digito_9_cuenta_dvpe = digit[8]
        self.digito_10_cuenta_dvpe = digit[9]
        self.digito_11_cuenta_dvpe = digit[10]
        self.digito_12_cuenta_dvpe = digit[11]
        self.digito_13_cuenta_dvpe = digit[12]
        self.digito_14_cuenta_dvpe = digit[13]
        self.digito_15_cuenta_dvpe = digit[14]
        self.digito_16_cuenta_dvpe = digit[15]

    # Relleno los digitos del ID del beneficiario
    @api.onchange('emision_id_bfi')
    def _onchange_emision_id_bfi(self):
        if self.emision_id_bfi:
            data = self.emision_id_bfi
            digit = [str(x) for x in data]
        else:
            digit = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

        if len(digit) == 11:
            self.digito_1_cuenta_beneficiario = digit[0]
            self.digito_2_cuenta_beneficiario = digit[1]
            self.digito_3_cuenta_beneficiario = digit[2]
            self.digito_4_cuenta_beneficiario = digit[3]
            self.digito_5_cuenta_beneficiario = digit[4]
            self.digito_6_cuenta_beneficiario = digit[5]
            self.digito_7_cuenta_beneficiario = digit[6]
            self.digito_8_cuenta_beneficiario = digit[7]
            self.digito_9_cuenta_beneficiario = digit[8]
            self.digito_10_cuenta_beneficiario = digit[9]
            self.digito_11_cuenta_beneficiario = digit[10]
        else:
            self.emision_id_bfi = ''
            # raise UserError(_('El campo ID BFI esta vacío o no contiene todos  # los caracteres requeridos (11), verifíquelo.'))

    # acción para emitir la transferencia del banco metropolitano
    def emitir_transferencia_banco_metropolitano(self):
        return {'type': 'ir.actions.report', 'model': 'sicpro.app.contratos.economia', 'report_type': 'qweb-pdf',
                'report_name': 'sicpro_app_contratos.reporte_transferencia_bancaria_metropolitano', }

    # acción para emitir la transferencia del banco BFI
    def emitir_transferencia_banco_bfi(self):
        return {'type': 'ir.actions.report', 'model': 'sicpro.app.contratos.economia', 'report_type': 'qweb-pdf',
                'report_name': 'sicpro_app_contratos.reporte_transferencia_bancaria_bfi', }

    @api.model
    def create(self, vals):
        # Crear la secuencia de incremento para el consecutivo de la
        # solicitud de pago
        res = super(ContratosEconomia, self).create(vals)
        res['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code('contratos_economia_consecutivo_incrementar')

        # busco los usuarios con permisos de visualización
        visualizar = self.env.ref('sicpro_app_contratos.grupo_app_contratos_economia_visual').users
        sp = self.env.ref('sicpro_app_contratos.grupo_app_contratos_economia_operaciones_sp').users
        sip = self.env.ref('sicpro_app_contratos.grupo_app_contratos_economia_operaciones_sip').users
        ep = self.env.ref('sicpro_app_contratos.grupo_app_contratos_economia_operaciones_ip').users
        # creo la lista de seguidores
        seguidores = visualizar + sp + sip + ep
        # agrego los seguidores al modelo
        res.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envió la notificación a los seguidores
        res.message_post(body='Solicitud de pago creada', subtype_xmlid='mail.mt_comment',
                         author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in seguidores:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            template = self.env.ref('sicpro_app_contratos.contratos_economia_nuevos')
            template.send_mail(res.id, force_send=True, email_values=email_values)
        return res


class ContratosEconomiaFacturas(models.Model):
    _name = 'sicpro.app.contratos.economia.facturas'
    _description = 'Facturas de los contratos'
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.contratos', 'Contratos', required=False, index=True)
    tipo = fields.Selection(string='Tipo factura', required=False,
                            selection=[('factura', 'Factura'), ('prefactura', 'Prefactura'), ], )
    ##########################################################################
    # La factura y prefactura se ejecutan dentro de la solicitud de pago
    # y solo se puede ejecutar una de las opciones
    ##########################################################################
    factura_numero = fields.Char(string='Factura', tracking=True, required=True)
    factura_Proveedor = fields.Many2one('sicpro.app.contratos.proveedores', string='Proveedor', tracking=True, )
    factura_fecha_emision = fields.Date(string='Emisión de Factura', tracking=True, )
    factura_fecha_recogida = fields.Date(string='Recibida y Aceptada', tracking=True, )
    factura_tipo_moneda = fields.Many2one('res.currency', string='Moneda', )
    factura_monto = fields.Monetary(string='Monto', tracking=True, required=True,
                                    currency_field='factura_tipo_moneda', )
    economia = fields.Many2one('sicpro.app.contratos.economia', 'economia', index=True, )

    # verifica que la fecha de recibida no sea anterior a
    # la emision de la factura
    @api.depends('factura_fecha_emision')
    @api.onchange('factura_fecha_recogida')
    def _onchange_factura_fecha_recogida(self):
        if self.factura_fecha_recogida < self.factura_fecha_emision:
            self.factura_fecha_recogida = ""
            raise UserError(_('La fecha de recogida de la factura no puede ser menor que '
                              'la fecha de emisión, verifíquelo.'))

    # verifica que la factura ya exista o que halla sido pagada
    @api.onchange('factura_numero')
    def _onchange_factura_numero(self):
        factura = self.factura_numero
        proveedor = self.factura_Proveedor.id

        facturas = self.env['sicpro.app.contratos.economia.facturas'].search(
            ['&', ('factura_numero', '=', factura), ('factura_Proveedor', '=', proveedor), ])
        data = self.env['sicpro.app.contratos.economia'].search(
            ['&', ('facturas_ids', '=', facturas.id), ('emision_aceptada_fecha', '!=', False), ])

        if data:
            raise UserError(
                _("Esta factura perteneciente al proveedor: " + str(self.factura_Proveedor.name) + "  verifíquelo."))

    ###########################################################################
