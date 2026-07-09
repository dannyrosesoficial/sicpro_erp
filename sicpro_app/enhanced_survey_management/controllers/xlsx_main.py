# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import io
import json
from datetime import datetime

from odoo import http
from odoo.http import content_disposition, request
try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class XlsxReportController(http.Controller):
    """Controlador para generar reportes XLSX de respuestas de encuestas en Odoo 19."""

    @http.route('/xlsx_report/<model("survey.survey"):survey_id>', type='http', auth='user', csrf=False)
    def get_report_xlsx(self, survey_id=None, **args):
        """Genera y descarga un reporte Excel con las respuestas."""
        # Búsqueda optimizada de participaciones
        user_inputs = request.env['survey.user_input'].sudo().search(
            [("survey_id", '=', survey_id.id), ("state", "=", "done")  # Recomendado: solo reportar encuestas terminadas
            ])

        answers = []
        for rec in user_inputs:
            # En Odoo 19 create_date ya es un objeto datetime, no necesitamos split de string
            submission_dt = rec.create_date.strftime('%Y-%m-%d %H:%M:%S')

            for line in rec.user_input_line_ids:
                # Ignorar códigos visuales en el Excel
                if line.question_id.question_type in ['barcode', 'qr', 'signature']:
                    continue

                answer_content = ''

                # Procesamiento de tipos complejos SICPRO
                try:
                    if line.question_id.question_type == 'address':
                        # Validamos si es JSON o string plano
                        display_name = line.value_address or line.display_name
                        data = json.loads(display_name) if display_name.startswith('{') else {}
                        answer_content = ", ".join([str(v) for v in data.values() if v]) if data else display_name

                    elif line.question_id.question_type == 'name':
                        display_name = line.value_name or line.display_name
                        data = json.loads(display_name) if display_name.startswith('{') else {}
                        answer_content = " ".join([str(v) for v in data.values() if v]) if data else display_name

                    elif line.question_id.question_type == 'time':
                        # El campo value_time se guarda como Float (ej: 14.30)
                        time_float = line.value_time
                        hours = int(time_float)
                        minutes = int(round((time_float - hours) * 100))
                        time_obj = datetime.strptime(f'{hours}:{minutes}', '%H:%M')
                        answer_content = time_obj.strftime('%I:%M %p')

                    else:
                        # Para otros tipos (many2one, selection, char, etc.)
                        answer_content = line.display_name
                except Exception:
                    answer_content = line.display_name

                answers.append(
                    [rec.id, rec.nickname or 'Anónimo', submission_dt, line.question_id.title, answer_content])

        # Construcción del Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Respuestas')

        # Formatos
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 14, 'bg_color': '#714B67', 'font_color': 'white'})
        cell_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 1, 'bg_color': '#EEEEEE'})
        txt = workbook.add_format({'font_size': 10, 'border': 1})
        sub_title = workbook.add_format({'bold': True, 'font_size': 11})

        # Configuración de columnas
        sheet.set_column('A:A', 15)  # Partner/Nickname
        sheet.set_column('B:B', 20)  # Fecha
        sheet.set_column('C:C', 40)  # Pregunta
        sheet.set_column('D:D', 50)  # Respuesta

        # Cabecera del Reporte
        sheet.merge_range('A1:D1', f'REPORTE DE ENCUESTA: {survey_id.title}', head)
        sheet.write('A3', 'Total de Respuestas:', sub_title)
        sheet.write('B3', len(user_inputs))

        # Encabezados de tabla
        headers = ['Participante', 'Fecha de Envío', 'Pregunta', 'Respuesta']
        for col, h_text in enumerate(headers):
            sheet.write(5, col, h_text, cell_format)

        # Llenado de datos
        row = 6
        for data in reversed(answers):
            sheet.write(row, 0, data[1], txt)
            sheet.write(row, 1, data[2], txt)
            sheet.write(row, 2, data[3], txt)
            sheet.write(row, 3, data[4], txt)
            row += 1

        workbook.close()
        output.seek(0)

        # Respuesta HTTP
        file_name = f"{survey_id.title}.xlsx"
        return request.make_response(output.read(),
            headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(file_name))])