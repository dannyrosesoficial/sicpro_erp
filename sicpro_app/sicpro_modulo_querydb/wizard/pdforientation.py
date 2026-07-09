# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models


class PdfOrientation(models.TransientModel):
    _name = 'pdforientation'
    _description = "Seleccionar la orientación del archivo PDF"

    def orientation_choices(self):
        return [('landscape', 'Landscape'), ('portrait', 'Portrait')]

    def get_default_caution_html(self):
        return """
        <div>
            <span style='color: red'>Tenga cuidado</span>, se ejecutará la consulta <span style='color: red; text-decoration: underline'>una vez más</span> en su base de datos para recuperar los datos utilizados al imprimir el resultado.
            <br/>
            Por ejemplo, una consulta con sentencias <span style='color: orange'>CREATE</span> o <span style='color: orange'>UPDATE</span> sin ninguna cláusula 'RETURNING' no imprimirá necesariamente una tabla a diferencia de una sentencia <span style='color: blue'>SELECT</span>,
            <br/>
            <span style='text-decoration: underline'>pero aun así se ejecutará una vez en segundo plano durante el proceso de impresión</span>.
            <br/>
            Por lo tanto, cuando desee imprimir el resultado, utilice preferiblemente la sentencia 'SELECT' para asegurarse de no ejecutar una consulta no deseada dos veces.
        </div>
        """

    orientation = fields.Selection(string="PDF orientación", selection=orientation_choices, default='landscape')
    name = fields.Text(string="Consulta")
    query_id = fields.Many2one('querydeluxe', string="Origen")
    caution_html = fields.Html(string="PRECAUCIÓN", default=get_default_caution_html)
    understand = fields.Boolean(string="Estoy de acuerdo")

    def print_pdf(self):
        if self:
            self = self.sudo()
            first = self[0]
            action_print_pdf = self.env.ref('sicpro_modulo_querydb.action_print_pdf')
            if first.orientation == 'landscape':
                action_print_pdf.paperformat_id.orientation = "Landscape"
            elif first.orientation == 'portrait':
                action_print_pdf.paperformat_id.orientation = "Portrait"
            return action_print_pdf.report_action(first.query_id)
