from odoo import models


class TrabajadoresDialogWizard(models.TransientModel):
    _name = "sicpro.app.trabajadores.dialog.wizard"
    _description = "Diálogo de cierre duplicado"

    def show_dialog(self):
        context = dict(self.env.context or {})
        return self.env['sicpro.app.trabajadores.cierre.wizard'].generar_cierre()
