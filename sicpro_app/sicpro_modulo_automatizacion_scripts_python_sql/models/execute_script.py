# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models, exceptions, _
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class execute_script(models.Model):
    _name = "execute.script"
    _description = "Ejecutar consultas PostgreSQL o de código Python desde la interfaz de SICPRO ERP"

    name = fields.Char(string="Name", required=True)
    execution_method = fields.Selection(
        selection=[('code', "Código Python"), ('query', "Consulta SQL")],
        default="code", string="Método de Ejecución", required=True)
    execution_script = fields.Text(string="Script de Ejecución", required=True)
    html = fields.Html(string="Resultado (HTML)", readonly=True)
    records_count = fields.Integer(string="Cantidad de registros")

    def _get_result_from_script(self, script):
        self = self.sudo()
        headers, datas = [], []

        if script:
            try:
                self.env.cr.execute(script)
            except Exception as error:
                raise exceptions.UserError(
                    "Error al ejecutar el script: %s" % error + MSG_SOPORTE_SICPRO)

            try:
                if self.env.cr.description:
                    headers = [col[0] for col in self.env.cr.description]
                    datas = self.env.cr.fetchall()
                    self.records_count = self.env.cr.rowcount
            except Exception as error:
                raise exceptions.UserError(
                    "Error al obtener los resultados del script: %s" % error + MSG_SOPORTE_SICPRO)

        return headers, datas

    def _execute_python_code(self):
        localdict = {'self': self, 'user_obj': self.env.user}

        for obj in self:
            try:
                exec(obj.execution_script, localdict)
                if localdict.get('result', False):
                    self.records_count = 0
                    result = localdict['result']
                    if not isinstance(result, str):
                        result = str(result)
                    self.html = result
                else:
                    self.html = ''
            except Exception as e:
                raise exceptions.UserError(
                    '¡El código Python no se puede ejecutar! mensaje: %s' % e + MSG_SOPORTE_SICPRO)

    def execute(self):
        for record in self.sudo():
            sql_keywords = (
                'select', 'insert', 'update', 'delete', 'create', 'alter',
                'drop', 'truncate', 'begin', 'commit', 'rollback',
                'create index', 'drop index', 'add constraint',
                'drop constraint', 'grant', 'revoke', 'explain', 'vacuum',
                'analyze')

            if record.execution_script.strip().lower().startswith(
                sql_keywords):
                record.execution_method = 'query'

            if record.execution_method == 'code':
                record._execute_python_code()
                return

            record.html = ''

            if record.execution_script:
                headers, datas = record._get_result_from_script(
                    record.execution_script)
                row = self.env.cr.rowcount
                rowcount = _("%s row%s processed") % (
                row, 's' if row > 1 else '')

                if headers and datas:
                    record.html = self._generate_html_table(headers, datas)
                else:
                    record.html = rowcount

    def _generate_html_table(self, headers, datas):
        header_html = "".join(
            f"<th style='border: 1px solid black; padding: 2px 120px 3px 10px;'>{header}</th>"
            for header in headers)
        header_html = f"<tr style='background-color: #dbdbdb;'>{header_html}</tr>"

        body_html = ""
        for idx, row in enumerate(datas, start=1):
            row_color = '#e1eaf9' if idx % 2 == 0 else '#ffffff'
            row_html = f"<tr style='background-color: {row_color};' >"
            row_html += "".join(
                f"<td style='border: 1px solid black; padding: 0px 10px;'>{str(value or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</td>"
                for value in row)
            row_html += "</tr>"
            body_html += row_html

        return f"""
        <table>
            <thead>
                {header_html}
            </thead>
            <tbody>
                {body_html}
            </tbody>
        </table>
        """

    @api.onchange('execution_method')
    def _onchange_execution_method(self):
        self.html = ""
        self.execution_script = ""
        self.records_count = 0

    @api.onchange('execution_script')
    def _onchange_execution_script(self):
        self.html = ""
        self.records_count = 0
