# -*- coding: utf-8 -*-

import hashlib
from random import choice

from odoo import SUPERUSER_ID, api, fields, models
from odoo.tools import pycompat


def _attachment2url(att):
    sha = hashlib.md5(pycompat.to_text(att.datas).encode("utf-8")).hexdigest()[
          0:7]
    return "/web/image/{}-{}".format(att.id, sha)


class IRAttachmentBackground(models.Model):
    _inherit = "ir.attachment"

    use_as_background = fields.Boolean("Usar como imagen del login",
                                       default=False, index=True)
    id_img_login = fields.Integer(string='Id_img_login', required=False)

    @api.onchange("use_as_background")
    def _onchange_use_as_background(self):
        if self.use_as_background:
            self.public = True

    def _get_background_images_domain(self):
        return [("use_as_background", "=", True)]

    @api.model
    def get_background_pic(self):
        pictures = self.with_user(SUPERUSER_ID).search(
            self._get_background_images_domain())
        if pictures:
            p = choice(pictures)
            picture_url = p.url or _attachment2url(p)
            return picture_url
        else:
            return False
