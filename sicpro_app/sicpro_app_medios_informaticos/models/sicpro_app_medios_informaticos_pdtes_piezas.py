# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MediosInformaticosPdtesPiezas(models.Model):
    _name = 'sicpro.app.medios.informaticos.pdtes.piezas'
    _description = "Medios Informáticos Pendiente por Piezas"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos.taller', 'No. de Inventario', required=True,
                           domain="[('tique_cerrado', '=', False)]", )
    active = fields.Boolean('Activo', default=True)
    equipo = fields.Char('Equipo', related='name.equipo', store=True, )
    no_orden = fields.Char('No. de Orden', required=True)
    no_tique = fields.Char('Tique', related='name.no_tique', store=True, )
    denominacion = fields.Text('Denominación del Equipo', related='name.denominacion', store=True, )
    usuario_ant = fields.Many2one('sicpro.app.trabajadores', 'Usuario anterior', )
    pieza_orden_trabajo = fields.Char('Pieza en la orden del Trabajo', )
    observaciones_glpi = fields.Text('Observaciones GLPI', )
    area = fields.Many2one('sicpro.app.trabajadores.areas', 'Área', related='name.unidad_org', store=True, )
    pieza_a_utilizar = fields.Char('Pieza a utilizar', )
    observaciones = fields.Text('Observaciones', )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)

    def notificar_nuevo_registro(self):
        # correo usuario actual
        email_usuario_actual = self.env.user.email_formatted
        # Envío del correo
        email_values = {'email_to': email_usuario_actual, }
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_pdtes_piezas')
        template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

        # Lista de correo de los responsables
        list_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable').users
        for responsable in list_responsable:
            # Envío del correo
            email_values = {'email_to': responsable.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_pdtes_piezas')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_notify(body='Baja de medio informático', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        if self.name.responsable:
            # correo usuario responsable del equipo
            email_responsable_equipo = self.name.name.trabajador_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_pdtes_piezas')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # correo jefe usuario responsable del equipo
            email_jefe_responsable_equipo = self.name.name.trabajador_id.parent_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_jefe_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_pdtes_piezas')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    @api.model
    def create(self, vals_list):
        res = super(MediosInformaticosPdtesPiezas, self).create(vals_list)

        medio_informatico = self.env['sicpro.app.medios.informaticos'].search([('name', '=', res['name'].name.name)])
        if medio_informatico:
            medio_informatico.sudo().write({'estado': 'piezas'})

        res.notificar_nuevo_registro()
        return res
