# -*- coding: utf-8 -*-


from odoo import fields, models, tools


class Alias(models.Model):
    _inherit = 'mail.alias'

    alias_contact = fields.Selection(
        selection_add=[('trabajadores', 'Authenticated Employees')])


class MailAlias(models.AbstractModel):
    _inherit = 'mail.alias.mixin'

    def _alias_check_contact_on_record(self, record, message, message_dict, alias):
        if alias.alias_contact == 'trabajadores':
            email_from = tools.decode_message_header(message, 'From')
            email_address = tools.email_split(email_from)[0]
            employee = self.env['sicpro.app.trabajadores.general'].search(
                [('work_email', 'ilike', email_address)], limit=1)
            if not employee:
                employee = self.env['sicpro.app.trabajadores.general'].search(
                    [('user_id.email', 'ilike', email_address)], limit=1)
            if not employee:
                return {
                    'error_message': 'restricted to employees',
                    'error_template': self.env.ref('hr.mail_template_data_unknown_employee_email_address').body_html,
                }
            return True
        return super(MailAlias, self)._alias_check_contact_on_record(record, message, message_dict, alias)
