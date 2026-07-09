# -*- coding: utf-8 -*-

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    html_color = fields.Char('Color')
