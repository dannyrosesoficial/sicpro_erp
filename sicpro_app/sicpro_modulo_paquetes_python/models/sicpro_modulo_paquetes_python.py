# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import fields, models


class PythonPaquetesInstalados(models.Model):
    _name = 'python.paquetes.instalados'
    _description = 'Paquetes Instalados de Python'
    _order = 'name asc'  # Ordenar por nombre por defecto

    name = fields.Char(string="Paquete", required=True)
    version = fields.Char(string="Versión Instalada")

    def update_packages(self):
        try:
            from importlib import metadata
        except ImportError:
            # Para versiones muy antiguas de Python (3.7)
            import importlib_metadata as metadata

        dists = metadata.distributions()
        self.search([]).unlink()
        vals_list = []
        for dist in dists:
            vals_list.append(
                {'name': dist.metadata['Name'], 'version': dist.version, })

        if vals_list:
            self.create(vals_list)

        return True
