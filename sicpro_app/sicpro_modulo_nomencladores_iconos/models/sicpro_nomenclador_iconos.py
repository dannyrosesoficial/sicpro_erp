# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models, api


class NomencladorIconos(models.Model):
    _name = 'sicpro.nomenclador.iconos'
    _description = 'Nomenclador de Iconos Font Awesome'
    _order = 'name asc'

    name = fields.Char(string='Nombre del Icono', required=True,
                       help="Ej: Cámara, Usuario, Guardar")
    tipo = fields.Selection(string='Estilo (Prefijo)', default='fa',
                            required=True,
                            selection=[('fa', 'FA Legacy (Standard)'),
                                       ('fas', 'FAS Solid'),
                                       ('far', 'FAR Regular'),
                                       ('fab', 'FAB Brands')])
    clase_icono = fields.Char(string='Clase CSS', required=True,
                              help="Ej: fa-camera")
    active = fields.Boolean(string="Activo", default=True, index=True)
    # Campo para mostrar el icono en la vista (Importante: sanitize=False para permitir el <i>)
    preview = fields.Html(string='Vista Previa', compute='_compute_preview',
                          sanitize=False)

    @api.depends('tipo', 'clase_icono')
    def _compute_preview(self):
        for rec in self:
            if rec.tipo and rec.clase_icono:
                # Odoo 19 maneja mejor fas que fas
                # Si es el legado 'fa', usamos 'fa' + la clase para compatibilidad

                clase_final = f"{rec.tipo} {rec.clase_icono}"

                # Inyectamos un estilo para asegurar que el icono se vea
                # independientemente del tema (claro/oscuro) de Odoo
                rec.preview = f"""
                    <div style="display: flex; align-items: center; justify-content: center; width: 100%; height: 100%;">
                        <i class="{clase_final}" 
                           style="font-size: 24px; color: #714B67; min-width: 30px; text-align: center;"></i>
                    </div>
                """
            else:
                rec.preview = '<span class="text-muted">N/A</span>'

    # Un método para obtener la clase completa rápidamente desde XML
    def get_full_class(self):
        self.ensure_one()
        return f"{self.tipo} {self.clase_icono}"
