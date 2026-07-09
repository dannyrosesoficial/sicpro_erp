# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class ReunionesEtiquetasCategorias(models.Model):
    _name = "sicpro.app.reuniones.categorias"
    _description = "Categorías de las etiquetas"
    _order = "sequence"

    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    etiquetas_ids = fields.One2many('sicpro.app.reuniones.etiquetas',
                                    'categoria_id', string="Etiquetas")
