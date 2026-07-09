# -*- coding: utf-8 -*-

from datetime import datetime
from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


def _default_color():
    return randint(1, 11)


Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class ControlInformacion(models.Model):
    _name = 'sicpro.app.control.informacion'
    _description = "Control de Información de la DVPE"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Many2one('sicpro.app.control.informacion.actividad', string='Actividad', required=True, index=True,
                           tracking=True, domain="[('areas', 'in', area)]")
    version = fields.Integer(string='Versión', required=False)
    descripcion = fields.Char(string="Descripción", related='name.descripcion')
    gestores = fields.Many2many(comodel_name='res.users', string='Gestores', required=True)
    active = fields.Boolean('Activo', default=True, tracking=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    user_id = fields.Many2one('res.users', string='Usuario', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso', related='user_id.company_id', store=True)
    identificador_corto = fields.Char(string='Id corto', related='company_id.identificador_corto', store=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    documentos_ids = fields.Many2many('ir.attachment', 'documentos_informacion_rel', 'documentos_informacion_id',
                                      'attachment_id', string="Documentos")
    etiquetas_ids = fields.Many2many('sicpro.app.control.informacion.etiquetas', 'etiquetas_informacion_rel',
                                     'etiquetas_id', 'etiqueta_id', string='Etiqueta', tracking=True)
    area = fields.Many2one('sicpro.app.control.informacion.areas', string='Área Informativa')
    fecha_entrega = fields.Date(string='Fecha de Entrega', default=lambda self: fields.Date.context_today(self))
    anio = fields.Char(string="Año", required=False, default=fields.Datetime.now().strftime("%Y"), )
    fecha_requerida = fields.Date(string='Fecha de Requerida', compute='_compute_fecha_requerida')
    estado = fields.Selection(string='Estado', required=True, tracking=True, default='pendiente',
                              selection=[('atrasado', 'Atrasado'), ('pendiente', 'Pendiente'), ('enviado', 'Enviado'),
                                         ('validado', 'Validado'), ('devuelto', 'Devuelto'), ],
                              group_expand='_group_expand_estados',)
    mes = fields.Char(string='Mes', required=False, tracking=True)
    devolucion_motivo = fields.Many2one('sicpro.app.control.informacion.motivos.devolucion',
                                        string="Motivo de Devolución", required=False)
    devolucion_detalles = fields.Text(string="Detalles de la devolución", required=False)
    devolucion_fecha = fields.Date(string='Fecha de devolución')
    devolucion_user_id = fields.Many2one('res.users', string='Devuelto por:', index=True, tracking=True,)
    observaciones = fields.Text(string="Observaciones de la información", required=False)
    doc_count = fields.Integer(compute='_compute_info_docs_count', string="Cuenta Documentos")

    # expandir estados de la vista kanban
    def _group_expand_estados(self, states, domain, order):
        return [key for key, val in type(self).estado.selection]

    # verifico que no exista otra información por validar o validada antes de volver a enviar
    @api.constrains('name')
    def _check_actividad_unica(self):
        uniq = self.env['sicpro.app.control.informacion'].search(
            ['&', '&', '&', '&', ("active", "=", True), ("id", "!=", self.id), ("anio", "=", self.anio),
             ("area", "=", self.area.id),  ("mes", "=", self.mes), ("name", "=", self.name.name),
             ("estado", "in", ['enviado', 'validado'])])

        if uniq:
            raise ValidationError(_("¡Esta información ya fue enviada!. "
                                    "Si cree que es un error contacte al administrador"))

    # genera la fecha requerida
    @api.onchange('name')
    def _compute_fecha_requerida(self):
        for date in self:
            if date.name and date.fecha_requerida is not True:
                mes = fields.Datetime.now().strftime("%m")
                requerida = datetime.strptime(str(date.anio) + '-' + str(mes) + '-' + str(date.name.dia_entrega),
                                              '%Y-%m-%d')
                date.fecha_requerida = requerida

    # genera el área informativa
    @api.onchange('user_id')
    def _compute_area_informativa(self):
        control = self.env['sicpro.app.control.informacion.areas'].search([('company_id', '=', self.company_id.id)])

        if control:
            self.sudo().area = control.id
        else:
            raise ValidationError(_("¡El usuario actual no pertenece a ninguna área de información!. "
                                    "Si cree que es un error contacte al administrador"))

    # genera el mes de la información
    @api.onchange('fecha_entrega')
    def _compute_mes(self):
        for item in self:
            fecha_entrega = item.fecha_entrega
            if fecha_entrega:
                mes_id = fecha_entrega.month
                nombre_mes = self.env['sicpro.nomenclador.meses'].search(
                    ['&', ('active', '=', True), ('codigo_mes', '=', mes_id)])
                item.mes = nombre_mes.name
            else:
                item.mes = '-'

    # control de versiones
    def action_empaty_version(self):
        action = None

    # control de versiones
    def action_empaty_documentos(self):
        action = None

    # Cuenta los adjuntos del registro
    def _compute_info_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count(
                ['&', ('res_model', '=', 'sicpro.app.control.informacion'), ('res_id', '=', documentos.id)])

    # botón para enviar la información
    def action_enviar_info(self):
        # verífico que no exista otra documentación igual en proceso
        self._check_actividad_unica()
        if self.doc_count != 0:
            # cambio el estado del registro
            self.estado = 'enviado'

            # actualizo la version de la información
            cuenta_version = self.env['sicpro.app.control.informacion'].search_count(
                ['&', '&', ("active", "=", True), ("anio", "=", self.anio), ("mes", "=", self.mes),
                 ("name", "=", self.name.name)])
            self.version = cuenta_version

            # ejecuto el cron de la aplicación para actualizar los controles
            control_info = self.env['sicpro.app.control.informacion.control.actividades'].search([], limit=1)
            control_info.cron_control_informaciones()

            # busco usuarios del rol de revisión de la documentación
            # agrego los seguidores al modelo
            for item in self.name.gestores:
                self.message_subscribe(partner_ids=item.partner_id.ids)
            # envío la notificación
            self.message_post(body='Validar Información', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_control_informacion.control_informacion_nueva')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # redirecciono la salida
            action = self.env.ref('sicpro_app_control_informacion.control_informaciones_action').sudo().read()[0]
            return action
        else:
            raise UserError(_('Debe proporcionar una documentación válida, verifíquelo '))

    # botón para validar la información
    def action_validar_info(self):
        if self.doc_count != 0:
            # cambio el estado del registro
            self.sudo().estado = 'validado'

            # ejecuto el cron de la aplicación para actualizar los controles
            control_info = self.env['sicpro.app.control.informacion.control.actividades'].search([], limit=1)
            control_info.cron_control_informaciones()

            # envío la notificación
            self.sudo().message_post(body='Información validada', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.sudo().message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.sudo().env.context.copy()
                template = self.sudo().env.ref('sicpro_app_control_informacion.control_informacion_validada')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_control_informacion.control_informaciones_action').sudo().read()[0]
            return action
        else:
            raise UserError(_('Debe proporcionar una documentación válida, verifíquelo '))


# motivo de rechazo
class ControlInformacionMotivoRechazo(models.TransientModel):
    _name = 'sicpro.app.control.informacion.devueltas'
    _description = 'Motivo de devolución de la información'

    motivo_id = fields.Many2one('sicpro.app.control.informacion.motivos.devolucion', string="Motivo de Devolución",
                                required=True)
    detalles = fields.Text(string="Detalles de la devolución", required=True)

    def action_motivo_devolucion(self):
        info = self.sudo().env['sicpro.app.control.informacion'].browse(self.env.context.get('active_ids'))
        for item in info.sudo():
            item.devolucion_motivo = self.motivo_id
            item.devolucion_detalles = self.detalles
            item.devolucion_fecha = datetime.today()
            item.devolucion_user_id = self.env.uid
            item.estado = 'devuelto'

        # ejecuto el cron de la aplicación para actualizar los controles
        control_info = self.env['sicpro.app.control.informacion.control.actividades'].search([], limit=1)
        control_info.cron_control_informaciones()

        # envío la notificación
        info.message_post(body='Información devuelta', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in info.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.sudo().env.context.copy()
            template = self.sudo().env.ref('sicpro_app_control_informacion.control_informacion_devuelta')
            template.with_context(local_context).send_mail(info.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_control_informacion.control_informaciones_action').sudo().read()[0]
        return action
