# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)



class SicproBackupEliminacion(models.TransientModel):
    _name = "sicpro.backup.eliminacion"
    _description = 'Backup Deletion Confirmation Wizard'
    
    backup_id = fields.Many2one(comodel_name="sicpro.backup.local.detalles", string="Backup Process Detail")
    message = fields.Html(string="Message")
    
    
    def action_delete_backup_detail(self):
        for rec in self:
            rec.backup_id.unlink()
    
