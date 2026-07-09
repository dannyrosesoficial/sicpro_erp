from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class UiPython(models.Model):
    _name = 'sicpro.modulo.ui.python'
    _description = 'Ui Python'
    _rec_name = 'rec_name'

    DEFAULT_ENV_VARIABLES = """ #Variables disponibles:
    # - self: Objeto actual
    # - self.env: Odoo Entorno en el que se desencadena la acción.
    # - self.env.user: Devuelve el usuario actual (como una instancia).
    # - self.env.is_system: Devuelve si el usuario actual tiene configuración de grupo o está en modo superusuario.
    # - self.env.is_admin: Devuelve si el usuario actual tiene el grupo Derechos de acceso o está en modo superusuario.
    # - self.env.is_superuser: Devolver Si el entorno está en modo de superusuario.
    # - self.env.company: Devolver la empresa actual (como instancia).
    # - self.env.companies: Devolver un conjunto de registros de las campañas habilitadas por el usuario.
    # - self.env.lang: Devuelve el código de idioma actual."""

    rec_name = fields.Char(default='Ui Python', readonly=1, invisible=True)
    model_id = fields.Many2one('ir.model', string='Modelo')
    python_code = fields.Text(string='Código Python')
    results = fields.Text(string='Resultados')
    helpful_commands = fields.Text(string='Comandos útiles', default=DEFAULT_ENV_VARIABLES)

    def execute_method(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            if self.python_code:
                self.results = safe_eval(self.python_code.strip(), {'self': model}, mode="eval")
            else:
                self.results = "¡Por favor agregue algún códigos!"
        except Exception as error:
            self.results = str(error)

    def clear_method(self):
        self.python_code = ''
        self.results = ''
