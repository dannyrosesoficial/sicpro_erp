# -*- coding: utf-8 -*-


from odoo import fields, models


class PythonPaquetesInstalados(models.Model):
    _name = 'python.paquetes.instalados'
    _description = 'Paquetes Instalados de Python'

    name = fields.Char(string="Paquetes")
    version = fields.Char(string="Versión Instalada")

    def update_packages(self):
        import pkg_resources
        installed_packages = pkg_resources.working_set

        self.search([]).unlink()
        for package in installed_packages:
            vals = {'name': package.key, 'version': package.version, }
            self.create([vals])
