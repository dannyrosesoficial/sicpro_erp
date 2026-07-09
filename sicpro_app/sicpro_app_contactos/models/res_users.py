# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, api, modules


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        """ Actualiza el icono del systray para que las actividades de contactos
        usen el icono de la app 'Contacts' en lugar del icono base. """
        activities = super(Users, self).systray_get_activities()

        for activity in activities:
            if activity.get('model') == 'res.partner':
                activity['icon'] = modules.module.get_module_icon('contacts')
        return activities
