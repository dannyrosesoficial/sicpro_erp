# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import pytz

from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class SicproWebAvisoMantenimiento(models.Model):
    _name = 'sicpro.modulo.web.aviso.mantenimiento'
    _description = 'Aviso de mantenimiento del Sistema'

    name = fields.Char(string="Descripción", default="Configuración General",
                       readonly=True)
    mantenimiento_activo = fields.Boolean(string="¿Mantenimiento Planificado?",
                                          default=False)
    fecha_mantenimiento = fields.Datetime(
        string="Fecha y Hora de Mantenimiento")

    @api.constrains('mantenimiento_activo')
    def _check_unique_record(self):
        # Evita que se creen más de un registro en la tabla
        if self.search_count([]) > 1:
            raise ValidationError(
                "Solo puede existir un registro de configuración.\n\n" + MSG_SOPORTE_SICPRO)

    def get_fecha_formateada(self):
        self.ensure_one()
        if not self.fecha_mantenimiento:
            return ""

        # 1. Obtener la fecha en UTC desde la base de datos
        fecha_utc = self.fecha_mantenimiento

        # 2. Determinar la zona horaria (Cuba)
        # Puedes usar el timezone del usuario o forzar 'America/Havana'
        tz_name = self.env.context.get('tz') or 'America/Havana'
        context_tz = pytz.timezone(tz_name)

        # 3. Convertir de UTC a la hora local de Cuba
        fecha_local = pytz.utc.localize(fecha_utc).astimezone(context_tz)

        # 4. Formatear manualmente para asegurar AM/PM y limpiar espacios
        hora_12 = fecha_local.strftime('%I:%M')
        am_pm = "AM" if fecha_local.hour < 12 else "PM"
        mes = fecha_local.strftime('%b').lower()

        # .strip() final para eliminar los espacios en blanco que mencionaste
        return f"{fecha_local.day} {mes}, {hora_12} {am_pm}".strip()
