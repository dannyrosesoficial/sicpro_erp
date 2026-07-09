

from odoo import models
import logging

_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(IrHttp, self).session_info()

        # ID exacto de tu grupo (Verifica que sea este)
        group_id = 'sicpro_app_administracion.group_allow_importar'

        user = self.env.user
        has_group = user.has_group(group_id)

        # Aplicamos la restricción
        if user.id in [1, 2]:
            res['can_import'] = True
        else:
            res['can_import'] = has_group

        return res