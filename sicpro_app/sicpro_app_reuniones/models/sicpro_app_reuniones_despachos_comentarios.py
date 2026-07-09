# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class ReunionesDespachosComentarios(models.Model):
    _name = 'sicpro.app.reuniones.despachos.comentarios'
    _description = 'Comentarios de los Despachos'

    despacho_id = fields.Many2one('sicpro.app.reuniones.despachos',
                                  string='Despacho', required=True, )
    name = fields.Char(string='Comentarios', required=True)
    agenda_ids = fields.Many2one('sicpro.app.reuniones.despachos.agenda',
                                 string='Agenda/Puntos vinculada',
                                 required=True)
    registro_activo = fields.Integer(string='Registro_activo',
                                     required=False, )
