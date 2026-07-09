# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import fields, models


class SicproWebManuales(models.Model):
    _name = 'sicpro.modulo.web.manuales'
    _description = 'Manuales de usuarios'
    _order = "sequence, id"

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Char(string='Descripción', required=False)

    # Campo Binario: Odoo lo guarda automáticamente en el FILESTORE
    manual = fields.Binary(string="Archivo", required=True, attachment=True)

    # Este campo es vital: almacenará el nombre del archivo (ej. guia_usuario.pdf)
    # y permite que Odoo sepa qué extensión tiene al descargarlo.
    manual_filename = fields.Char(string="Nombre del Archivo")
    texto_boton = fields.Char(required=True, string='Texto Botón',
                              default="Descargar")
    icono_id = fields.Many2one('sicpro.nomenclador.iconos', string="Icono")
    tipo = fields.Selection(string='Estilo', related='icono_id.tipo',
                            readonly=True)
    clase_icono = fields.Char(string='Clase CSS',
                              related='icono_id.clase_icono', readonly=True)
    preview = fields.Html(string='Vista Previa', related='icono_id.preview',
                          readonly=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    def buscar_datos_manuales(self):
        # Usamos sudo() para garantizar que la web pueda leer los archivos en el filestore
        manuales = self.sudo().search([('active', '=', True)])
        manuales_ids = []

        # Obtenemos la URL base (importante para entornos locales/offline)
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')

        for item in manuales:
            # Construcción de la URL técnica para el Filestore
            # filename_field le dice a Odoo que use el nombre guardado en 'manual_filename'
            url_manual = (
                f"{base_url}/web/content?model={self._name}&id={item.id}"
                f"&field=manual&filename_field=manual_filename&download=true")

            manuales_ids.append(
                {'nombre': item.name, 'descripcion': item.descripcion,
                 'texto_boton': item.texto_boton,
                 'icono_clase_completa': f"{item.tipo} {item.clase_icono}",
                 'manual': url_manual,
                 })

        return manuales_ids
