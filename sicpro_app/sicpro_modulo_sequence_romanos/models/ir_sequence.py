# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import datetime
import pytz
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
from odoo import api, fields, models
from odoo.exceptions import UserError


ROMAN_NUMERAL_MAP = (
            ('M', 1000),
            ('CM', 900),
            ('D', 500),
            ('CD', 400),
            ('C', 100),
            ('XC', 90),
            ('L', 50),
            ('XL', 40),
            ('X', 10),
            ('IX', 9),
            ('V', 5),
            ('IV', 4),
            ('I', 1)
        )


class IrSequence(models.Model):
    _inherit = 'ir.sequence'
    
    is_roman = fields.Boolean()
    
    def to_roman(self, number):
        number = int(number)
        if not (0 <= number < 5000):
            raise UserError("número fuera de rango (debe ser 0..4999)")

        if number == 0:
            return 'N'
        
        result = []
        for numeral, integer in ROMAN_NUMERAL_MAP:
            while number >= integer:
                result.append(numeral)
                number -= integer
        
        return ''.join(result)
    
    @api.constrains('is_roman')
    def _check_padding(self):
        for rec in self:
            if rec.is_roman and rec.padding != 1:
                raise UserError("Para utilizar la numeración romana, el tamaño de la secuencia debe ser igual a 1.\n\n" + MSG_SOPORTE_SICPRO)
            
    def get_next_char(self, number_next):
        if self.is_roman:
            number_next_roman = self.to_roman(number_next[0]) 
            interpolated_prefix, interpolated_suffix = self._get_prefix_suffix()
            return interpolated_prefix + number_next_roman + interpolated_suffix

        return super().get_next_char(number_next)

    def _get_prefix_suffix(self, date=None, date_range=None):
        def _interpolate(s, d):
            return (s % d) if s else ''

        def _interpolation_dict():
            now = range_date = effective_date = datetime.now(pytz.timezone(self.env.context.get('tz') or 'UTC'))
            if date or self.env.context.get('ir_sequence_date'):
                effective_date = fields.Datetime.from_string(date or self.env.context.get('ir_sequence_date'))
            if date_range or self.env.context.get('ir_sequence_date_range'):
                range_date = fields.Datetime.from_string(date_range or self.env.context.get('ir_sequence_date_range'))

            sequences = {
                'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
                'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
            }
            res = {}
            for key, format in sequences.items():
                res[key] = effective_date.strftime(format)
                res['range_' + key] = range_date.strftime(format)
                res['current_' + key] = now.strftime(format)
                
                # convert to roman, ensure_integer
                res['roman_' + key] = self.to_roman(res[key])
                res['roman_range_' + key] = self.to_roman(res['range_' + key])
                res['roman_current_' + key] = self.to_roman(res['current_' + key])

            return res

        self.ensure_one()
        d = _interpolation_dict()
        try:
            interpolated_prefix = _interpolate(self.prefix, d)
            interpolated_suffix = _interpolate(self.suffix, d)
        except (ValueError, TypeError):
            raise UserError("Prefijo o sufijo no válido para secuencia “%s”\n\n", self.name + MSG_SOPORTE_SICPRO)
        return interpolated_prefix, interpolated_suffix