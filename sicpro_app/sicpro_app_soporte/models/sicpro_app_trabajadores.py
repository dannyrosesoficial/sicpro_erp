# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteTrabajadores(models.Model):
    _inherit = "sicpro.app.trabajadores"

    ticket_count = fields.Integer(
        compute="_compute_cuenta_ticket", string="Cantidad Ticket")
    ticket_activos_count = fields.Integer(compute="_compute_cuenta_ticket",
                                          string="Ticket Activos")
    ticket_count_string = fields.Char(compute="_compute_cuenta_ticket",
                                      string="Tickets")

    def _compute_cuenta_ticket(self):
        for item in self:
            ticket_ids = self.env["sicpro.app.soporte"].search(
                [("partner_user_id.trabajador", '=', item.id)])

            item.ticket_count = len(ticket_ids)
            item.ticket_activos_count = len(ticket_ids.filtered(
                lambda ticket: not ticket.stage_id.closed))
            count_active = item.ticket_activos_count
            count = item.ticket_count
            item.ticket_count_string = ("{} / {}".format(count_active, count))

    def action_view_soporte_tickets(self):
        return {
            "name": self.name,
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "sicpro.app.soporte",
            "type": "ir.actions.act_window",
            "domain": [("partner_user_id.trabajador", "=", self.id)],
            "context": self.env.context,
        }
