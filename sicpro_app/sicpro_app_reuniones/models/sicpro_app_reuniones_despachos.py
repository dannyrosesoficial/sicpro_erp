# -*- coding: utf-8 -*-


from odoo import fields, models


class ReunionesDespachos(models.Model):
    _name = 'sicpro.app.reuniones.despachos'
    _description = 'Gestión de los Despachos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Nombre del despacho', required=True)
    fecha_inicio = fields.Datetime(string='Fecha Inicio', required=True, tracking=True)
    organizador_id = fields.Many2one('res.users', string='Organizador', tracking=True,
                                     domain="[('tipo', '=', 'interno')]")
    lugar = fields.Many2one(comodel_name='sicpro.app.reuniones.lugares', string='Lugar', required=True)
    active = fields.Boolean(default=True)
    responsable = fields.Many2one('res.users', string='Responsable', tracking=True)
    user_id = fields.Many2one('res.users', string='Crea la reunión', tracking=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Proceso', change_default=True,
                                 default=lambda self: self.env.company, required=False)
    description = fields.Text(string='Descripción detallada', required=True)
    participantes_ids = fields.One2many('sicpro.app.reuniones.despachos.participantes', 'despacho_id',
                                        string='Participantes')
    agenda_ids = fields.One2many('sicpro.app.reuniones.despachos.agenda', 'despacho_id',
                                 string='Agenda/Puntos a tratar', )
    comentarios_ids = fields.One2many('sicpro.app.reuniones.despachos.comentarios', 'despacho_id',
                                      string='Comentarios de los puntos tratados', )
    decisiones_ids = fields.One2many('sicpro.app.reuniones.decisiones', 'reunion', string='Decisiones', )
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    estados = fields.Selection(string='Estados', selection=[('sin_iniciar', 'Sin Iniciar'), ('pospuesto', 'Pospuesto'),
                                                            ('cumplida', 'Cumplido'), ('cancelado', 'Cancelado'), ],
                               default='sin_iniciar', required=True, group_expand='_group_expand_estados',)
    agenda_count = fields.Integer('Cantidad puntos', compute='_compute_agenda_count')

    # Cuenta la cantidad de puntos a tratar
    def _compute_agenda_count(self):
        for item in self:
            agenda_ids = self.env['sicpro.app.reuniones.despachos.agenda'].sudo().search([('despacho_id', '=', item.id)])
            item.agenda_count = len(agenda_ids)

    def _group_expand_estados(self, states, domain, order):
        return [key for key, val in type(self).estados.selection]

    # enviar notificación a los participantes
    def notificar_participantes(self):
        participantes = self.env['sicpro.app.reuniones.despachos.participantes'].search(
            [('despacho_id', '=', self._origin.id)])

        # envió la notificación a los seguidores
        responsable = self.responsable
        organizador = self.organizador_id
        self.message_subscribe(partner_ids=responsable.partner_id.ids)
        self.message_subscribe(partner_ids=organizador.partner_id.ids)
        self.message_subscribe(partner_ids=participantes.name.partner_id.ids)
        self.message_post(body='Nuevo Despacho', subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)

        for item in participantes:
            # envío el correo electrónico a los participantes
            email_values = {'email_to': item.name.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.despachos_nuevo_participante')
            template.send_mail(self.id, force_send=True, email_values=email_values)

    def write(self, vals):
        res = super(ReunionesDespachos, self).write(vals)
        for despacho in self:
            participantes = self.env['sicpro.app.reuniones.despachos.participantes'].search(
                [('despacho_id', '=', self._origin.id)])
            if despacho['estados'] == 'pospuesto':
                # envió la notificación a los seguidores
                despacho.message_post(body='Despacho pospuesto', subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)

                for item in participantes:
                    # envío el correo electrónico
                    email_values = {'email_to': item.name.partner_id.email_formatted, }
                    template = self.env.ref('sicpro_app_reuniones.despachos_pospuesto_participante')
                    template.send_mail(despacho.id, force_send=True, email_values=email_values)

            if despacho['estados'] == 'cancelado':
                # envió la notificación a los seguidores
                despacho.message_post(body='Despacho cancelado', subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)

                for item in participantes:
                    # envío el correo electrónico
                    email_values = {'email_to': item.name.partner_id.email_formatted, }
                    template = self.env.ref('sicpro_app_reuniones.despachos_cancelado_participante')
                    template.send_mail(despacho.id, force_send=True, email_values=email_values)

        return res