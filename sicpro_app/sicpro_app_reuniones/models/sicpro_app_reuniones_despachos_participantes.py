# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class ReunionesDespachosParticipantes(models.Model):
    _name = 'sicpro.app.reuniones.despachos.participantes'
    _description = 'Participantes de los Despachos'

    despacho_id = fields.Many2one('sicpro.app.reuniones.despachos',
                                  string='Despacho', required=True,
                                  readonly=True, )
    name = fields.Many2one('res.users', string='Trabajador',
                           domain="[('tipo', '=', 'interno')]")
    email = fields.Char(string='Correo', related='name.email', store=True)
    cargo = fields.Char(string='Cargo', related='name.ocupacion_id.name.name',
                        store=True)
    company_trabajador = fields.Many2one('res.company',
                                         string='Proceso Trabajador',
                                         related='name.company_id', store=True)
