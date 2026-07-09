# -*- coding: utf-8 -*-

import collections
import json
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError
import logging
from collections import Counter

_logger = logging.getLogger(__name__)


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    selection_ids = fields.One2many('question.selection', 'question_id', string='Selección',
                                    help="Campo utilizado para crear preguntas de tipo selección.")
    question_type = fields.Selection(
        selection_add=[('time', 'Tiempo'), ('month', 'Mes'), ('name', 'Nombre'), ('address', 'Dirección'),
                       ('email', 'Correo Electrónico'), ('password', 'Contraseña'), ('qr', 'Código QR'), ('url', 'URL'),
                       ('week', 'Semana'), ('color', 'Color'), ('range', 'Rango'), ('many2one', 'Many2one'),
                       ('file', 'Subir archivo'), ('date', 'Fecha'), ('selection', 'selección'),
                       ('barcode', 'código de barras')], help="Tipos de preguntas admitidas por encuestas")
    matrix_subtype = fields.Selection(selection_add=[('custom', 'Matriz personalizada')],
                                      help="Pregunta de tipo de selección de matriz")
    model_id = fields.Many2one('ir.model', string='Modelo', domain=[('transient', '=', False)],
                               help="pregunta tipo many2one")
    range_min = fields.Integer(string='Min', help='Rango mínimo, pregunta de tipo de rango')
    range_max = fields.Integer(string='Max', help='Rango máximo, pregunta de tipo de rango')
    qrcode = fields.Text(string='Qrcode', help='Mostrar código qr en la encuesta')
    qrcode_png = fields.Binary(string='Qrcode PNG', help="Código QR PNG")
    barcode = fields.Char(string='Barcode', help="Número de código de barras")
    barcode_png = fields.Binary(string='Barcode PNG', help="Guarda el archivo png de código de barras")

    @api.constrains('barcode')
    def _check_barcode(self):
        """Restricción para garantizar que el código de barras tenga exactamente 12 dígitos."""
        for record in self:
            if record.barcode:
                if len(record.barcode) != 12:
                    raise ValidationError(_("El código de barras debe tener exactamente 12 caracteres."))
                if not record.barcode.isdigit():
                    raise ValidationError(_("El código de barras debe contener solo dígitos."))

    def get_selection_values(self):
        """Opciones de devolución de funciones para preguntas de tipo de selección"""
        if self.question_type == 'many2one' and self.model_id:
            # Obtener el modelo y su campo de nombre para retornar las opciones, si fuera necesario
            model_rec = self.env[self.model_id.model].sudo().search([])
            return model_rec.read(['display_name'])

        return self.selection_ids

    def prepare_model_id(self, model):
        """Función para devolver opciones para muchas preguntas"""
        if model:
            model_data = self.env[model.model].sudo().search([])
            return [rec.read([model_data._rec_name])[0] for rec in model_data]
        model_data = self.env[self.model_id.model].sudo().search([])
        return [rec.read([model_data._rec_name])[0] for rec in model_data]

    # Tipos que el método base de Odoo no conoce
    CUSTOM_COUNTABLE_TYPES = ['many2one', 'selection']
    CUSTOM_SIMPLE_INPUT_TYPES = ['time', 'month', 'week', 'color', 'email', 'url', 'range', 'name', 'address', 'qr',
                                 'barcode', 'password', 'file']
    ALL_CUSTOM_TYPES = CUSTOM_COUNTABLE_TYPES + CUSTOM_SIMPLE_INPUT_TYPES

    def _prepare_statistics(self, user_input_lines):
        """
        Prepara los datos estadísticos para preguntas customizadas (many2one y selection),
        asegurando un conteo correcto y el formato de grupo requerido por Odoo JS.
        """

        # 1. Llamar al método base de Odoo para manejar los tipos estándar
        question_data = super(SurveyQuestion, self)._prepare_statistics(user_input_lines)

        if isinstance(question_data, dict):
            question_data = [question_data]

        # Verificar que las variables customizadas existan
        if not hasattr(self, 'ALL_CUSTOM_TYPES') or not hasattr(self, 'CUSTOM_COUNTABLE_TYPES'):
            return question_data

        for question in self:
            # Encontrar los datos de la pregunta actual ya procesados por el super
            existing_data = next((data for data in question_data if data.get('question') == question), None)

            if question.question_type in self.ALL_CUSTOM_TYPES:
                current_lines = user_input_lines.filtered(lambda line: line.question_id == question)
                # table_data: respuestas que no fueron saltadas
                table_data = current_lines.filtered(lambda line: not line.skipped)
                common_lines_data = []  # Lista de tuplas (Label, Count)

                # --- Lógica de Conteo (Solo si es un tipo contable) ---
                if question.question_type in self.CUSTOM_COUNTABLE_TYPES:

                    if question.question_type == 'many2one':
                        m2o_ids = table_data.filtered('value_many2one').mapped(lambda line: line.value_many2one)
                        if m2o_ids:
                            # 1. Contamos las ocurrencias de cada ID
                            counter = Counter(m2o_ids)

                            # 2. Obtenemos los nombres (labels) correspondientes a esos IDs
                            target_model_name = question.model_id.model if question.model_id else False

                            if target_model_name and target_model_name in self.env:
                                target_ids = [int(i) for i in m2o_ids if i.isdigit()]
                                m2o_records = self.env[target_model_name].browse(target_ids).exists()

                                # Mapeo {ID (str): Nombre (str)}
                                name_mapping = {str(rec.id): rec.display_name for rec in m2o_records}

                                # 3. Construimos common_lines_data (Label, Count)
                                for m2o_id, count in counter.most_common():
                                    label = name_mapping.get(m2o_id)
                                    if not label:
                                        label = _("Registro Borrado (ID %s)") % m2o_id
                                    common_lines_data.append((label, count))

                    elif question.question_type == 'selection':
                        answers_keys = table_data.mapped('value_selection')

                        if answers_keys:
                            counter = Counter(answers_keys)

                            for key, count in counter.items():
                                common_lines_data.append((key, count))

                # --- Generación de GRAPH DATA (FORMATO DE GRUPO REQUERIDO POR ODOO JS) ---
                graph_data = []

                if common_lines_data:

                    # 1. Transformar common_lines_data (lista de tuplas) al formato values:
                    values_list = []
                    for label, count in common_lines_data:
                        values_list.append({'text': label, 'count': count, })

                    # 2. Crear el objeto principal del dataset (grupo)
                    graph_data.append({'key': _('Respuestas'), 'values': values_list, })

                # --- Actualizar existing_data con los datos calculados ---
                data_update = {'answer_input_done_ids': current_lines.filtered(lambda line: not line.skipped),
                    'answer_input_skipped_ids': current_lines.filtered(lambda line: line.skipped),
                    'table_data': table_data,
                    'comment_line_ids': current_lines.filtered(lambda line: line.value_comment),
                    'common_lines': common_lines_data, 'right_answers': [], # Serialización final
                    'graph_data': json.dumps(graph_data)}

                if existing_data:
                    existing_data.update(data_update)
                else:
                    data_update['question'] = question
                    data_update['is_page'] = question.is_page
                    question_data.append(data_update)

        return question_data

    @api.model
    def _get_stats_data(self, answer_lines):
        self.ensure_one()
        q_type = self.question_type

        # 1. Lógica para el tipo de pregunta 'selection'
        if q_type == 'selection':
            # Aseguramos el retorno de una tupla (table_data, graph_data)
            # Mantenemos la lógica de read_group anterior que estaba funcionando.
            field_group_by = 'value_selection'
            table_data = []

            # Usamos 'id:count' para forzar el campo 'id_count' y ordenar por él
            read_group_res = self.env['survey.user_input.line'].read_group(
                domain=[('question_id', '=', self.id), ('id', 'in', answer_lines.ids), (field_group_by, '!=', False)],
                fields=[field_group_by, 'id:count'], groupby=[field_group_by], orderby='id_count desc')

            for result in read_group_res:
                count = result.get('id_count', 0)
                label = result.get(field_group_by)
                table_data.append({'value': label, 'count': count})

            return table_data, []

            # 2. Lógica para el tipo de pregunta 'many2one' (MANTENIDO)
        elif q_type == 'many2one':
            # Asumiendo que el campo para Many2one es 'value_many2one'
            field_group_by = 'value_many2one'
            table_data = []

            read_group_res = self.env['survey.user_input.line'].read_group(
                domain=[('question_id', '=', self.id), ('id', 'in', answer_lines.ids), (field_group_by, '!=', False)],
                fields=[field_group_by, 'id:count'], groupby=[field_group_by], orderby='id_count desc')

            for result in read_group_res:
                count = result.get('id_count', 0)
                m2o_data = result.get(field_group_by)

                # --- CORRECCIÓN DE LA LÍNEA 181 ---
                try:
                    # Accedemos por índice para evitar el error 'too many values to unpack'
                    label_id = m2o_data[0]
                    label_name = m2o_data[1]
                except (TypeError, IndexError, ValueError):
                    # Maneja si m2o_data es None, si tiene menos de 2 elementos, o si tiene demasiados.
                    # Se omite este resultado y se continúa.
                    self.env.cr.warning("Many2one read_group retornó datos inesperados. Pregunta: %s. Datos: %s" % (
                        self.title, str(m2o_data)))
                    continue
                # ----------------------------------

                table_data.append({'value': label_name, 'count': count, 'id': label_id})

            # Aseguramos un retorno de tupla para este tipo
            return table_data, []

        return super(SurveyQuestion, self)._get_stats_data(answer_lines)
