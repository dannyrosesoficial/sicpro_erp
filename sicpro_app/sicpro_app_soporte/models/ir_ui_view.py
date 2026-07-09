from odoo import models, fields


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('soporte_gantt', "Soporte Gantt")], ondelete={'soporte_gantt': 'cascade'})
