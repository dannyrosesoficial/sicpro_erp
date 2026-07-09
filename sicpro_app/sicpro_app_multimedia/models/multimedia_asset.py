# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
import io
import hashlib
from PIL import Image
from odoo import models, fields, api, errors


class SicproMultimediaAsset(models.Model):
    _name = 'sicpro.multimedia.asset'
    _description = 'Activo Multimedia Centralizado'
    _order = 'create_date desc'

    name = fields.Char(string='Nombre del Archivo', required=True)
    description = fields.Text(string='Descripción / Notas')

    # Almacenamiento físico directo en el filestore del sistema operativo
    file_content = fields.Binary(string='Archivo Original', required=True,
                                 attachment=True)
    thumbnail = fields.Binary(string='Miniatura (Thumbnail)', attachment=True,
                              readonly=True)

    checksum = fields.Char(string='SHA-1 Checksum', max_length=40,
                           readonly=True, index=True)
    file_size = fields.Integer(string='Tamaño (Bytes)', readonly=True)
    file_type = fields.Char(string='Tipo de Archivo', readonly=True)

    # Atributos Relacionales Polimórficos
    res_model_id = fields.Many2one('ir.model', string='Modelo Destino',
                                   ondelete='cascade', required=True,
                                   index=True)
    res_model = fields.Char(related='res_model_id.model',
                            string='Nombre Técnico del Modelo', store=True,
                            readonly=True)
    res_id = fields.Integer(string='ID del Registro Relacionado',
                            required=True, index=True)
    res_name = fields.Char(string='Registro Enlazado',
                           compute='_compute_res_name', store=False)

    tag_ids = fields.Many2many('sicpro.multimedia.tag',
                               'sicpro_multimedia_asset_tag_rel', 'asset_id',
                               'tag_id', string='Etiquetas')

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for record in self:
            record.res_name = False
            if record.res_model and record.res_id:
                obj = self.env[record.res_model].browse(record.res_id)
                if obj.exists():
                    record.res_name = obj.display_name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('file_content'):
                vals = self._optimize_and_analyze_file(vals)
        return super(SicproMultimediaAsset, self).create(vals_list)

    def write(self, vals):
        if vals.get('file_content'):
            vals = self._optimize_and_analyze_file(vals)
        return super(SicproMultimediaAsset, self).write(vals)

    def _optimize_and_analyze_file(self, vals):
        """Procesa el binario, calcula el hash, tamaño y comprime si es una imagen"""
        try:
            binary_data = base64.b64decode(vals['file_content'])
            vals['file_size'] = len(binary_data)
            vals['checksum'] = hashlib.sha1(binary_data).hexdigest()

            # Intentar procesar con Pillow para optimización
            image_stream = io.BytesIO(binary_data)
            try:
                with Image.open(image_stream) as img:
                    vals['file_type'] = img.format

                    # 1. Crear Miniatura Ligera para Vistas Rápidas (Max 256x256)
                    thumb_img = img.copy()
                    thumb_img.thumbnail((256, 256))
                    thumb_stream = io.BytesIO()
                    thumb_img.save(thumb_stream, format='JPEG', quality=75)
                    vals['thumbnail'] = base64.b64encode(
                        thumb_stream.getvalue())

                    # 2. Optimizar Imagen Original si supera FullHD para no saturar almacenamiento
                    if img.width > 1920 or img.height > 1080:
                        optimized_img = img.copy()
                        optimized_img.thumbnail((1920, 1080))
                        optimized_stream = io.BytesIO()
                        optimized_img.save(optimized_stream, format=img.format,
                                           quality=85)
                        vals['file_content'] = base64.b64encode(
                            optimized_stream.getvalue())
                        vals['file_size'] = len(optimized_stream.getvalue())
            except Exception:
                # Si no es una imagen válida (ej. PDF, DOCX), se guarda intacto sin miniatura
                vals['file_type'] = 'application/octet-stream'
                vals['thumbnail'] = False
        except Exception as e:
            raise errors.ValidationError(
                f"Error procesando el archivo multimedia: {str(e)}")
        return vals

    @api.model
    def _cron_clean_orphaned_assets(self):
        """Busca y destruye registros multimedia cuyos padres ya no existan en el sistema"""
        assets = self.search([])
        orphaned_ids = []
        for asset in assets:
            if asset.res_model:
                parent_model = self.env[asset.res_model]
                parent_record = parent_model.browse(asset.res_id)
                if not parent_record.exists():
                    orphaned_ids.append(asset.id)
        if orphaned_ids:
            self.browse(orphaned_ids).unlink()
