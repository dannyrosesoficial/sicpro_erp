# -*- coding: utf-8 -*-


from imaplib import IMAP4

from odoo import models, fields, _
from odoo import tools
from odoo.exceptions import ValidationError


class ApiConector(models.Model):
    _inherit = 'sicpro.modulo.api.conector'

    name = fields.Selection(selection_add=[('sicpro.api.gitlab.backup', 'APLICACIÓN GITLAB BACKUP')],
                            ondelete={'sicpro.api.gitlab.backup': 'cascade'})

    # IMPORTANTE: El nombre de la acción debe ser 'api_test_' + el nombre del valor del campo name
    def conector_api_test_sicpro_api_gitlab_backup(self):
        app = self.env['sicpro.modulo.api.conector'].sudo().search([('name', '=', 'sicpro.api.gitlab.backup')])
        password = app.password
        username = app.usuario
        proyecto = app.url_config_data
        servidor = 'mail.etecsa.cu'
        puerto = 143

        # verífico que el usuario y contraseña sea el correcto.
        # como el servicio de autenticación de gitlab etecsa está desactivado para realizarlo por usuario y contraseña
        # verífico que las credenciales esten correcta con la alternativa del servicio de IMAP que utiliza
        # las mismas credenciales que las de gitlab etecsa
        if password and username and proyecto:
            try:
                conectar = IMAP4(servidor, int(puerto))
                self.ensure_one()
                conectar.login(username, password)
            except (OSError, Exception) as err:
                raise ValidationError(_("Conexión fallida, revise los campos de url, usuario y contraseña. Error: %s", tools.ustr(err)))

            try:
                conectar.close()
            except Exception:
                raise ValidationError(_('Conexión establecida con éxito.'))
                pass

        else:
            raise ValidationError(_("Conexión fallida, campos del registro incompletos, verifíquelo."))