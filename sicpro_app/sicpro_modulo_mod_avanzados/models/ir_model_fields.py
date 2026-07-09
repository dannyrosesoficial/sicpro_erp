# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging

from odoo import api, fields, models, SUPERUSER_ID, tools,  _

_logger = logging.getLogger(__name__)


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    def name_get(self):
        res = []
        if self.env.context.get('show_field_description_only', False) == True:
            for field in self:
                res.append((field.id, field.field_description))
        else:
            for field in self:
                res.append((field.id, '%s (%s,%s)' % (field.field_description, field.name, field.model)))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            domain = ['|', ('name', operator, name), ('field_description', operator, name)]
            res = self.search_fetch(domain, ['display_name'], limit=limit)
            return [(rec.id, rec.display_name) for rec in res]
        return super().name_search(name, args, operator, limit)
