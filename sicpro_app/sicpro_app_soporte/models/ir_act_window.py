from odoo import models, fields


class IrActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('soporte_gantt', "Soporte Gantt")],
                                 ondelete={'soporte_gantt': 'cascade'})
