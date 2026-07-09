# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ServiciosInternosSolicitudesObservaciones(models.Model):
    _name = 'sicpro.app.servicios.internos.solicitudes.observaciones'
    _description = "Gestión de observaciones de las solicitudes"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    active = fields.Boolean(default=True, )
    name = fields.Text(string='Observaciones', required=True)
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('anexo1', 'Anexo 1'), ('anexo2', 'Anexo 2'),
                                       ('Compromiso_nauta', 'Compromiso Nauta'),('Planilla_unica', 'Planilla Única'), ],)
