# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields


class ApiConectorHistorial(models.Model):
    _name = 'sicpro.app.medios.informaticos.historial'
    _order = "id desc"
    _description = 'Historial de actualizaciones del inventario'

    name = fields.Char(string="Aplicación", required=True, )
    fecha = fields.Datetime(string='Fecha', required=False)
    registros_creados = fields.Integer(string='Registros Creados',
                                       required=False)
    list_registros_creados = fields.Text(string='Lista Registros Creados')
    registros_actualizados = fields.Integer(string='Registros Actualizados',
                                            required=False)
    list_registros_actualizados = fields.Text(
        string='Lista Registros Actualizados')
    registros_archivados = fields.Integer(string='Registros Archivados',
                                          required=False)
    list_registros_archivados = fields.Text(
        string='Lista Registros Archivados')
    estado = fields.Selection(string='Estado', required=False,
                              selection=[('exito', 'Éxito'),
                                         ('fallido', 'Fallido'), ])
    descripcion_estado = fields.Text(string='Descripción del Estado')
