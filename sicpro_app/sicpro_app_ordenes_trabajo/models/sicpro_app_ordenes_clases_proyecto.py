# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

class OrdenesClasesProyectos(models.Model):
    _name = 'sicpro.app.ordenes.clases.proyecto'
    _description = 'Clase de trabajo para las órdenes de proyecto'

    name = fields.Char(string='Clase', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    control_autor = fields.Boolean(string='Control de autor', required=False,
                                   default=False)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_name_uniqueness(self):
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "El identificador de la clase de proyecto ya existe.\n\n" + MSG_SOPORTE_SICPRO)