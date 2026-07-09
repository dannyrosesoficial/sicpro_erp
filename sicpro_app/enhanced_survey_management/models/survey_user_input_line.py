# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import json
import textwrap
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    """Herencia para añadir campos de respuesta y lógica de visualización."""
    _inherit = 'survey.user_input.line'

    answer_type = fields.Selection(
        selection_add=[('url', 'URL'), ('many2one', 'Many2one'), ('many2many', 'Many2many'), ('week', 'Week'),
            ('time', 'Time'), ('color', 'Color'), ('email', 'Email'), ('month', 'Month'), ('name', 'Name'),
            ('matrix', 'Matrix'), ('address', 'Address'), ('selection', 'Selection'), ('password', 'Password'),
            ('range', 'Range'), ('file', 'Archivo'), ('qr', 'QR'), ('barcode', 'Barcode'), ('signature', 'Firma')],
        ondelete={t: 'cascade' for t in
                  ['url', 'many2one', 'many2many', 'week', 'time', 'color', 'email', 'month', 'name', 'matrix',
                   'address', 'selection', 'password', 'range', 'file', 'qr', 'barcode', 'signature']})

    # Campos de almacenamiento SICPRO (Idénticos a v17)
    value_url = fields.Char(string='URL Usuario')
    value_email = fields.Char(string='Email Usuario')
    value_week = fields.Char(string='Semana Usuario')
    value_color = fields.Char(string='Color Usuario')
    value_many2one = fields.Char(string='ID Many2one')
    value_many2one_option = fields.Char(string='Nombre Many2one')
    value_many2many = fields.Char(string='IDs Many2many')
    value_time = fields.Float(string='Valor Hora')
    value_matrix = fields.Text(string='Matriz Personalizada')
    value_selection = fields.Char(string='Selección Usuario')
    value_password = fields.Char(string='Contraseña')
    value_range = fields.Char(string='Valor Rango')
    value_file = fields.Many2one('ir.attachment', string='Archivo Adjunto')
    filename = fields.Char(string='Nombre del Archivo')
    value_month = fields.Char(string='Mes Usuario')
    value_address = fields.Text(string='Dirección Usuario')
    value_name = fields.Text(string='Nombre Usuario')
    value_qr = fields.Char(string='Valor QR')
    value_barcode = fields.Char(string='Valor Barcode')
    value_signature = fields.Binary(string='Firma Usuario')

    @api.depends('answer_type', 'skipped', 'value_char_box', 'value_numerical_box', 'value_many2one_option',
                 'value_time', 'value_range', 'value_selection')
    def _compute_display_name(self):
        """
        Sustituye la lógica de visualización de v17.
        Mapea dinámicamente cada tipo de respuesta a su valor legible.
        """
        for line in self:
            if line.skipped:
                line.display_name = 'Omitida'
                continue

            res = False
            # Lógica por tipo de respuesta (Recuperada de v17)
            if line.answer_type == 'char_box':
                res = line.value_char_box
            elif line.answer_type == 'numerical_box':
                res = str(line.value_numerical_box)
            elif line.answer_type == 'time':
                res = str(line.value_time)
            elif line.answer_type == 'many2one':
                res = line.value_many2one_option
            elif line.answer_type == 'file':
                res = line.filename
            elif line.answer_type in ['address', 'name', 'matrix']:
                val = line[f'value_{line.answer_type}']
                res = textwrap.shorten(val or "", width=50)
            elif line.answer_type == 'suggestion':
                if line.matrix_row_id:
                    res = f'{line.suggested_answer_id.value}: {line.matrix_row_id.value}'
                else:
                    res = line.suggested_answer_id.value
            else:
                # Intenta obtener el valor de los campos value_ personalizados
                field_name = f'value_{line.answer_type}'
                if field_name in line._fields:
                    res = str(line[field_name])

            line.display_name = res or 'Respondida'