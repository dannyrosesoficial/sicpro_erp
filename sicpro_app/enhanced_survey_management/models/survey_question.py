# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class SurveyQuestion(models.Model):
    """Hereda survey.question para añadir tipos de pregunta personalizados."""
    _inherit = 'survey.question'

    question_type = fields.Selection(
        selection_add=[('time', 'Hora'), ('month', 'Mes'), ('name', 'Nombre Completo'), ('address', 'Dirección'),
            ('email', 'Email'), ('password', 'Contraseña'), ('qr', 'Código QR'), ('url', 'URL'), ('week', 'Semana'),
            ('color', 'Color'), ('range', 'Rango'), ('many2one', 'Relación (Many2one)'), ('file', 'Subir Archivo'),
            ('many2many', 'Relación (Many2many)'), ('selection', 'Selección Personalizada'),
            ('barcode', 'Código de Barras'), ('signature', 'Firma')],
        ondelete={'time': 'cascade', 'month': 'cascade', 'name': 'cascade', 'address': 'cascade', 'email': 'cascade',
            'password': 'cascade', 'qr': 'cascade', 'url': 'cascade', 'week': 'cascade', 'color': 'cascade',
            'range': 'cascade', 'many2one': 'cascade', 'file': 'cascade', 'many2many': 'cascade',
            'selection': 'cascade', 'barcode': 'cascade', 'signature': 'cascade'})

    selection_ids = fields.One2many('question.selection', 'question_id', string='Opciones',
                                    help="Campos usados para almacenar opciones en tipos de selección.")
    model_id = fields.Many2one('ir.model', string='Modelo', domain=[('transient', '=', False)],
                               help="Modelo para obtener valores dinámicos.")
    range_min = fields.Integer(string='Mínimo', help="Valor mínimo para el rango.")
    range_max = fields.Integer(string='Máximo', help="Valor máximo para el rango.")

    qrcode = fields.Text(string='QR Code', help='Contenido a mostrar en el QR.')
    qrcode_png = fields.Binary(string='QR PNG', attachment=True)
    barcode = fields.Char(string='Código de Barras', help="Número del código de barras.")
    barcode_png = fields.Binary(string='Barcode PNG', attachment=True)

    @api.constrains('barcode')
    def _check_barcode_validity(self):
        """Valida que el código de barras tenga exactamente 12 dígitos (estándar)."""
        for rec in self:
            if rec.barcode:
                if len(rec.barcode) != 12:
                    raise ValidationError("El código de barras debe tener exactamente 12 caracteres.\n\n" + MSG_SOPORTE_SICPRO)
                if not rec.barcode.isdigit():
                    raise ValidationError("El código de barras solo debe contener dígitos.\n\n" + MSG_SOPORTE_SICPRO)

    def get_selection_values(self):
        """Retorna las opciones para preguntas de tipo selección."""
        return self.selection_ids

    def prepare_model_id(self, model=None):
        """Retorna registros para poblar Many2one/Many2many dinámicamente."""
        target_model = model if model else self.model_id
        if not target_model:
            return []
        model_pool = self.env[target_model.model].sudo()
        records = model_pool.search([])
        rec_name = model_pool._rec_name or 'name'
        return [rec.read([rec_name])[0] for rec in records]