# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models
from odoo.http import request


class UserSelection(models.Model):
    _name = 'user.selection'
    _description = 'User Selection'

    user_id = fields.Many2one('res.users', string="Usuario", required=True,
                              domain=lambda self: [
                                  ('id', '!=', self.env.user.id)])
    access_ids = fields.One2many('res.groups', 'user_id', string="Grupo",
                                 readonly=True)

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.access_ids = self.user_id.group_ids

    def action_switch(self):
        self.ensure_one()
        session = request.session
        session.update({'previous_user': self.env.user.id, })
        session.authenticate_without_password(self.env.cr.dbname,
                                              self.user_id.login, self.env)
        return {'type': 'ir.actions.act_url', 'url': '/', 'target': 'self'}
