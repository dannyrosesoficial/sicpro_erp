# -*- coding: utf-8 -*-

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import Warning


class PartesHorasTemporizador(models.TransientModel):
    _name = "sicpro.app.partes.horas.temporizador"

    start_date = fields.Datetime(string="Fecha inicial", readonly=True)
    end_date = fields.Datetime(string="Fecha fin", readonly=True)
    description = fields.Text(string="Descripción", required=True)
    duration = fields.Float('Duración', readonly=True)

    @api.model
    def default_get(self, default_fields):
        context = self._context
        s_date = context.get('start_date')
        e_date = context.get('end_date')
        diff = datetime.datetime.strptime(
            e_date, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
            s_date, "%Y-%m-%d %H:%M:%S")
        duration = float(diff.days) * 24 + (float(diff.seconds) / 3600)
        final_output = round(duration, 2)
        res = super(PartesHorasTemporizador, self).default_get(default_fields)
        res.update({
            'start_date': s_date,
            'end_date': e_date,
            'duration': final_output,
        })
        return res

    # guarda el registro del temporizador de actividades
    def save_entry(self):
        context = self._context
        preparacion = context.get('preparaciones_id', False)
        data = self.env['sicpro.app.preparacion.tecnica.preparaciones'].browse(
            preparacion)
        ejecutor = data.especialista_ejecutor_id
        if ejecutor:
            if self.duration == 0.0:
                raise Warning(
                    _("No se puede guardar la entrada para %s duración") % (
                        self.duration))
            vals = {'fecha': fields.Date.context_today(self),
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'user_id': self.env.user.id,
                    'name': self.description,
                    'preparaciones': preparacion,
                    'especialista_ejecutor_id': ejecutor.id,
                    'duracion': self.duration
                    }
            partes = self.env['sicpro.app.partes.horas'].create(vals)
            data.write({'partes_horas_ids': [(4, 0, [partes.id])],
                        'is_start': False})
        else:
            raise Warning(_(
                "Vincula el parte a esta preparación para guardar la entrada"))
