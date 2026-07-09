# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class ReunionesDespachosAgenda(models.Model):
    _name = 'sicpro.app.reuniones.despachos.agenda'
    _description = 'Agenda de los Despachos'

    despacho_id = fields.Many2one('sicpro.app.reuniones.despachos',
                                  string='Despacho', required=True,
                                  readonly=True, )
    name = fields.Char(string='Agenda', )
