# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class SicproWebTrabajadores(models.Model):
    _name = 'sicpro.modulo.web.trabajadores'
    _description = 'Configuración de los contactos RH'
    _order = "sequence, id"

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    name = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                           string='Trabajador', required=True)
    active = fields.Boolean(string='Archivado', default=True, index=True)
    image_1024 = fields.Image("Image 1024", related="name.image_1024",
                              store=False)
    ocupacion_id = fields.Char(string='Puesto de trabajo',
                               related="name.ocupacion_id.name.name")
    area_id = fields.Char(string='Departamento', related="name.area_id.name")
    telefono_trabajo = fields.Char(string='Teléfono Trabajo',
                                   related="name.telefono_trabajo")
    movil_trabajo = fields.Char(string='Móvil Trabajo', related="name.movil_trabajo")
    correo_trabajo = fields.Char(string='Correo Trabajo',
                                 related="name.correo_trabajo")

    @api.constrains('name')
    def _check_unique_contacto_trabajador(self):
        for record in self:
            domain = [('name', '=', record.name.id), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre del trabajador existe!.\n\n" + MSG_SOPORTE_SICPRO)

    @api.model
    def buscar_datos_trabajadores(self):
        # Buscamos con sudo
        records = self.sudo().search([('active', '=', True)])
        lista_trabajadores = []

        for item in records:
            if item.name:
                img_bin = item.name.sudo().image_128

                if img_bin:
                    # Si hay imagen, la convertimos a una cadena que el navegador entienda
                    img_data = f"data:image/png;base64,{img_bin.decode('utf-8')}"
                else:
                    # Si no hay, ponemos la ruta del placeholder
                    img_data = "/web/static/img/placeholder.png"

                lista_trabajadores.append({'nombre': item.name.name or '',
                                           'puesto': item.ocupacion_id or '',
                                           'departamento': item.area_id or '',
                                           'telefono': item.telefono_trabajo or '',
                                           'movil': item.movil_trabajo or '',
                                           'correo': item.correo_trabajo or '',
                                           'imagen': img_data,
                                           })
        return lista_trabajadores
