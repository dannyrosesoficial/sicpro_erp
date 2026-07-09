# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models, exceptions


class QueryDeluxe(models.Model):
    _name = "querydeluxe"
    _description = "Consultas aPostgreSQL desde la interfaz de SICPRO ERP"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    active = fields.Boolean(string='Activo', default=True, index=True)
    rowcount = fields.Text(string='Recuento de filas')
    html = fields.Html(string='HTML')
    name = fields.Text(string='Tipo de consulta : ')
    note = fields.Char(string="Notas")

    def print_result_pdf(self):
        if self:
            self = self.sudo()
            first = self[0]
            return {
                'name': "Seleccionar la orientación del archivo PDF",
                'view_mode': 'form',
                'res_model': 'pdforientation',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {
                    'default_name': first.name,
                    'default_query_id': first.id
                },
            }

    def _get_result_from_query(self, query):
        self = self.sudo()
        headers = []
        datas = []

        if query:
            try:
                self.env.cr.execute(query)
            except Exception as e:
                raise exceptions.UserError(e)

            try:
                if self.env.cr.description:
                    headers = [d[0] for d in self.env.cr.description]
                    datas = self.env.cr.fetchall()
            except Exception as e:
                raise exceptions.UserError(e)

        return headers, datas

    def execute(self):
        for record in self.sudo():
            vals = {
                "rowcount": False,
                "html": False
            }

            if record.name:
                record.message_post(body=str(record.name))

                headers, datas = self._get_result_from_query(record.name)

                rowcount = record.env.cr.rowcount
                vals["rowcount"] = "{0} fila{1} procesada{1}".format(rowcount, 's' if 1 < rowcount else '')

                if headers and datas:
                    header_html = "<tr style='background-color: lightgrey'> <th style='background-color:white'/>"
                    header_html += "".join(["<th style='border: 1px solid black'>"+str(header)+"</th>" for header in headers])
                    header_html += "</tr>"

                    body_html = ""
                    i = 0
                    for data in datas:
                        i += 1
                        body_line = "<tr style='background-color: {0}'> <td style='border-right: 3px double; border-bottom: 1px solid black; background-color: yellow'>{1}</td>".format('cyan' if i%2 == 0 else 'white', i)
                        for value in data:
                            display_value = ''
                            if value is not None:
                                display_value = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            body_line += "<td style='border: 1px solid black'>{0}</td>".format(display_value)
                        body_line += "</tr>"
                        body_html += body_line

                    vals["html"] = """
                    <table style="text-align: center">
                        <thead">
                            {0}
                        </thead>
                        
                        <tbody>
                            {1}
                        </tbody>
                    </table>
                    """.format(header_html, body_html)
            record.update(vals)
