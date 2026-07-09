# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, api, SUPERUSER_ID
from odoo.tools import format_date

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class FuerzasMedios(models.Model):
    _name = 'sicpro.app.fuerzas.medios'
    _description = "Fuerzas y Medios"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.fuerzas.medios.estados'].search([('company_id', '=', self.env.company.id)], limit=1)

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Orden de Trabajo", required=False, index=True, tracking=True, default='-')
    active = fields.Boolean('Activo', default=True, tracking=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    user_id = fields.Many2one('res.users', string='Solícita la Orden', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    estado_id = fields.Many2one('sicpro.app.fuerzas.medios.estados', string='Estados', ondelete='restrict',
                                tracking=True, group_expand='_read_group_stage_ids', index=True, copy=False,
                                default=_get_default_stage_id)
    is_paralizado = fields.Boolean('Paralizada', related='estado_id.is_paralizado')
    is_cancelado = fields.Boolean('Cancelada', related='estado_id.is_cancelado')
    is_terminada = fields.Boolean('Terminada', related='estado_id.is_terminada')
    is_en_proceso = fields.Boolean('En Proceso', related='estado_id.is_en_proceso')
    etiquetas_ids = fields.Many2many('sicpro.app.fuerzas.medios.etiquetas', 'sicpro_app_ordenes_etiquetas_rel',
                                     'orden_id', 'etiqueta_id', string='Etiqueta', tracking=True)
    priority = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')


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

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

# motivo de rechazo
class FuerzasMediosMotivoRechazo(models.TransientModel):
    _name = 'sicpro.app.fuerzas.medios.rechazadas'
    _description = 'Motivo de rechazo de las fuerzas medios'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        orden = self.env['sicpro.app.fuerzas.medios'].browse(self.env.context.get('active_ids'))
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
            template = self.env.ref('sicpro_app_fuerzas_medios.ordenes_rechazo_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_fuerzas.medios_transferencias_gastos_action').sudo().read()[0]
        return action


# motivo de cancelación
class FuerzasMediosMotivoCancelacion(models.TransientModel):
    _name = 'sicpro.app.fuerzas.medios.canceladas'
    _description = 'Motivo de cancelación de las fuerzas medios'

    motivo_id = fields.Text(string="Motivo de Cancelación", required=True)

    def action_motivo_cancelacion(self):
        orden = self.env['sicpro.app.fuerzas.medios'].browse(self.env.context.get('active_ids'))
        for item in orden.sudo():
            estado = self.env['sicpro.app.fuerzas.medios'].search(
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
            template = self.env.ref('sicpro_app_fuerzas_medios.ordenes_cambios_orden')
            template.with_context(local_context).send_mail(orden.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_fuerzas_medios.transferencias_gastos_action').sudo().read()[0]
        return action
