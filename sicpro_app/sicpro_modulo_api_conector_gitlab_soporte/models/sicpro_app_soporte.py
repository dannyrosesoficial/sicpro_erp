# -*- coding: utf-8 -*-


from odoo import _, fields, models
from odoo.addons.sicpro_modulo_api_conector_gitlab.models.sicpro_api_conector import ApiConector
from odoo.exceptions import ValidationError


class SoporteTicket(models.Model):
    _inherit = 'sicpro.app.soporte'

    commit = fields.Many2one(comodel_name='sicpro.modulo.api.conector.gitlab.commits', string='Commit', required=False)
    branch_nombre = fields.Char(string='Branch', related='commit.branch_nombre', required=False)
    branch_web_url = fields.Char(string='Url Branch', related='commit.branch_web_url', required=False)
    commit_id_largo = fields.Char(string='Commit ID Largo', related='commit.commit_id_largo', required=False)
    commit_id_corto = fields.Char(string='Commit ID Corto', related='commit.commit_id_corto', required=False)
    commit_creado = fields.Datetime(string='Fecha Creado', related='commit.commit_creado', required=False)
    commit_mensaje = fields.Text(string='Mensaje', related='commit.commit_mensaje', required=False)
    commit_autor = fields.Char(string='Autor', related='commit.commit_autor', required=False)
    commit_web_url = fields.Char(string='Url Commit', related='commit.commit_web_url', required=False)

    def conector_api_cron_sicpro_api_gitlab(self):
        # realizo la llamada para ejecutar la actualización del registro de commits
        ApiConector.conector_api_cron_sicpro_api_gitlab(self)

    # se le realiza herencia al método write de la app de Soporte
    def write(self, vals):
        res = super(SoporteTicket, self).write(vals)
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['sicpro.app.soporte.estados'].browse(
                    [vals['stage_id']])
                ticket['last_stage_update'] = now
                if stage_obj.closed:
                    # verífico que tenga acceso al commits obligatorio
                    if ticket['team_id_commits']:
                        if ticket['aplicaciones'] and ticket['version_id']:
                            ticket['closed_date'] = now
                            # envió la notificación a los seguidores
                            ticket.message_post(body='Ticket cerrado', subtype_xmlid='mail.mt_comment',
                                                author_id=self.env.user.partner_id.id)
                            for participante in ticket.message_partner_ids:
                                # envío el correo electrónico
                                email_values = {'email_to': participante.email_formatted}
                                template = self.env.ref('sicpro_app_soporte.soporte_ticket_cambio_estado')
                                template.send_mail(ticket.id, force_send=True, email_values=email_values, )
                        else:
                            raise ValidationError(_("Campos no válidos: Verifique el campo de Aplicación o de"
                                                    " Versión. Si cree que es un error contacte al administrador"))
                    else:
                        # si el equipo no pertenece a la solicitud de acceso verífico que este lleno el campo commits
                        if ticket['aplicaciones'] and ticket['version_id'] and ticket['commit']:
                            ticket['closed_date'] = now
                            # envió la notificación a los seguidores
                            ticket.message_post(body='Ticket cerrado', subtype_xmlid='mail.mt_comment',
                                                author_id=self.env.user.partner_id.id)
                            for participante in ticket.message_partner_ids:
                                # envío el correo electrónico
                                email_values = {'email_to': participante.email_formatted}
                                template = self.env.ref('sicpro_app_soporte.soporte_ticket_cambio_estado')
                                template.send_mail(ticket.id, force_send=True, email_values=email_values, )
                        else:
                            raise ValidationError(_("Campos no válidos: Verifique el campo de Commit, Aplicación o de"
                                                    " Versión. Si cree que es un error contacte al administrador"))

            if vals.get('user_id'):
                ticket['assigned_date'] = now

        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        return res