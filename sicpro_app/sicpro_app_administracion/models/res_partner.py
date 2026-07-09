# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, SUPERUSER_ID, Command


class Partner(models.Model):
    _inherit = "res.partner"

    # modifico el orden del partner para que salga el nombre primero y después el proceso
    def _get_contact_name(self, partner, name):
        return "%s, %s" % (name, partner.commercial_company_name or partner.sudo().parent_id.name)
