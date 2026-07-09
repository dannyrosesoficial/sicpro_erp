# -*- coding: utf-8 -*-


from random import randint
import base64
from odoo import api, Command, fields, models, modules, _
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class AppCMIPerspectivasPeriodos(models.Model):
    _name = 'sicpro.app.cmi.perspectivas.periodos'
    _order = "id asc"
    _description = 'Periodos del CMI'

    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True,)
    name = fields.Selection(
        string='Período', selection=[
            ('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'),
            ('abril', 'Abril'), ('mayo', 'Mayo'), ('junio', 'Junio'),
            ('julio', 'Julio'), ('agosto', 'Agosto'),
            ('septiembre', 'Septiembre'), ('octubre', 'Octubre'),
            ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre'),
            ('1t', 'Primer Trimestre'), ('2t', 'Segundo Trimestre'),
            ('3t', 'Tercer Trimestre'), ('4t', 'Cuarto Trimestre'),
            ('1s', 'Primer Semestre'), ('2s', 'Segundo Semestre'),
            ('anual', 'Anual'), ],
        required=False, )
    image_128 = fields.Image("Imagen", max_width=128, max_height=128)
    anio_temp = fields.Char(string="Año", compute='compute_mes_anio_temp')

    # calcula el mes temporal del context
    def compute_mes_anio_temp(self):
        for item in self:
            item.anio_temp = self._context.get('default_anual')

    # llamada para ir a las perspectivas por año y periodo
    def action_objetivos_anuales(self):
        anio_activo = self._context.get('default_anual')
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.cmi_perspectivas_dashboard_action')
        action['context'] = {'default_anual': anio_activo,
                             'default_periodo': self.name}
        return action
