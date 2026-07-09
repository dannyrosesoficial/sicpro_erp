# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import math

from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    # Se recomienda Char para poder incluir el sufijo (MB, KB, etc.)
    size = fields.Char(string="Tamaño Legible", compute="_compute_convert_size",
                       store=True)

    @api.depends("file_size")
    def _compute_convert_size(self):
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

        for rec in self:
            if rec.file_size <= 0:
                rec.size = "0 B"
                continue

            try:
                # Calculamos el índice logarítmico en base 1024
                i = int(math.floor(math.log(rec.file_size, 1024)))
                p = math.pow(1024, i)
                s = round(rec.file_size / p, 2)

                # Manejo de seguridad por si el índice excede la tupla
                unit = size_name[i] if i < len(size_name) else "???"
                rec.size = f"{s} {unit}"
            except Exception:
                rec.size = "Error"
